from PyQt5.QtWidgets import *
from PyQt5 import uic

import smtplib
import imaplib
import email

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("mail.ui",self)
        self.show()
        
        self.loginButton.clicked.connect(self.login)
        self.attachButton.clicked.connect(self.attach)
        self.sendButton.clicked.connect(self.send)
        self.fetchButton.clicked.connect(self.fetch)
    def login (self):
        try:
            self.server = smtplib.SMTP(self.smtpField.text(), self.portField.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.emailField.text(), self.pwdField.text())


            self.msg=MIMEMultipart()

            message_box = QMessageBox()
            message_box.setText("Login Successful!")
            message_box.exec() 

        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setText("Invalid Login Information")
            message_box.exec()
        except:
            message_box = QMessageBox()
            message_box.setText("Login Failed!")
            message_box.exec()    
    def attach (self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.get.OpenFialeNames(self ,"Open File", "", "All Files (*.*")
        if filenames !=[]:
            for filename in filenames:
                attachment = open(filename, 'rb')
                filename = filename[filename.rfind("/") +1:]
                p = MIMEBase ('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                if not self.label_8.text().endswith(":"):
                    self.label_8.setText(self.label_8.text() + ",")
                self.label_8.setText(self.label_8.text() + " " +filename)
    def send (self):
        dialog=QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)

        if dialog.exec_() == 0:
            try:
                self.msg['From'] = "Aymane"
                self.msg['To'] = self.toField.text()
                self.msg['Subject'] = self.subjectField.text()
                
                self.msg.attach(MIMEText(self.textField.toPlaintext(), 'plain'))
                txt_msg = self.msg.as_string()

                self.server.sendmail(self.emailField.text(), self.toField.text(), txt_msg)
                
                message_box = QMessageBox()
                message_box.setText("Mail sent!")
                message_box.exec()
            except:
                message_box = QMessageBox()
                message_box.setText("Mail Sending Failed!")
                message_box.exec() 

    def fetch(self):
    
        imap = imaplib.IMAP4_SSL(self.imapField.text())
        imap.login(self.emailField.text(),self.pwdField.text())

        imap.select("Inbox")

        _, msgnum = imap.search(None, "ALL")

        for msgnum in msgnum[0].split():
            _, data = imap.fetch(msgnum, "(RFC822")

        message = email.message_from_bytes(data[0][1])

        def output():
            print(f"Message Number: {msgnum}")
            print(f"From: {message.get('From')}")
            print(f"To: {message.get('To')}")
            print(f"BCC: {message.get('BCC')}")
            print(f"Date: {message.get('Date')}")
            print(f"Subject: {message.get('From')}")

            print(f"Content:")
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    print(part.as_string())

        self.fetchField.append(str(output))
        imap.close()

app = QApplication([])
window = MyGui()
app.exec_()