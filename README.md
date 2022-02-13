# Remote_Control
4-wheel remote-controlled platform and controller with 2 joysticks

## Needed stuff:
### Controller:
- Raspberry Pi Pico
- NRF24L01
- 2x analog joystick

### 4-wheel platform:
- Raspberry Pi Pico
- NRF24L01
- dc engines controller (I used a two-channel motor driver - Pololu TB6612FNG)
- 4x dc engine (I used N20 motors which are similar to the popular Pololu DC motors)<br /> <br />

## Wiring:

NRF24L01 modules use SPI(0), which means they must be connected to the following pins:
- VCC - Pin 36 / 3V3 
- GND - Pin 38 / GND (or any other GND Pin)	
- CE - Pin 22 / GP17	/ SPI0 CSn
- CS - Pin 19 / GP14	
- SCK - Pin 9 / GP6 /	SPI0 SCK
- MOSI - Pin 10 / GP7	/ SPI0 TX
- MISO - Pin 6 / GP4	/ SPI0 RX

Joystick 1 should be connected to the following pins:
- GND - Pin 38 / GND (or any other GND Pin)
- +5V - Pin 36 / 3V3 Out	
- VRX - Pin 32 / GP27 / ADC1

Joystick 2 should be connected to the following pins:
- GND - Pin 38 / GND (or any other GND Pin)
- +5V - Pin 36 / 3V3 Out	
- VRY - Pin 31 / GP26 / ADC0

Motor controller should be connected to the following pins:
- PWM A - Pin 11 / GP8
- A IN 1 - Pin 12 / GP9
- A IN 2 - Pin 14 / GP10
- STBY - Pin 15 / GP11
- PWM B - Pin 20 / GP15
- B IN 1 - Pin 17 / GP13
- B IN 2 - Pin 16 / GP12
- VCC - Pin 36 / 3V3 Out	
- GND - Pin 38 / GND (or any other GND Pin)
- A OUT 1 - Motor +
- A OUT 2 - Motor -
- B OUT 2 - Motor -
- B OUT 1 - Motor +
- V MOT - external power source (power supply to motors (3-12 V) I used 6 AA batteries which gives 9V source)
- GND - GND from external power source

I used 3 AA batteries to power the RPi Picos (which gives a source of 4.5V) by connecting + to Pin 39 / VSYS and - to Pin 38 / GND

## Program description:

In project, to control the NRF24L01 modules the dedicated library where used: https://github.com/micropython/micropython/blob/master/drivers/nrf24l01/nrf24l01.py 

The controller works as a master and sends a direction instruction based on the position of the joysticks, one is for Forward, Backward, and the other is for Left, Right turns.

The platform works as a slave, receives direction instructions from the controller, and uses them to send control signals to the DC motors via the motor controller.
