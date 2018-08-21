#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QAction, qApp, QMenu, QTreeView, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TreeView(QTreeView):
    """
    TreeView contains the detailed list of packages for a given recipe.
    """
    def __init__(self):
        super(TreeView, self).__init__()
        self.setAlternatingRowColors(True)
        self.model = QStandardItemModel(0, 2, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Package")
        self.model.setHeaderData(1, Qt.Horizontal, "Values")
        self.rootNode = self.model.invisibleRootItem()
        self.setModel(self.model)
        self.setColumnWidth(0, 150)
        self.expandAll()

    def populate(self, info, clear=False):
        if clear:
            if self.rootNode.rowCount() > 0:
                self.rootNode.removeRows(0, self.rootNode.rowCount())
        if info == []:
            branch = QStandardItem("No packages found.")
        else:
            for package in info:
                branch = QStandardItem(package["id"])
                for key, value in package.items():
                    if key == "id":  # Already got it
                        continue
                    if isinstance(value, list):
                        p = QStandardItem(key)
                        branch.appendRow([p])
                        for item in value:
                            p.appendRow(item)
                    elif isinstance(value, dict):
                        p = QStandardItem(key)
                        branch.appendRow([p])
                        for key_, value_ in value.items():
                            p.appendRow([QStandardItem(key_), QStandardItem(value_)])
                    else:
                        p = QStandardItem(key)
                        q = QStandardItem(str(value))
                        branch.appendRow([p, q])

        self.rootNode.appendRow([branch])