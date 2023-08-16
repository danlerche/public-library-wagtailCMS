# public-library-wagtailCMS
This is an example public library website using wagtail CMS, originally created for the Penticton Public Library, in Penticton, British Columbia, Canada. 
The project allows for reocurring library programs, dynamic opening hours and holiday, website and catalogue search. Features on the home page, and much more. WagtailCMS is based on Django, a python framework. 

Prerequistites: 
1) Python 3
2) Python Virtual Environment

To Install: 
1) Enable a python virtual environment (source YOUR_PYTHON_ENVIRONMENT/bin/activate)
2) Download the repository
3) cd public-library-wagtailCMS
4) pip install -r requirements.txt
5) python manage.py createsuperuser
6) python manage.py runserver

First Steps: 
1) Navigate to http://localhost:8000 on a web browser to check out the front end. 
2) Log in to admin with the createsuperuser credentials you created earlier by going to http://localhost:8000/admin
