[![Build Status](https://travis-ci.org/CodeFN/thecodefellowsnetwork.svg?branch=master)](https://travis-ci.org/CodeFN/thecodefellowsnetwork) [![Coverage Status](https://coveralls.io/repos/github/CodeFN/thecodefellowsnetwork/badge.svg?branch=master)](https://coveralls.io/github/CodeFN/thecodefellowsnetwork?branch=master)
# The Code Fellows Network
The perfect network for the code academy: http://52.35.131.204/

## Authors: 
[Marc Fieser](https://github.com/midfies), [Ben Shields](https://github.com/iamrobinhood12345), [Ben Petty](https://github.com/benpetty)

## Concept

The Code Fellows Network is a social media platform designed by and for use by students of [Code Fellows](https://www.codefellows.org/). It is a social media tool to assist students in their studies as they progress through Code Fellows bootcamp. The site is designed to be easily extendable and the hope is that future classes will build upon this original project.

## Requirements

python3.4 or newer
postgresql

## Detailed Build Instructions

This build is for Linux and OSX systems. Microsoft=unknown.
python3.4 or newer
postgresql

GIT:
Clone thecodefellowsnetwork into your system.

```bash
git clone https://github.com/CodeFN/thecodefellowsnetwork.git
```

VIRTUAL ENVIRONMENTS:
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

ENVIRONMENT VARIABLES:
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

REQUIREMENTS.PIP:
Install reqiurements.
```bash
pip install -r requirements.pip
```

CREATEDB:
```bash
createdb <DB_NAME>
```

To destroy database
```bash
dropdb <DB_NAME>
```

GITHUB SOCIAL AUTH:


clone
venv
envs
reactivate
pip install
createdb
github social auth
makemigrations
migrate
./manage.py runserver
tests

architecture overview
built with django
app name cfn
apps: profilecfn posts

directions

security, groups, assignments, direct messaging, javascript, code comparison, front end improvements




On Linux and OSX systems:

```bash
git clone https://github.com/CodeFN/thecodefellowsnetwork.git
python3 -m venv <env>
source <env>/bin/activate
```

envs

```bash
export DB_NAME=

export 

pip install requirements -r requirements.pip
```






