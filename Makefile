test:
		docker-compose run --rm web poetry run python manage.py test --settings=base.settings_test
