#include <Arduino.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Preferences.h>

#include <ArduinoWebsockets.h>
#include <ESP8266WiFi.h>

// Local Deps
#include "ApiCaller/apiCaller.h"
#include "CoreComp/CoreComp.h"
#include "Configuration.h"

// Create an instance of the ApiCaller class
ApiCaller *apiCaller;
CoreComp * coreComp;
String uid;

using namespace websockets;

WebsocketsClient client;

void attemptReconnect()
{
  bool socket_connected = false;
  Serial.println("Connecting to websocket");
  while (!socket_connected)
  {
    // change the '-' to a '_' in the uid
    // The full address needs to append the uid to the end of the WEBSOCKET_ADDRESS_PROPER
    String fullAddress = String(WEBSOCKET_ADDRESS_PROPER) + "/" + uid;
    socket_connected = client.connect(fullAddress);
    delay(2000);
    Serial.print(".");
  }
  
  Serial.println("\nConnected to websocket");
}

void setup()
{
  // Start the apiCaller
  Serial.begin(9600);
  Serial.println("------------ Starting up ------------");
  apiCaller = new ApiCaller(NETWORK_SSID, NETWORK_PASSWORD, API_ENDPOINT);
  coreComp = new CoreComp(apiCaller);
  coreComp->hardsaveUID();

  uid = coreComp->getUID();

  // Setup callbacks
  client.onMessage([&](WebsocketsMessage message)
                   {
      String status = coreComp->UserCommandHandler(message.data());
      if (status != "heartbeat")
        client.send("{'outcome' : '" + status + "'}");
  });


  // access the client of websockets
  attemptReconnect();
  client.send("Hello Server from ESP8266");

  // Testing websocket things
}

void loop()
{
  if (client.available())
  {
    client.poll();
  }
  // If I lose connection, reconnect
  if (!client.available())
  {
    Serial.println("Lost connection, reconnecting");
    attemptReconnect();
  }
  coreComp->heartbeat();
  coreComp->needsUpdate();
  delay(50);
}