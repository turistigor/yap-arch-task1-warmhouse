#ifndef TEMP_SENSORS_H
#define TEMP_SENSORS_H

#include "../drogon_defines.h"


extern DrogonHandlerPtr<> temp_handler_location;
extern DrogonHandlerPtr<std::string> temp_handler_sensor;

std::string get_location(const std::string& sensor_id);
Json::Value create_temp_json(float temp, const std::string& location, const std::string& sensor_id);
std::string get_sensor_id(const std::string& location);

#endif  // TEMP_SENSORS_H