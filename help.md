
*******************************************************
#### Wifi Md or Wifi button
*******************************************************

1.  If GPIO16 is HIGH (less then < 5 sec) at startup it will go in N  mode - not going in sleep mode.
2.  In N mode if GPIO16 is HIGH it will go in AP mode - not going in sleep mode.
3.  From N mode or AP mode after 2 min go to sleep.

Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT
4.  3 sec       Normal mode

Button = EN pin



*******************************************************
#### Wifi 3Button
*******************************************************

1.  If GPIO16 is HIGH (less then < 5 sec) at startup it will go in N  mode - not going in sleep mode.
2.  In N mode if GPIO16 is HIGH it will go in AP mode - not going in sleep mode.
3.  From N mode or AP mode after 2 min go to sleep.

Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT
4.  3 sec       Normal mode

GPIO12
GPIO13
GPIO14



*******************************************************
#### myEsp
*******************************************************

1.  After the firmware upload:
    a.  GPIO16 set to C_AP_MODE_BTN_I allways go in AP mode. Active after 5 seconds after start-up.
    b.  GPIO2 (Led) set to status Led_0.
2.  After the Wifi config is done the GPIO16 must be set to not C_AP_MODE_BTN_I.
3.  If no Wifi or MQTT connection restart after 5 min.






Blink:
1.  100 msec    Connecting to Wifi
2.  1 sec       AP mode
3.  2 sec       No MQTT



<pre>

/*******************************************************

Event Commands - the key is the first element in the json object

cmnd
stat
tele

*******************************************************
----------- Module configurations -----------
*******************************************************
Multisensor:
{"o_0":255,"o_1":255,"o_2":14,"o_3":0,"o_4":255,"o_5":6,"o_12":8,"o_13":9,"o_14":15,"o_15":10,"o_16":255,"o_17":81}

Irrigation:
{"o_0":12,"o_1":255,"o_2":14,"o_3":0,"o_4":4,"o_5":4,"o_12":4,"o_13":5,"o_14":4,"o_15":4,"o_16":10,"o_17":255}

MyPlug:
{"o_0":255,"o_1":255,"o_2":255,"o_3":0,"o_4":4,"o_5":154,"o_12":8,"o_13":9,"o_14":255,"o_15":255,"o_16":10,"o_17":255}





-----------   Get MQTT State   -----------
cmnd/ws/state


-----------   Get MQTT Status   -----------
cmnd/ws/Status 0


-----------   Get Webpage Info   -----------
cmnd/ws/info


-----------   Get Webpage Config   -----------
cmnd/ws/config

-----------   Get Webpage GPIO Config   -----------
cmnd/ws/config_gpio

-----------   Reboot ESP   -----------
cmnd/ws/reboot


-----------   Get filesystem of ESP   -----------
cmnd/ws/in {"fsys":""}


-----------   Get I2Cscan   -----------
cmnd/ws/I2Cscan




----------- Just for EN_WS2812B - Set Color  -----------
cmnd/ws/color 255,0,0
cmnd/ws/color 255,255,255
response --> {"topic":"stat/ws/RESULT","color":"ff0000","bri":100}
Input is: RBG color


----------- Just for EN_WS2812B - Set Brightness  -----------
1 - 100
cmnd/ws/bri 50
response --> {"topic":"stat/ws/RESULT","color":"000080","bri":50}


----------- Just for EN_WS2812B - Set speed  -----------
cmnd/ws/speed 50

1 - 255
default: 50


----------- Just for EN_WS2812B - Set effect -----------
cmnd/ws/effect Rainbow

Input is the effect name.


----------- Just for EN_WS2812B - Set maxpower  -----------
1 -255 -> 100mA - 25 500 mA
Power set to ledstreep = maxpower * 100 = 100 - 25500 milliamps
cmnd/ws/maxpower 10




*******************************************************
-----------   ARDUINO commands  -----------
*******************************************************

-----------   Arduino OTA   -----------

- Working just with wsS - Wifi serial Gateway. Used to reset the Arduino for OTA update.
----------------------------
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


-----------   Arduino get state  -----------
Get power data

state;time

-----------   Arduino get stauts  -----------
Status;time

-----------   Arduino set time   -----------
Send the configuration to arduino after boot
xtime;time



*******************************************************
-----------   TASMOTA compatibile commands  -----------
*******************************************************


All index represents the real GPIO pin number (POWER0 -> POWER16)


-----------   Power   -----------

- Power can be 0, 1 ,ON, OFF, toggle
- msg can be (POWER0 -> POWER16)
- toggle = if power state is ON switch to OFF and vice versa
----------------------------
Get the Power status
cmnd/ws/POWER7
Set the Power status
cmnd/ws/POWER7 ON
cmnd/ws/POWER7 OFF


-----------   PulseTime   -----------

Msg can be (PulseTime0 -> PulseTime16) represents (POWER0 -> POWER16)

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

----------------------------
- PulseTime - set pulse time to (POWER0 -> POWER16)
- if PulseTime is 0 then - PulseTime is off
- if PulseTime is empty then will be request the state
----------------------------
cmnd/ws/PulseTime5
cmnd/ws/PulseTime5 300

-----------   PulseTimeOn   -----------

PulseTimeOn - Turn ON the GPIO without sending a POWER ON msg
            - It can be 1 or other
            - defult 255
----------------------------
cmnd/ws/PulseTimeOn
cmnd/ws/PulseTimeOn 1


-----------   TelePeriod   -----------

How often sends the telemetry MQTT msg.

- TelePeriod in seconds (min time is 10 sec max time is 3600)
- if TelePeriod is empty then will be request the state
----------------------------
cmnd/ws/TelePeriod
cmnd/ws/TelePeriod 300


-----------   Dimmer   -----------
- msg can be (Dimmer0 -> Dimmer16)

Dimmer led with PWM 1 - 100%
Get or Set the dimmer
----------------------------
cmnd/ws/Dimmer1
cmnd/ws/Dimmer1 50



*******************************************************/

</pre>
