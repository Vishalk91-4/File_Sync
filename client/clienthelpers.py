import os
import json
import socket
import threading

def initializer(client_socket,port):
    cmd = "Update@"+f'{port}@' + directory_tree_as_json()
    a = False
    for i in range(1,11):
        client_socket.sendall(cmd)
        response = ""
        while True:
            data = client_socket.recv(1024)
            if not data: 
                break
            response+=data.decode("utf-8")
        if response.strip() == "Data successfully published":
            a = True
            break
    return a

def publish_peer_info(json_info):
    data = json.loads(json_info)
    with open('peers.json', 'w') as f:
        json.dump(data, f)
    f.close()

def print_peer_info():
    with open('peers.json', 'r') as f:
        data = json.loads(f)
    print(json.dump(data))
    f.close()

def folder_to_dict(dirpath):
    return {
        'name' : os.path.dirname(dirpath),
        'type' : 'folder',
        'path' : dirpath,
        'children' : []
    }

def file_to_dict(filepath):
    return {
        'name' : os.path.basename(filepath),
        'type' : 'file',
        'path' : filepath
    }

def tree_to_dict(rootdir):
    folder_dict = folder_to_dict(rootdir)
    for rootpath, folders, files in os.walk(rootdir):
        for file in files:
            folder_dict['children'].append(file_to_dict(os.path.join(rootpath,file)))
        for folder in folders:
            folder_dict['children'].append(tree_to_dict(os.path.join(rootpath,folder)))
def directory_tree_as_json(rootdir = "Client"):
    json_dict = []
    for rootpath, folders, files in os.walk(rootdir):
        for file in files:
            json_dict.append(file_to_dict(os.path.join(rootpath,file)))
        for folder in folders:
            json_dict.append(tree_to_dict(os.path.join(rootpath,folder)))

    return json.dump(json_dict)


        