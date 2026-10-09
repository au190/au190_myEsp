
***
Upload the first html page: ip/upload

***
### Wifi Md or Wifi button

1.  If GPIO16 pull to HIGH (less then < 5 sec) at startup it will go in N  mode - not going in sleep mode.
2.  In N mode if GPIO16 is HIGH it will go in AP mode - not going in sleep mode.
3.  From N mode or AP mode after 3 min go to sleep.

Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT
4.  3 sec       Normal mode

- Button = EN pin


*******************************************************
### Wifi 3Button

1.  If GPIO16 pull to HIGH (less then < 5 sec) at startup it will go in N  mode - not going in sleep mode.
2.  In N mode if GPIO16 is HIGH it will go in AP mode - not going in sleep mode.
3.  From N mode or AP mode after 3 min go to sleep.

Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT
4.  3 sec       Normal mode

- GPIO12
- GPIO13
- GPIO14



*******************************************************
### WS2812B

1.  Same as myEsp just GPIO4 is the output for WS2812B - do not use this pin for other config !!!


*******************************************************
### Timeout Logic.
1.	Set up the wifi.
2.	Before using this logic, must start with internet to save the time. Device is getting the time from NTP server.
3.	Restarting the device without the internet, the device is using its own clock.
4.	After 1 minute the device is checking the time and swiching the output (ON or OFF) with timeout.
5.	If the time is equal to set time the device is swiching ON with timeout.


*******************************************************
### myEsp


1.  After the firmware upload GPIO2 (Led) set to status Led_i_0.
2.  After the restart all the output set to OFF.
3.  4x4 power cycle. Power the device on for 4 sec 4 times (at cycle 4 do not power off !!!), on the 4 power cycle go in AP mode. Interval (ON > 4, OFF < 9) sec. Power cycle 4 reseting the PowerCycle to default. 
4.	AP ip: http://192.168.4.1


Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT


#### Configuration info
  - Input
    - GPIO pin set as input
    - Checks in every 50msec and send the status ON or OFF
  - Input_i
    - GPIO pin set as inverted input
    - Checks in every 50msec and send the status ON or OFF
  - Input_pull
    - GPIO pin set as input and GPIO_16 is pulled to LOW internally and GPIO_0 --> GPIO_15 is pulled to HIGH internally.
    - Checks in every 50msec and send the status ON or OFF
  - Motion
    - GPIO pin set as input. I must use resistance on the input (pull down resitor). The MD is active HIGH, and the output is 3.3 V.
    - Checks in every 50msec and send the status ON or OFF
    - If the input is HIGH send the md message in every 10sec until the input is HIGH.
  - Motion_i
    - GPIO pin set as input. I must use resistance on the input (pull up resitor). The MD is active HIGH, and the output is 3.3 V.
    - Checks in every 50msec and send the status ON or OFF
    - If the input is LOW send the md message in every 10sec untl the input is LOW.
  - Led_x
    - Status info Led for Wifi, AP mode, MQTT connections.
    - If GPIOx set as an output then show the output status. Ex: GPIO4 = Output, GPIO2 = Ledx_i_4
  - AP Button
    - GPIO pulled to HIGH the device go in AP mode. Ip: 192.168.4.1
  - AP Button_i
    - GPIO pulled to LOW the device go in AP mode. Ip: 192.168.4.1

    
