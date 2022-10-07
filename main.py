import datetime
import json
import os.path
import sys

import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class App(QDialog):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        # Init Window
        self.formGroupBox = None
        self.title_app = 'Create Task Bitrix24 (HashMicro)'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 200
        # Check Config
        if os.path.isfile('config.json'):
            config = json.load(open('config.json'))
        else:
            config = open('config.json', 'w')
            with config as f:
                json.dump({
                    'title': 'Test API',
                    'description': 'Test API',
                    'deadline': '2023-06-30 00:00:00',
                    'observer': '1179,113',
                    'group': '127',
                    'responsible': '113',
                    'created_by': '1179'}, f)
            config = json.load(open('config.json', 'r'))
        # Set Config
        self.title = config['title']
        self.description = config['description']
        self.deadline = config['deadline']
        self.observer = config['observer']
        self.group = config['group']
        self.responsible = config['responsible']
        self.created_by = config['created_by']
        # Init UI
        self.le_title = QLineEdit(self.title)
        self.le_description = QTextEdit(self.description)
        self.le_deadline = QLineEdit(self.deadline)
        self.le_observer = QLineEdit(self.observer)
        self.le_group = QLineEdit(self.group)
        self.le_responsible = QLineEdit(self.responsible)
        self.le_created_by = QLineEdit(self.created_by)
        self.le_title.setFixedSize(200, 20)
        self.le_description.setFixedSize(200, 100)
        self.le_deadline.setFixedSize(200, 20)
        self.le_observer.setFixedSize(200, 20)
        self.le_group.setFixedSize(200, 20)
        self.le_responsible.setFixedSize(200, 20)
        self.le_created_by.setFixedSize(200, 20)
        self.setWindowTitle(self.title_app)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.initui()

    def popup(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return

    def addtask(self):
        # Get Config
        self.title = self.le_title.text()
        self.description = self.le_description.toPlainText()
        self.deadline = datetime.datetime.strptime(self.le_deadline.text(), '%Y-%m-%d %H:%M:%S')
        # Convert to Bitrix24 format
        self.deadline = self.deadline.strftime('%Y-%m-%dT%H:%M:%S+07:00')
        self.observer = self.le_observer.text()
        self.group = self.le_group.text()
        self.responsible = self.le_responsible.text()
        self.created_by = self.le_created_by.text()
        # Create Task
        if ',' in self.observer:
            # Create Array
            self.observer = self.observer.split(',')
        headers = {'content-type': 'application/json'}
        data_task = {
            'fields': {
                'TITLE': self.title,
                'DESCRIPTION': self.description,
                'DEADLINE': self.deadline,
                'AUDITORS': self.observer,
                'GROUP_ID': self.group,
                'RESPONSIBLE_ID': self.responsible,
                'CREATED_BY': self.created_by,
            }
        }
        data_task_json = json.dumps(data_task)

        req = requests.post(
            "https://hashmicro.bitrix24.id/rest/1179/8yak2y35krao098c/tasks.task.add", data=data_task_json,
            headers=headers)
        if req.status_code == 200:
            self.popup('Success', 'Task Created')
        else:
            self.popup('Error', 'Task Failed')

    def save(self):
        config = open('config.json', 'w')
        with config as f:
            json.dump({
                'title': self.le_title.text(),
                'description': self.le_description.toPlainText(),
                'deadline': self.le_deadline.text(),
                'observer': self.le_observer.text(),
                'group': self.le_group.text(),
                'responsible': self.le_responsible.text(),
                'created_by': self.le_created_by.text()}, f)
        self.popup('Success', 'Config Saved')

    def initui(self):
        self.formGroupBox = QGroupBox("Task")
        layout = QFormLayout()
        layout.addRow(QLabel("Title:"), self.le_title)
        layout.addRow(QLabel("Description:"), self.le_description)
        layout.addRow(QLabel("Deadline:"), self.le_deadline)
        layout.addRow(QLabel("Observer:"), self.le_observer)
        layout.addRow(QLabel("Group:"), self.le_group)
        layout.addRow(QLabel("Responsible:"), self.le_responsible)
        layout.addRow(QLabel("Created By:"), self.le_created_by)
        self.formGroupBox.setLayout(layout)
        buttonCreate = QPushButton('Create Task')
        buttonCreate.clicked.connect(self.addtask)
        buttonSave = QPushButton('Save Config')
        buttonSave.clicked.connect(self.save)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonCreate)
        mainLayout.addWidget(buttonSave)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.jpg'))
    form = App()
    form.show()
    app.exec_()
