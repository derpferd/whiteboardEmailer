import json
import os

class Config(object):
    """Config is a class for holding all user configurations"""
    def __init__(self, filename="userSettings.json", autosave=False):
        self.settings = {
        }
        self.filename = filename
        self.autosave = autosave

    def __getitem__(self, item):
        if item in self.settings:
            return self.settings[item]
        else:
            raise IndexError("Setting does not exist")

    def __setitem__(self, key, value):
        print "setting item"
        self.settings[key] = value
        if self.autosave:
            self.save()

    def save(self, filename=None):
        if not filename and self.filename:
            filename = self.filename
        print "Saving current config to:", filename
        fp = open(filename, "wb")
        json.dump(self.settings, fp)
        fp.close()

    def load(self, filename=None):
        if not filename and self.filename:
            filename = self.filename
        if os.path.exists(filename):
            self.settings = json.load(open(filename, "rb"))
        else:
            raise IOError("Config file do not exist.")
