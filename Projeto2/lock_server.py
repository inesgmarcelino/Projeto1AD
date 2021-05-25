#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""

# Zona para fazer importação

import sys
from sock_utils import create_tcp_server_socket
from sock_utils import receive_all
from lock_pool import lock_pool
from lock_skeleton import Skeleton
import select
import struct
import pickle

###############################################################################

def recv_data(socket):
    size_bytes = receive_all(socket,4)
    size = struct.unpack('i',size_bytes)[0]
    msg_bytes = receive_all(socket,size)
    return msg_bytes

def send_data(socket,data):
    size_bytes = struct.pack('i',len(data))
    socket.sendall(size_bytes)
    socket.sendall(data)

# código do programa principal 

if (len(sys.argv)==6):

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
        n = int(sys.argv[3])
        k = int(sys.argv[4])
        y = int(sys.argv[5])

    except ValueError:
        print('INVALID ARGUMENTS')
        exit()
    
    try:
        sock = create_tcp_server_socket(host,port)
    except OSError:
        print('CONNECTION WITH SOCKET-SERVER FAILED')
        exit()

    socketList = [sock]
    skeleton = Skeleton(n,k,y)
    while True:
        try:
            R, W, X = select.select(socketList, [], [])
            for s in R: 
                if s is sock:
                    (conn_sock, (addr,port)) = sock.accept()
                    print('Novo cliente ligado desde %s:%d' % (addr,port))
                    socketList.append(conn_sock)
                else:
                    try:
                        msg = recv_data(s)
                        if msg:
                            resp = skeleton.processMessage(msg)
                            send_data(s,resp)
                        else: #DONT WORK... 
                            s.close()
                            socketList.remove(s)
                            print('Cliente fechou ligação')
                    except:
                        s.close()
                        socketList.remove(s)
                        print('Cliente fechou ligação')

        except select.error:
            print('MULTIPLEXING FAILED')

    sock.close()

else:
    print('MISSING ARGUMENTS')
        
