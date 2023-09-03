## Functions
# Navigation: Project features by URLs:<br>
127.0.0.1:8000/news/ - list of all posts<br>
127.0.0.1:8000/news/<id>/ - detail data about post with id=<id><br>
127.0.0.1:8000/news/create/ - create new New**<br>
127.0.0.1:8000/news/<id>/edit/ - edit current New**<br>
127.0.0.1:8000/news/<id>/delete/ - delete current New**<br>
127.0.0.1:8000/articles/create/ - create new Article**<br>
127.0.0.1:8000/articles/<id>/edit/ - edit current Article**<br>
127.0.0.1:8000/articles/<id>/delete/ - delete current Article**<br>
127.0.0.1:8000/news/search/ - search post by filter<br>
127.0.0.1:8000/news/search/subscriptions/ - manage subscriptions of current user*<br>

127.0.0.1:8000/news/admin/ - admin control panel***<br>
127.0.0.1:8000/news/accounts/login/ - login to site by user account (if logined user will be redirected to /news/)<br>
127.0.0.1:8000/news/accounts/logout/ - logout from user account on site*<br>
127.0.0.1:8000/news/accounts/signup/ - signup new user account<br>

\* - these actions available for signed users<br>
\*\* - these actions available for signed authors<br> 
\*\*\* - these actions available for signed admins<br>

# Celery testing
In Windows Celery Worker can works unstable<br>
Install eventlet for troubleshooting<br>

Celery worker starts with command:<br>
celery -A NewsPortal worker -l INFO -P eventlet<br>

Celery scheduler starts with command:<br>
celery -A NewsPortal beat -l INFO<br>

# database commands
Use "python -Xutf8 manage.py dumpdata --format=xml -o mydata.xml" for dumpdata

# logging test
Use for "python manage.py test_logger" for test logging system