#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_skeleton.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""
# Zona para fazer imports

import pickle
from lock_pool import lock_pool

# Programa principal


class Skeleton:
    def __init__(self, n, k, y):
        """
        Inicializa o conjunto dos recursos existentes no servidor.
        """
        self.resources = lock_pool(n, k, y)

    def processMessage(self, cmd):
        """
        Processa o pedido do cliente.
        """
        self.resources.clear_expired_locks()
        pedido = self.bytesToList(cmd)
        print(pedido)
        if pedido[0] == 10:
            resp = self.lock(pedido[1], pedido[2], pedido[3])

        elif pedido[0] == 20:
            resp = self.unlock(pedido[1], pedido[2])

        elif pedido[0] == 30 or pedido[0] == 40:
            resp = self.status(pedido[0], pedido[1])

        elif pedido[0] == 50 or pedido[0] == 60 or pedido[0] == 70:
            resp = self.stats(pedido[0])

        elif pedido[0] == 80:
            resp = self.print()

        elif pedido[0] == 'SLEEP':
            resp = ['SLEPT', pedido[1]]

        print(resp)
        resposta = self.listToBytes(resp)
        return resposta

    def lock(self, resource, time, client):
        """
        Acede á estrutura de dados para processar pedido de lock.
        """
        return self.resources.lock(resource, time, client)

    def unlock(self, resource, client):
        """
        Acede á estrutura de dados para processar pedido de unlock.
        """
        return self.resources.unlock(resource,client)

    def status(self,option,resource):
        """
        Acede á estrutura de dados para processar pedido de status.
        """
        return self.resources.status(option,resource)

    def stats(self,option):
        """
        Acede á estrutura de dados para processar pedido de stats.
        """
        return self.resources.stats(option)

    def print(self):
        """
        Acede á estrutura de dados para processar pedido de print.
        """
        return self.resources.__repr__()

    def bytesToList(self,msg_bytes):
        """
        Desserializa a mensagem. 
        """
        try:
            msg = pickle.loads(msg_bytes)
            return msg

        except pickle.PickleError:
            print('PICKLING FAILED')

    def listToBytes(self,resp):
        """
        Serializa a mensagem. 
        """
        try:
            resp_bytes = pickle.dumps(resp,-1)
            return resp_bytes

        except pickle.PickleError:
            print('PICKLING FAILED')
