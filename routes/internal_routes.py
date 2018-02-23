from flask import Blueprint, render_template, abort, session, redirect, url_for, request
from functools import wraps
from lib.Users import Users
from lib.Groups import Groups
from lib.Database import Database
import json

def requires_auth(f):
	@wraps(f)
	def decorated_auth(*args, **kwargs):
		if 'username' not in session:
			return redirect(url_for('page_routes.login'))
		return f(*args, **kwargs)
	return decorated_auth

def requires_admin(f):
	@wraps(f)
	def decorated_admin(*args, **kwargs):
		#Check if admin
		if not users.isAdmin():
			return json.dumps({"error": "Unauthorized"}),401
		return f(*args, **kwargs)
	return decorated_admin

internal_routes = Blueprint('internal_routes', __name__, template_folder='templates')
users = Users()
groups = Groups()
db = Database()

#Internal routes

#Users
@internal_routes.route('/internal/users/getAllUsers')
@requires_auth
@requires_admin
def getAllUsers():
	return json.dumps(users.getAllUsers())

@internal_routes.route('/internal/users/getUserInfo')
@requires_auth
def getUserInfo():
	return json.dumps(users.getUserInfo())

@internal_routes.route('/internal/users/addUser', methods=["POST"])
@requires_auth
@requires_admin
def addUser():
	res = users.addUser(request.form)
	return redirect(url_for('page_routes.admin'))

@internal_routes.route('/internal/users/getUserInfoAdmin/<user>')
@requires_auth
@requires_admin
def getUserInfoAdmin(user):
	return json.dumps(users.getUserInfo(user))

@internal_routes.route('/internal/users/editUserAdmin', methods=["POST"])
@requires_auth
@requires_admin
def editUserInfoAdmin():
	res = users.editUser(request.form)
	return redirect(url_for('page_routes.admin'))

@internal_routes.route('/internal/users/saveUserPassword', methods=["POST"])
@requires_auth
def saveUserPassword():
	res = users.saveUserPassword(request.form["password"])
	redirectPage = list(filter(None, request.form["page"].split("/")))
	if len(redirectPage) == 0:
		redirectPage = 'index'
	else:
		redirectPage = redirectPage[1]
	return redirect(url_for('page_routes.'+redirectPage))
	
#Groups
@internal_routes.route('/internal/groups/getAllGroups')
@requires_auth
@requires_admin
def getGroups():
	return json.dumps(groups.getGroups())

@internal_routes.route('/internal/groups/getGroupDetails/<group>')
@requires_auth
@requires_admin
def getGroupDetails(group):
	return json.dumps(groups.getGroupDetails(group))

@internal_routes.route('/internal/groups/addGroup', methods=["POST"])
@requires_auth
@requires_admin
def addGroup():
	res = groups.addGroup(request.form)
	return redirect(url_for('page_routes.admin'))

@internal_routes.route('/internal/groups/editGroup', methods=["POST"])
@requires_auth
@requires_admin
def editGroup():
	res = groups.editGroup(request.form)
	return redirect(url_for('page_routes.admin'))

@internal_routes.route('/internal/groups/delGroup/<group>')
@requires_auth
@requires_admin
def delGroup(group):
	res = groups.delGroup(group)
	return redirect(url_for('page_routes.admin'))