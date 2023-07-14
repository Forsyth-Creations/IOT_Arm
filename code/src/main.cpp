#include <Arduino.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Preferences.h>


// Local Deps
#include "ApiCaller/apiCaller.h"
#include "Configuration.h"

const char* ssid = ""; // Write here your router's username
const char* password = ""; // Write here your router's password
int count = 0;

// Create an instance of the ApiCaller class
ApiCaller apiCaller;
Preferences preferences;


// Save value to persistant memory
void saveValue(String key, String value) {
  preferences.putString(key.c_str(), value);
}


void setup()
{
  // Start the apiCaller
  Serial.begin(9600);
  preferences.begin("my-app", false);
  apiCaller = ApiCaller(ssid, password, "http://192.168.1.119:8000/api");

  // See if uid is in persistant memory
  // If not, get a new uid from the API
  // then save it to persistant memory

  String memUID = preferences.getString("uid", "empty");
  if ( memUID == "empty")
  {
    Serial.println("No UID found in persistant memory");
    StaticJsonDocument<200> response = apiCaller.get("/v1/uid");
    String uid = response["uid"];
    Serial.println("Got a new UID from the API: " + uid);
    saveValue("uid", uid);
  }
  else {
    Serial.println("Found UID in persistant memory");
    String uid = preferences.getString("uid", "empty");
    Serial.println(uid);
  }

}

void loop()
{
  
}