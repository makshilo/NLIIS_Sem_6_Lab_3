# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import json
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QFileDialog
from generate_semantic_tree import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 560)
        MainWindow.setMinimumSize(QtCore.QSize(850, 560))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.openFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.openFileButton.setObjectName("openFileButton")
        self.verticalLayout_3.addWidget(self.openFileButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_3.addWidget(self.saveButton)
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setObjectName("helpButton")
        self.verticalLayout_3.addWidget(self.helpButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.inputTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.inputTextEdit.setObjectName("inputTextEdit")
        self.horizontalLayout_3.addWidget(self.inputTextEdit, 0, QtCore.Qt.AlignTop)
        self.generateButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateButton.setObjectName("generateButton")
        self.horizontalLayout_3.addWidget(self.generateButton)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logLabel = QtWidgets.QLabel(self.centralwidget)
        self.logLabel.setObjectName("logLabel")
        self.verticalLayout_2.addWidget(self.logLabel)
        self.logTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logTextBrowser.setObjectName("logTextBrowser")
        self.verticalLayout_2.addWidget(self.logTextBrowser, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.outputLabel = QtWidgets.QLabel(self.centralwidget)
        self.outputLabel.setObjectName("outputLabel")
        self.verticalLayout_4.addWidget(self.outputLabel)
        self.outputTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.outputTextBrowser.setFont(QFont("Ubuntu Mono", 11))
        self.outputTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.outputTextBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.outputTextBrowser.setObjectName("outputTextBrowser")
        self.verticalLayout_4.addWidget(self.outputTextBrowser)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.openFileButton.clicked.connect(self.open_file)
        self.helpButton.clicked.connect(self.help_display)
        self.generateButton.clicked.connect(self.generate_output)
        self.saveButton.clicked.connect(self.save_output)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Semantic analysis"))
        self.openFileButton.setText(_translate("MainWindow", "Open file"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.helpButton.setText(_translate("MainWindow", "Help"))
        self.generateButton.setText(_translate("MainWindow", "Generate tree"))
        self.logLabel.setText(_translate("MainWindow", "Log"))
        self.outputLabel.setText(_translate("MainWindow", "Output"))

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Open file', '', 'TXT files (*.txt)')
        if file_name:
            self.inputTextEdit.setText(open(file_name).read())
            self.logTextBrowser.clear()
            self.logTextBrowser.append("File opened")
        else:
            self.logTextBrowser.append('File not selected')

    def help_display(self):
        # display help dialog
        help_dialog = QDialog()
        help_dialog.setWindowTitle('Help')
        help_dialog.setFixedSize(500, 250)
        # add text
        help_text = QLabel('<h1>Syntax analysis</h1>'
                           '<p>This program is a simple semantic analysis program. '
                           'It can be used to parse the semantic tree of any text loaded from text file. '
                           'It can also be used to save result into xml file.</p>')
        help_text.setWordWrap(True)
        help_text.setAlignment(Qt.AlignCenter)
        # add buttons
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(help_dialog.close)
        # add layout
        layout = QVBoxLayout()
        layout.addWidget(help_text)
        layout.addWidget(ok_button)
        help_dialog.setLayout(layout)
        help_dialog.exec_()

    def generate_output(self):
        input_text = self.inputTextEdit.toPlainText()
        if input_text:
            # generate tree
            try:
                self.logTextBrowser.append('Generating tree...')
                start = time.time()
                sem_tree = generate_semantic_tree(input_text)
                end = time.time()
                self.logTextBrowser.append('Tree generated in ' + str(end - start) + ' seconds')
                self.outputTextBrowser.setText(tree_to_text(sem_tree))
            except Exception as e:
                self.logTextBrowser.append(str(e))
        else:
            self.logTextBrowser.append('No input')

    def save_output(self):
        input_text = self.inputTextEdit.toPlainText()
        if input_text:
            sem_tree = generate_semantic_tree(input_text)
            if tree_to_text(sem_tree) != self.outputTextBrowser.toPlainText():
                self.outputTextBrowser.setText(tree_to_text(sem_tree))
            tree_xml = tree_to_xml(sem_tree)
            # write using qt
            file_dialog = QFileDialog()
            file_dialog.setDefaultSuffix('xml')
            file_name, _ = file_dialog.getSaveFileName(None, 'Save file', '', 'XML files (*.xml)')
            if file_name:
                with open(file_name, 'wb') as file:
                    file.write(tree_xml)
                    self.logTextBrowser.append('File saved')
            else:
                self.logTextBrowser.append('File not selected')
        else:
            self.logTextBrowser.append('No input')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
