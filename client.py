#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv, exit

from PyQt4 import QtCore
from PyQt4 import QtGui

import tftpy


class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._init_ui()

        self.server = None

    def _init_ui(self):
        self.main_layout = QtGui.QVBoxLayout(self)

        self.main_layout.addWidget(QtGui.QLabel('Адрес сервера:'))
        self.ip_edit = QtGui.QLineEdit('127.0.0.1')
        ip_reg_exp = QtCore.QRegExp('[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.['
                                    '0-9]{1,3}')
        ip_validator = QtGui.QRegExpValidator(ip_reg_exp)
        self.ip_edit.setValidator(ip_validator)
        self.main_layout.addWidget(self.ip_edit)

        self.main_layout.addWidget(QtGui.QLabel('Порт:'))
        self.port_edit = QtGui.QLineEdit('8069')
        self.port_edit.setValidator(QtGui.QIntValidator(1024, 65536))
        self.main_layout.addWidget(self.port_edit)

        self.main_layout.addWidget(QtGui.QLabel('Имя скачиваемого файла:'))
        self.file_download_edit = QtGui.QLineEdit('')
        self.main_layout.addWidget(self.file_download_edit)

        self.main_layout.addWidget(QtGui.QLabel('Место сохранения файла:'))
        self.save_location_layout = QtGui.QHBoxLayout(self)
        self.save_location_edit = QtGui.QLineEdit()
        self.save_location_edit.setReadOnly(True)
        self.save_location_layout.addWidget(self.save_location_edit)

        self.choose_save_location_btn = QtGui.QPushButton('Выбрать')
        self.connect(self.choose_save_location_btn, QtCore.SIGNAL('pressed()'),
                     self.choose_save_location)
        self.save_location_layout.addWidget(self.choose_save_location_btn)
        self.main_layout.addLayout(self.save_location_layout)

        self.download_btn = QtGui.QPushButton('Скачать')
        self.connect(self.download_btn, QtCore.SIGNAL('pressed()'),
                     self.download)
        self.download_btn.setDisabled(True)
        self.main_layout.addWidget(self.download_btn)

        self.main_layout.addWidget(QtGui.QLabel('Имя загружаемого файла:'))
        self.file_save_edit = QtGui.QLineEdit('')
        self.main_layout.addWidget(self.file_save_edit)

        self.main_layout.addWidget(QtGui.QLabel('Файл на компьютере:'))
        self.file_upload_layout = QtGui.QHBoxLayout(self)
        self.file_upload_edit = QtGui.QLineEdit()
        self.file_upload_edit.setReadOnly(True)
        self.file_upload_layout.addWidget(self.file_upload_edit)

        self.choose_file_upload_btn = QtGui.QPushButton('Выбрать')
        self.connect(self.choose_file_upload_btn, QtCore.SIGNAL('pressed()'),
                     self.choose_file_upload)
        self.file_upload_layout.addWidget(self.choose_file_upload_btn)
        self.main_layout.addLayout(self.file_upload_layout)

        self.upload_btn = QtGui.QPushButton('Загрузить')
        self.connect(self.upload_btn, QtCore.SIGNAL('pressed()'), self.upload)
        self.upload_btn.setDisabled(True)
        self.main_layout.addWidget(self.upload_btn)

        self.setLayout(self.main_layout)
        self.setWindowTitle('TFTP Клиент')
        self.setMinimumWidth(300)
        self.center()
        self.show()

    def choose_save_location(self):
        save_location = QtGui.QFileDialog().getSaveFileName(self, '')
        if not save_location:
            return

        self.save_location_edit.setText(save_location)
        self.download_btn.setEnabled(True)

    def choose_file_upload(self):
        upload_file = QtGui.QFileDialog().getOpenFileName(self, '')
        if not upload_file:
            return

        self.file_upload_edit.setText(upload_file)
        self.upload_btn.setEnabled(True)

    def download(self):
        client = tftpy.TftpClient(str(self.ip_edit.text()),
                                  int(self.port_edit.text()))
        try:
            client.download(str(self.file_download_edit.text()),
                            unicode(self.save_location_edit.text()))
        except tftpy.TftpShared.TftpTimeout:
            QtGui.QMessageBox().warning(self, 'Ошибка',
                                        'Ошибка доступа к серверу')
        except tftpy.TftpShared.TftpException:
            QtGui.QMessageBox().warning(self, 'Ошибка',
                                        'Ошибка скачивания файла')

    def upload(self):
        client = tftpy.TftpClient(str(self.ip_edit.text()),
                                  int(self.port_edit.text()))
        try:
            client.upload(str(self.file_save_edit.text()),
                          unicode(self.file_upload_edit.text()), timeout=1)
        except tftpy.TftpShared.TftpTimeout:
            QtGui.QMessageBox().warning(self, 'Ошибка',
                                        'Ошибка доступа к серверу')

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
