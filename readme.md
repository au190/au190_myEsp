*******************************************************
### Wifi Md or Wifi button

1.  If GPIO0 pull to LOW (less then < 5 sec) at startup it will go in N  mode - not going in sleep mode.
2.  In N mode if GPIO0 is LOW it will go in AP mode - not going in sleep mode.
3.  From N mode or AP mode after 3 min go to sleep.

Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT
4.  3 sec       Normal mode

- Button = EN pin



*******************************************************
### Wifi 3Button

1.  If GPIO0 pull to LOW (less then < 5 sec) at startup it will go in N  mode - not going in sleep mode.
2.  In N mode if GPIO0 is LOW it will go in AP mode - not going in sleep mode.
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
### myEsp


1.  After the firmware upload GPIO2 (Led) set to status Led_i_0.
2.  After the restart all the output set to OFF.
3.  4x3 power cycle. Power the device on for 4 sec, repeat 3 times after that go in AP mode. Interval (ON > 4, OFF < 9) sec. After 3 correct power cycle go in AP mode, on the next power cycle go again in Normal mode.


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
    - GPIO pin set as input and GPIO_16 is pulled to LOW internally and GPIO_0 --> GPIO_15 is pulled to HIGH internally.
    - Checks in every 50msec and send the status ON or OFF
    - If the input is HIGH send the md message in every 10sec untl the input is HIGH.
  - Motion_i
    - GPIO pin set as input and GPIO_16 is pulled to LOW internally and GPIO_0 --> GPIO_15 is pulled to HIGH internally.
    - Checks in every 50msec and send the status ON or OFF
    - If the input is LOW send the md message in every 10sec untl the input is LOW.
  - Led_x
    - Status info Led for Wifi, AP mode, MQTT connections.
    - If GPIOx set as an output then show the output status. Ex: GPIO4 = Output, GPIO2 = Ledx_i_4
  - AP Button
    - GPIO pulled to HIGH the device go in AP mode. Ip: 192.168.4.1
  - AP Button_i
    - GPIO pulled to LOW the device go in AP mode. Ip: 192.168.4.1

    

#### Module functions
 
```
/*******************************************************

Event Commands - the key is the first element in the json object

cmnd
stat
tele

*******************************************************
----------- Module configurations -----------
*******************************************************
Multisensor:
{"o_0":255,"o_1":255,"o_2":155,"o_3":255,"o_4":255,"o_5":6,"o_12":8,"o_13":9,"o_14":15,"o_15":255,"o_16":255,"o_17":81}

Irrigation:
{"o_0":12,"o_1":255,"o_2":255,"o_3":255,"o_4":4,"o_5":4,"o_12":4,"o_13":5,"o_14":4,"o_15":4,"o_16":255,"o_17":255}

MyPlug:
{"o_0":255,"o_1":255,"o_2":255,"o_3":255,"o_4":4,"o_5":154,"o_12":8,"o_13":9,"o_14":255,"o_15":255,"o_16":255,"o_17":255}


-----------   Just for test   -----------
cmnd/ws/in {"test":"","t1":100,"t2":4294967100}

-----------   Get MQTT State   -----------
cmnd/ws/state

-----------   Get MQTT Status   -----------
cmnd/ws/Status 0

-----------   Get Webpage Info   -----------
cmnd/ws/info

-----------   Get Webpage Config   -----------
cmnd/ws/config

-----------   Get filesystem of ESP   -----------
cmnd/ws/in {"fsys":""}

-----------   Temperature offset   -----------
Save the offset in byte: Convert -12.7 - +12.8 C -> convert to 0 - 255. Just 1 decimal.

cmnd/ws/tempoffset -2.6

-----------   Get I2Cscan   -----------
cmnd/ws/I2Cscan

-----------   Get Webpage GPIO Config   -----------
cmnd/ws/config_gpio

-----------   Reboot ESP   -----------
cmnd/ws/reboot



*******************************************************
-----------   TASMOTA compatibile commands  -----------
*******************************************************
All index represents the real GPIO pin number (POWER0 -> POWER16)


-----------   Power   -----------
Get - Set the Power status

- Power can be 0, 1 ,ON, OFF, toggle
- Command can be (POWER0 -> POWER16)
- toggle = if power state is ON switch to OFF and vice versa

cmnd/ws/POWER7
cmnd/ws/POWER7 toggle
cmnd/ws/POWER7 ON
cmnd/ws/POWER7 OFF

-----------   PulseTime   -----------
Command can be (PulseTime0 -> PulseTime16) represents (POWER0 -> POWER16)

Display the amount of PulseTime remaining on the corresponding Relay<x> <value> Set the duration to keep Relay<x> ON when Power<x> ON command is issued. 
After this amount of time, the power will be turned OFF.
0 / OFF     = disable use of PulseTime for Relay<x>
1..111      = set PulseTime for Relay<x> in 0.1 second increments
112..64900  = set PulseTime for Relay<x>, offset by 100, in 1 second increments. 
              Add 100 to desired interval in seconds, e.g., PulseTime 113 = 13 seconds and PulseTime 460 = 6 minutes (i.e., 360 seconds)

1     - 100 ms
2     - 200 ms
10    - 1 sec - 1000 ms 
20    - 2 sec
100   - 10 sec
111   - 11100 ms

112   - 12 sec
113   - 13 sec
(sec + 100) = in second

- PulseTime - set pulse time to (POWER0 -> POWER16)
- If PulseTime is 0 then - PulseTime is off
- If PulseTime is empty return the current value

cmnd/ws/PulseTime5
cmnd/ws/PulseTime5 300

-----------   PulseTimeOn   -----------
PulseTimeOn - Turn ON the GPIO without sending a POWER ON msg
            - It can be 1 or other
            - defult 255

cmnd/ws/PulseTimeOn
cmnd/ws/PulseTimeOn 1

----------- Set cpuspeed  -----------
Working interval for cpu in millisec
Input 1 - 255
default: 50

cmnd/ws/cpuspeed 50

-----------   TelePeriod   -----------
How often sends the telemetry MQTT msg.

- TelePeriod in seconds (min time is 10 sec max time is 3600)
- TelePeriod 65535 will reset the Esp memmory to default (new the flash).

cmnd/ws/TelePeriod
cmnd/ws/TelePeriod 300

-----------   Dimmer   -----------
Command can be (Dimmer0 -> Dimmer16)
Dimmer led with PWM 1 - 100%

cmnd/ws/Dimmer1
cmnd/ws/Dimmer1 50



*******************************************************
-----------   Just for EN_WS2812B  -----------
*******************************************************

----------- Set Color  -----------
Input is: RBG color
response --> {"topic":"stat/ws/RESULT","color":"ff0000","bri":100}

cmnd/ws/color 255,0,0
cmnd/ws/color 255,255,255

----------- Set Brightness  -----------
Input 1 - 100
response --> {"topic":"stat/ws/RESULT","color":"000080","bri":50}

cmnd/ws/bri 50

----------- Set effect -----------
Input is the effect name.

cmnd/ws/effect Rainbow

----------- Set maxpower  -----------
Input 1 -255 --> 100mA - 25 500 mA
Power set to ledstreep = maxpower * 100 = 100 - 25500 milliamps

cmnd/ws/maxpower 10

*******************************************************
-----------   Just for EN_WS2812B  -----------
*******************************************************



*******************************************************
-----------   Just for ARDUINO -----------
*******************************************************

-----------   Arduino OTA   -----------
- Working just with wsS - Wifi serial Gateway. Used to reset the Arduino for OTA update.

cmnd/ws/ard_ota {"ard_ota":"1"}
cmnd/ws/ard_ota {"ard_ota":"0"}

-----------   Arduino get Configuration  -----------
cmnd/ws/ar {"getConf":""}

-----------   Arduino Reset Power  -----------
cmnd/ws/ar {"resetPow":""}

-----------   Arduino Get Set Power threshold  -----------
cmnd/ws/ar {"powThre":""}
cmnd/ws/ar {"powThre":"200"}

-----------   Arduino Set Power Calibration  -----------
Calibraton calculated automatically if not set the vaule, or set a specific vaule

cmnd/ws/ar {"calib":""}
cmnd/ws/ar {"calib":"540"}

-----------   Arduino set time  -----------
Get the power info from Arduino, used internally, runs periodically at state_telemetry_period

state;time

-----------   Arduino get stauts  -----------
Get all the output status form Arduino, used internally

Status;time

-----------   Arduino set time   -----------
Send the configuration to arduino after boot, used internally

xtime;time

*******************************************************
-----------   Just for ARDUINO -----------
*******************************************************

*******************************************************/
```
