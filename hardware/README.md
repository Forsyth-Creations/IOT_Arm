# Getting Started with the Hardware

The hardware is designed with a software called KiCAD. Many of the symbols and footprints are either crafted from scratch or they are pulled from EasyEDA.

Here are some tutorials that could be useful in the future for your development. As a general rule: developing symbols and footprints is not preferred unless __absolutely necessary__.

## Links

[Importing from EasyEDA](https://www.youtube.com/watch?v=W9cLnIjvybo&ab_channel=PlumPot)

[Creating Custom Symbols](https://www.youtube.com/watch?v=LhFWFO8H0jQ)


# Understand KiCAD... Again

So there's a hierarchy ro these things. Note the following:

- Project
    - Symbol (Which is a subset of a symbol library)
    - footprint (Which is a subset of a footprint library)

**The footprint and symbol libraries actually happen in parallel: this is an important distinction, as it abstracts out the idea that you can have multiple of the same basic symbol element that might correspond to a different footprint (you'll catch on)

TLDR: with EasyEDA you can download and import whatever you want (symbol, footprint, or the 3D model) into your project or the global scope of KiCad. Best practice is still to keep all project files local, as it makes it easier to share the project

# Some Notes on Communication Schemes:

- I2C
    - Pins: **SCL, SDA**
    ![I2C Diagram](assets/I2C-SDA-SCL-01.jpg "I2C Diagram")


- SPI
    - Pins: **Serial Clock (SCK), Master Out Slave In (MOSI, also known as SDO), and Master In Slave Out (MISO, also known as SDI), and SS (Slave select)**
    ![SPI Diagram](assets/1200px-SPI_three_slaves.svg.png "SPI Diagram")
    For this project, with so many SPI devices, having numerous SS will be critical

- UART
    - Pins: **RX and TX**
    ![UART Diagram](assets/uart.webp "UART Diagram")
