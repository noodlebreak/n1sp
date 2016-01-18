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

Install dependencies:
	
	pip install -r requirements.txt

Run main() in `initial_data.py` in Django shell:
	
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


