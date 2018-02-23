#!/usr/bin/env python3
#General imports
import json, os

#Config import
from lib.Config import Config

#Flask Import
from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for, send_from_directory

#Route imports
from routes.page_routes import page_routes, navigation_bar
from routes.internal_routes import internal_routes

#Fix logging when using Nginx
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.register_blueprint(page_routes)
app.register_blueprint(internal_routes)
app.wsgi_app = ProxyFix(app.wsgi_app)

#Favicon
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(
			os.path.join(app.root_path, 'static'),
			'facicon.ico',
			mimetype='image/vnd.microsoft.icon'
		)

#Error handling
@app.errorhandler(400)
def page_not_found(e):
	#Add code here. Eg add session info to logging
	return render_template('error_pages/400.html', navigation_bar=navigation_bar),400

@app.errorhandler(404)
def page_not_found(e):
	#Add code here. Eg add session info to logging
	return render_template('error_pages/404.html', navigation_bar=navigation_bar),404

@app.errorhandler(500)
def page_not_found(e):
	#Add code here. Eg add session info to logging
	return render_template('error_pages/500.html', navigation_bar=navigation_bar),500

if __name__ == '__main__':
	config = Config()

	app.secret_key = config.getConfig()["server"]["appKey"]

	options = {
		"host": config.getConfig()["server"]["ip"],
		"port": config.getConfig()["server"]["port"],
		"debug": config.getConfig()["server"]["debug"]
	}

	if config.getConfig()["server"]["ssl"]:
		options.update({
				"ssl_context": (
					config.getConfig()["server"]["ssl_cert"],
					config.getConfig()["server"]["ssl_key"]
					)
			})

	app.run(**options)