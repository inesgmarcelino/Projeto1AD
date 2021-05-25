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
import time
import pickle

###############################################################################

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.id = resource_id
        self.estado = 'UNLOCKED'
        self.qntLocks = 0
        self.clientLock = -1
        self.time = None

    def lock(self, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK.
        """
        if self.estado == 'UNLOCKED':
            self.estado = 'LOCKED'
            self.time = time.time() + time_limit
            self.clientLock = client_id
            self.qntLocks += 1
            return 'OK' 
            
        else:
            if client_id == self.clientLock:
                self.qntLocks += 1
                self.time += time_limit
                return 'OK'
            else:
                return 'NOK'

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.estado = 'UNLOCKED'
        self.clientLock = -1
        self.time = None

    def unlock(self, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.
        """
        if self.estado == 'LOCKED':
            if client_id == self.clientLock:
                self.estado = 'UNLOCKED'
                self.clientLock = -1
                return 'OK'
            else:
                return 'NOK'
        else:
            return 'NOK'

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna LOCKED ou UNLOCKED 
        ou DISABLED. Se option for K, retorna <número de bloqueios feitos no 
        recurso>.
        """
        if option == 'R':
            return self.estado
        else:
            return self.qntLocks
   
    def disable(self):
        """
        Coloca o recurso como desabilitdado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.estado = 'DISABLE'
        self.clientLock = -1

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = "R " + str(self.id) + " " + str(self.estado) + " " + str(self.qntLocks) + " "
        if self.estado == 'LOCKED':
            output += str(self.clientLock) + " " + str(self.time)
        return output

###############################################################################

class lock_pool:
    def __init__(self, N, K, Y):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe. Define K, o número máximo 
        de bloqueios permitidos para cada recurso. Ao atingir K, o recurso fica 
        desabilitdado. Define Y, o número máximo permitido de recursos 
        bloqueados num dado momento. Ao atingir Y, não é possível realizar mais 
        bloqueios até que um recurso seja libertado.
        """
        self.resources = []
        for i in range(0,N):
            self.resources.append(resource_lock(i))
        self.blockMax = K
        self.blockNow = Y
        self.blocks = 0
        self.free = N
        self.off = 0
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for i in range(0,len(self.resources)):
            if self.resources[i].estado == 'LOCKED':
                if self.resources[i].time <= time.time():
                    self.resources[i].release()
                    self.blocks -= 1

    def lock(self, resource_id, time_limit, client_id):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, durante
        time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id < len(self.resources) and resource_id >= 0:
            if self.resources[resource_id].qntLocks < self.blockMax and self.blocks < self.blockNow:
                if self.resources[resource_id].estado == 'LOCKED':
                    result = self.resources[resource_id].lock(client_id,time_limit)
                    self.free -= 1
                else:
                    result = self.resources[resource_id].lock(client_id,time_limit)
                    self.free -= 1
                    self.blocks += 1
                return result
            else:
                return 'NOK'
        else:
            return 'UNKNOWN RESOURCE'

    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id < len(self.resources) and resource_id >= 0:
            result = self.resources[resource_id].unlock(client_id)
            self.blocks -= 1
            self.free += 1
            if self.resources[resource_id].qntLocks == self.blockMax:
                self.resources[resource_id].disable()
                self.off += 1
            return result
        else:
            return 'UNKNOWN RESOURCE'

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou UNKNOWN RESOURCE.
        """
        if resource_id < len(self.resources) and resource_id >= 0:
            if option == 'R' or option == 'K':
                result = self.resources[resource_id].status(option)
                return result
        else:
            return 'UNKNOWN RESOURCE'

    def stats(self, option):
        """
        Obtém o estado do serviço de exclusão mútua. Se option for Y, retorna 
        <número de recursos bloqueados atualmente>. Se option for N, retorna 
        <número de recursos disponíveis>. Se option for D, retorna 
        <número de recursos desabilitdados>
        """
        if option == 'Y':
            return self.blocks
        elif option == 'N':
            return self.free
        elif option == 'D':
            return self.off

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        for i in range(0,len(self.resources)):
            output += "\n" + self.resources[i].__repr__()
        return output

###############################################################################

# código do programa principal

def send_data(socket,r):
    """
    Envia dados para o cliente a resposta ao seu pedido
    """
    resposta = pickle.dumps(r,-1)
    socket.sendall(resposta)
    print(r)

##############################################################    

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
    
    resources = lock_pool(n,k,y)
    try:
        sock = create_tcp_server_socket(host,port)
    except OSError:
        print('CONNECTION WITH SOCKET-SERVER FAILED')
        exit()

    while True:
        (conn_sock, (addr,port)) = sock.accept()

        print('ligado a %s no porto %s' % (addr,port))
        msg = receive_all(conn_sock,1024)
        if msg:
            obj = pickle.loads(msg) 
            msgTokens = obj.split(' ')
            print(obj)

            resources.clear_expired_locks()
            try:
                if msgTokens[0] == 'LOCK':
                        r = resources.lock(int(msgTokens[1]),int(msgTokens[2]),int(msgTokens[3]))
                        send_data(conn_sock,r)

                elif msgTokens[0] == 'UNLOCK':
                        r = resources.unlock(int(msgTokens[1]),int(msgTokens[2]))
                        send_data(conn_sock,r)

                elif msgTokens[0] == 'STATUS':
                        r = resources.status(msgTokens[1],int(msgTokens[2]))
                        send_data(conn_sock,r)
                   
                elif msgTokens[0] == 'STATS':
                        r = resources.stats(msgTokens[1])
                        send_data(conn_sock,r)

                elif msgTokens[0] == 'PRINT':
                    r = resources.__repr__()
                    send_data(conn_sock,r)

                elif msgTokens[0] == 'SLEEP':
                        r = 'CLIENT SLEPT FOR '+ msgTokens[1] + ' SECONDS'
                        send_data(conn_sock,r)

            except ValueError:
                r = 'INVALID ARGUMENTS'
                send_data(conn_sock,r)

    sock.close()

else:
    print('MISSING ARGUMENTS')
        
