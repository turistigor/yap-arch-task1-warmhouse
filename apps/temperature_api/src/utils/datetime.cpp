#include <string>
#include <ctime>
#include <iomanip>

#include <trantor/utils/Date.h>

#include "datetime.h"


std::string get_now_timestamp() {
    auto now = trantor::Date::date();
    std::time_t t = now.secondsSinceEpoch();
    std::tm* tm = std::gmtime(&t);
    
    std::ostringstream oss;
    oss << std::put_time(tm, "%Y-%m-%dT%H:%M:%SZ");
    return oss.str();
}
