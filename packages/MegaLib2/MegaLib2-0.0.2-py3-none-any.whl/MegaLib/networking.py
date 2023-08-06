import socket
from urllib.request import Request, urlopen
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def setup():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client
def connect(host,port):
    client.connect((host,port))
    return f"Connected to {host} at port {port}"
def host(port):
    client.bind((str(socket.gethostbyname(socket.gethostname())),port))
    client.listen()
    return f"Host started at port={port}"

def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

def getlocalip():
    return str(socket.gethostbyname(socket.gethostname()))

