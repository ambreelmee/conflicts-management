install:
	docker-compose run --rm server pip install -r requirements-dev.txt --user --upgrade

start:
	docker-compose up server

daemon:
	docker-compose up -d server

tests:
	docker-compose run --rm testserver pip install -r requirements-dev.txt --user --upgrade

lint:
	docker-compose run --rm server bash -c "python -m flake8 ./src ./test"

update_bce:
	docker-compose run --rm server python src/manage.py script_update_from_bce

update_sirene:
	docker-compose run --rm server python src/manage.py script_update_from_sirene

db/connect:
	docker exec -it conflictsmanagement_db_1 psql -Upostgres

db/downgrade:
	docker-compose run --rm server python src/manage.py db downgrade

db/upgrade:
	docker-compose run --rm server python src/manage.py db upgrade

db/migrate:
	docker-compose run --rm server python src/manage.py db migrate

db/seed:
	docker-compose run --rm server python src/manage.py seed
