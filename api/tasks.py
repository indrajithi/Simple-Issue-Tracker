from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from api import models
from django.core.mail import send_mail
from celery import task
from django.core.validators import validate_email
import threading
import time


@task()
def shedule_emails():
	"""
	Fetches all the issues from the  and finds the open issues and email the person to which the 
	issue is assigned.
	"""

	all_issues = models.Issue.objects.all()

	for issue in all_issues: #this can be parellized for better performance
		issue_data = str(issue).split('-')
		if issue_data[-2] == 'O':      #for all open issues
			_user = User.objects.get(username=issue_data[-1])
			email_now(_user, issue_data)
			


def email_now(_user, issue_data ):
    """
    Verify and send an email
    """
    try:
        validate_email(email_address)
        send_email( 
            'Aircto Open Issue: #{}'.format(issue_data[0]),
            create_email_data(_user.first_name, issue_data),
            'issue@aircto.com',
            _user.email,
            fail_silently=False,
                )
    except:
        print('Unable to send email for issue {},'.format(issue_data[0]))
        print('Please configure redis and smtp in settings.py')

def create_email_data(first_name, content=None):
    """
    Email template
    """
    content = '''
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Aircto Open Issue: #{}</title>
        </head>
        <body>
        Hello {},

        This email is regarding your open issue on Aircto.
        <h2> Issue: </h2>
        <pre>
        	{}
        <pre>
        </body>
        </html>'''.format(content[1], first_name, content[0], content[2])
    return content		
    

def email_trigger(seconds, issue_id):
    issue_data = str(models.Issue.objects.get(issue_id=issue_id)).split('-')
    if issue_data[-1] != '': # issue assigned to someone
        _user = User.objects.get(username=str(issue_data[-1]).lstrip().rstrip())
        print("An email is sheduled to send after 12 minutes.")
        t = threading.Timer(seconds, email_now, [_user, issue_data] )
        t.start()
        


