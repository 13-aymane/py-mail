import sqlite3
#conn = sqlite3.connect("domains.db")
#c= conn.cursor()

#c.execute("CREATE TABLE domains (domain_name text, smtp_server text, smtp_port interger, imap_server text, imap_port integer )")
#conn.commit()
#insert domain query
#c.execute("INSERT INTO domains VALUES (:domain_name,:smtp_server, :smtp_port, :imap_server, :imap_port)", 
#           {'domain_name':'outlook.com', 
 #         'smtp_server': 'outlook.office365.com',
  #    'smtp_port':'587',
   # 'imap_server': 'smtp-mail.outlook.com',
  #'imap_port':'993' })
#conn.commit()

#c.execute("SELECT * FROM domains")
#print(c.fetchall())

#c.execute("DROP TABLE domains")
#conn.close()

results = [('outlook.office365.com', 587, 'smtp-mail.outlook.com', 993)]

results_tuple = results[0]
smtp_server, smtp_port, imap_server, imap_port = results_tuple
print(smtp_server)
print(smtp_port)