"""sets up the channel"""
import sys 
import select
import socket
import struct
import random
MAGICNUM = 0x497E
"""
imitates packages being lost as data is sent across a network.

"""
def looper(csi_sock, cso_sock, cri_sock, cro_sock, prob):
    while True:
        inputReady,_,_ = select.select([csi_sock, cri_sock],[],[])
        for socket in inputReady:
            recevPack = socket.recv(2**10)
            print(recevPack)
            check = struct.unpack('!iiii', recevPack[0:16])
            if (check[0] != MAGICNUM):
                continue
            if (random.random() < prob):
                continue
            if socket == csi_sock:
                cro_sock.send(recevPack)
            else:
                cso_sock.send(recevPack)
                


def main():
    
    csi_port = int(sys.argv[1])
    cso_port = int(sys.argv[2])
    cri_port = int(sys.argv[3])
    cro_port = int(sys.argv[4])
    channelports = [csi_port, cso_port, cri_port, cro_port]
    for i in channelports:  #checks values are in acceptable range
            if 64000 < i < 2024:
                sys.exit(0)
                
    sIn_port = int(sys.argv[5])
    rIn_port = int(sys.argv[6])
    
    if 1 > float(sys.argv[7]) >= 0:    #checks value in expected range
            pack_loss = float(sys.argv[7])
    else:
        sys.exit(0)
    sIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sIn.bind(('127.0.0.1',csi_port))
    
    sOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sOut.bind(('127.0.0.1',cso_port))
    sOut.connect(('127.0.0.1',sIn_port))
    
    rIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rIn.bind(('127.0.0.1',cri_port))
    
    rOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rOut.bind(('127.0.0.1',cro_port)) 
    rOut.connect(('127.0.0.1',rIn_port))
    print(rIn_port)
    
    looper(sIn, sOut, rIn, rOut, pack_loss)
    



main()
