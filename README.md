# Micro Breakout

## Introduction

Nowadays, the use of cyber-physical systems and their interest among societies has been increasing. Essentially, these systems are designed to interact with the physical world and perform specific tasks such as system automation, which involves controlling and monitoring constantly changing physical variables. The physical variables, usually of analog nature, are detected by sensors and translated by them into electrical signals. These signals will then be processed according to the desired application. Typically, microcontrollers are used to receive information from the sensors and subsequently send it to processing units with greater processing capacity. It is important not to forget that these systems also encompass actuators, i.e., the reverse process, in which the processing unit, for some reason, sends instructions to the microcontroller to activate some actuator. The communication was established by way of a **STIM-NCAP protocol**, which is a standard defined by the IEEE 1451 standard. The microcontroller used in this project was the [PIC18F47Q10](https://www.microchip.com/en-us/product/PIC18F47Q10), which is a microcontroller with an 8-bit architecture and a 16-bit floating point unit. The processing unit was developed in Python and was responsible for receiving the data sent by the microcontroller and processing it.

## Microcontroller

We used a microcontroller was programmed to perform the following tasks:

- Read the analog signal from a potentiometer and convert it to a digital signal.
- Read the digital signal from 4 push buttons.
- Send the digital signal to a processing (my laptop) unit via UART. This was done in accordance with the protocol defined by the [IEEE 1451](https://standards.ieee.org/wp-content/uploads/import/documents/tutorials/1451d4.pdf) standard.

## Processing Unit

There was also the need to develop a processing unit capable of receiving the data sent by the microcontroller and processing it. The processing unit was developed in Python and was responsible for:

- Receiving the data sent by the microcontroller. For this purpose, the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) library was used.
- Pre-processing the data received from the microcontroller.
- Serve as a user interface for the user to interact with the breakout game.

## Breakout Game

The game was developed in Python and was displayed 4 different screens:

- The first screen was the main menu, where the user could choose between 3 options: `Start`, `Teds` and `Options`.
  - The `Start` option would start the game.
  - The `Teds` option would display the teds menu
  - The `Options` option would display the options menu.
- The second screen was the teds menu, where the user could closely interect with the teds that were programmed on the microcontroller.
- The third screen was the options menu, where the user could change the sound effects and the music of the game.

The code for the breakout game was inspired from [this](https://www.101computing.net/breakout-tutorial-using-pygame-getting-started/) website.

## How to run the code

The software was developed in using [MPLAB X IDE](https://www.microchip.com/en-us/tools-resources/develop/mplab-x-ide) with the [xc8](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers) compiler. This means that in order to use the game you must have a microcontroller with the same architecture as the one used in this project. You than have to compile the code and run the [main.py](breakout/main.py) script. Don't forget to set the appropriate port and baudrate.

## Authors

- [Fábio Carneiro](https://github.com/fabiocfabini)
- [Vitória Sousa](https://github.com/Victoria751)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
