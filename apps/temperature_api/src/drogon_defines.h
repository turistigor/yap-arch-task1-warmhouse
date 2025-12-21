#include <drogon/drogon.h>

using DrogonHandlerCallback = std::function<void(const drogon::HttpResponsePtr&)>;

template<typename... Args>
using DrogonHandlerPtr = std::function<void (
    const drogon::HttpRequestPtr& req,
    DrogonHandlerCallback&& callback,
    Args&&...
)>;
