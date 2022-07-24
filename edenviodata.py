import network, time 
import json
from dht import DHT11
from machine import Pin, ADC
from utime  import sleep_ms
import ujson
import urequests as requests
from dht import DHT11
from machine import Pin, ADC
from utime  import sleep_ms
from MQ7 import MQ7

class myforestsensor():
   
    def __init__(self):
        self.datah = {}
        self.datahs = {}
        self.datat = {}
        self.datac = {} 
        self.summaryh  = 0
        self.summaryhs  = 0
        self.summaryt  = 0
        self.summaryc  = 0
        
    def getdatasensor(self,sensor):
        
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        j = 0
        u = 0
        for n in nums:
            sh = 0
            shs = 0
            st = 0
            sc = 0
            a = [0] * len(nums)
            b = [0] * len(nums)
            c = [0] * len(nums)
            d = [0] * len(nums)
            
            i = 0
            for r in a:
                a[i] = getdatasensorh()
                sh = sh + a[i]
                b[i] = getdatasensorhs()
                shs = shs + b[i]
                c[i] = getdatasensort()
                st = st + c[i]
                d[i] = getdatasensorc(sensor)
                sc = sc + d[i]
                i += 1
                u += 1
                print ("Muestras={:02d} / {:02d}".format(u, 4* len(nums)* len(nums))) 
            self.summaryh  = self.summaryh  + (sh / i)
            self.summaryhs  = self.summaryhs  + (shs / i)
            self.summaryt  = self.summaryt  + (st / i)
            self.summaryc  = self.summaryc  + (sc / i)
            self.datah[n]= a
            self.datahs[n]= b
            self.datat[n]= c
            self.datac[n]= d
            j += 1
        self.summaryh = str(self.summaryh / j)
        self.summaryhs = str(self.summaryhs / j)
        self.summaryt = str(self.summaryt / j)
        self.summaryc = str(self.summaryc / j)
      
            


   
    
    def getdatah(self):
        return self.datah
    
    def getsummaryh(self):
        return self.summaryh
    
    def getdatahs(self):
        return self.datahs
    
    def getsummaryhs(self):
        return self.summaryhs
    
    def getdatat(self):
        return self.datat
    
    def getsummaryt(self):
        return self.summaryt
    
    def getdatac(self):
        return self.datac
    
    def getsummaryc(self):
        return self.summaryc

def conectaWifi (red, password):
      
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True
  
    
def getdatasensorh():
    try:
        sleep_ms(350)
        sensorDHT.measure()
        hum=sensorDHT.humidity()
        print ("H={:02d} % ".format(hum)) 
        return hum;
    except:
      print("An exception occurred")
      return 0;
    

def getdatasensort():
    try:
        sleep_ms(350)
        sensorDHT.measure()
        temp=sensorDHT.temperature()
        print ("T={:02d} % ".format(temp)) 
        return temp;
    except:
        print("An exception occurred")
        return 0;


def getdatasensorhs():
    try:
        sleep_ms(50)
        lectura = sensor1.read()
        l = (0.000000036*(lectura**3))-(0.0001*(lectura**2)) -0.0329*lectura + 99.9440
        print(int(l))
        sleep_ms(100)
        return int(l);
    except:
        print("An exception occurred")
        return 0;
    

def getdatasensorc(sensor):
    try:
        c =  int(sensor.readCarbonMonoxide()*1000)
        print("Smoke: {0}".format(c))
        return c;
    except:
        print("An exception occurred")
        return 0;
    
        
sensorDHT = DHT11(Pin(2))
sensor1 = ADC(Pin(34))
sensor1.atten(ADC.ATTN_11DB)
sensor1.width(ADC.WIDTH_10BIT)
sensor = Pin(22,Pin.IN, Pin.PULL_UP)


class demo():
    def __init__(self): 
        if conectaWifi ("MIWIFI_uXQR", "xNYfQMAe"):
            print ("Conexión exitosa!")
            print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
            self.sensor4 = MQ7(pinData = 32, baseVoltage = 3.3)
            
            print("Calibrating")
            self.sensor4.calibrate()
            print("Calibration completed")
            print("Base resistance:{0}".format(self.sensor4._ro))
		
            while True:
        
                estado = sensor.value()
                sleep_ms(300)
                print(estado)
                if estado == 1:
                    newsensor= myforestsensor()
                    newsensor.getdatasensor(self.sensor4)
                    post_data = ujson.dumps({ 'zone': 'zona 4', 'data':newsensor.getdatah(), 'summary': newsensor.getsummaryh(), 'typeSensor': 'humedad'})
                    request_url = 'https://hqa2-zud6rvkima-uc.a.run.app/sensor'
                    respuesta = requests.post(request_url, headers = {'content-type': 'application/json', 'Authorization': 'Basic ZW50cnVzdDpaVzUwY25WemREcHdZWE56TWpBeU1RPT0='}, data = post_data).json()
                    print(respuesta)
                    sleep_ms(200)
                    post_data = ujson.dumps({ 'zone': 'zona 4', 'data': newsensor.getdatahs(), 'summary': newsensor.getsummaryhs(), 'typeSensor': 'humedad suelo'})
                    request_url = 'https://hqa2-zud6rvkima-uc.a.run.app/sensor'
                    respuesta = requests.post(request_url, headers = {'content-type': 'application/json', 'Authorization': 'Basic ZW50cnVzdDpaVzUwY25WemREcHdZWE56TWpBeU1RPT0='}, data = post_data).json()
                    print(respuesta)
                    sleep_ms(200)
                    post_data = ujson.dumps({ 'zone': 'zona 4', 'data': newsensor.getdatat(), 'summary': newsensor.getsummaryt(), 'typeSensor': 'temperatura'})
                    request_url = 'https://hqa2-zud6rvkima-uc.a.run.app/sensor'
                    respuesta = requests.post(request_url, headers = {'content-type': 'application/json', 'Authorization': 'Basic ZW50cnVzdDpaVzUwY25WemREcHdZWE56TWpBeU1RPT0='}, data = post_data).json()
                    print(respuesta)
                    sleep_ms(200)
                    post_data = ujson.dumps({ 'zone': 'zona 4', 'data': newsensor.getdatac(), 'summary': newsensor.getsummaryc(), 'typeSensor': 'carbono'})
                    request_url = 'https://hqa2-zud6rvkima-uc.a.run.app/sensor'
                    respuesta = requests.post(request_url, headers = {'content-type': 'application/json', 'Authorization': 'Basic ZW50cnVzdDpaVzUwY25WemREcHdZWE56TWpBeU1RPT0='}, data = post_data).json()
                    print(respuesta)
                    sleep_ms(200)
        else:
            print ("Imposible conectar")
            miRed.active (False)
        
if __name__ == "__main__":
    d = demo()