/*
  Listfiles

  This example shows how print out the files in a
  directory on a SD card

  The circuit:
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)

  created   Nov 2010
  by David A. Mellis
  modified 9 Apr 2012
  by Tom Igoe
  modified 2 Feb 2014
  by Scott Fitzgerald

  This example code is in the public domain.

*/
#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

File root;

void printDirectory(File dir, int numTabs) {
  while (true) {

    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      printDirectory(entry, numTabs + 1);
    } else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
    }
    entry.close();
  }
}

// Find the firmware.bin file
// For ease of use, we assume that the firmware.bin file is in the root directory

void findFirmwareBin()
{

  root = SD.open("/");

  File entry = root.openNextFile();
  while (entry)
  {
    if (!entry.isDirectory())
    {
      Serial.println(entry.name());
      if (strcmp(entry.name(), "firmware.bin") == 0)
      {
        Serial.println("Found firmware.bin");
        return;
      }
    }
    entry = root.openNextFile();
  }
  entry.close();
  Serial.println("Did not find firmware.bin");
  // print all files in top directory
  printDirectory(root, 0);
}

// transfer the firmware.bin file to the ESP32
// we will be using binary transfer mode


void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.print("Initializing SD card...");

  if (!SD.begin(15)) {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");
  findFirmwareBin();
  Serial.println("done!");
}

void loop() {
  // nothing happens after setup finishes.
}