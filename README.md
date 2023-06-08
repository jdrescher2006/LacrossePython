# LacrossePython
This script connects to a CUL device (e.g. nanoCUL 433Mhz). Then the CUL is configured to receive data from Lacrosse TX3-TH thermo sensors.
If there is data from a Lacrosse sensor received, the data is then sent via MQTT.
I use this script to send the data to an ioBroker MQTT adapter.

This script is testet with a TFA Dostmann 30.3120.90 sensor. 
Should also work with:
TFA 30.3125 Temperature and Humidity sensor 
TFA 30.3120.30
TFA 30.3120.90

This projekt is based on following information:<br>
https://www.f6fbb.org/domo/sensors/tx3_th.php<br>
https://github.com/merbanan/rtl_433/blob/master/src/devices/lacrosse.c<br>
http://culfw.de/commandref.html

<h3>Installation (for Linux e.g. Raspberry OS)</h3>
- download the script file and make it executable: chmod +x lacrosse.py<br>
- install the MQTT python library: pip3 install paho-mqtt<br>
- execute the script with: python3 lacrosse.py &
