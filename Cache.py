import subprocess
import json


class Cache(object):
    def __init__(self):
        self.__remotes = None
        self.__data = None

    @property
    def data(self):
        return self.__data

    @property
    def remotes(self):
        if not self.__remotes:
            remotes = []
            cmd = subprocess.run(["conan", "remote", "list", "--raw"], stdout=subprocess.PIPE)
            output = cmd.stdout.decode("utf-8")
            for remote in output.split("\n"):
                if remote:
                    remotes.append(remote)  # Only the name. For the moment.
        self.__remotes = remotes
        return self.__remotes

    def scan_remotes(self):
        cache = []
        for remote in self.remotes:
            element = {}
            name, url, ssl = remote.split()
            temp_file = "/tmp/{}.json".format(name)
            _ = subprocess.run(["conan", "search", "*", "-r", name, "--json", temp_file], stdout=subprocess.PIPE)
            element["name"] = name
            element["url"] = url
            element["ssl"] = ssl
            element["packages"] = []
            with open(temp_file) as f:
                results = json.load(f)["results"]
            for item in results[0]["items"]:
                element["packages"].append(item["recipe"]["id"])
            cache.append(element)
        self.__data = cache

    def dump(self, filename):
        """ Writes a JSON file with the data of the object."""
        with open(filename, "w") as o:
            json.dump(self.__data, o)


if __name__ == "__main__":
    c = Cache()
    c.scan_remotes()
    print(c.data)