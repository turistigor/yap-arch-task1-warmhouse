#include "root.h"


DrogonHandlerPtr<> root_handler = [](
    const drogon::HttpRequestPtr& req,
    DrogonHandlerCallback&& callback
) {
    Json::Value json;
    json["service"] = "Temperature API";
    json["endpoint"] = "GET /temperature?location=<city_name>";
    json["example"] = "curl http://localhost:8081/temperature-api?location=London";

    auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
    callback(resp);
};
