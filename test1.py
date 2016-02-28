#!/usr/bin/python

import subprocess
import re
import sys
import time
import MySQLdb




id_thermometer = "DHT110000000001"
gpio_thermometer = 4  

def DHT_read(pin):

    #define lists:
    temp_list=[]
    hum_list=[]

    #define the number of times toread the sensor
    read_count=5

    #set counters to zero
    i=0
    sensor_error=0

    #begin the loop for reading the sensor
    while i<read_count:

        #run DHT driver to read data from sensor
        output = subprocess.check_output(["sudo","python","/home/pi/libraries/Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver/test.py"]);

        #get the temperature out of the 'output' string
        matches_temp = re.search("Temp =\s+([0-9.]+)", output)
        matches_hum = re.search("Hum =\s+([0-9.]+)", output)

       #check for an error
        if (not matches_temp):
            time.sleep(3)
            print "error detected"
            sensor_error=sensor_error+1
            continue

        temp = (float(matches_temp.group(1)))

        #add to temp list
        temp_list.append(temp)
        i=i+1

        #calculate humidity
        humidity = float(matches_hum.group(1))

        #add to humidity list
        hum_list.append(humidity)

    #calculate average temp
    sum_temp=0
    w= len(temp_list)

    while w > 0:
        sum_temp=sum_temp+temp_list[w-1]
        w=w-1

    temp_avg=sum_temp / len(temp_list)
    #calculate average humidity
    sum_hum=0
    w= len(hum_list)

    while w > 0:
        sum_hum=sum_hum+hum_list[w-1]
        w=w-1

    hum_avg=sum_hum / len(hum_list)
    return float(round(temp_avg,1)), float(round(hum_avg,1))


# adds a record to the database
def insert_temp_reading (thermometer,temperature,humidity):

 conn = MySQLdb.connect("localhost","przemek","Json123","pi_base" )
 cursor = conn.cursor()
 params = [thermometer,temperature,humidity]

 try:
   cursor.execute("INSERT INTO temperature_monitor (counter,thermometer,date,temperature,humidity) VALUE (NULL,%s,NOW(),%s,%s)",params)
   conn.commit()
 except MySQLdb.Error, e:
   print "An error has occurred. %s" %e
 finally:
  cursor.close()
  conn.close()



# main section
def main():

    current_temp,current_humidity = DHT_read(gpio_thermometer)
    insert_temp_reading (id_thermometer,current_temp,current_humidity)
    print "Thermometer:" + id_thermometer + "|Temperature:" + `current_temp` + "|Humidity:" + `current_humidity`

if __name__ == '__main__':
    main()
