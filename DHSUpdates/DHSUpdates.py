# -*- coding: utf-8 -*-
import os
import cgi
import jinja2
import webapp2
from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

feedback_key = ndb.Key('Feedback', 'default_feedback')
upload_key = ndb.Key('Upload','default_upload')
	
class Event(ndb.Model):
	author = ndb.StringProperty(indexed=False)
	inputName = ndb.TextProperty()
	inputStart = ndb.DateTimeProperty()
	inputEnd = ndb.DateTimeProperty()
	inputVenue = ndb.TextProperty()
	inputDescription = ndb.TextProperty()

class Comment(ndb.Model):
	author = ndb.StringProperty(indexed=False)
	content = ndb.TextProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'LOGOUT'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'LOGIN'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class AboutAppPage(webapp2.RequestHandler):
	
    def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'
			
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('aboutapp.html')
		self.response.write(template.render(template_values))

class HistoryPage(webapp2.RequestHandler):
	
    def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'
			
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('history.html')
		self.response.write(template.render(template_values))

class HowToUsePage(webapp2.RequestHandler):
	
    def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'
			
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('how_to_use.html')
		self.response.write(template.render(template_values))

class EventsPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'
			
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('events.html')
		self.response.write(template.render(template_values))
		
		events = ndb.gql('SELECT * '
			'FROM Event '
			'WHERE ANCESTOR IS :1 '
			'ORDER BY inputStart ASC LIMIT 10',
			upload_key)
		
		for event in events:
			self.response.out.write('<div class="panel panel-info" id="post" class="col-sm-6 col-md-4"><div class="panel-heading">%s<h3 class="panel-title"></h3></div>' % cgi.escape(event.inputName))
			self.response.out.write('<div class="panel-body"><p>Starting Time: %s</p>' % event.inputStart.strftime("%d-%m-%Y %H:%M"))
			self.response.out.write('<p>Ending Time: %s</p>' % event.inputEnd.strftime("%d-%m-%Y %H:%M"))
			self.response.out.write('<p>Venue: %s</p>' % cgi.escape(event.inputVenue))
			self.response.out.write('<p>Description: %s</p><br>' % cgi.escape(event.inputDescription))
			self.response.out.write('<p>Uploaded by <strong>%s</strong></p></div></div>' % event.author)

		self.response.out.write("""
				</div>
				</div>
				<br>
				<footer id="main-footer">
					<p class="copyright">© 2016 linda♥</p>
				</footer>
				</body>
				</html>""")

class UploadPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'
			
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('upload.html')
		self.response.write(template.render(template_values))
		
		if user:
			self.response.out.write("""
					<div class="container">
					<div class="row">
						<section class="col-xs-12">
							<form action="/postUpload" method="post">
								<div class="form-group">
									<label>Event Name</label>
									<input class="form-control" type="text" name="inputName" placeholder="Event Name" required>
								</div>
								
								<div class="form-group">
									<label>Starting Time</label>
									<input class="form-control" type="datetime-local" name="inputStart"
										placeholder="Starting Time" required>
								</div>
								
								<div class="form-group">
									<label>Ending Time</label>
									<input class="form-control" type="datetime-local" name="inputEnd"
										placeholder="Ending Time" required>
								</div>
								
								<div class="form-group">
									<label>Venue</label>
									<input class="form-control" type="text" name="inputVenue" placeholder="Venue" required>
								</div>

								<div class="form-group">
									<label>Description</label>
									<textarea class="form-control" name="inputDescription" placeholder="Description" required></textarea>
								</div>
								
								<a>
									<input class="btn btn-default" type="submit" value="Upload">
								</a>
							</form>
						</section>
					</div>
					</div>
					<br>
					<footer id="main-footer">
						<p class="copyright">© 2016 linda♥</p>
					</footer>
				</body>
				</html>""")
		
		else:
			self.response.out.write("""
					<br>
					<div class="content container"><p>Please login before uploading your event.</p></div>
					<br>
					<footer id="main-footer">
						<p class="copyright">© 2016 linda♥</p>
					</footer>
					</body>
					</html>""")

class PostUpload(webapp2.RequestHandler):
	def post(self):
		event = Event(parent = upload_key)
		event.author = users.get_current_user().email()
		event.inputName = self.request.get("inputName")
		event.inputStart = datetime.strptime(self.request.get("inputStart"), "%d-%m-%YT%H:%M")
		event.inputEnd = datetime.strptime(self.request.get("inputEnd"), "%d-%m-%YT%H:%M")
		event.inputVenue = self.request.get("inputVenue")
		event.inputDescription = self.request.get("inputDescription")
		event.put()
		self.redirect('/events' + self.request.query_string)

class FeedbackPage(webapp2.RequestHandler):
	
    def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('feedback.html')
		self.response.write(template.render(template_values))
		
		comments = ndb.gql('SELECT * '
                            'FROM Comment '
                            'WHERE ANCESTOR IS :1 '
                            'ORDER BY date DESC LIMIT 10',
                            feedback_key)
		
		for comment in comments:
			if comment.author:
			    self.response.out.write('<p>%s:</p>' % comment.author)
			else:
				self.response.out.write('<p>Anonymous:</p>')
			self.response.out.write('<blockquote>%s</blockquote><hr>' % cgi.escape(comment.content))
			
		self.response.out.write("""
						<form action="/postFeedback" method="post">
							<div class="form">
								<textarea class="form-control" name="content" placeholder="What can I improve on?"></textarea>
							</div>
							<br>
							<input class="btn btn-default" type="submit" value="Submit">
						</form>
					</div>
				</div>
				<br>
				<footer id="main-footer">
					<p class="copyright">© 2016 linda♥</p>
				</footer>
				</body>
			</html>""")

class PostFeedback(webapp2.RequestHandler):
	def post(self):
		comment = Comment(parent = feedback_key)
		if users.get_current_user():
			comment.author = users.get_current_user().email()
		comment.content = self.request.get("content")
		comment.put()
		self.redirect('/feedback')

app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/history', HistoryPage),
	('/aboutapp', AboutAppPage),
	('/how_to_use',HowToUsePage),
	('/events',EventsPage),
	('/upload',UploadPage),
	('/feedback',FeedbackPage),
	('/postUpload',PostUpload),
	('/postFeedback',PostFeedback)
], debug=True)
