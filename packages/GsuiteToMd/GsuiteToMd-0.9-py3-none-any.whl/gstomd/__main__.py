# -*- coding: utf-8 -*-
import getopt
import logging
import sys
from .my_settings import LoadSettingsFile
from .my_settings import ValidateSettings
from .my_settings import SettingsError
from .my_settings import InvalidConfigError
from .my_settings import SetupLogging
from .corpus import Corpus


DEFAULT_SETTINGS = {
    'pydrive_settings': 'pydrive_settings.yaml',
    'dest_folder': './data',
    'root_folder_id': '',
    'root_folder_name': '',
    'drive_id': '',
    'collections': []
}


def main():
    SetupLogging()

    logger = logging.getLogger()

    try:
        opts, _ = getopt.getopt(sys.argv[1:], '-c', [
            'config=',
        ])
    except getopt.GetoptError:
        sys.exit(2)
    settings_file = 'settings.yaml'
    for opt, arg in opts:

        if opt in ('-c', '--config'):
            settings_file = arg

    logging.debug("configfile : %s", settings_file)

    try:
        settings = LoadSettingsFile(settings_file)
    except SettingsError as err:
        logging.debug("incorrect config file : %s", err)
        settings = DEFAULT_SETTINGS
    else:
        if settings is None:
            settings = DEFAULT_SETTINGS
        # else:
            # ValidateSettings(settings)

    dest_folder = settings.get('dest_folder')
    pydrive_settings = settings.get('pydrive_settings')
    collections = settings.get('collections')

    logger.debug("%s, %s, %s", dest_folder, pydrive_settings, collections)

    for collection in collections:
        logger.debug("collection : %s", collection)
        corpus = Corpus(pydrive_settings=pydrive_settings,
                        drive_id=collection['drive_id'],
                        root_folder_id=collection['root_folder_id'],
                        dest_folder=dest_folder,
                        root_folder_name=collection['root_folder_name'])
        corpus.get_source()
        corpus.root_folder.to_disk()


if __name__ == "__main__":
    # execute only if run as a script
    main()
