from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from .tasks import email_trigger

def generate_ticket_id():
    return str(uuid.uuid4()).split("-")[-1] #generate unique ticket id

class Issue(models.Model):
    STATUS = (
            ('O','Open'),
            ('C', 'Closed'),
            )
    issue_id = models.CharField(max_length=225)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, null=True, related_name='assignee', on_delete=models.CASCADE)
    created_by = models.ForeignKey('auth.User', related_name='creator', on_delete=models.CASCADE) 
    status = models.CharField(max_length=1, choices=STATUS, default='O', blank=True) 
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.issue_id, self.title, self.description ,

         self.status , self.assigned_to)

    def save(self, *args, **kwargs):
        if len(self.issue_id.strip(" "))==0:
            self.issue_id = generate_ticket_id()

        super(Issue, self).save(*args, **kwargs) # Call the real   save() method
        email_trigger(720, self.issue_id) #720 seconds (12 min)


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    

class IssueUsers(User):
    def __str__(self):
        return "{} - {} - {} - {}".format(self.username, 
            self.firstname, self.lastname, self.email)