// Write me something
#include "CoreComp.h"

CoreComp::CoreComp(ApiCaller *apiCaller)
{
    this->apiCaller = apiCaller;
    preferences = new Preferences();
    preferences->begin("my-app", false);
    pinMode(LED_BUILTIN2, OUTPUT);
}

void CoreComp::saveValue(String key, String value)
{
    preferences->putString(key.c_str(), value);
}

void CoreComp::hardsaveUID()
{
    String memUID = preferences->getString("uid", "empty");
    if (memUID == "empty")
    {
        Serial.println("No UID found in persistant memory");
        StaticJsonDocument<200> response = apiCaller->get("/v1/uid");
        uid = response["uid"].as<String>();
        Serial.println("Got a new UID from the API: " + uid);
        saveValue("uid", uid);
    }
    else
    {
        Serial.println("Found UID in persistant memory");
        uid = preferences->getString("uid", "empty");
        Serial.println(uid);
    }
}

void CoreComp::keepTryingForUID()
{
    uid = preferences->getString("uid", "empty");
    while (uid == "null" || uid == "empty") // This means it didn't get it properly from the api
    {
        StaticJsonDocument<200> response = apiCaller->get("/v1/uid");
        uid = response["uid"].as<String>();
        Serial.println("Got a new UID from the API: " + uid);
        delay(3000);
    }
    Serial.println("Success!");
}

// refactor the above code to only make a heartbeat request every 10 seconds
// hint: use the millis() function

void CoreComp::heartbeat()
{
    if (millis() - lastHeartbeat > heartbeatInterval)
    {
        // Serial.println("Making heartbeat request to API");
        StaticJsonDocument<200> body;
        body["ip"] = WiFi.localIP().toString();
        body["firmware_version"] = FIRMWARE_VERSION;
        body["needs_update"] = needsUpdate() ? "true" : "false";
        apiCaller->post("/v1/heartbeat/" + uid, body);
        lastHeartbeat = millis();
    }
}

String CoreComp::UserCommandHandler(WSInterfaceString message)
{
    // Pull the "type" field out of the message
    Serial.println("Got message: " + message);

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, message);
    if (error)
    {
        Serial.print(F("deserializeJson() failed for socket command: "));
        Serial.println(error.c_str());
        delay(250);
        return "-error: " + String(error.c_str());
    }
    String type = doc["type"].as<String>();

    // Check if the message type is toggleLED
    if (type == "toggleLED")
    {
        ledState = !ledState;
        if (ledState)
        {
            // Serial.println("Turning LED on");
            digitalWrite(LED_BUILTIN2, HIGH);
        }
        else
        {
            // Serial.println("Turning LED off");
            digitalWrite(LED_BUILTIN2, LOW);
        }
    }
    else if (type == "restart")
    {
        forceRestart();
    }
    else if (type != "heartbeat")
    {
        Serial.println("Unknown message type: " + type + ". Ignoring");
        return '-' + type;
    }
    return type;
}

void CoreComp::forceRestart()
{
    Serial.println("Restarting device. Hang tight!");
    ESP.reset();
}

String CoreComp::getUID()
{
    return uid;
}

bool CoreComp::needsUpdate()
{
    // Only check for firmware updates every 60 seconds
    if (millis() - lastFirmwareCheck > 60000)
    {
        lastFirmwareCheck = millis();
        StaticJsonDocument<200> response = apiCaller->get("/v1/firmware/" + String(FIRMWARE_VERSION));
        shouldUpdate = response["message"].as<String>() == "True" ? true : false;
    }
    return shouldUpdate;
}