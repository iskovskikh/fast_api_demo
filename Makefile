DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose/app.yml
STORAGES_FILE = docker-compose/storages.yml
APP_CONTAINER = app-main

# ------------------------------------------

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

# ------------------------------------------

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

# ------------------------------------------

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

# ------------------------------------------