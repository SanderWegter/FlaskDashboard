from lib.Database import Database
from lib.Mail import Mail
from flask import session, request
import bcrypt

class Users:
	def __init__(self):
		self.db = Database()
		self.mail = Mail()
		self.rounds = 10

	def loginUser(self, form):
		username = form['username']
		cur = self.db.query("SELECT COUNT(1) FROM users WHERE user = %s", [username])

		if not cur.fetchone()[0]:
			session["notificationtype"] = "error"
			session["notification"] = "Incorrect username or password"
			return "Error: Incorrect username or password"

		password = form['password']
		cur = self.db.query("SELECT pass,firstname,lastname, G.name FROM users LEFT JOIN groupmembers M ON M.uid = id LEFT JOIN groups G ON G.id = M.gid WHERE user = %s", [username])

		for row in cur.fetchall():
			pwbytes = password.encode('utf-8')
			saltbytes = row[0].encode('utf-8')
			if bcrypt.hashpw(pwbytes, saltbytes) == saltbytes:
				session['username'] = form['username']
				session['flname'] = row[1] + " " + row[2]
				session['group'] = row[3]
				session["notificationtype"] = "success"
				session["notification"] = "Logged in"
				return None

		session["notificationtype"] = "error"
		session["notification"] = "Incorrect username or password"
		return "Error: Incorrect username or password"

	def logoutUser(self):
		session.pop('username', None)
		session.pop('group', None)
		session.pop('flname', None)
		return

	def getAllUsers(self):
		userlist = []
		cur = self.db.query("SELECT user, firstname, lastname, email, G.name, lastseen FROM users LEFT JOIN groupmembers M ON M.uid = users.id LEFT JOIN groups G ON G.id = M.gid")
		for row in cur.fetchall():
			userlist.append({
				"username": row[0],
				"name": row[1]+" "+row[2],
				"email": row[3],
				"group": row[4],
				"lastseen": str(row[5])
				})
		return userlist

	def getUserInfo(self, user=None):
		username = session["username"]
		if user:
			username = user

		cur = self.db.query("SELECT firstname, lastname, email, G.name FROM users LEFT JOIN groupmembers M on M.uid = users.id LEFT JOIN groups G on G.id = M.gid WHERE users.user = %s",[username])
		userInfo = cur.fetchone()
		if len(userInfo) == 0:
			return {"error": "Nothing found"}
		firstName, lastName, email, groupName = userInfo
		
		ret = {
			"username": username,
			"firstname": firstName,
			"lastname": lastName,
			"email": email,
			"group": groupName
		}
		return ret

	def saveUserPassword(self, password):
		password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(self.rounds))
		cur = self.db.query("UPDATE users SET pass = %s WHERE user = %s",[password,session["username"]])
		session["notificationtype"] = "success"
		session["notification"] = "Password saved"
		return None

	def updateLastseen(self):
		cur = self.db.query("UPDATE users SET lastseen = NOW(), lastip = %s WHERE user = %s",[request.remote_addr,session["username"]])
		return None

	def isAdmin(self):
		cur = self.db.query("SELECT COUNT(M.uid) FROM users LEFT JOIN groupmembers M ON M.uid = users.id WHERE users.user = %s AND M.gid = 1",[session["username"]])
		return cur.fetchone()[0] > 0

	def addUser(self, form):
		username = form["addUsername"]
		password = form["addPassword"]
		firstname = form["addFirstname"]
		lastname = form["addLastname"]
		email = form["addEmail"]

		cur = self.db.query("SELECT COUNT(*) FROM users WHERE user = %s",[username])
		if cur.fetchone()[0] > 0:
			return "User exists"

		pwbytes = password.encode('utf-8')
		password = bcrypt.hashpw(pwbytes, bcrypt.gensalt(self.rounds))

		cur = self.db.query("""
			INSERT INTO users (
			`user`,
			`firstname`,
			`lastname`,
			`email`,
			`pass`,
			`created`
			)
			VALUES (%s,%s,%s,%s,%s, NOW())""",
			[
			username,
			firstname,
			lastname,
			email,
			password
			])
		cur = self.db.query("SELECT id FROM users WHERE user = %s",[username])
		userID = cur.fetchone()[0]
		cur = self.db.query("INSERT INTO groupmembers VALUES (%s,2)",[userID])
		session["notificationtype"] = "success"
		session["notification"] = "User "+username+" added"
		return None

	def editUser(self, form):
		username = form["username"]
		password = form["password"]
		firstname = form["firstname"]
		lastname = form["lastname"]
		email = form["email"]
		group = form["group"]

		if len(password) < 3:
			cur = self.db.query("SELECT pass FROM users WHERE user = %s",[username])
			password = cur.fetchone()[0]
		else:
			pwbytes = password.encode('utf-8')
			password =  bcrypt.hashpw(pwbytes, bcrypt.gensalt(self.rounds))

		cur = self.db.query("""
			UPDATE users SET user=%s, pass=%s, firstname=%s, lastname=%s, email=%s
			WHERE user = %s
			""",
			[
			username,
			password,
			firstname,
			lastname,
			email,
			username
			])

		cur = self.db.query("SELECT users.id, G.id FROM users LEFT JOIN groupmembers M ON M.uid = users.id LEFT JOIN groups G ON G.id = M.gid WHERE users.user = %s",[username])
		uid,ogid = cur.fetchone()
		cur = self.db.query("SELECT id FROM groups WHERE name = %s",[group])
		gid = cur.fetchone()[0]

		cur = self.db.query("UPDATE groupmembers SET gid = %s WHERE uid = %s AND gid = %s",[gid,uid,ogid])

		session["notificationtype"] = "success"
		session["notification"] = "User "+username+" changed"
		return None