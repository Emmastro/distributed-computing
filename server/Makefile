SHELL := /bin/bash
include .env

build-docker:
	docker build -t ${SERVICE_NAME} .

run-docker:
	docker run -p ${PORT}:${PORT} ${SERVICE_NAME}
