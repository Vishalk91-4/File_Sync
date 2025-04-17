import os
import json
import socket
import threading

def sendpeerinfo(ip,port):
    try:
     with open("swarm.json",'r') as f:
        data = json.load(f)
        del data[ip+":"+port]
     f.close()
     return json.dumps(data)
    except:
       raise

def terminate_connection(ip,port):
 threading.Lock().acquire()
 try:
   with open("swarm.json",'r') as f:
      data = json.load(f)
      f.close()
   addr = ip + ":" + port
   if addr in data.keys():
      del data[addr]
   with open("swarm.json", 'w') as f:
      json.dumps(data,f)  
 except:
    raise
threading.Lock().release()
 

def publish_data(ip,port,json_string):
   threading.Lock().acquire()
   try:
      data_to_publish = json.loads(json_string)
      with open("swarm.json","r") as f:
         data = json.load(f)
         f.close()
      addr = ip + ":" + port
      data[addr] = data_to_publish
      with open("swarm.json","w") as f:
         json.dumps(data,f)
   except:
      raise
   threading.Lock().release()

      