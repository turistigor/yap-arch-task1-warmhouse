#include <cstdlib>
#include <string>
#include <cstdint>

// Базовый случай для строк
template<typename T>
T get_env(const std::string& key, T default_value = T{}) {
    const char* val = std::getenv(key.c_str());
    if (!val) return default_value;
    return T(val);
}

template const char* get_env(const std::string& key, const char* default_value);
template std::string get_env(const std::string& key, std::string default_value);

// Специализация для числовых типов
template<>
int get_env<int>(const std::string& key, int default_value) {
    const char* val = std::getenv(key.c_str());
    if (!val) return default_value;
    return std::stoi(val);
}

template<>
uint16_t get_env<uint16_t>(const std::string& key, uint16_t default_value) {
    const char* val = std::getenv(key.c_str());
    if (!val) return default_value;
    return std::stoul(val);
}

template<>
double get_env<double>(const std::string& key, double default_value) {
    const char* val = std::getenv(key.c_str());
    if (!val) return default_value;
    return std::stod(val);
}

template<>
bool get_env<bool>(const std::string& key, bool default_value) {
    const char* val = std::getenv(key.c_str());
    if (!val) return default_value;
    std::string s(val);
    return s == "true" || s == "1" || s == "TRUE" || s == "yes";
}
