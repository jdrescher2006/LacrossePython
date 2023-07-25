#!/usr/bin/python3

import serial
import time
import json
import paho.mqtt.publish as publish
from datetime import datetime

#MQTT Config
MQTT_SERVER = "192.168.0.139"
MQTT_PATH = "Sensor_"
MQTT_PORT = 1883
MQTT_AUTH = {'username':"mqttuser", 'password':"xxxx"}

culVersion = None
adressCode = 0
rssiValue = 0
tempvalue = 0
humvalue = 0
timeStamp = 0

def parseLacrosseData(data):
    global adressCode
    global rssiValue
    global tempvalue
    global humvalue
    global timeStamp

    #check first nibbles
    if data[0] == 't' and data[1] == 'A':
        #extract and calculate Checksum
        sumValue = int(data[1], 16) + int(data[2], 16) + int(data[3], 16) + int(data[4], 16) + int(data[5], 16) + int(data[6], 16) + int(data[7], 16) + int(data[8], 16) + int(data[9], 16)    
        checksumValue = sumValue & 0x0F
        
        #check if checksums match
        if hex(checksumValue) == hex(int(data[10], 16)):

            #extract address code from 3 and 4 nibbles
            adressCode = (((int(data[3], 16)) << 4) | (int(data[4], 16))) >> 1

            print("adressCode", adressCode)
                    
            #extract and calculate RSSI
            rssiValue = data[11] + data[12]
            rssiValue = int(rssiValue, 16)
            if rssiValue >= 128:
                rssiValue = ((rssiValue-256)/2)-74;
            else:
                rssiValue=(rssiValue/2)-74;

            rssiValue=round(rssiValue)

            print("RSSI", rssiValue)    
            
            print("timeStamp", timeStamp.strftime('%Y-%m-%d %H:%M:%S'))                 
                                                  
            #third byte == '0', temperature
            #third byte == 'E', humidity
            if data[2] == '0':
                tempvalue = data[5] + data[6] + data[7]
                tempvalue = int(tempvalue) - 500
                tempvalue = tempvalue / 10                
                print("tempvalue", tempvalue)                
            elif data[2] == 'E':                
                humvalue = data[5] + data[6] + data[7]
                humvalue = int(humvalue) / 10                
                print("humvalue", humvalue)
                
            return True
        else:
            print("Checksum Error!")
            return False
                

def writeMQTT():
    global culVersion
    global adressCode
    global rssiValue
    global tempvalue
    global humvalue
    global timeStamp
    
    body = {
        "culVersion": culVersion,
        "timeStamp": timeStamp.strftime('%Y-%m-%d %H:%M:%S'),
        "adressCode": adressCode,
        "RSSI": rssiValue,
        "tempvalue": tempvalue,
        "humvalue": humvalue
    }  
        
    json_string = json.dumps(body)
    #print(json_string)

    for key, value in body.items():        
        topic = MQTT_PATH + f"{adressCode}/{key}"
        
        try:
            publish.single(topic, value, hostname=MQTT_SERVER, port=MQTT_PORT, auth=MQTT_AUTH)  
            print("Nachricht erfolgreich gesendet.")
        except Exception as e:
            print(f"Fehler beim Senden der Nachricht: {str(e)}")        
        
        
# configure serial interface for CUL
try:
    ser = serial.Serial('/dev/ttyUSB0', baudrate=38400, timeout=8)
except serial.SerialException as e:
    print("Fehler beim Öffnen der seriellen Verbindung:", str(e))
    sys.exit(1)

# Check if serial interface was opened
if ser.is_open:
    print("serial interface opened.")
    
    time.sleep(6)  # Wait to make sure CUL is ready

    command = "V\r\n"  # Request CUL version
    ser.write(command.encode())  # Send command as byte sequence
                                 
    timeout = 5  # Set wait timeout
    start_time = time.time()

    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            culVersion = response
            break

        if time.time() - start_time > timeout:
            print("Timeout while waiting for CUL version.")
            break
   
    print("culVersion:", culVersion)
    
    command = "X21\r\n" #send command for data reporting for SlowRF
    ser.write(command.encode()) #send command as byte sequence
    
    time.sleep(1)
    
    while True:
        if ser.in_waiting > 0:  #check if we have new data
            data = ser.readline().decode().strip() #read data from serial interface
            print("Empfangene Daten:", data)
            timeStamp = datetime.now()
            
            success = parseLacrosseData(data)
            if success == True:
                writeMQTT()
        
        time.sleep(0.1)  # Kurze Wartezeit, um die CPU-Last zu reduzieren
        

    # Serielle Schnittstelle schließen
    ser.close()
    print("serial interface closed.")
else:
    print("Error while opening the serial interface!")
