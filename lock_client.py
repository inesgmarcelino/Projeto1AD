#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""
# Zona para fazer imports

import time
import sys
import pickle
from net_client import server

# Programa principal

if (len(sys.argv)==4):

    host = sys.argv[2]
    try:
        port = int(sys.argv[3])
        cliente = int(sys.argv[1])

    except ValueError:
        print('INVALID ARGUMENTS')
        exit()

    while True:
        comando = input('comando > ')
        comandoTokens = comando.split(' ')

        try:
            sock =server(host,port)
            socket = sock.connect()
        except OSError:
            print("CONNECTION WITH SOCKET-SERVER FAILED")
            exit()

        if comandoTokens[0] == 'SLEEP' or comandoTokens[0] == 'EXIT':
            if comandoTokens[0] == 'SLEEP':
                if len(comandoTokens)==2:
                    try:
                        time.sleep(int(comandoTokens[1]))
                        resposta = sock.send_receive(comando)
                        sock.close()
                    except ValueError:
                        resposta = 'INVALID ARGUMENTS'
                        sock.close()
                    
                elif len(comandoTokens) < 2:
                    resposta = 'MISSING ARGUMENTS'
                    
                else:
                    resposta = 'UNKNOWN COMMAND'
                    
            elif comandoTokens[0] == 'EXIT':
                exit()
        else:
            if comandoTokens[0] == 'LOCK':
                if len(comandoTokens) == 3:
                    comando += ' ' + str(cliente)
                    resposta = sock.send_receive(comando)

                elif len(comandoTokens) < 3:
                    resposta = 'MISSING ARGUMENTS'
                    
                else:
                    resposta = 'UNKNOWN COMMAND'

            elif comandoTokens[0] == 'UNLOCK':
                if len(comandoTokens) == 2:
                    comando += ' ' + str(cliente)
                    resposta = sock.send_receive(comando)
                    
                elif len(comandoTokens) < 2:
                    resposta = 'MISSING ARGUMENTS'
                    
                else:
                    resposta = 'UNKNOWN COMMAND'
            
            elif comandoTokens[0] == 'STATUS':
                if len(comandoTokens)==3:
                    resposta = sock.send_receive(comando)
        
                elif len(comandoTokens) < 3:
                    resposta = 'MISSING ARGUMENTS'
                    
                else:
                    resposta = 'UNKNOWN COMMAND'

            elif comandoTokens[0] == 'STATS':
                if len(comandoTokens)==2:
                    resposta = sock.send_receive(comando)
                
                elif len(comandoTokens) < 2:
                    resposta = 'MISSING ARGUMENTS'
                    
                else:
                    resposta = 'UNKNOWN COMMAND'

            elif comandoTokens[0] == 'PRINT':
                resposta = sock.send_receive(comando)

            else:
                resposta = 'UNKNOWN COMMAND'
             
        if comando:
            print('\n%s' % comando)
        print(resposta)
        sock.close()

        
else:
    print('MISSING ARGUMENTS')
