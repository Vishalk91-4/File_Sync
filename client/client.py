import socket
import threading
import os
import clienthelpers
import json
import traceback
connection_established = False
MY_IP = '127.0.0.1'
MY_PORT = 5000

def start_client_server():
  try:
    client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_server_socket.bind(socket.gethostname(),5000)
    client_server_socket.listen(5)
    global connection_established
    while connection_established is True:
        soc, addr = client_server_socket.accept()
        print(f"Handling requests from {addr}")
        handle_peer(soc,addr)
    print("Closing CLient Side Server...")
    client_server_socket.close()
  except:
      traceback.print_exc()

def handle_peer(soc,addr):
 try:
    soc.sendall(f"Welcome!! You are now connected to {MY_IP}:{MY_PORT}. Kindly state your requirements.")
    response = ""
    while 1:
        data = soc.recv(1024)
        if not data: break
        response+=data.decode('utf-8') #we will recevie file/folder path in this step
    if not os.path.exists(response):
        soc.sendall("Invalid file/folder path. Update the information about your peers.")
        return
    if os.path.isdir(response):
        for rootdir,_,files in os.walk(response):
            for file in files:
                filename = os.path.relpath(os.path.join(rootdir,file),"Client")
                filesize = os.path.getsize(filename)
                soc.sendall(filename.encode("utf-8"))
                soc.sendall(str(filesize).encode("utf-8"))
                with open(filename,'r') as f:
                    while True:
                        data = f.read(1024)
                        if not data: break
                        soc.sendall(data.encode("utf-8"))
    else:
        filename = os.path.relpath(response,"Client")
        filesize = os.path.getsize(filename)
        soc.sendall(filename.encode("utf-8"))
        soc.sendall(str(filesize).encode("utf"))
        with open(filename,'r') as f:
            while True:
                data = f.read(1024)
                if not data: break
                soc.sendall(data.encode("utf-8"))
            
    soc.close()
 except:
    traceback.print_exc()
    print("Data Sent successfully")
    return


def main():
 try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1',3000))
    response = ""
    while True:
        data = client_socket.recv(1024)
        if not data: break
        response += data.decode("utf-8")
    global connection_established
    connection_established = clienthelpers.initializer(client_socket,MY_PORT)
    print(response)
    if connection_established == False:
        print("Tracker unreachable. Use Reconnect command to establish connection")
        client_socket.close()
    else :
        threading.Thread(target=start_client_server).start()
    while True:
        cmd = input("Enter your command")
        global connection_established
        if connection_established == False:
            if cmd == "Reconnect":
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('127.0.0.1',3000))
                response = ""
                while True:
                   data = client_socket.recv(1024)
                   if not data: break
                   response += data.decode("utf-8")
                global connection_established
                connection_established = clienthelpers.initializer(client_socket,MY_PORT)
                print(response)
                if connection_established == False:
                    print("Tracker unreachable. Use Reconnect command to establish connection")
                    client_socket.close()
                else:
                    threading.Thread(target = start_client_server).start()
            elif cmd == "End":
                break
            else:
                print("Client not connected to the Tracker. Use Reconnect Command to establish connection")
        else:
            if cmd =="Reconnect":
                print("Connection already established")
            elif cmd == "Terminate":
                data = {}
                with open("peers.json",'w')  as f:
                    json.dump(data,f)
                global connection_established
                connection_established = False
                client_socket.sendall(f"Terminate@{MY_PORT}")
                response = ""
                while 1:
                    data = client_socket.recv(1024)
                    if not data: break
                    response += data.decode("utf-8")
                print(response)
                client_socket.close()
            elif cmd == "List":
                cmd+=f"@{MY_PORT}"
                client_socket.sendall(cmd)
                response = ""
                while True:
                    data = client_socket.recv(1024)
                    if not data :  break
                    response+=data.decode("utf-8")
                clienthelpers.publish_peer_info(response)
                clienthelpers.print_peer_info()
            elif cmd == "Read":
                clienthelpers.print_peer_info()
            elif cmd == "Update":
                info = clienthelpers.directory_tree_as_json()
                client_socket.sendall(cmd+f"@{MY_PORT}@"+info)
                print(client_socket.recv(1024).decode("utf-8"))
            elif cmd == "All":
                print("""Kindly follow the commands listed below:
                         1. List : To get the updated information of your peers in the Swarm.
                         2. Terminate : To end your connection.
                         3. Update : To update the data information available with you to the tracker.
                         4. Fetch IpAddressOFPeer PortNumberOfPeer file/folderpath : To download the file/folder
                         5. Reconnect : To reestablish connection with the Tracker.
                         6: Read : To display current list of peers.
                         7. All : To display command list.
                         8. End : To exit the program.
                         Note: You will not be able to download the file/folder until only when your data information is available with the tracker. Use Reconnect command to reconnect to the tracker.
                        """)
            elif cmd.strip().startswith("Fetch"):
                cmd = cmd.strip().split(" ")
                if len(cmd) < 4: 
                    print("Invalid command")
                    continue
                folder_name = input("Enter the name of the in which the downloaded file/folder will be saved. Your folder will be saved in downloads/host:port/foldername")
                folder_path = ""
                for i in range(3,len(cmd)):
                    folder_path+=cmd[i]
                threading.Thread(target=handle_data_download,args=(cmd[1],cmd[2],folder_path,folder_name))
            elif cmd == "End":
                global connection_established
                connection_established = False
                data = {}
                with open("peers.json",'w')  as f:
                    json.dump(data,f)
                client_socket.sendall(f"Terminate@{MY_PORT}")
                response = ""
                while 1:
                    data = client_socket.recv(1024)
                    if not data: break
                    response += data.decode("utf-8")
                print(response)
                break
    client_socket.close()
 except:
     traceback.print_exc()

def handle_data_download(ip,port,folder_path,folder_name):
 try:
    data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    data_socket.connect((ip,int(port)))
    print(data_socket.recv(1024).decode("utf-8"))
    data_socket.sendall(folder_path.encode("utf-8"))
    os.makedirs(os.path.join("downloads",f"{ip}:{port}",folder_name),exist_ok=True)
    with data_socket.makefile('r') as reader:
        while True:
            filename = reader.readline().decode("utf-8")
            if not filename: break
            print(filename)
            filesize = int(reader.readline().decode("utf-8"))  
            with open(os.path.join("downloads",f"{ip}:{port}",filename),'w') as f:
                while filesize>0:
                    filesize -= min(filesize,1024)
                    data = reader.read(min(filesize,1024)).decode("utf-8")
                    if not data: break
                    f.write(data)
                f.close()
    print("Download Complete")
 except:
     traceback.print_exc()

    
if __name__ == "__main__":
    main()