#ifndef API_CALLER_H
#define API_CALLER_H

#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

class ApiCaller {
    public:
        ApiCaller();
        ApiCaller(const char* ssid, const char* password, const char* endpoint);
        StaticJsonDocument<200> post(String route, StaticJsonDocument<200> body);
        StaticJsonDocument<200> get(String route);
        WiFiClient getWifiClient();
    private:
        const char* ssid;
        const char* password;
        const char* endpoint;
        WiFiClient client;
        HTTPClient http;
};

#endif // API_CALLER_H