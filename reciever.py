"""RECIEVER"""
#!/usr/bin/python
import socket
import sys
import select
import struct
from struct import Struct
MAGICNUM = 0x497E
DATA = 0
ACK = 1
struct = Struct("!iiii")
struct1 = Struct("!iiiis")
def looper(socIn, socOut, writeFile):
    expected = 0
    flag = True
    while flag == True:
        
        recvPack = socIn.recv(2**10)
        fields = struct.unpack(recvPack[:struct.size])
        data = recvPack[struct.size:]
        if fields[0] != MAGICNUM:
            continue
        if fields[1] != 0:
            continue
        if fields[2] != expected:
            ack_package = struct.pack(MAGICNUM, ACK, fields[2], 0)
            socOut.send(ack_package)
        else:
            ack_package = struct1.pack(MAGICNUM, ACK, fields[2], 0, b"")
            socOut.send(ack_package)
            expected = 1 - expected
            if fields[3] > 0:
                writeFile.write(data)
            else:
                writeFile.close()
                flag = False
                
            
           
            
        
    
def main():
    rIn_port = int(sys.argv[1])
    rOut_port = int(sys.argv[2])
    if isinstance(rIn_port,int) != True or isinstance(rOut_port, int) != True:
        sys.exit(0)
    if (1024 > rIn_port > 64000 or 1024 > rOut_port > 64000):
        sys.exit(0)
    crIn_port = int(sys.argv[3])
        
    fileName = sys.argv[4]
        
    rIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    writeFile = open(fileName, "xb")
    rIn.bind(("127.0.0.1", rIn_port))
    rOut.bind(("127.0.0.1", rOut_port))
    rOut.connect(("127.0.0.1", crIn_port))
    
    looper(rIn, rOut, writeFile)
    rIn.close()
    rOut.close()
    sys.exit(0)
    
main()