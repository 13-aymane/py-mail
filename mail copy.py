from os import sep
from PyQt5.QtWidgets import *
from PyQt5 import uic

import smtplib
import imaplib
import email
import sqlite3

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class MyGui(QMainWindow):
    
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("mail2.ui",self)
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,150)
        self.tableWidget.setColumnWidth(3,75)
        self.tableWidget.setColumnWidth(4,150)
        self.tableWidget.setColumnWidth(5,75)
        self.show()
        self.list()
        
        self.loginButton.clicked.connect(self.login)
        self.attachButton.clicked.connect(self.attach)
        self.sendButton.clicked.connect(self.send)
        self.fetchButton.clicked.connect(self.fetch)
        self.addButton.clicked.connect(self.add)
        self.listButton.clicked.connect(self.list)
        self.testButton.clicked.connect(self.test)
        self.searchButton.clicked.connect(self.search)
        self.search_domainButton.clicked.connect(self.searchDomain)
        self.delete_domainButton.clicked.connect(self.deleteDomain)
        self.add_termButton.clicked.connect(self.add_term)
    def login (self):
        try:
            #Getting Domain Details
            conn = sqlite3.connect("domains.db")
            c= conn.cursor()
            domain = self.emailField.text()
            x = domain.split("@", 1)
            target_domain = x[1]
            query=f"SELECT smtp_server, smtp_port, imap_server, imap_port FROM domains WHERE domain_name = '{target_domain}'"
            c.execute(query)
            results = list(c.fetchall())
            results_tuple = results[0]
            smtp_server, smtp_port, imap_server, imap_port = results_tuple
            #SMTP
            self.server = smtplib.SMTP(smtp_server, smtp_port)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.emailField.text(), self.pwdField.text())

            self.fetchButton.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.termField_2.setEnabled(True)
            self.termField.setEnabled(True)
            self.searchButton.setEnabled(True)
            self.add_termButton.setEnabled(True)
            self.termField.setEnabled(True)
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
                self.msg.attach(MIMEText(self.textField.toPlainText(), 'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.emailField.text(), self.toField.text(), text)

                
                message_box = QMessageBox()
                message_box.setText("Mail sent!")
                message_box.exec()
            except:
                message_box = QMessageBox()
                message_box.setText("Mail sending Failed!")
                message_box.exec() 
    def fetch(self):
        conn = sqlite3.connect("domains.db")
        c= conn.cursor()
        domain = self.emailField.text()
        x = domain.split("@", 1)
        target_domain = x[1]
        query=f"SELECT smtp_server, smtp_port, imap_server, imap_port FROM domains WHERE domain_name = '{target_domain}'"
        c.execute(query)
        results = list(c.fetchall())
        results_tuple = results[0]
        smtp_server, smtp_port, imap_server, imap_port = results_tuple    
        imap = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap.login(self.emailField.text(),self.pwdField.text())

        if self.comboBox.currentText() == "Inbox":
            imap.select("Inbox")

            _, msgnums = imap.search(None, "ALL")

            for msgnum in msgnums[0].split():
                _, data = imap.fetch(msgnum, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            self.fetchField.setPlainText(f"Message Number: {msgnum}")
            self.fetchField.setPlainText(f"From: {message.get('From')}")
            self.fetchField.setPlainText(f"To: {message.get('To')}")
            self.fetchField.setPlainText(f"BCC: {message.get('BCC')}")
            self.fetchField.setPlainText(f"Date: {message.get('Date')}")
            self.fetchField.setPlainText(f"Subject: {message.get('From')}")
            self.fetchField.setPlainText(f"Content:")
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    self.fetchField.setPlainText(part.as_string())
        else:
            imap.select("Sent")

            _, msgnums = imap.search(None, "ALL")

            for msgnum in msgnums[0].split():
                _, data = imap.fetch(msgnum, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            self.fetchField.setPlainText(f"Message Number: {msgnum}")
            self.fetchField.setPlainText(f"From: {message.get('From')}")
            self.fetchField.setPlainText(f"To: {message.get('To')}")
            self.fetchField.setPlainText(f"BCC: {message.get('BCC')}")
            self.fetchField.setPlainText(f"Date: {message.get('Date')}")
            self.fetchField.setPlainText(f"Subject: {message.get('From')}")
            self.fetchField.setPlainText(f"Content:")
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    self.fetchField.setPlainText(part.as_string())

        
        imap.close()
    def list(self):
        conn = sqlite3.connect("domains.db")
        c= conn.cursor()
        query="SELECT * FROM domains"
        results = c.execute(query) 
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.close()  
    def add(self):
            conn = sqlite3.connect("domains.db")
            c= conn.cursor()
            x = self.domainField.toPlainText()
            y = x.split("\n")
            for z in y:
                c.execute("INSERT INTO domains VALUES (:domain_grp,:domain,:smtp_server, :smtp_port, :imap_server, :imap_port)", 
                {'domain_grp':self.domaingrpField.text(),
                'domain':z, 
                'smtp_server': self.smtpField.text(),
                'smtp_port':self.smtp_portField.text(),
                'imap_server': self.imapField_2.text(),
                'imap_port':self.imap_portField.text()}
                )
                conn.commit()
            conn.close()
            message_box = QMessageBox()
            message_box.setText("Domains Added Successfully!")
            message_box.exec()
    def test(self):
        x = self.testField.toPlainText()
        y = x.split("\n")
        results_succ = []
        results_fail = []
        #individual mail and pwd
        for z in y:
            a = z.split( )
            #Getting Domain Details
            conn = sqlite3.connect("domains.db")
            c= conn.cursor()
            domain = a[0]
            x = domain.split("@", 1)
            target_domain = x[1]
            query=f"SELECT smtp_server, smtp_port, imap_server, imap_port FROM domains WHERE domain_name = '{target_domain}'"
            c.execute(query)
            result = list(c.fetchall())
            result_tuple = result[0]
            smtp_server, smtp_port, imap_server, imap_port = result_tuple
            server = smtplib.SMTP(smtp_server, smtp_port)
            try:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(a[0], a[1]) 
                results_succ +=[f"{a[0]} {a[1]}"]
                res_succ = "\n".join(results_succ)
                self.successField.setPlainText(res_succ) 
            except smtplib.SMTPAuthenticationError:
                results_fail +=[f"{a[0]} {a[1]}"]
                res_fail = "\n".join(results_fail)
                self.failureField.setPlainText(res_fail) 
            except:
                message_box = QMessageBox()
                message_box.setText("Login Failed!")
                message_box.exec()     
    def search(self):
        try:    
            #connection
            conn = sqlite3.connect("domains.db")
            c= conn.cursor()
            domain = self.emailField.text()
            x = domain.split("@", 1)
            target_domain = x[1]
            query=f"SELECT smtp_server, smtp_port, imap_server, imap_port FROM domains WHERE domain_name = '{target_domain}'"
            c.execute(query)
            results = list(c.fetchall())
            results_tuple = results[0]
            smtp_server, smtp_port, imap_server, imap_port = results_tuple    
            imap = imaplib.IMAP4_SSL(imap_server, imap_port)
            imap.login(self.emailField.text(),self.pwdField.text())
            term = self.termField.text()
            part = self.termField_2.text()
            #search in InBox
            if self.comboBox.currentText() == "Inbox":
                imap.select("Inbox")

                _, msgnums = imap.search(None, f'({part} {term})')

                for msgnum in msgnums[0].split():
                    _, data = imap.fetch(msgnum, "(RFC822)")

                message = email.message_from_bytes(data[0][1])
                self.fetchField.setPlainText(f"Message Number: {msgnum}")
                self.fetchField.setPlainText(f"From: {message.get('From')}")
                self.fetchField.setPlainText(f"To: {message.get('To')}")
                self.fetchField.setPlainText(f"BCC: {message.get('BCC')}")
                self.fetchField.setPlainText(f"Date: {message.get('Date')}")
                self.fetchField.setPlainText(f"Subject: {message.get('From')}")
                self.fetchField.setPlainText(f"Content:")
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        self.fetchField.setPlainText(part.as_string())                            
            #Search in Sent
            elif self.comboBox.currentText() == "Sent":
                imap.select("Inbox")
                _, msgnums = imap.search(None, f'({part} {term})')

                for msgnum in msgnums[0].split():
                    _, data = imap.fetch(msgnum, "(RFC822)")

                message = email.message_from_bytes(data[0][1])
                self.fetchField.setPlainText(f"Message Number: {msgnum}")
                self.fetchField.setPlainText(f"From: {message.get('From')}")
                self.fetchField.setPlainText(f"To: {message.get('To')}")
                self.fetchField.setPlainText(f"BCC: {message.get('BCC')}")
                self.fetchField.setPlainText(f"Date: {message.get('Date')}")
                self.fetchField.setPlainText(f"Subject: {message.get('From')}")
                self.fetchField.setPlainText(f"Content:")
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        self.fetchField.setPlainText(part.as_string())
                
        except:
            message_box = QMessageBox()
            message_box.setText("An Error has accured. Please check that you entered the right data!")
            message_box.exec()
    def searchDomain(self):
            conn = sqlite3.connect("domains.db")
            c= conn.cursor()
            query=f"SELECT * FROM domains WHERE domain_name= '{self.search_domainField.text()}'"
            results = c.execute(query) 
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            conn.close()
    def deleteDomain(self):
        try:
            pass
        except:
           pass
    def add_term(self):
        count = 1
        count = count + 1
        inputField_2 = QLineEdit()
        self.formLayout.addWidget(inputField_2)
        print(self.inputField_2.text())

app = QApplication([])
window = MyGui()
app.exec_()