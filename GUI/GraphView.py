#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl


class GraphView(QWebView):
    def __init__(self):
        super().__init__()

    def load(self, string):
        super().load(QUrl("file://"+string))