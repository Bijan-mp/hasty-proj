build:
	docker compose --build 

run:
	docker compose up

build-run:
	docker compose up --build

stop:
	docker compose down

stop-and-remove-volumes:
	docker compose down -v

build-and-test:
	docker compose up -d --build
	docker compose exec hastyweb pytest
