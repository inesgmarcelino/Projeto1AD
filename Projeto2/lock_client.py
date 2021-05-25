#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_client.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""
# Zona para fazer imports

import time
import sys
from lock_stub import Stub

# Programa principal

if (len(sys.argv)==4):

    host = sys.argv[2]
    try:
        port = int(sys.argv[3])
        cliente = int(sys.argv[1])

    except ValueError:
        print('INVALID ARGUMENTS')
        exit()
    
    try:
        sock = Stub()
        sock.connect(host,port)
    except OSError:
        print("CONNECTION WITH SOCKET-SERVER FAILED")
        exit()

    while True:
        comando = input('comando > ')
        comandoTokens = comando.split(' ')
        
        if comando:
            if comando == 'EXIT':
                exit()
            else:
                if comandoTokens[0] == 'SLEEP':
                    if len(comandoTokens) == 2:
                        try:
                            time.sleep(int(comandoTokens[1]))
                            cmd = sock.sleep(int(comandoTokens[1]))
                            resposta = sock.send_receive(cmd)
                        except ValueError:
                            resposta = 'INVALID ARGUMENTS'
                        
                    elif len(comandoTokens) < 2:
                        resposta = 'MISSING ARGUMENTS'
                        
                    else:
                        resposta = 'UNKNOWN COMMAND'
            
                else:
                    if comandoTokens[0] == 'LOCK':
                        if len(comandoTokens) == 3:
                            cmd = sock.lock(int(comandoTokens[1]),int(comandoTokens[2]),cliente)
                            resposta = sock.send_receive(cmd)

                        elif len(comandoTokens) < 3:
                            resposta = 'MISSING ARGUMENTS'
                            
                        else:
                            resposta = 'UNKNOWN COMMAND'

                    elif comandoTokens[0] == 'UNLOCK':
                        if len(comandoTokens) == 2:
                            cmd = sock.unlock(int(comandoTokens[1]),cliente)
                            resposta = sock.send_receive(cmd)
                            
                        elif len(comandoTokens) < 2:
                            resposta = 'MISSING ARGUMENTS'
                            
                        else:
                            resposta = 'UNKNOWN COMMAND'
                    
                    elif comandoTokens[0] == 'STATUS':
                        if len(comandoTokens) == 3 and (comandoTokens[1] == 'R' or comandoTokens[1] == 'K'):
                            cmd = sock.status(comandoTokens[1],int(comandoTokens[2]))
                            resposta = sock.send_receive(cmd)
                
                        elif len(comandoTokens) < 3:
                            resposta = 'MISSING ARGUMENTS'
                            
                        else:
                            resposta = 'UNKNOWN COMMAND'

                    elif comandoTokens[0] == 'STATS':
                        if len(comandoTokens) == 2 and (comandoTokens[1] == 'Y' or comandoTokens[1] == 'N' or comandoTokens[1] == 'D'):
                            cmd = sock.stats(comandoTokens[1])
                            resposta = sock.send_receive(cmd)
                        
                        elif len(comandoTokens) < 2:
                            resposta = 'MISSING ARGUMENTS'
                            
                        else:
                            resposta = 'UNKNOWN COMMAND'

                    elif comandoTokens[0] == 'PRINT':
                        cmd = sock.print()
                        resposta = sock.send_receive(cmd)

                    else:
                        resposta = 'UNKNOWN COMMAND'
                    
                if cmd:
                    print(cmd)
                print(resposta)
                
    sock.disconnect()

        
else:
    print('MISSING ARGUMENTS')
