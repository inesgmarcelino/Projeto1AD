#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_pool.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""

# Zona para fazer importação

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
        segundos. Retorna True ou False.
        """
        if self.estado == 'UNLOCKED':
            self.estado = 'LOCKED'
            self.time = time.time() + time_limit
            self.clientLock = client_id
            self.qntLocks += 1
            return True
        else:
            if client_id == self.clientLock:
                self.qntLocks += 1
                self.time += time_limit
                return True
            else:
                return False

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
        Retorna True ou False.
        """
        if self.estado == 'LOCKED':
            if client_id == self.clientLock:
                self.estado = 'UNLOCKED'
                self.clientLock = -1
                return True
            else:
                return False
        else:
            return False

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna True ou False 
        ou Ellipsis. Se option for K, retorna <número de bloqueios feitos no 
        recurso>.
        """
        if option == 30:
            return self.estado
        else:
            return self.qntLocks

    def disable(self):
        """
        Coloca o recurso como desabilitdado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.estado = Ellipsis
        self.clientLock = -1

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = "R " + str(self.id) + " " + \
            str(self.estado) + " " + str(self.qntLocks)
        if self.estado == 'LOCKED':
            output += " " + str(self.clientLock) + " " + str(self.time)
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
        for i in range(0, N):
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
        for i in range(0, len(self.resources)):
            if self.resources[i].estado == 'LOCKED':
                if self.resources[i].time <= time.time():
                    if self.resources[i].qntLocks == self.blockMax:
                        self.resources[i].disable()
                        self.off += 1
                    else:
                        self.resources[i].release()
                    self.blocks -= 1

    def lock(self, resource_id, time_limit, client_id):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, durante
        time_limit segundos. Retorna True, False ou None.
        """
        end = [11]
        if resource_id < len(self.resources) and resource_id >= 0:
            if self.resources[resource_id].qntLocks < self.blockMax and self.blocks < self.blockNow:
                if self.resources[resource_id].estado == 'LOCKED':
                    result = self.resources[resource_id].lock(
                        client_id, time_limit)
                    self.free -= 1
                else:
                    result = self.resources[resource_id].lock(
                        client_id, time_limit)
                    self.free -= 1
                    self.blocks += 1

                end.append(result)
            else:
                end.append(False)
        else:
            end.append(None)

        return end

    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna True, False ou None.
        """
        end = [21]
        if resource_id < len(self.resources) and resource_id >= 0:
            result = self.resources[resource_id].unlock(client_id)
            self.blocks -= 1
            self.free += 1
            if self.resources[resource_id].qntLocks == self.blockMax:
                self.resources[resource_id].disable()
                self.off += 1

            end.append(result)
        else:
            end.append(None)

        return end

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna True, False,
        Ellipsis ou None. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou None.
        """
        if option == 30:
            end = [31]
        else:
            end = [41]
        if resource_id < len(self.resources) and resource_id >= 0:
            result = self.resources[resource_id].status(option)
            end.append(result)
        else:
            end.append(None)

        return end

    def stats(self, option):
        """
        Obtém o estado do serviço de exclusão mútua. Se option for Y, retorna 
        <número de recursos bloqueados atualmente>. Se option for N, retorna 
        <número de recursos disponíveis>. Se option for D, retorna 
        <número de recursos desabilitdados>
        """
        if option == 50:
            end = [51, self.blocks]
        elif option == 60:
            end = [61, self.free]
        else:
            end = [71, self.off]

        return end

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        end = [81]
        output = []
        for i in range(0, len(self.resources)):
            output.append(self.resources[i].__repr__())

        end.append('; '.join(output))
        return end
