.PHONY: all build run docker-build docker-run clean help

# Переменные
APP_NAME = temperature_api
DOCKER_IMAGE = temperature-api
PORT = 8081
HOST = 0.0.0.0

# Основные цели
all: build

# Сборка приложения
build:
	@echo "Building $(APP_NAME)..."
	@mkdir -p build
	@cd build && cmake .. -DCMAKE_TOOLCHAIN_FILE=/home/igor/Programs/vcpkg/scripts/buildsystems/vcpkg.cmake && make

# Запуск приложения (предварительно установить Drogon)
run: build
	@echo "Running $(APP_NAME)..."
	@PORT=$(PORT) HOST=$(HOST) ./build/$(APP_NAME)

# Очистка
clean:
	@echo "Cleaning..."
	@rm -rf build

# Сборка Docker образа
docker-build:
	@echo "Building Docker image..."
	@docker build -t $(DOCKER_IMAGE):latest .

# Запуск в Docker
docker-run:
	@echo "Running in Docker..."
	@docker run -p $(PORT):8081 \
		-e PORT=8081 \
		-e HOST=0.0.0.0 \
		--name $(APP_NAME) \
		$(DOCKER_IMAGE):latest

# Удалить образ
docker-rmi:
	@echo "Docker image deletion..."
	@docker rmi $(DOCKER_IMAGE)

# Удалить контейнер
docker-rm:
	@echo "Docker container deletion..."
	@docker rm $(APP_NAME)

# Справка
help:
	@echo "Available targets:"
	@echo "  build          - Build application locally"
	@echo "  run            - Run application locally"
	@echo "  clean          - Clean build artifacts"
	@echo "------------------------------------------"
	@echo "  docker-build   - Build Docker image"
	@echo "  docker-run     - Run Docker container (default port 8080)"
	@echo "  docker rmi     - Docker image deletion"
	@echo "  docker-rm      - Docker container deletion"
	@echo "------------------------------------------"
	@echo "  help           - Show this help"
