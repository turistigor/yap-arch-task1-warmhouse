#include <cmath>

#include "sensors.h"
#include "../utils/datetime.h"
#include "../utils/randoms.h"

static constexpr std::string UNKNOWN_LOCATION {"unknown"};


DrogonHandlerPtr<> temp_handler_location = [](
    const drogon::HttpRequestPtr& req,
    DrogonHandlerCallback&& callback
) {
    LOG_INFO << "temp_handler_location";

    double temperature = generate_temp();

    auto location_param = req->getOptionalParameter<std::string>("location");
    std::string location = (location_param) ? *location_param : UNKNOWN_LOCATION;
    std::string sensor_id = get_sensor_id(location);
    
    auto json = create_temp_json(temperature, location, sensor_id);
    auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
    resp->setStatusCode(drogon::k200OK);

    callback(resp);
};

DrogonHandlerPtr<std::string> temp_handler_sensor = [](
    const drogon::HttpRequestPtr& req,
    DrogonHandlerCallback&& callback,
    const std::string& sensor_id
) {
    LOG_INFO << "temp_handler_sensor";

    float temperature = generate_temp();
    std::string location {get_location(sensor_id)};

    auto json = create_temp_json(temperature, location, sensor_id);
    auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
    resp->setStatusCode(drogon::k200OK);

    callback(resp);
};


Json::Value create_temp_json(
    float temp, const std::string& location, const std::string& sensor_id
) {
    Json::Value json;

    json["Value"] = std::round(temp * 10) / 10.0; // Округление до 0.1
    json["Unit"] = "°C";
    json["Timestamp"] = get_now_timestamp();
    json["Status"] = "active";
    json["SensorID"] = sensor_id;
    json["SensorType"] = "temperature";
    json["Location"] = location;
    json["Description"] = "Description";

    return json;
}


std::string get_location(const std::string& sensor_id) {
    if (sensor_id == "1") {
        return "Living Room";
    } if (sensor_id == "2") {
        return "Bedroom";
    } if (sensor_id == "3") {
        return "Kitchen";
    } else {
		return UNKNOWN_LOCATION;
    }
}


std::string get_sensor_id(const std::string& location) {
    if (location == "Living Room") {
        return "1";
    } if (location ==  "Bedroom") {
        return  "2";
    } if (location ==  "Kitchen") {
        return  "3";
    } else {
		return "0";
    }
}
