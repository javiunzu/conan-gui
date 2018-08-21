import os
from PyQt5.QtWidgets import QApplication
from Cache import Cache
from GUI.RemoteBrowser import RemoteBrowser

if __name__ == "__main__":
    """ Run the app."""
    import sys
    # Generate a new cache unless it already exists
    if not os.path.exists("cache.json"):
        c = Cache()
        c.scan_remotes()
        c.dump("cache.json")
    app = QApplication(sys.argv)
    browser = RemoteBrowser("cache.json")
    sys.exit(app.exec_())