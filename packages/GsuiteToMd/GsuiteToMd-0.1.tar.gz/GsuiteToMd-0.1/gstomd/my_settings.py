from os.path import isfile, join
import logging
import logging.config
from yaml import YAMLError, load
logger = logging.getLogger(__name__)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

SETTINGS_FILE = 'settings.yaml'
SETTINGS_STRUCT = {
    'dest_folder': {
        'type': str,
        'required': False,
        'default': './data'

    },
    'pydrive_settings': {
        'type': str,
        'required': False,
        'default': 'pydrive_settings.yaml'
    },

    'collections': {
        'type': dict,
        'required': True,
        'struct': {
            'drive_id': {
                'type': str,
                'required': False,
                'default': ""
            },
            'root_folder_id': {
                'type': str,
                'required': True
            },
            'root_folder_name': {
                'type': str,
                'required': False,
                'default': ""
            }, }

    },
}


class SettingsError(IOError):
    """Error while loading/saving settings"""


class InvalidConfigError(IOError):
    """Error trying to read client configuration."""


def LoadSettingsFile(filename=SETTINGS_FILE):
    """Loads settings file in yaml format given file name.

    :param filename: path for settings file. 'settings.yaml' by default.
    :type filename: str.
    :raises: SettingsError
    """
    try:
        stream = open(filename, 'r')
        data = load(stream, Loader=Loader)
    except (YAMLError, IOError) as e:
        from os import listdir
        logger.debug("in current directory : %s", listdir("."))
        raise SettingsError(e) from e
    return data


def ValidateSettings(data):
    """Validates if current settings is valid.

    :param data: dictionary containing all settings.
    :type data: dict.
    :raises: InvalidConfigError
    """
    _ValidateSettingsStruct(data, SETTINGS_STRUCT)


def _ValidateSettingsStruct(data, struct):
    """Validates if provided data fits provided structure.

    :param data: dictionary containing settings.
    :type data: dict.
    :param struct: dictionary containing structure information of settings.
    :type struct: dict.
    :raises: InvalidConfigError
    """
    # Validate required elements of the setting.
    for key in struct:
        if struct[key]['required']:
            _ValidateSettingsElement(data, struct, key)


def _ValidateSettingsElement(data, struct, key):
    """Validates if provided element of settings data fits provided structure.

    :param data: dictionary containing settings.
    :type data: dict.
    :param struct: dictionary containing structure information of settings.
    :type struct: dict.
    :param key: key of the settings element to validate.
    :type key: str.
    :raises: InvalidConfigError
    """
    # Check if data exists. If not, check if default value exists.
    value = data.get(key)
    data_type = struct[key]['type']
    if value is None:
        try:
            default = struct[key]['default']
        except KeyError as e:
            raise InvalidConfigError(
                'Missing required setting %s' % key) from e
        else:
            data[key] = default
    # If data exists, Check type of the data
    elif type(value) is not data_type:
        raise InvalidConfigError(
            'Setting %s should be type %s' % (key, data_type))
    # If type of this data is dict, check if structure of the data is valid.
    if data_type is dict:
        _ValidateSettingsStruct(data[key], struct[key]['struct'])
    # If type of this data is list, check if all values in the list is valid.
    elif data_type is list:
        for element in data[key]:
            if type(element) is not struct[key]['struct']:
                raise InvalidConfigError('Setting %s should be list of %s' %
                                         (key, struct[key]['struct']))
    # Check dependency of this attribute.
    dependencies = struct[key].get('dependency')
    if dependencies:
        for dependency in dependencies:
            if value == dependency['value']:
                for reqkey in dependency['attribute']:
                    _ValidateSettingsElement(data, struct, reqkey)


def SetupLogging(filename='logging.yaml',
                 default_level=logging.DEBUG,):
    """initialize logging

    Args:
        filename name (str, optional). the configuration file name
        default_level ( optional):  Defaults to logging.DEBUG.
    """
    try:
        log_cfg = LoadSettingsFile(filename=filename)
        logging.config.dictConfig(log_cfg)
    except (YAMLError, IOError) as e:
        logging.basicConfig(level=default_level)
        logging.info("No logging config file, level set to debug %s", e)
