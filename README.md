[![Build Status](https://travis-ci.org/CodeFN/thecodefellowsnetwork.svg?branch=master)](https://travis-ci.org/CodeFN/thecodefellowsnetwork) [![Coverage Status](https://coveralls.io/repos/github/CodeFN/thecodefellowsnetwork/badge.svg?branch=master)](https://coveralls.io/github/CodeFN/thecodefellowsnetwork?branch=master)
# The Code Fellows Network
The perfect network for the code academy: codefellows.network

## Authors: 
[Marc Fieser](https://github.com/midfies), [Ben Shields](https://github.com/iamrobinhood12345), [Ben Petty](https://github.com/benpetty)

## Concept

The Code Fellows Network is a social media platform designed by and for use by students of [Code Fellows](https://www.codefellows.org/). It is a social media tool to assist students in their studies as they progress through Code Fellows bootcamp. The site is designed to be easily extendable and the hope is that future classes will build upon this original project.

## Contents

  1. Requirements
  2. Detailed Build Instructions
  3. Testing
  4. Future

## 1. Requirements

python3.4 or newer

postgresql

## 2. Detailed Build Instructions

This build is for Linux and OSX systems. Microsoft=unknown.
python3.4 or newer
postgresql

###Git:
Clone thecodefellowsnetwork into your system.

```bash
git clone https://github.com/CodeFN/thecodefellowsnetwork.git
```

###Virtual Environments:
We suggest developing in a virtual environment.

```bash
python3 -m venv env
```

To activate
```bash
source env/bin/activate
```
To deactivate
```bash
deactivate
```
You may have to deactivate and reactivate after making adjustments to environment variables.

###Environment Variables:
The following environment variables are required.
```bash
DB_NAME
DB_USERNAME
DB_PASSWORD
DB_HOST
DEBUG
DB_PORT
ALLOWED_HOSTS
SECRET_KEY
GITHUB_APP_ID
GITHUB_API_SECRET
```
Export or add to env/bin/activate script.
Some of these must match values from your database instance or Github Social Auth.

###Requirements.pip:
Install reqiurements.
```bash
pip install -r requirements.pip
```

###Createdb:
```bash
createdb <DB_NAME>
```

To destroy database
```bash
dropdb <DB_NAME>
```

###Github Social Auth:

Set GITHUB_APP_ID and GITHUB_API_SECRET to the correct variables after signing up for social authentication through your github account. You must have a github account.

###Migrations:

Migrate database models for successful model rendering in your database instance.
```bash
./manage.py makemigrations
./manage.py migrate
```

###Runserver:
```bash
./manage.py runserver
```

## 3. Architecture

cfn: main django app name

cfn/cfn: main django app

cfn/profile_cfn: profile/fellow app

cfn/posts: posts/comments/likes app


## 3. Testing

Files

cfn/cfn/tests.py
cfn/profile_cfn/tests.py
cfn/posts/tests.py

To run
```bash
./manage.py test
```

## 4. Future

Not implemented... yet!

groups, assignments, direct messaging, code comparison, code analysis, design, 
