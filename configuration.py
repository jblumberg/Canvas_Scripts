import configparser
import os
from datetime import date
from datetime import datetime
from dateutil.parser import parse


class Configuration(object):
    """Manage the configuration of Canvas API tokens

    This code is designed to store the token outside of the project folder in a .ini style config file
    This allows the codebase to be easily shared without the token information

    """

    def __init__(self, file_path="Default"):
        """
        Returns a configuration object

        :param file_path: path of the config file
        """
        self.config = configparser.ConfigParser()

        # Default file path
        if file_path == "Default":
            self.file_path = os.path.expanduser(
                "~/Library/CanvasAPI/canvas_api_key.ini"
            )
        else:
            self.file_path = file_path

    def load_config_file(self, filepath=""):
        """Read the config file.

        :param file_path: file to read.  Overrides the default if provided
        """
        if filepath:
            self.file_path = filepath

        try:
            self.config.read(self.file_path)
        except:
            print("Error reading config file")

    def add_canvas_api(self, api_url, api_key, user_email, expiration_date):
        """FIll in the information when the key is generated


        :param api_url:  Should be in the form: "https://________.instructure.com/api/v1"
        :param api_key:
        :param user_name:
        :param expiration_date:
        :return:
        """
        self.config["CANVAS_API"] = {
            "API_URL": api_url,
            "API_KEY": api_key,
            "User": user_email,
            "Expiration Date": expiration_date,
        }
        with open(self.file_path, "w") as configfile:
            self.config.write(configfile)

    @property
    def api_key(self):
        current_date = datetime.combine(date.today(), datetime.min.time())
        expiration_date = parse(self.config["CANVAS_API"]["Expiration Date"])
        if current_date < expiration_date:
            return self.config["CANVAS_API"]["API_KEY"]
        else:
            raise ValueError("The key is expired")

    @property
    def api_url(self):
        return self.config["CANVAS_API"]["API_URL"]
