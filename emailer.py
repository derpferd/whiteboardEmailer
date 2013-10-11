import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


class Mailer(object):
	"""Mailer is a class for sending emails through a smtp server."""
	def __init__(self, server, port, username=None, password=None, useTLS=False):
		self.server = server
		self.port = port
		self.username = username
		self.password = password
		self.useTLS = useTLS
	
	def __sendMsg(self, sendFrom, sendTo, msg):
		print "Connecting to smtp server..."
		smtp = smtplib.SMTP(self.server, self.port)
		if self.useTLS:
			print "Starting tls..."
			smtp.starttls()
		if self.username and self.password:
			print "Logging in..."
			smtp.login(self.username, self.password)
		if type(msg)!=str:
			msg = msg.as_string()
		print "Sending Mail..."
		smtp.sendmail(sendFrom, sendTo, msg)
		print "Closing connection with smtp server..."
		smtp.close()

	def tryConnection(self):
		smtp = smtplib.SMTP(self.server, self.port)
		smtp.close()

	def tryLogin(self):
		smtp = smtplib.SMTP(self.server, self.port)
		if self.useTLS:
			smtp.starttls()
		if self.username and self.password:
			smtp.login(self.username, self.password)
		smtp.close()


	def sendMail(self, sendFrom, sendTo, subject, text, attachments=[]):
		"""
		attachments must be a list of name value pairs.
		Ex. [(name, data)]
		"""
		if type(sendTo)==str:
			sendTo = [sendTo]

		assert type(sendFrom)==str
		assert type(sendTo)==list
		assert type(subject)==str
		assert type(text)==str
		assert type(attachments)==list

		msg = MIMEMultipart()
		msg['From'] = sendFrom
		msg['To'] = COMMASPACE.join(sendTo)
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = subject

		msg.attach(MIMEText(text))

		for attachment in attachments:
			part = MIMEBase('application', "octet-stream")
			part.set_payload( attachment[1] )
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % attachment[0])
			msg.attach(part)

		self.__sendMsg(sendFrom, sendTo, msg)
