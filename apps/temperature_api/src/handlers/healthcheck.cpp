#include "healthcheck.h"


DrogonHandlerPtr<> healthcheck_handler = [](
    const drogon::HttpRequestPtr& req,
    DrogonHandlerCallback&& callback
) {
    Json::Value json;
    json["status"] = "OK";

    auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
    resp->setStatusCode(drogon::k200OK);

    callback(resp);
};
