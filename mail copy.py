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
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2,75)
        self.tableWidget.setColumnWidth(3,150)
        self.tableWidget.setColumnWidth(4,75)
        self.show()
        self.list()
        
        self.loginButton.clicked.connect(self.login)
        self.attachButton.clicked.connect(self.attach)
        self.sendButton.clicked.connect(self.send)
        self.fetchButton.clicked.connect(self.fetch)
        self.addButton.clicked.connect(self.add)
        self.listButton.clicked.connect(self.list)
        self.testButton.clicked.connect(self.test)
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
        try:    
            conn = sqlite3.connect("domains.db")
            c= conn.cursor()
            c.execute("INSERT INTO domains VALUES (:domaini_grp,:domain,:smtp_server, :smtp_port, :imap_server, :imap_port)", 
            {'domain_grp':self.domaingrpField.text(),
            'domain':self.domainField.text(), 
            'smtp_server': self.smtpField.text(),
            'smtp_port':self.smtp_portField.text(),
            'imap_server': self.imapField.text(),
            'imap_port':self.imap_portField.text()}
            )
            conn.commit()
            message_box = QMessageBox()
            message_box.setText("Domain Added Successfully!")
            message_box.exec()
            conn.close()
        except:
            message_box = QMessageBox()
            message_box.setText("An Error Has Accured")
            message_box.exec() 
    
   
    def test(self):
        x = self.testField.toPlainText()
        y = x.split("\n")
        results = []
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
                results +=[f"{a[0]} {a[1]} success "]
            except:
                results +=[f"{a[0]} {a[1]} failure "]        
        for b in results:
            self.resultField.setPlainText(str(b))
        
            
            
        


             
app = QApplication([])
window = MyGui()
app.exec_()