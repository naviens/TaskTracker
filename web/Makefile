initdb:
	python src/manage.py makemigrations  --settings=api.settings_local
	python src/manage.py migrate  --settings=api.settings_local

install:
	pip install --upgrade setuptools
	pip install --upgrade -r requirements.txt

test:
	python src/manage.py test webapp --settings=api.settings_test

run:
	python src/manage.py runserver 0.0.0.0:8000 --settings=api.settings_local
