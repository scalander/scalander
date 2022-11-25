.PHONY: init start backendshell frontendshell migrate test

init:
	touch backend/db.sqlite3
	docker compose up -d
	$(MAKE) migrate

start:
	docker compose up -d

migrate:
	docker compose exec backend python manage.py makemigrations
	docker compose exec backend python manage.py migrate

backendshell:
	docker compose exec backend /bin/bash

frontendshell:
	docker compose exec frontend /bin/bash

test:
	docker compose exec backend python manage.py test

