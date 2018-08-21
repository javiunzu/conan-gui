#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TreeView(QTreeView):
    """
    TreeView contains the list of packages for each remote.
    It reads a cache file
    """
    def __init__(self, cache):
        super(TreeView, self).__init__()
        self.setAlternatingRowColors(False)
        self.model = QStandardItemModel(0, 1, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Remote")
        self.rootNode = self.model.invisibleRootItem()
        for remote in cache:
            branch = QStandardItem(remote["name"])
            for package in remote["packages"]:
                p = QStandardItem(package)
                branch.appendRow([p])
            self.rootNode.appendRow([branch])
        self.setModel(self.model)
        self.setColumnWidth(0, 150)
        self.expandAll()
