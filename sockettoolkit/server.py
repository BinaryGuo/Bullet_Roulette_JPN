from socket import socket # import
from json import load,dump
from os import system
from os.path import dirname
from argparse import ArgumentParser
import sys

def configure():
    print("ST server configurator")
    log = open("log.dat","rb")
    config = load(open("config.json","w+"))
    while True:
        if int(input("Enter adminstrator's password to access config:")).to_bytes(8,"big") == log.read(8):break
        else:print("permission denind")
    while True:
        mode = input("Enter option(ask config,clean log,white list,black list,exit):")
        if mode == "exit":
            print("configurator SHUTDOWN")
            dump(config,open("config.json","w",encoding="utf-8"),indent=2)
            exit()
        elif mode == "ask config":
            config[0] = not config[0]
            print("ask config is now " + config[0])
        elif mode == "white list":
            print("white list:\n" + config[1])
            while True:
                op = input("Enter operation(add,remove,exit):")
                if op == "add":config[1].append(op[4:])
                elif op == "exit":break
                elif op == "remove":config[1].remove(op[7:])
                else :print("Operation Error")
        elif mode == "black list":
            print("black list:\n" + config[2])
            while True:
                op = input("Enter operation(add,remove,exit):")
                if op == "add":config[2].append(op[4:])
                elif op == "exit":break
                elif op == "remove":config[2].remove(op[7:])
                else :print("Operation Error")
        elif mode == "clean log":
            if input("###Please do not clean logs unless necessary###\nAre you sure you want to clean logs(y,n)?") == 'y':
                logs = open("log.dat","wb")
                logs.write(log.read(8))

def accept():
    global trans
    trans = True
    while True:
        buff = sw.recv(1024).decode("utf-8")
        if buff[-1] == "\x06":
            file.write(buff[:-1])
            break
        elif buff == "canceled":
            print("ERR:Transmission canceled by Client")
        file.write(buff)
    sw.close()
    trans = False

def send():
    pass

def shell():
    global trans
    if input("Set passwd: ") == sw.recv(1024).decode("utf-8"):
        sw.send("allowed".encode("utf-8"))
        print("Permission allowed")
    else:
        sw.send("denied".encode("utf-8"))
        print("Permission denied")
        return
    trans = True
    while True:
        buff = sw.recv(1024).decode("utf-8")
        if buff == "exit":
            print("exited")
            return
        print(buff)
        file.write(buff + "\nreturn:")
        content.clear()
        print(content)
        system(buff)
        print(content)
        for con in content:
            file.write(con + "\n")
        for con in content:
            sw.send(con.encode())
        print("okya")
        sw.send("\x06".encode())
        print("ookk")
content = []
class InterceptSTD():
    def __init__(self):
        self.stdoutbak = sys.stdout
        sys.stdout = self
        sys.stderr = self

    def write(self,info) -> None:
       self.stdoutbak.write(info) #可以将信息再输出到原有标准输出，在定位问题时比较有用
       content.append(info) # "awa:",
    
    def flush(self):self.stdoutbak.flush()
mystd = InterceptSTD()

parse = ArgumentParser()
parse.add_argument("-a",required=False,type=str)
parse.add_argument("-f",required=False,type=str)
parse.add_argument("-p",required=True,type=int)
args = parse.parse_args()
if args.f == "config":configure()
s = socket() # init socket
#config = load(open(f"{dirname(__file__)}/config.json","r",encoding="utf-8")) # load config
config = [False,[],[]]
file = open(dirname(__file__) + "/" + args.f,"a",encoding="utf-8")
trans = False
log = open(f"{dirname(__file__)}/log.dat","+ab")
s.bind((args.a,args.p)) # bind this ip
s.listen(1) # only listen 1

while True:
    try:
        print("Waiting connection...")
        sw,addr = s.accept() # connect
        print("Connection from:",addr) # print ip
        mode = sw.recv(1024).decode("utf-8")
        if addr in config[2]:
            sw.send("black list".encode("utf-8"))
            sw.close()
            print("black list")
        elif addr not in config[1] or config[0]:
            if input(f"Mode:{mode},do you agree(y,n)?: ") == "n":
                print("Disagreed")
                sw.send("disagreed".encode("utf-8"))
                sw.close()
                log.write((str(addr) + str(args.p)).encode(""))
                log.write(args.p.to_bytes(1,"big"))
                #d = 0
                #log.write(d.to_bytes(1))
                continue
        sw.send("agreed".encode("utf-8"))
        print("Start transmission")
        if mode == "send":accept()
        elif mode == "accept":send()
        elif mode == "shell":shell()
        else:print("ERR:Mode Error")
        print("Transmission finish")
    except BrokenPipeError:
        print("ERR:Client abnormal quit")
    except KeyboardInterrupt:
        if trans == True:
            print("ERR:Transmission canceled by User")
            sw.send("canceled".encode("utf-8"))
            sw.close()
        else :
            print("SHUTDOWN")
            s.close()
            file.close()
            exit()
