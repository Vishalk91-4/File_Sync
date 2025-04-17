import socket
import traceback
import threading
import swarmhelpers

command_list = """Kindly follow the commands listed below:
1. List : To get the updated information of your peers in the Swarm.
2. Terminate : To end your connection.
3. Update : To update the data information available with you to the tracker.
4. Fetch IpAddressOFPeer PortNumberOfPeer file/folderpath : To download the file/folder
5. Reconnect : To reestablish connection with the Tracker.
6: Read : To display current list of peers.
7. All : To display command list.
8. End : To exit the program.
Note: You will not be able to download the file/folder until only when your data information is available with the tracker. Use Reconnect command to reconnect to the tracker.
"""
def handle_connection(connection, addr):
     connection.sendall("""You are know contacting the Tracker. Kindly state your demand.
                  {command_list}
                  """.encode("utf-8"))
    #  Publish the data for the first time to the tracker to establish the connection
     while True:
         cmd = ""
         while True:
             data = connection.recv(1024)
             if not data:
                 break
             cmd+=data.decode("utf-8")
         if cmd == "":
            continue
         cmd = cmd.split("@")
         if cmd[0] == "List":
             try:
              connection.sendall(swarmhelpers.sendpeerinfo(addr[0],cmd[1]).encode("utf-8"))
             except:
              traceback.print_exc()
              connection.senndall("Unable to retrieve Peers".encode("utf-8"))
         elif cmd[0] == "Terminate":
             try:
              swarmhelpers.terminate_connection(addr[0],cmd[1])
              connection.sendall("Connection Terminated".encode("utf-8"))
              break
             except:
                 traceback.print_exc()
                 connection.sendall("Unable to Terminate Connection try again".encode("utf-8"))
         elif cmd[0] == "Update":
             try:
              swarmhelpers.publish_data(addr[0],cmd[1],cmd[2])
              connection.sendall("Data successfully published".encode("utf-8"))
             except:
                traceback.print_exc()
                connection.sendall("Unable to Update user info try again".encode("utf-8"))
         else:
             connection.sendall(command_list)
     print("Connection closed with {addr[0]}:{addr[1]}")
     connection.close()

def server():
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tracker_socket.bind(socket.gethostname(),3000)
        tracker_socket.listen(5)
        while True:
            conn, addr = tracker_socket.accept()
            print(f"New Connection to {addr[0]}:{addr[1]} established")
            threading.Thread(target=handle_connection, args=(conn, addr)).start()
    except socket.error as err:
        traceback.print_exc()

if __name__ == "__main__":
    server()