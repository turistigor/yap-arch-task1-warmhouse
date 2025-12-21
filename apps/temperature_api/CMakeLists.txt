cmake_minimum_required(VERSION 3.16)
project(temperature_api VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Поиск пакета Drogon
find_package(Drogon REQUIRED)

# Исполняемый файл
set (SOURCES 
    src/main.cpp /
    src/handlers/root.cpp /
    src/handlers/healthcheck.cpp /
    src/handlers/sensors.cpp /
    src/utils/envs.cpp /
    src/utils/datetime.cpp /
    src/utils/randoms.cpp
)
add_executable(${PROJECT_NAME} ${SOURCES})

# Подключение зависимостей
target_link_libraries(${PROJECT_NAME} PRIVATE Drogon::Drogon)

# Установка для Docker
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
