TaskTracker

Task Tracker Django application. Keeps track of hours spent on each task for a week

# Prerequisites:
1. Docker
2. Docker-compose

# Running (Docker):
```bash
$ sudo docker-compose build
$ sudo docker-compose up 
```

# Running Unittest:
```bash
$ python src/manage.py test task_tracker --settings=api.settings_test
```