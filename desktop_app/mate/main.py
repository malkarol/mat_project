import sys
import os
import importlib
import requests
import importlib.util
from PyQt5.QtWidgets import (
    QWidget,QTextEdit, QFileDialog, QComboBox, QVBoxLayout, QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

# https://pythonspot.com/pyqt5-file-dialog/
class LearningWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'MATE'
        self.left = 10
        self.top = 10
        self.width = 200
        self.height = 200

        self.python_script = ''
        button_learn = QPushButton('Learn',self)
        button_learn.resize(100,32)
        button_learn.move(50, 100)
        button_learn.clicked.connect(self.run_learning)
        button_upload = QPushButton('Upload',self)
        button_upload.resize(100,32)
        button_upload.move(50, 50)
        button_upload.clicked.connect(self.openFileNameDialog)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"MATE", "","Python Files (*.py)", options=options)
        if fileName:
            self.python_script = fileName

    def run_learning(self):
        spec = importlib.util.spec_from_file_location(self.python_script, self.python_script)
        aggregator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aggregator)
        # function bellow is executed from aggregation script
        aggregator.hello()
        # we can also execute the script but params dont work for now
        # exec(open(self.python_script).read())


    # def openFileNamesDialog(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
    #     if files:
    #         print(files)

    # def saveFileDialog(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
    #     if fileName:
    #         print(fileName)

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MATE')
        self.resize(500, 120)

        layout = QGridLayout()

        label_name = QLabel('<font size="4"> Email </font>')
        self._email = QLineEdit()
        self._email.setPlaceholderText('Please enter your email')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self._email, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self._password = QLineEdit()
        self._password.setEchoMode(QLineEdit.Password)
        self._password.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self._password, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def check_password(self):
        msg = QMessageBox()
        myobj = {'email': self._email.text(), 'password': self._password.text()}
        login_resp = requests.post('http://127.0.0.1:8000/api/v1/token/login/',  data=myobj)
        print(login_resp)
        # new_r = r.content.decode("utf-8")[len('{"auth_token":"'):-2]
        if login_resp.status_code == 200:
            self.show_learning()
        else:
            msg.setText('Incorrect Password')
            msg.exec_()

    def show_learning(self):
        self.w = LearningWindow()
        self.w.show()
        self.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
