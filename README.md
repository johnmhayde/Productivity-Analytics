# Productivity Analytics

## Project Overview
The goal of this project is to analyze your email usage over a period of time (currently set to 24 hours) and relay that informaiton to you. This information will be available to the users in text and graphical form.

## Usage
### Django Application
Start the Django application by navigating into the productivity_analysis directory
and running the command `python manage.py runserver`
### Email Test
Test sample program by nagivating to email_test directory, entering your
email information info the config.ini file, and running the program with
the command `python get_email.py`
## Requirements
Must have the following installed:  
`Python3`  
`Django`  
`django-crispy-forms`
### Personal Use
Note: this project currently requires editing the conf.ini file to add your personal
email information. The project is not ready for usage other than on a personal machine.
2FA will need to be implemented with Gmail before the project can be safely hosted
on a public access point. 
