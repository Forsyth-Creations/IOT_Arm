#include "apiCaller.h"

ApiCaller::ApiCaller()
{
    this->ssid = "";
    this->password = "";
    this->endpoint = "";
}

ApiCaller::ApiCaller(const char *ssid, const char *password, const char *endpoint)
{
    this->ssid = ssid;
    this->password = password;
    this->endpoint = endpoint;
    WiFi.begin(ssid, password);
    Serial.println("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected");
    // print the IP
    Serial.println(WiFi.localIP());
}

// Write me a post script
StaticJsonDocument<200> ApiCaller::post(String route, StaticJsonDocument<200> body)
{
    StaticJsonDocument<200> doc;
    String fullEndpoint = this->endpoint + String(route);

    // Serial.println("Making request to " + fullEndpoint);

    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        WiFiClient client;

        http.begin(client, fullEndpoint); // Specify the URL
        // Make a post request, where the body is a json object
        http.addHeader("Content-Type", "application/json");
        // convert body into a string
        String bodyString;
        serializeJson(body, bodyString);
        http.POST(bodyString); // Send the request
        // Use ArudinoJson to parse the response
        String response = http.getString();
        if (response.length() > 0)
        {
            DeserializationError error = deserializeJson(doc, response);
            if (error)
            {
                Serial.print(F("deserializeJson() failed 'post': "));
                Serial.println(error.c_str());
                delay(2000);
                return doc;
            }
        }

        http.end(); // Close connection
    }
    return doc;
}

StaticJsonDocument<200> ApiCaller::get(String route)
{
    StaticJsonDocument<200> doc;
    String fullEndpoint = this->endpoint + String(route);

    Serial.println("Making request to " + fullEndpoint);

    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        WiFiClient client;

        http.begin(client, fullEndpoint); // Specify the URL
        // Make a post request, where the body is a json object
        http.GET(); // Send the request

        // Use ArudinoJson to parse the response
        DeserializationError error = deserializeJson(doc, http.getString());
        if (error)
        {
            Serial.print(F("deserializeJson() failed: "));
            Serial.println(error.c_str());
            delay(2000);
            return doc;
        }
        http.end(); // Close connection
    }
    return doc;
}

// return wifi object
WiFiClient ApiCaller::getWifiClient()
{
    return this->client;
}