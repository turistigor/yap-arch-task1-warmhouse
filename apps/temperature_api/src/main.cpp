#include <string>

#include <drogon/drogon.h>

#include "handlers/handlers.h"
#include "utils/envs.h"

static constexpr uint16_t PORT_DEF {8081};
static constexpr std::string HOST_DEF {"0.0.0.0"};

static constexpr uint64_t THREADS_COUNT {4};


int main() {
    uint16_t port = get_env("PORT", PORT_DEF);
    std::string host = get_env("HOST", HOST_DEF);

    auto& app = drogon::app();
    app.setUploadPath("/tmp/drogon_uploads");

    app.setLogLevel(trantor::Logger::kInfo);

    app.registerHandler("/", root_handler, { drogon::Get });
    app.registerHandler("/healthcheck", healthcheck_handler, { drogon::Get });
    app.registerHandler("/temperature/{sensor_id}", temp_handler_sensor, { drogon::Get });
    app.registerHandler("/temperature", temp_handler_location, { drogon::Get });

    LOG_INFO << "Server starting on " << host << ":" << port;
    app.addListener(host, port);
    app.setThreadNum(THREADS_COUNT);
    
    app.run();

    return 0;
}