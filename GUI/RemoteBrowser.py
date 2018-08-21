#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QTabWidget, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import json
import ConanCommander
#import MenuBar
from GUI import NavigationPanel
from GUI import PackagePanel
from GUI import GraphView


class RemoteBrowser(QMainWindow):

    def __init__(self, cache_file):
        super().__init__()
        with open(cache_file) as fp:
            self.__cache = json.load(fp)
        self.commander = ConanCommander.ConanCommander()
        self.init_menu_bar()
        self.tabs = QTabWidget()
        self.navigation = NavigationPanel.TreeView(self.cache)
        self.details = PackagePanel.TreeView()
        self.navigation.clicked.connect(self.onItemClicked)
        self.graph = GraphView.GraphView()
        self.tabs.addTab(self.details, "Details")
        self.tabs.addTab(self.graph, "Graph")
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.navigation)
        self.splitter.addWidget(self.tabs)
        self.setCentralWidget(self.splitter)
        self.statusBar().showMessage('Ready')
        self.setGeometry(800, 600, 800, 600)
        self.setWindowTitle('Remote Browser')
        self.setWindowIcon(QIcon('web.png'))
        self.show()

    @property
    def cache(self):
        return self.__cache

    def onItemClicked(self, index):
        item = self.navigation.selectedIndexes()[0]
        search = item.model().itemFromIndex(index)
        result = self.commander.package_info(search.text(), search.parent().text())
        self.details.populate(result, clear=True)
        table = self.commander.package_table(search.text(), search.parent().text())
        self.graph.load(table)
        self.graph.show()

    def init_menu_bar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        aboutMenu = menubar.addMenu('&About')
        remotes = QAction('Manage &Remotes', self)
        remotes.setShortcut("Ctrl+Shift+R")
        remotes.setStatusTip("Open the remote management window.")
        fileMenu.addAction(remotes)
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAct)


if __name__ == "__main__":
    """ Do some trivial tests."""
    import sys
    app = QApplication(sys.argv)
    browser = RemoteBrowser("../cache.json")

    sys.exit(app.exec_())