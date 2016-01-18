# n1sp
========

Simple django project that demonstrates:
* Django ORM
* notifications
* row level permissions (django-rulez)
* background tasks (celery)
* templating (custom tags, rendering, etc)
etc

Running
========

Install Python dependencies:
	
	pip install -r requirements.txt

System level dependencies:
	
* Install rabbitmq-server (for celery):
	
	sudo apt-get install rabbitmq-server

Run main() in `initial_data.py` in Django shell,
to crudely install some initial data (users, groups, admins..)
	
	>>>from initial_data import main
	>>>main()

Run server:

	$>> python manage.py runserver

Run celery:
	
	$>> celery -A n1sp worker -lDEBUG

Run omnibusd for notifications

	$>> python manage.py omnibusd

Visit page:

	http://localhost:8000/


