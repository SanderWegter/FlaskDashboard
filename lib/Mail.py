#from lib.Database import LocalDatabase
from lib.Config import Config
from jinja2 import Environment, PackageLoader, FileSystemLoader
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail:
	def __init__(self):
		self.config = Config()
		self.env = Environment(loader=FileSystemLoader(searchpath="templates/mail"))

	def connect(self):
		self.server = SMTP_SSL(self.config.getConfig()["email"]["smtp_host"],self.config.getConfig()["email"]["smtp_port"])
		self.server.login(self.config.getConfig()["email"]["username"],self.config.getConfig()["email"]["password"])

	def sendMail(self, template, subject, information, targets):
		template = self.env.get_template(template)
		mailbody = template.render(information=information)
		
		msg = MIMEMultipart('alternative')
		msg["Subject"] = subject
		msg['From'] = self.config.getConfig()["email"]["from"]
		msg['To'] = ", ".join(targets)

		part1 = MIMEText(mailbody,'plain')
		part2 = MIMEText(mailbody,'html')

		msg.attach(part1)
		msg.attach(part2)

		self.connect()
		self.server.sendmail(self.config.getConfig()["email"]["from"], targets, msg.as_string())
		self.server.quit()