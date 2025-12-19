# Этап 1: Сборка vcpkg и зависимостей
FROM alpine:3.19 AS vcpkg-builder

RUN apk add --no-cache \
    git \
    build-base \
    cmake \
    ninja \
    curl \
    zip \
    unzip \
    tar \
    pkgconfig \
    openssl-dev \
    perl \
    bash \
    linux-headers

RUN git clone https://github.com/microsoft/vcpkg.git /opt/vcpkg && \
    /opt/vcpkg/bootstrap-vcpkg.sh -disableMetrics

RUN cd /opt/vcpkg && \
    export VCPKG_FORCE_SYSTEM_BINARIES=1 && \
    ./vcpkg install \
        drogon \
        --triplet=x64-linux \
        --overlay-triplets=/opt/vcpkg/triplets/community \
        --clean-after-build

# Этап 2: Сборка приложения
FROM alpine:3.19 AS app-builder

WORKDIR /app

COPY --from=vcpkg-builder /opt/vcpkg /opt/vcpkg

RUN apk add --no-cache \
    build-base \
    cmake \
    ninja \
    openssl-dev

COPY src ./src
COPY CMakeLists.txt ./

RUN mkdir -p build  && \
    cmake \
        -S . \
        -B build \
        -DCMAKE_TOOLCHAIN_FILE=/opt/vcpkg/scripts/buildsystems/vcpkg.cmake \
        -GNinja && \
    cmake --build build --config Release


# Этап 3: Минимальный runtime образ
FROM alpine:3.19

RUN apk add --no-cache \
    libstdc++ \
    openssl

COPY --from=app-builder /app/build/temperature_api /usr/local/bin/

RUN addgroup -S appuser && adduser -S appuser -G appuser

USER appuser

ENV PORT=8081
ENV HOST=0.0.0.0

EXPOSE 8081

CMD ["temperature_api"]