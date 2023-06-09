# LacrossePython
This script connects to a CUL device (e.g. nanoCUL 433Mhz). Then the CUL is configured to receive data from Lacrosse TX3-TH thermo sensors.
If there is data from a Lacrosse sensor received, the data is then sent via MQTT.
I use this script to send the data to an ioBroker MQTT adapter.

This script is testet with a TFA Dostmann 30.3120.90 sensor. 
Should also work with:<br>
- TFA 30.3125 Temperature and Humidity sensor <br>
- TFA 30.3120.30<br>
- TFA 30.3120.90<br>
- Conrad S555TH<br>
- Conrad S300TH<br>
- ELV S555TH<br>
- ELV S300TH<br>

This projekt is based on following information:<br>
https://www.f6fbb.org/domo/sensors/tx3_th.php<br>
https://github.com/merbanan/rtl_433/blob/master/src/devices/lacrosse.c<br>
http://culfw.de/commandref.html<br>
https://github.com/cgommel/fhem/blob/master/fhem/FHEM/14_CUL_TX.pm

<h3>Installation (for Linux e.g. Raspberry OS)</h3>
- download the script file and make it executable: chmod +x lacrosse.py<br>
- install the MQTT python library: pip3 install paho-mqtt<br>
- execute the script with: python3 lacrosse.py &
