#include <Arduino.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <ArduinoWebsockets.h>
#include "../ApiCaller/apiCaller.h"

// Import Configuration
#include "../Configuration.h"

using namespace websockets;

class CoreComp {
    public:
        CoreComp(ApiCaller * apiCaller);
        void saveValue(String key, String value);
        void hardsaveUID();
        void heartbeat();
        void UserCommandHandler(WSInterfaceString message);
        String getUID();
        void forceReset();
    private:
        Preferences* preferences;
        ApiCaller * apiCaller;
        String uid;
        long unsigned int heartbeatInterval = 5000;
        long unsigned int lastHeartbeat = 0;
        bool ledState = false;
};