#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv, exit
from multiprocessing import Process

from PyQt4 import QtCore
from PyQt4 import QtGui

import tftpy


class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._init_ui()

        self.server = None

    def __del__(self):
        self.server.terminate()

    def _init_ui(self):
        self.main_layout = QtGui.QVBoxLayout(self)

        self.main_layout.addWidget(QtGui.QLabel('Каталог TFTP-сервера:'))

        self.catalog_layout = QtGui.QHBoxLayout(self)
        self.catalog_edit = QtGui.QLineEdit()
        self.catalog_edit.setReadOnly(True)
        self.catalog_layout.addWidget(self.catalog_edit)

        self.choose_catalog_btn = QtGui.QPushButton('Выбрать')
        self.connect(self.choose_catalog_btn, QtCore.SIGNAL('pressed()'),
                     self.choose_catalog)
        self.catalog_layout.addWidget(self.choose_catalog_btn)

        self.main_layout.addLayout(self.catalog_layout)

        self.main_layout.addWidget(QtGui.QLabel('Порт:'))
        self.port_edit = QtGui.QLineEdit('8069')
        self.port_edit.setValidator(QtGui.QIntValidator(1024, 65536))
        self.main_layout.addWidget(self.port_edit)

        self.run_btn = QtGui.QPushButton('Запустить сервер')
        self.connect(self.run_btn, QtCore.SIGNAL('pressed()'), self.start)
        self.run_btn.setDisabled(True)
        self.main_layout.addWidget(self.run_btn)

        self.setLayout(self.main_layout)
        self.setWindowTitle('TFTP Сервер')
        self.setMinimumWidth(300)
        self.center()
        self.show()

    def choose_catalog(self):
        catalog = QtGui.QFileDialog().getExistingDirectory(self,
                                                           'Выбор каталога')

        if not catalog:
            return

        self.catalog_edit.setText(catalog)
        self.run_btn.setEnabled(True)

    def start(self):
        self.server = Process(target=self.run, args=(
            unicode(self.catalog_edit.text()), int(self.port_edit.text())))
        self.server.start()

        self.run_btn.setText('Остановить сервер')
        self.disconnect(self.run_btn, QtCore.SIGNAL('pressed()'), self.start)
        self.connect(self.run_btn, QtCore.SIGNAL('pressed()'), self.stop)

    def run(self, catalog, port):
        server = tftpy.TftpServer(catalog)
        while True:
            try:
                server.listen('0.0.0.0', port)
            except Exception:
                continue

    def stop(self):
        self.server.terminate()
        self.run_btn.setText('Запустить сервер')
        self.disconnect(self.run_btn, QtCore.SIGNAL('pressed()'), self.stop)
        self.connect(self.run_btn, QtCore.SIGNAL('pressed()'), self.start)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    QtCore.QTextCodec.setCodecForCStrings(
        QtCore.QTextCodec.codecForName('UTF-8'))
    app = QtGui.QApplication(argv)
    window = MainWindow()
    exit(app.exec_())
