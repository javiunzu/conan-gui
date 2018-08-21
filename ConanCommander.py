#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
from conans.client.command import Command, CommandOutputer, Conan
from conans.errors import ConanException


class ConanCommander(Command):
    def __init__(self):
        """ Wrapper over the command line client. """
        try:
            conan_api, client_cache, user_io = Conan.factory()
        except ConanException:  # Error migrating
            sys.exit(2)

        self.outputer = CommandOutputer(user_io, client_cache)
        super(ConanCommander, self).__init__(conan_api, client_cache, user_io, self.outputer)

    def package_info(self, package, remote):
        """
        conan search --raw "Assimp/4.1.0@jacmoe/stable" -r conan-center -j package.json
        """
        # TODO /tmp is exclusive of Linux.
        self.search(["--raw", package, "-r", remote, "-j", "/tmp/{}.json".format(package)])
        with open("/tmp/{}.json".format(package)) as f:
            info = json.load(f)
        if not info["error"]:
            return info["results"][0]["items"][0]["packages"]
        else:
            if not info["results"]:
                return []
            else:
                print(info)
                raise Warning("Errors occurred.")

    def package_table(self, package, remote):
        temp_file = "/tmp/{}.html".format(package)
        self.search([package, "-r", remote, "--table", temp_file])
        return temp_file


if __name__ == "__main__":
    """ Do some trivial tests """
    com = ConanCommander()
    print(com.package_info("Assimp/4.1.0@jacmoe/stable"))