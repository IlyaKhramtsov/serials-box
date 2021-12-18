install:
	@poetry install

shell:
	@poetry run python manage.py shell

migrate:
	@poetry run python manage.py migrate

start: migrate
	@poetry run python manage.py runserver

test:
	@poetry run coverage run --source '.' manage.py test

test-coverage-report: test
	@poetry run coverage report

test-coverage-report-html: test
	@poetry run coverage xml

.PHONY: install shell start test