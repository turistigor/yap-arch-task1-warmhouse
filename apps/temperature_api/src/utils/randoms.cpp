
#include <random>

#include "randoms.h"


double generate_temp() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    static int16_t temp_min {-50}, temp_max {50};
    static std::uniform_real_distribution<> dis(temp_min, temp_max);

    return dis(gen);
}
