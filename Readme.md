# Peer-2-Peer File Sharing CLI

The architecture of this program draws its inspiration from the bittorrent protocol

## Available chain of commands are as follows:
 1. List : To get the updated information of your peers in the Swarm.
 2. Terminate : To end your connection.
 3. Update : To update the data information available with you to the tracker.
 4. Fetch IpAddressOFPeer PortNumberOfPeer file/folderpath : To download the file/folder
 5. Reconnect : To reestablish connection with the Tracker.
 6: Read : To display current list of peers.
 7. All : To display command list.
 8. End : To exit the program.

 ## Steps to use
 1. Start the Tracker for the p2p network.
 `python Tracker/tracker.py`
 2. Start the Client application.
 `python Client/client.py`
 3. Fetch the list of peers in the swarm using the List command.
 4. Fetch the files/folder of your interest from the available peers with Fetch command.

 #### Exposure : Socket Programming, Multithreading, Python


 ###### Note : You can only download files/folders from peers only when the information of the shareable file/folderfrom the clients device gets registered with the tracker.
