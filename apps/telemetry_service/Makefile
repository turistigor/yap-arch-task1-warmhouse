IMG_TAG=telemetry-service
APP_NAME=telemetry_service
VOLUME_DIR=/root/.news
VOLUME_NAME=news_log
CFG_DIR=~/.news/mnt/
SHELL_CMD=/bin/sh


docker-build:
	docker build -t $(IMG_TAG):latest .

docker-rm:
	docker rm $(APP_NAME)

docker-rmi:
	docker rmi $(IMG_TAG)

docker-clear:
	docker system prune

docker-run:
	docker run \
		--name $(APP_NAME) \
		$(IMG_TAG):latest

