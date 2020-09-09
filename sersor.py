# Carrega as bibliotecas
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import json
from time import gmtime, strftime,sleep
import time
import uuid
from datetime import datetime
import psycopg2
# Define o tipo de sensor
sensor = Adafruit_DHT.DHT11
#sensor = Adafruit_DHT.DHT22
GPIO.setmode(GPIO.BOARD)

# Define a GPIO nectada ao pino de dados do sensor
pino_sensor = 22
con = psycopg2.connect(host='localhost', database='dados',user='pi', password='1020')


def gravarDados(dados):
   arq = open("dados_sensor.txt",'r')
   data = []
   data = arq.readlines()
   arq.close()
   arq = open("dados_sensor.txt",'w')
   data.append(str(dados))
   arq.writelines(data)
   arq.close()
   print ("DADOS SALVADOS!\n")

def sendData(input):
   uuidx = uuid.uuid4()
   headers = {"Content-Type": "application/json"}
   print (headers)
   url = "http://192.168.1.230:9200/sensorrasp/_doc/%s"%uuidx
   print (url)
   try:
      response = requests.post(url=url, headers=headers, data=json.dumps(input))
      return response.text
   except:
      print("ERRO SEND DATA\n\n")
      return response.text
   
def colector(local,temp,umid):
   insTime = strftime("%Y%m%d%H%M%S", gmtime())
   hour=int(strftime("%H", gmtime()))
   hour = hour - 3
   #insTime2 = strftime("%Y-%m-%d "+str(hour)+":%M:%S", gmtime())
   insTime2 = strftime("%b %d, %Y @ "+str(hour)+":%M:%S.000", gmtime())
   #insTime2 = time.time()
   print (insTime2)
   data = {
       "local": local,
       "temp": temp,
       "umid": umid,
       "date": insTime2
           }
   return data


while(1):
# Informacoes iniciais
   print ("*** Lendo os valores de temperatura e umidade\n");
   umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
   if umid is not None and temp is not None:
      tempo = time.strftime('%Y-%b-%d-%H:%M:%S')
      print (tempo)
      print (("Temperatura = %0.0fC  Umidade = %0.0f%%")%(temp, umid))
      #ret = sendData(colector("RASPBERRY",temp,umid))
      #print (ret)
      #print ("DADOS ENVIADOS:",colector("RASPBERRY",temp,umid))
      #print ("Aguarda 15 segundos para efetuar nova leitura...")
      #time.sleep(60)

     #try:
      #   conn = http.client.HTTPConnection("srv03.labnet.nce.ufrj.br",80)
     #conn.set_tunnel("srv03.labnet.nce.ufrj.br")
       #  url = '/tempCode/marcos/termo/?leitura={"temperatura":'+str(temp)+',"umidade":'+str(umid)+'}'
     #params = urllib.parse.urlencode({'leitura':'{"temperatura":'+str(temp)+',"umidade":'+str(umid)+',"timestamp":'+str(tempo)+'}'})
     #params = urllib.parse.urlencode({leitura:"{teste:10}")
     #print (params)
     #url2 = "srv03.labnet.nce.ufrj.br/tempCode/marcos/termo/?"+params
        # conn.request("GET",url)
         #response = conn.getresponse()
         #print(response.status, response.reason)
     #except:
      #    print ("ERRRO AO ENVIAR")
     #urlopen(url2)
     #print (url)
     #conn.close()

      #dados_to_save = "%s,%s,%s,%s,%s,%s,%s,%s\n"%(time.strftime('%Y'),time.strftime('%b'),time.strftime('%d'),time.strftime('%H'),time.strftime('%M'),time.strftime('%S'),temp,umid)
      #gravarDados(dados_to_save)
      cur = con.cursor()
      tstamp = time.time()
      sql = "insert into sensor (temp,umid,timestamp) values ('%d','%d','%d')"%(temp,umid,float(tstamp))
      print (sql)
      cur.execute(sql)
      con.commit()
      time.sleep(60)
   else:
      #Mensagem de erro de comunicacao com o sensor
      print("Falha ao ler dados do DHT11 !!!")
   print ("==========================================================================")

