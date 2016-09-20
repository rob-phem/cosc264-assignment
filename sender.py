"""sets up the sender"""
import socket
import sys
import os.path
import struct
import select
MAGICNO = 0x497E
DATA = 0
ACK = 1


"""
looper which contiues to send packets until all are sent.
will resend those that arn't acknowleged as arrived.
"""
def looper(fname, sOut, sIn):
    count = 0
    sent = 0
    next_ = 0
    exitFlag = False
    readfile = open(fname, 'rb')
    
    while exitFlag == False:
        recieved = False
        data = readfile.read(512)
        n = len(data)
    
        if n == 0:
            header = struct.pack('!iiii', MAGICNO, DATA, next_, 0)
            exitFlag = True
            
        else:
            header = struct.pack('!iiii', MAGICNO, DATA, next_, n)
            
        packet = header + data
            
            
        while recieved == False:
            
            sOut.send(packet)
            sent += 1
            reply, _, _ = select.select([sIn], [], [], 1)
            
            if not reply and count <= 15:
                if n == 0:
                    count += 1
                continue
            if(count >= 15):
                readfile.close()
                sIn.close()
                sOut.close()
                
            rcvd = sIn.recv(2**16)
            
            try:
                fields = struct.unpack('!iiiis', rcvd)
            except:
                fields = struct.unpack('!iiii', rcvd[0:16])
            
            
            if fields[0] != MAGICNO or fields[1] != ACK or fields[2] != next_ or fields[3] != 0:
                continue
            
            else:
                next_ = 1 - next_ 
                if exitFlag == True:
                    readfile.close()
                    print(sent)
                    sys.exit()
                else:
                    recieved = True
                    
                    
def main():
    #create and bind sockets
    
    if 64000 > int(sys.argv[1]) > 1024 and 64000 > int(sys.argv[2]) > 1024:    
        sIn_port, sOut_port = int(sys.argv[1]), int(sys.argv[2])
        
        
    sIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    sIn.bind(("127.0.0.1", sIn_port))
    sOut.bind(("127.0.0.1", sOut_port))
    
    #create and connect channel port
    
    csi_port = int(sys.argv[3])
    
    sOut.connect(('127.0.0.1', csi_port))
    
    
    #read filename and checks if file exists
    
    fname = sys.argv[4]
    if os.path.isfile(fname) == False:
        sys.exit(0)
    looper(fname, sOut, sIn)

main()
