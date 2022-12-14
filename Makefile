.PHONY: init start restart backendshell frontendshell migrate test coverage

init:
	@if [  ! -f backend/.env ]; then\
		echo;\
		echo "@@@ ERROR: missing secrets file in ./backend/.env @@@";\
		echo "Please ensure that the environment file is correctly placed";\
		echo "in that location before continuing. If you do not have a copy";\
		echo "of that file, please reach out.";\
		echo;\
		exit 1;\
	fi
	docker compose up -d --build
	$(MAKE) migrate

start:
	docker compose up -d --build

restart:
	docker compose up -d --build

migrate:
	ls -lah backend
	docker compose exec backend python manage.py makemigrations
	docker compose exec backend python manage.py migrate --run-syncdb

backendshell:
	docker compose exec backend /bin/bash

frontendshell:
	docker compose exec frontend /bin/bash

test:
	docker compose exec backend python manage.py test

coverage:
	docker compose exec backend coverage run --source='.' manage.py test
	docker compose exec backend coverage html
	open backend/htmlcov/index.html