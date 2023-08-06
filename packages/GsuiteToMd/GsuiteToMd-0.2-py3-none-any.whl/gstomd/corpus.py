# -*- coding: utf-8 -*-
from itertools import chain
import logging
import os
import re
import unicodedata
import zipfile
from datetime import datetime

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .my_settings import LoadSettingsFile
from .my_settings import ValidateSettings
from .my_settings import SettingsError
from .my_settings import InvalidConfigError
from .my_settings import SetupLogging
logger = logging.getLogger(__name__)
FILETYPE = {
    "DOC": ("application/vnd.google-apps.document", "Google Doc"),
    "FOLDER": ("application/vnd.google-apps.folder", "Folder")
}


def DebugInOut(fn):
    """Decorator to add in and out logs
    """
    def wrapped(*v, **k):
        name = fn.__name__
        logger.debug("IN %s(%s)", name, ", ".join(
            map(repr, chain(v, k.values()))))
        result = fn(*v, **k)
        logger.debug("OUT %s", name)
        return result
    return wrapped


def mime_to_filetype(mime_string):
    """convert mimi type in simple string

    Args:
        mime_string (string)

    Returns:
        string : [description]
    """
    for label, carac in FILETYPE.items():
        if carac[0] == mime_string:
            return label
    logger.warning("Unknown mime type : %s", mime_string)
    return "UNKNOWN"


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'[-\s]+', '', value).strip('-_')


class Node:
    """
    class for Google Drive item
    """

    def __init__(self, path, basename, id_, depth=1):
        self.path = path
        self.basename = basename
        self.depth = depth
        self.id_ = id_

    def unix_name(self):
        return slugify(self.basename)


class Gdoc(Node):
    def __init__(self,  path, basename, id_, content, depth=1):

        super().__init__(path, basename, id_, depth)
        self.content = content
        self.content_zip = ""

    def __str__(self):
        return "\n%sD : %50s|%20s|%20s|%s" % ("-" * self.depth*4,
                                              self.id_,
                                              self.basename,
                                              self.unix_name(),
                                              self.path)

    def to_md(self):
        os.makedirs(self.path)
        zip_path = self.path+"/"+os.path.basename(self.path)+".zip"
        md_path = self.path+"/"+os.path.basename(self.path)+".md"
        f_zip = open(zip_path, "wb")
        f_zip.write(self.content_zip)
        f_zip.close()
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:

            files_names = zip_ref.namelist()
            for file_name in files_names:
                if file_name.endswith('.html'):
                    f_md = open(md_path, "w")
                    html = zip_ref.read(file_name)
                    parsed_html = BeautifulSoup(html, features="lxml")
                    body = "%s" % (parsed_html.body)

                    body_md = md(body)
                    f_md.write(body_md)
                    f_md.close()
                else:
                    zip_ref.extract(file_name, os.path.dirname(md_path))
            os.remove(zip_path)


class Gfolder(Node):
    def __init__(self,  path, basename, id_, depth=1):

        super().__init__(path, basename, id_, depth)
        self.children = []
        self.files = []

    def __str__(self):
        message = "\n%sF : %50s|%20s|%20s|%s" % (
            "-" * self.depth*4, self.id_, self.basename, self.unix_name(), self.path)
        for child in self.children:
            message = "%s%s" % (message, child)
        return message

    def to_disk(self):
        os.makedirs(self.path)
        if self.children:
            for child in self.children:
                if isinstance(child, Gfolder):
                    child.to_disk()

                elif isinstance(child, Gdoc):
                    child.to_md()

    def all_subfolders(self):
        """
        list all subfolders
        """
        list_folders = set()

        for child in self.children:
            if isinstance(child, Gfolder):
                list_folders.add(child.id_)
                child_folders = child.all_subfolders()
                if child_folders:
                    list_folders = list_folders.union(child_folders)
        return list_folders

    def complement_children_path_depth(self):
        """
        generate children's path and depth information from basename
        """
        for child in self.children:
            child.path = "{0}/{1}".format(self.path, child.unix_name())
            child.depth = self.depth + 1
            if isinstance(child, Gfolder):
                child.complement_children_path_depth()


@DebugInOut
class Corpus():
    DEFAULT_SETTINGS = {
        'pydrive_settings': 'pydrive_settings.yaml',
        'dest_folder': './data',
        'root_folder_id': '',
        'root_folder_name': '',
        'drive_id': '',
        'collections': []
    }

    def __init__(self, settings_file='settings.yaml'):
        """Create an instance of Corpus.
        :param settings_file: path of settings file. 'settings.yaml' by default.
        :type settings_file: str.

        """
        try:
            settings = LoadSettingsFile(settings_file)
        except SettingsError as err:
            logging.info("incorrect config file : %s", err)
            settings = self.DEFAULT_SETTINGS
        else:
            if settings is None:
                settings = self.DEFAULT_SETTINGS
            # else:
                # ValidateSettings(settings)

        self.dest_folder = settings.get('dest_folder')
        self.pydrive_settings = settings.get('pydrive_settings')
        self.ga = GoogleAuth(
            self.pydrive_settings)
        self.drive_connector = GoogleDrive(self.ga)
        collections_from_settings = settings.get('collections')
        logger.debug(collections_from_settings)
        self.collections = []
        for item in collections_from_settings.items():
            logger.debug(item)
        for col_id, col_params in collections_from_settings.items():
            logger.debug(col_id)
            self.collections.append(Collection(
                id_=col_id,
                drive_id=col_params['drive_id'],
                root_folder_id=col_params['root_folder_id'],
                dest_folder=self.dest_folder,
                root_folder_name=col_params['root_folder_name'],
                drive_connector=self.drive_connector,)
            )

        logger.debug("%s, %s, %s", self.dest_folder,
                     self.pydrive_settings, self.collections)

    @DebugInOut
    def fetch(self, collection_id=""):

        for col in self.collections:
            if not collection_id or col.id_ == collection_id:
                logger.debug("collection : %s", col.id_)
                col.fetch()

    @DebugInOut
    def to_disk(self, collection_id=""):
        for col in self.collections:
            if not collection_id or col.id_ == collection_id:
                logger.debug("collection : %s", col)
                col.to_disk()


class Collection():
    @DebugInOut
    def __init__(self, drive_connector, id_, drive_id='', root_folder_id='root', dest_folder='./data', root_folder_name='root'):
        """Create an instance of Collection.
        :param drive : GoogleDrive
        :type settings_file: str.
        """
        self.id_ = id_
        self.fetched = False
        self.drive_id = drive_id
        self.root_folder_id = root_folder_id
        self.dest_folder = dest_folder
        self.root_folder_name = root_folder_name
        self.root_folder = {}
        self.drive_connector = drive_connector

    @DebugInOut
    def fetch(self):
        """
        Generate folder structure with files

        Returns:
            Gfolder: root folder of the coprus
        """

        drive_id = self.drive_id
        root_folder_id = self.root_folder_id
        dest_folder = self.dest_folder
        root_folder_name = self.root_folder_name
        root_drive = Gfolder(
            path="./",
            basename="root",
            depth=1,
            id_=drive_id,
        )
        root_folder = root_drive

        nodes = {root_drive.id_: (root_drive, None)}
        query = "trashed=false and mimeType='application/vnd.google-apps.folder'"
        if drive_id != "":
            param = {
                'corpora': "drive",
                'supportsAllDrives': True,
                'includeItemsFromAllDrives': True,
                'driveId': drive_id,
                'q': query,

            }
        else:
            param = {
                'corpora': "user",
                'q': query,
            }
        folders_list = self.drive_connector.ListFile(
            param).GetList()
        for item in folders_list:
            file_name = item["title"]
            file_id = item["id"]
            item_parents = item.get("parents")
            if not item_parents:
                parent_id = root_drive.id_
            else:
                parent_id = item_parents[0]['id']

            node = Gfolder(
                path=None,
                basename=file_name,
                depth=1,
                id_=file_id)

            nodes[file_id] = (node, parent_id)

        for file_id, (node, parent_id) in nodes.items():
            if file_id == root_folder_id:
                root_folder = node
                logger.debug("root_folder found :%s", root_folder)
            if parent_id is None:
                continue
            if parent_id in nodes.keys():
                nodes[parent_id][0].children.append(node)
            else:
                logger.warning("parent id %s not found", parent_id)
        root_folder.depth = 1
        now = datetime.now()
        date_time = now.strftime("%Y.%m.%d.%H.%M.%S")
        root_folder.path = "%s/%s/%s" % (dest_folder,
                                         root_folder_name, date_time)

        root_folder.complement_children_path_depth()
        folders = root_folder.all_subfolders()
        parents_id = ' or '.join(
            "'{!s}' in parents".format(key) for key in folders)
        parents_id = "%s or '%s' in parents" % (parents_id, root_folder_id)

        query_for_files = "trashed=false and mimeType='application/vnd.google-apps.document' and (" + \
            parents_id+")"
        param['q'] = query_for_files
        files_list = self.drive_connector.ListFile(
            param).GetList()

        for item in files_list:
            file_name = item["title"]
            file_id = item["id"]
            content = item.get("content")
            item_parents = item.get("parents")
            is_root = item.get("isRoot")
            if not item_parents:
                parent_id = "None"
            else:
                if is_root:
                    parent_id = "root"
                else:
                    parent_id = item_parents[0]['id']

                node = Gdoc(
                    path=None,
                    basename=file_name,
                    depth=1,
                    id_=file_id,
                    content=content
                )
                logger.debug("fetch content for %s", node)
                item.FetchContent(
                    mimetype='application/zip', remove_bom=True)
                node.content_zip = item.content.getvalue()
                if parent_id in nodes.keys():

                    nodes[parent_id][0].children.append(node)
                else:
                    logger.warning("parent id %s not found", parent_id)
        root_folder.complement_children_path_depth()

        self.root_folder = root_folder
        logger.debug(root_folder)
        self.fetched = True
        return root_folder

    def to_disk(self):
        if not self.fetched:
            self.fetch()
        self.root_folder.to_disk()
