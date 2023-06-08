# LacrossePython
This script connects to a CUL device (e.g. nanoCUL 433Mhz). Then the CUL is configured to receive data from Lacrosse thermo sensors.
If there is data from a Lacrosse sensor received, the data is then sent via MQTT.

This projekt is based on following information:
https://www.f6fbb.org/domo/sensors/tx3_th.php
https://github.com/merbanan/rtl_433/blob/master/src/devices/lacrosse.c
http://culfw.de/commandref.html
