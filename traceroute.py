from socket import *
import os
import sys
import struct
import time
import select
import binascii
import pandas as pd

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 60
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    #Fill in start
    myChecksum = 0
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    header = struct.pack("bbHh", ICMP_ECHO_REQUEST, 0, myChecksum, 1)
    data = struct.pack("d", time.time())
    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
    myChecksum = checksum(header + data)

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)


    header = struct.pack("bbHh", ICMP_ECHO_REQUEST, 0, myChecksum, 1)
    
    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end

    # So the function ending should look like this

    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    df = pd.DataFrame(columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
    destAddr = gethostbyname(hostname)
    
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
 
            #Fill in start
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp) # Make a raw socket named mySocket
            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    #Fill in start
                    stats = [[ttl, tries, destAddr, hostname, "timeout"]]
                    stats_frame = pd.DataFrame(stats, columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
                    df = pd.concat([df,stats_frame], ignore_index=True)
                    #append df to your dataframe including hop #, try #, and "timeout" responses as required by the acceptance criteria
                    #print (df)
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    #Fill in start
                    stats = [[ttl, tries, destAddr, hostname, "timeout"]]
                    stats_frame = pd.DataFrame(stats, columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
                    df = pd.concat([df,stats_frame], ignore_index=True)
                    #append df to your dataframe including hop #, try #, and "timeout" responses as required by the acceptance criteria
                    print (df)
                    #Fill in end
            except Exception as e:
                print (e) # uncomment to view exceptions
                continue

            else:
                TTL = recvPacket[8]
                ICMP_HEADER = recvPacket[20:28]
                types, resCode, checkSum, packetID, seq = struct.unpack("bbHHh", ICMP_HEADER)#Fetch the icmp type from the IP packet
                
                verbalTypes = {
                    11: "TTL Exceeded",
                    3: "Destination Unreachable",
                    0: "Success"
                }
                
                try: #try to fetch the hostname of the router that returned the packet - don't confuse with the hostname that you are tracing
                    #Fill in start
                    hopHostname = gethostbyaddr(addr[0])
                    #Fill in end
                except herror:   #if the router host does not provide a hostname use "hostname not returnable"
                    #Fill in start
                    hopHostname = "hostname not returnable"
                    #Fill in end

                if types == 11:
                    bytes = struct.calcsize("d")
                    #timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    stats = [[ttl, tries, destAddr, hopHostname, verbalTypes[types]]]
                    stats_frame = pd.DataFrame(stats, columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
                    df = pd.concat([df,stats_frame], ignore_index=True)
                    #Fill in end
                elif types == 3:
                    bytes = struct.calcsize("d")
                    #timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    stats = [[ttl, tries, destAddr, hopHostname, verbalTypes[types]]]
                    stats_frame = pd.DataFrame(stats, columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
                    df = pd.concat([df,stats_frame], ignore_index=True)
                    #You should update your dataframe with the required column field responses here
                    #Fill in end
                elif types == 0:
                    bytes = struct.calcsize("d")
                    #timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    stats = [[ttl, tries, destAddr, hopHostname, verbalTypes[types]]]
                    stats_frame = pd.DataFrame(stats, columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
                    df = pd.concat([df,stats_frame], ignore_index=True)
                    #You should update your dataframe with the required column field responses here
                    #Fill in end
                    return df
                else:
                    #Fill in start
                    stats = [[ttl, tries, destAddr, hopHostname, "ERROR"]]
                    stats_frame = pd.DataFrame(stats, columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
                    df = pd.concat([df,stats_frame], ignore_index=True)
                    #If there is an exception/error to your if statements, you should append that to your df here
                    #Fill in end
                break
    return df

if __name__ == '__main__':
    get_route("google.co.il")