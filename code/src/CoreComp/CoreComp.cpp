// Write me something
#include "CoreComp.h"

CoreComp::CoreComp(ApiCaller * apiCaller)
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

// refactor the above code to only make a heartbeat request every 10 seconds
// hint: use the millis() function

void CoreComp::heartbeat()
{
    if (millis() - lastHeartbeat > heartbeatInterval)
    {
        // Serial.println("Making heartbeat request to API");
        StaticJsonDocument<200> body;
        body["ip"] = WiFi.localIP().toString();
        StaticJsonDocument<200> response = apiCaller->post("/v1/heartbeat/" + uid,  body);
        // Serial.println(response["message"].as<String>());
        lastHeartbeat = millis();
    }
}

void CoreComp::UserCommandHandler(WSInterfaceString message)
{
    // Pull the "type" field out of the message
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, message);
    if (error)
    {
        Serial.print(F("deserializeJson() failed for socket command: "));
        Serial.println(error.c_str());
        delay(250);
        return;
    }
    String type = doc["type"].as<String>();
    Serial.println("Got message of type: " + type);

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

}

void CoreComp::forceReset()
{
    Serial.println("Resetting device");
    ESP.reset();
}

String CoreComp::getUID()
{
    return uid;
}
