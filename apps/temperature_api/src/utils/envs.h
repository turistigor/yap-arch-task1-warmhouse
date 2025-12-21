#ifndef TEMP_ENVS_H
#define TEMP_ENVS_H


template<typename T>
T get_env(const std::string& key, T default_value = T{});


#endif  // TEMP_ENVS_H
