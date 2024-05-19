import socket # import
from os import system

def run():
    s = socket.socket()
    mode = input("Enter mode(send,accept,shell):")
    if mode != "shell":file = open(input("Enter file name:"),"+w",encoding="utf-8")
    ip = input("Enter IP: ")
    port = int(input("Enter port: "))
    s.connect((ip,port))
    s.send(mode.encode("utf-8"))
    if s.recv(1024) == "disagreed".encode("utf-8"):
        print("Disagreed")
        exit()
    print("agreed")
    print("Start transmission")
    try:
        if mode == "send":
            rdl = file.read()
            ca = 0
            if len(rdl) >= 1024:
                s.send(rdl[:1024].encode("utf-8"))
                del rdl[:1024]
                if len(rdl) == 0:
                    s.send(chr(6).encode("utf-8"))
                    exit()
            else:
                rdl += "\x06"
                s.send(rdl.encode("utf-8"))
                exit()
            if s.recv(1024) == "canceled":
                print("ERR:Transmission canceled by Server")
                exit()
        elif mode == "shell":
            s.send(input("passwd:").encode("utf-8"))
            if s.recv(1024).decode("utf-8") == "allowed":print("Permission allowed")
            else:
                print("Permission denied")
                exit()
            while True:
                pwd = system("pwd")
                buff = input(f"socket@{ip}:{pwd}$ ")
                s.send(buff.encode("utf-8"))
                if buff == "exit" or buff == "^D":
                    print("[exited]")
                    exit()
                while True:
                    recv = s.recv(1024).decode()
                    if recv != "\x06":
                        print(recv)
                        continue
                    break
        s.close()
        print("Transmission finish")
    except KeyboardInterrupt:
        print("ERR:Transmission canceled by User")
        s.send("canceled".encode("utf-8"))
        s.close()

run()