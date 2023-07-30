/*
 * Update firmware with external SD
 * Check firmware.bin, if present start update then rename in firmware.bak
 *
 * Renzo Mischianti <www.mischianti.org>
 *
 * https://mischianti.org/
 */

// include the SD library:
#include <SPI.h>
#include <SD.h>

// WeMos D1 esp8266: D8 as standard
const int chipSelect = SS;

void progressCallBack(size_t currSize, size_t totalSize)
{
    Serial.printf("CALLBACK:  Update process at %d of %d bytes...\n", currSize, totalSize);
}

#define FIRMWARE_VERSION 0.2

void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(9600);
    Serial.println("Firmware version: " + String(FIRMWARE_VERSION));
    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for native USB port only
    }

    Serial.print("\nInitializing SD card...");

    // we'll use the initialization code from the utility libraries
    // since we're just testing if the card is working!
    if (!SD.begin(SS))
    {
        Serial.println("initialization failed. Things to check:");
        Serial.println("* is a card inserted?");
        Serial.println("* is your wiring correct?");
        Serial.println("* did you change the chipSelect pin to match your shield or module?");
        while (1)
            ;
    }
    else
    {
        Serial.println("Wiring is correct and a card is present.");
    }

    FSInfo fs_info;
    SDFS.info(fs_info);

    Serial.print("Total bytes: ");
    Serial.println(fs_info.totalBytes);

    Serial.print("Used bytes: ");
    Serial.println(fs_info.usedBytes);

    Serial.print(F("\nCurrent firmware version: "));
    Serial.println(FIRMWARE_VERSION);

    Serial.print(F("\nSearch for firmware.."));
    File firmware = SD.open("/firmware.bin");
    if (firmware)
    {
        Serial.println(F("found!"));
        Serial.println(F("Try to update!"));

        Update.onProgress(progressCallBack);

        Update.begin(firmware.size(), U_FLASH);
        Update.writeStream(firmware);
        if (Update.end())
        {
            Serial.println(F("Update finished!"));
        }
        else
        {
            Serial.println(F("Update error!"));
            Serial.println(Update.getError());
        }

        firmware.close();

        if (SD.rename("/firmware.bin", "/firmware.bak"))
        {
            Serial.println(F("Firmware rename sucessfully!"));
        }
        else
        {
            Serial.println(F("Firmware rename error!"));
        }
        delay(2000);

        ESP.reset();
    }
    else
    {
        Serial.println(F("not found!"));
    }
}

void loop(void)
{
}