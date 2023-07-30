/*
  Ellipse drawing example

  This sketch does not use any fonts.
*/

#include <Arduino.h>

#include <SPI.h>

#include <TFT_eSPI.h> // Hardware-specific library

TFT_eSPI tft = TFT_eSPI();       // Invoke custom library

void setup(void) {
  tft.init();

  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
}

void loop() {
  // Print out some text
  tft.drawString("Hello Catherine", 10, 10, 4);
  delay(1500);
  tft.drawString("I don't need sleep", 10, 50, 4);
  delay(1500);
  tft.drawString("I need answers", 10, 90, 4);
  delay(1500);
  tft.drawString("I also need you", 10, 130, 4);
  delay(1500);
  tft.drawString("I love you", 10, 170, 4);
  delay(1500);
  tft.drawString(":-)", 10, 210, 4);
  delay(1500);
  tft.drawString("Good night", 10, 250, 4);

  // End the SPI transaction (Added by Henry Forsyth)
  tft.endWrite();
}
