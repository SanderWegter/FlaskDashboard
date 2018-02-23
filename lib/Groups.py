from lib.Database import Database
from flask import session

class Groups:
	def __init__(self):
		self.db = Database()

	def getGroups(self):
		groupList = []
		cur = self.db.query("SELECT name, (SELECT COUNT(*) FROM groupmembers WHERE groups.id = groupmembers.gid), id FROM groups");
		for row in cur.fetchall():
			groupList.append({
				"name": row[0],
				"members": row[1],
				"id": row[2],
				})
		return groupList

	def addGroup(self, form):
		groupname = form["groupname"]
		cur = self.db.query("SELECT COUNT(*) FROM groups WHERE name = %s",[groupname])
		if cur.fetchone()[0] > 0:
			return "Group exists"
		cur = self.db.query("INSERT INTO groups (`name`) VALUES(%s)",[groupname])
		session["notificationtype"] = "success"
		session["notification"] = "Group "+groupname+" added"
		return None

	def delGroup(self, group):
		if group != 2 and group != 1:
			cur = self.db.query("SELECT name FROM groups WHERE id = %s",[group])
			grname = cur.fetchone()[0]
			cur = self.db.query("UPDATE groupmembers SET gid = 2 WHERE gid = %s",[group])
			cur = self.db.query("DELETE FROM groups WHERE id = %s",[group])

		session["notificationtype"] = "success"
		session["notification"] = "Group deleted"
		return None