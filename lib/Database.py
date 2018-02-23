from lib.Config import Config
from lib.Mail import Mail
import MySQLdb
from warnings import filterwarnings

class Database:
	conn = None
	filterwarnings('ignore', category = MySQLdb.Warning)

	def connect(self):
		config = Config()

		self.conn = MySQLdb.connect(
			host=config.getConfig()['mysql']['host'],
			port=config.getConfig()['mysql']['port'],
			user=config.getConfig()['mysql']['user'],
			passwd=config.getConfig()['mysql']['pass'],
			db=config.getConfig()['mysql']['db']
			)
		self.conn.autocommit(True)
		self.conn.set_character_set('utf8')

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		except:
			self.connect()
			cursor = self.conn.cursor()
			try:
				cursor.execute(sql,args)
			except MySQLdb.Error as e:
				print(e)
				"""
				#The next lines are to send an email with errors regarding MySQL queries
				if args and e:
					information = "Query: "+sql.replace("\\t"," ").replace("\\n","<br>")+"<br>Arguments:"+(''.join(str(args)))+"<br>Error: "+str(e)
				else:
					information = "Query: "+sql.replace("\\t"," ").replace("\\n","<br>")+"<br>Error: "+str(e.args[0])
				
				#Mail().sendMail('errors.html', "MySQL Errors", information,[])
				"""
		return cursor

	def queryMany(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.executemany(sql,args)
		except:
			self.connect()
			cursor = self.conn.cursor()
			cursor.executemany(sql,args)
		return cursor