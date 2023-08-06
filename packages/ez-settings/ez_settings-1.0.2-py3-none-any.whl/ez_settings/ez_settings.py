import os
import json

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EZSettingsBase(object):
    def __init__(self, file_location=""):
        """
        Initializer

        :param file_location: this is the location where the settings file will be saved
        """
        self.__file_location = file_location
        if os.path.exists(self.__file_location):
            with open(file_location) as f:
                self.__settings_dictionary = json.load(f)
        else:
            self.__settings_dictionary = {}
            dir_name = os.path.dirname(self.__file_location)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            self.__save_json()

    def reset(self):
        """
        Deletes the save json file and re-initializes, resetting all saved settings
        :return:
        """
        if os.path.isfile(self.__file_location):
            os.remove(self.__file_location)

        self.__init__(self.__file_location)
        self.__settings_dictionary = {}

    def get_file_location(self):
        """
        Gets the location of the file on disc where the settings are saved
        :return: filepath
        """
        return self.__file_location

    def exists(self, setting_name):
        """
        Check if a setting with a certain name exists

        :param setting_name: setting you're looking for
        :return: bool
        """
        if setting_name in self.__settings_dictionary:
            return True
        return False

    def get_setting_with_value(self, value):
        """
        Gets all the settings with a particular value

        :param value: value you're looking for
        :return: a list of all the setting names that match the value
        """
        keys = []
        for k, v in self.__settings_dictionary.items():
            if v == value:
                keys.append(k)

        return keys

    def get_all_settings(self):
        """
        Gets all the settings

        :return: a list with all the settingnames
        """
        return self.__settings_dictionary.keys()


    def set(self, setting_name, value):
        """
        Sets the value of a setting

        :param setting_name: name of the setting you want to zet
        :param value: value of the setting
        :return: nothing
        """
        self.__settings_dictionary[setting_name] = value
        self.__save_json()

    def get(self, setting_name, *args):
        """
        Gets the value of the settings you're using

        :param setting_name: name of the setting you want to get
        :param args: the default value you want to load if the setting can't be found
        :return: value or default value
        """
        if args:
            return self.__settings_dictionary.get(setting_name, *args)

        return self.__settings_dictionary.get(setting_name)

    def append(self, setting_name, value):
        """
        Provided the setting is a list, this appends the value to the provided setting value.
        The function will raise a TypeError if settingName is a not a list

        :param setting_name: name of the setting list you want to add value to
        :param value: value you want to add
        :return: nothing
        """
        old_value = self.get(setting_name, [])
        if not isinstance(old_value, list):
            raise TypeError("This method expects the setting to be a list, %s is a %s" % (setting_name, type(old_value)))

        if not isinstance(value, list):
            value = [value]

        newValue = old_value + value

        self.set(setting_name, newValue)

    def pop(self, setting_name, value):
        """
        Provided the setting is a list, this removes the value to the provided setting value.
        The function will raise a TypeError if settingName is a not a list

        :param setting_name: name of the setting you want to remove the value from
        :param value: value you want to remove
        :return:
        """
        old_value = self.get(setting_name, [])
        if not isinstance(old_value, list):
            raise TypeError("This method expects the setting to be a list, %s is a %s" % (setting_name, type(old_value)))

        if value in old_value:
            old_value.remove(value)
            self.set(setting_name, old_value)

    def remove(self, setting_name):
        """
        Removes a setting from the settings file

        :param setting_name: setting you want to remove
        :return:
        """
        self.__settings_dictionary.pop(setting_name)
        self.__save_json()

    def __save_json(self):
        with open(self.__file_location, 'w+') as outfile:
            json.dump(self.__settings_dictionary, outfile, indent=4)


class EZSettingsPy2(EZSettingsBase):
    __meta_class__ = Singleton
    def __init__(self, file_location=""):
        super(EZSettingsPy2, self).__init__(file_location=file_location)


class EZSettings(EZSettingsBase, metaclass=Singleton):
    def __init__(self, file_location=""):
        super().__init__(file_location=file_location)


