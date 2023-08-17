# public-library-wagtailCMS
This is an example public library website using wagtail CMS, originally created for the Penticton Public Library, in Penticton, British Columbia, Canada. You can view their website at https://pentictonlibrary.ca

Some features: 
1) Displaying single and re-occuring events
2) Displaying ranges and event categories
3) Dynamic opening hours
4) responsive and (mostly) accessible design
5) Search box integrated with a catalogue (in this instance, Aspen Discovery)
6) Pages with reordable elements such a richtext paragraphs, images, upcoming programs, hours, etc
7) Alert messages 
8) Simple editing of the header and footer of the site for content that rarely changes and needs to be consistent accross all pages
9) Edible home page
10) Person app for putting together an image based list of staff or library board members
11) Digital Resources app for adding new databases
12) Homepage contains feature boxes and upcoming library programs

Assumptions: 
Technical expertise including command line, preferably Linux. Understanding of Python and python virtual environments would be a huge plus. 

Prerequistites: 
1) Python 3 (HINT - Ubuntu style systems this would be: sudo apt install python3-venv python3-dev)
2) Python Virtual Environment (Again, in Ubuntu: python3 -m venv YOUR_PYTHON_ENVIRMENT)

These environments can be set up on any OS that supports up to date versions of python. 

To Install: 
1) Enable a python virtual environment: source YOUR_PYTHON_ENVIRONMENT/bin/activate
2) Download the repository
3) navigate to the repo in the command line (cd public-library-wagtailCMS)
4) pip install -r requirements.txt
5) python manage.py createsuperuser
6) python manage.py runserver

First Steps: 
1) Navigate to http://localhost:8000 on a web browser to check out the front end. 
2) Log in to admin with the createsuperuser credentials you created earlier by going to http://localhost:8000/admin
3) To other others on the same network you can use python manage.py runserver 0.0.0.0:8000

Further Considerations: 
1) This repo has been created to show how a public library website can be developed in WagtailCMS. It runs on a development server with SQLite and is not configured for production use.
2) Further progress on this repo including documentation could be considered if others are interested.  
