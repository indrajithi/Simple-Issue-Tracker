# Simple Issue Tracker (SIT)

## Design:

System will have two models called User and Issue. With following information

### User:
- Email
- Username
- FirstName
- LastName
- Password
- AccessToken
- Issue
- Title
- Description
- AssignedTo (User relation)
- Createdby (User relation)
- Status (Open, Closed)

## Problem Statement:

Expose a RESTful API to make CRUD operation of Issue resource. 
Every endpoint need user authentication
Authentication should be stateless (access_token)
User who created the issue only should be able to edit or delete that issue

## Note:
    
- Whenever an Issue is created or assigned to different user(in case of update), an email should be triggered exactly after 12 mins to the particular user saying issue has been assigned to him/her.

- Every 24 hours an email should be triggered to every users with details of all the issues assigned to him/her. Here 24 hours should be configurable.(for e.g we may ask you to send emails for every 10 hours or even every 10 secs)

## Configuration

Edit these in `settings.py`

```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'me@gmail.com'  #change to your email
EMAIL_HOST_PASSWORD = 'password'  #change to your password
```

If you are using gmail as your email host, please make sure that you allow third party app to use smtp protocols. You will receive an email asking you to confirm the login activity.

## Implementation.
Python Version: 3.5.6

Django Version:  2.1

**Install requirements, crate user and migrate:**

- `$ pip install -r requirements.txt`

- `$ python manage.py createsuperuser`  
(while creating user please privide an email address)

- `$ python manage.py makemigrations && python manage.py migrate`

**Run serever**: 

- `$ python manage.py runserver`


### Access Token

You can fetch the access token by making `POST` calls to `http://127.0.0.1:8000/get-token/`

**Example:**

`$ curl -d "username=test&password=root123" -X POST http://127.0.0.1:8000/get-token/`

We can make our life easier by using Postman by providing `username` and `password` in  the body.

**sample output:** 

`{"token":"086d9d2966b40a4e369a17e56b748994cfad0ac7"}`


### Creating Issue

We can create an Issue by making `POST` call to  `http://127.0.0.1:8000/api/` with `description`, `title`, and `assigned_to` fields in the body. 

Please note that `assigned_to` field is the `id` of the user `<pk>`. 

**sample output:**

```
{
    "title": "Simple Issue",
    "description": "Just a simple issue",
    "assigned_to": 1,
    "created_by": "indra",
    "status": "O",
    "issue_id": "1d63b1e355e2"
}
```
*The creater of the issue can only edit the issue.*

*Once the Issue is created an email is sent to the `assigned_to` User.*

**sample output:**
```
Open Issue: #3fecaacd668e (subject)

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Open Issue: # Sample issue </title>
</head>
<body>
Hello ,

This email is regarding your open issue on.
<h2> Issue: </h2>
<pre>
    3fecaacd668e
<pre>
</body>
</html>
```


## Endpoints:

- `/get-token/`

   **Allow:** *POST* 

-  `/ `and `api/` 
    
    **Allow:** *GET, POST, HEAD, OPTIONS*
   
- `api/(?P<pk>[0-9]+`

  **Allow:** *GET, PUT, PATCH, DELETE, HEAD, OPTIONS*
   

## The Model:

The model consists `class Issue(models.Model):` which can have a status of `Opned/Closed.` By default when an Issue is created it is set to Open.

The database I used is `sqlite3`. After a successful `POST` call a new Issue entry is saved in the database and `email_trigger(720, seld.issue_id)` is called.   

## Task scheduling and email

For task scheduling I have used Celery and for email I have used gmail `smtp`.


*This code is developed using python v3.5.2. on 16.04.2-Ubuntu SMP x86_64 x86_64 GNU/Linux. 4.10.0-28-generic kernel*


