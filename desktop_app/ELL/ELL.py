from cgitb import text
from fileinput import filename
from gc import isenabled
import sys
import os
import importlib
import requests
import tensorflow
from PyQt5 import QtGui
import importlib.util
from PyQt5.QtWidgets import (
    QFormLayout, QRadioButton, QGroupBox, QWidget,QTextEdit, QFileDialog, QComboBox, QVBoxLayout, QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)


# https://pythonspot.com/pyqt5-file-dialog/
class LearningWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle('ELL')
        self.resize(600, 600)
        self.setMaximumWidth(600)
        self.setMaximumHeight(600)
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        layout = QGridLayout()

        self.token = token
        self.python_script = ''
        self.federated_round = 0
        self.isTestUploaded = False
        self.isTrainUploaded = False
        self.isScriptUploaded = False
        self.isWeightUploaded = False

        groupbox2 = QGroupBox("Upload file paths")
        layout.addWidget(groupbox2)

        vbox2 = QVBoxLayout()

        button_upload_train = QPushButton('Select training dataset',self)
        button_upload_train.clicked.connect(self.get_training_folder)
        vbox2.addWidget(button_upload_train)

        flo1 = QFormLayout()
        self.line_train = QLineEdit("...")
        self.line_train.setReadOnly(True)
        self.line_train.setFixedWidth(300)
        flo1.addRow("Train dataset path: ",self.line_train)
        vbox2.addLayout(flo1)

        button_upload_test = QPushButton('Select test dataset',self)
        button_upload_test.clicked.connect(self.get_testing_folder)
        vbox2.addWidget(button_upload_test)

        flo2 = QFormLayout()
        self.line_test = QLineEdit("...")
        self.line_test.setReadOnly(True)
        self.line_test.setFixedWidth(300)
        flo2.addRow("Test dataset path: ",self.line_test)
        vbox2.addLayout(flo2)

        self.button_upload_learning = QPushButton('Select learning script',self)
        self.button_upload_learning.clicked.connect(self.get_script_path)
        vbox2.addWidget( self.button_upload_learning)

        flo3 = QFormLayout()
        self.line_script = QLineEdit("...")
        self.line_script.setReadOnly(True)
        self.line_script.setFixedWidth(300)
        flo3.addRow("Learning script path: ",self.line_script)
        vbox2.addLayout(flo3)

        self.button_upload_weights = QPushButton('Select weights .h5',self)
        self.button_upload_weights.clicked.connect(self.get_weights_path)
        self.button_upload_weights.hide()
        vbox2.addWidget(self.button_upload_weights)


        flo4 = QFormLayout()
        self.line_weights = QLineEdit("...")
        self.line_weights.setReadOnly(True)
        self.line_weights.setFixedWidth(300)
        self.label_weights = QLabel("Previous learning weights' path: ")

        flo4.addRow(self.label_weights,self.line_weights)
        self.label_weights.hide()
        self.line_weights.hide()
        vbox2.addLayout(flo4)



        groupbox2.setLayout(vbox2)

        groupbox = QGroupBox('Learning')
        layout.addWidget(groupbox)

        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)


        self.button_results = QPushButton('Select where to store local weights',self)
        self.button_results.clicked.connect(self.get_results_folder)
        vbox.addWidget(self.button_results)


        flo5 = QFormLayout()
        self.line_results = QLineEdit("...")
        self.line_results.setReadOnly(True)
        self.line_results.setFixedWidth(300)
        self.label_results = QLabel("Path to local weights: ")

        flo5.addRow(self.label_results,self.line_results)
        vbox.addLayout(flo5)

        self.button_learn = QPushButton('Run',self)
        self.button_learn.setEnabled(False)
        self.button_learn.clicked.connect(self.run_learning)

        vbox.addWidget(self.button_learn)


        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def get_training_folder(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            self.isTrainUploaded = True
            is_enabled = self.isTrainUploaded and self.isTestUploaded and self.isScriptUploaded and  self.isWeightUploaded
            self.button_learn.setEnabled(is_enabled)
            self.line_train.setText(folderpath)
            # self.line_train.adjustSize()
            print(self.line_train.text())
            print(self.token)

    def get_results_folder(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            self.line_results.setText(folderpath)
            # self.line_results.adjustSize()
            print(self.line_results.text())

    def get_testing_folder(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            self.isTestUploaded = True
            is_enabled = self.isTrainUploaded and self.isTestUploaded and self.isScriptUploaded and self.isWeightUploaded
            self.button_learn.setEnabled(is_enabled)
            self.line_test.setText(folderpath)
            # self.line_test.adjustSize()
            print(self.line_train.text())

    def get_script_path(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self,"ELL", "","Python Files (*.py)")
        if fileName[0]:
            self.python_script = fileName[0]
            f = open(fileName[0],'r')

            with f:
                data = f.read()
                for item in data.split("\n"):
                    if "federated_round" in item:
                        self.federated_round = eval(item.strip("federated_round = "))
                        break
            if self.federated_round > 1:
                self.label_weights.show()
                self.line_weights.show()
                self.button_upload_weights.show()
            else:
                self.isWeightUploaded = True

            self.isScriptUploaded = True
            is_enabled = self.isTrainUploaded and self.isTestUploaded and self.isScriptUploaded and self.isWeightUploaded
            self.button_learn.setEnabled(is_enabled)
            self.line_script.setText(fileName[0])
            # self.line_script.adjustSize()
            print(self.line_script.text())

    def get_weights_path(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self,"ELL", "","HDF5 Files (*.h5)")
        if fileName[0]:
            self.isWeightUploaded= True
            is_enabled = self.isTrainUploaded and self.isTestUploaded and self.isScriptUploaded and self.isWeightUploaded
            self.button_learn.setEnabled(is_enabled)
            self.line_weights.setText(fileName[0])
            # self.line_weights.adjustSize()
            print(self.line_weights.text())

    def run_learning(self):
        spec = importlib.util.spec_from_file_location(self.python_script, self.python_script)
        learner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(learner)
        # function bellow is executed from aggregation script
        datapath = str(self.line_train.text())
        testpath = str(self.line_test.text())
        weights =  str(self.line_weights.text()) if self.federated_round != 0 else None
        absolute_path = str(self.line_results.text()) if str(self.line_results.text()) != '...' else os.getcwd()

        print(self.token)
        print(datapath)
        print(testpath)
        print(weights)
        print(absolute_path)
        learner.local_learning(self.token, datapath, testpath, absolute_path, weights)

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ELL')
        self.resize(500, 120)
        self.setMaximumWidth(500)
        self.setMaximumHeight(120)
        self.setMinimumWidth(500)
        self.setMinimumHeight(120)
        self.layout = QGridLayout()

        label_name = QLabel('<font size="4"> Email </font>')
        self._email = QLineEdit()
        self._email.setPlaceholderText('Please enter your email')
        self.layout.addWidget(label_name, 0, 0)
        self.layout.addWidget(self._email, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self._password = QLineEdit()
        self._password.setEchoMode(QLineEdit.Password)
        self._password.setPlaceholderText('Please enter your password')
        self.layout.addWidget(label_password, 1, 0)
        self.layout.addWidget(self._password, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        self.layout.addWidget(button_login, 2, 0, 1, 2)
        self.layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)

    def check_password(self):
        msg = QMessageBox()
        myobj = {'email': self._email.text(), 'password': self._password.text()}
        login_resp = requests.post('http://127.0.0.1:8000/api/v1/token/login/',  data=myobj)
        print(login_resp)
        token = login_resp.content.decode("utf-8")[len('{"auth_token":"'):-2]
        if login_resp.status_code == 200:
            self.show_learning(token)
        else:
            msg.setText('Incorrect credentials')
            msg.exec_()

    def show_learning(self,token):
        self.w = LearningWindow(token)
        self.w.show()
        self.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('logo.png'))
    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
