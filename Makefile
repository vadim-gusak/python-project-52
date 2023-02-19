lint:
	poetry run flake8 task_manager

test-start:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	poetry update && poetry run python manage.py makemigrations && poetry run python manage.py migrate && poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

tests:
	poetry run python manage.py test --verbosity 2

test-cov:
	poetry run coverage run --source='.' manage.py test task_manager && poetry run coverage xml