from os import sep
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import Qt
from PyQt5 import QtCore

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
        self.remove_termButton.clicked.connect(self.remove_term)
        self.count = 1
        self.lineEdits = [self.termForm]
        self.whereEdits = [self.whereForm]
        self.c = 0
        self.mail_list = []
        self.comboList = []
        self.list_terms = []
        self.list_where =[]
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
            
            self.searchButton.setEnabled(True)
            self.add_termButton.setEnabled(True)
            self.termForm.setEnabled(True)
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
        
            self.mail_list=[]
            res_mail= " "
            self.fetchField.setPlainText(res_mail)
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
            #search in InBox
            if self.comboBox.currentText() == "Inbox":
                imap.select("Inbox")
                #making the query
                for i in self.lineEdits:
                    x = i.text()
                    t=f'"{x}"'
                    self.list_terms.append(t)
                for j in self.whereEdits:
                    #print(j.text())
                    self.list_where.append(j.text())
                l = list(map(' '.join, zip(self.list_where, self.list_terms)))
                #print (l)
                s = ' '.join(l)
                print(s)
                _, msgnums = imap.search(None, f'{s}')
                for msgnum in msgnums[0].split():
                            _, data = imap.fetch(msgnum, "(RFC822)")
                            message = email.message_from_bytes(data[0][1])
                            mail_num =f"Message Number: {msgnum}"
                            mail_from =f"From: {message.get('From')}"
                            mail_to = f"To: {message.get('To')}"
                            mail_bcc = f"BCC: {message.get('BCC')}"
                            mail_date = f"Date: {message.get('Date')}"
                            mail_subject = f"Subject: {message.get('From')}"
                            mail_content = f"Content:"
                            for part in message.walk():
                                if part.get_content_type() == "text/plain":
                                    mail_part = part.as_string()
                            line = "========================================="
                            mail = "\n".join([mail_num] + [mail_from] + [mail_to] + [mail_bcc] + [mail_date] + [mail_subject] + [mail_content] +[mail_part] + [line])           
                            self.mail_list.append(mail)   
                    
                res_mail = "\n".join(self.mail_list)
                print(res_mail)
                self.fetchField.setPlainText(res_mail)
                self.fetchField.setEnabled(True) 
            #Search in Sent
            elif self.comboBox.currentText() == "Sent":
                imap.select("Sent")
                
                for i in self.lineEdits:
                    term = i.text()
                    part = self.termField_2.text()
                    mail_num = ""
                    mail_from = ""
                    mail_to = ""
                    mail_bcc = ""
                    mail_date = ""
                    mail_subject = ""
                    mail_content = ""
                    mail_part = ""
                    
                    _, msgnums = imap.search(None, f"{part} {term}")
                    print(f"{part} {term}")
                    for msgnum in msgnums[0].split():
                        _, data = imap.fetch(msgnum, "(RFC822)")
                        message = email.message_from_bytes(data[0][1])
                        mail_num =f"Message Number: {msgnum}"
                        mail_from =f"From: {message.get('From')}"
                        mail_to = f"To: {message.get('To')}"
                        mail_bcc = f"BCC: {message.get('BCC')}"
                        mail_date = f"Date: {message.get('Date')}"
                        mail_subject = f"Subject: {message.get('From')}"
                        mail_content = f"Content:"
                        for part in message.walk():
                            if part.get_content_type() == "text/plain":
                                mail_part = part.as_string()
                        line = "========================================="
                        mail = "\n".join([mail_num] + [mail_from] + [mail_to] + [mail_bcc] + [mail_date] + [mail_subject] + [mail_content] +[mail_part] + [line])           
                        self.mail_list.append(mail)   
                
                res_mail = "\n".join(self.mail_list)
                print(res_mail)
                self.fetchField.setPlainText(res_mail)       
        
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
        self.count += 1
        #label
        self.termLable = QLabel(self)
        self.termLable.setText(f"Term {self.count} :")
        self.gridLayout.addWidget(self.termLable)
        #term
        self.termForm = QLineEdit(self)
        self.gridLayout.addWidget(self.termForm )
        self.lineEdits.append(self.termForm)
        #where
        self.whereForm = QLineEdit(self)
        self.gridLayout.addWidget(self.whereForm )
        self.whereEdits.append(self.whereForm)
        
        return self.lineEdits, self.whereEdits    
    def remove_term(self):
        c = self.gridLayout.count()
        #Where
        self.gridLayout.itemAt(c-1).widget().setParent(None)
        #term
        self.gridLayout.itemAt(c-2).widget().setParent(None)
        #label
        self.gridLayout.itemAt(c-3).widget().setParent(None)
        

app = QApplication([])
window = MyGui()
app.exec_()
