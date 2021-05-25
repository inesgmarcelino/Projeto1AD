#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_stub.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""
# Zona para fazer imports

from net_client import server

# Programa principal

class Stub:
    def __init__(self):
        """
        Define atributo sock.
        """
        self.sock = None

    def connect(self,host,port):
        """
        Chama funções para estabelecer a ligação ao servidor especificado.
        """
        self.sock = server(host,port)
        self.sock.connect()

    def disconnect(self):
        """
        Chama função para terminar a ligação ao servidor.
        """
        self.sock.close()

    def send_receive(self,comando):
        """
        Chama função para enviar os dados do comando e receber a resposta.
        """
        resp = self.sock.send_receive(comando)
        return resp

    def sleep(self,time):
        """
        Cria comando sleep.
        """
        cmd = ['SLEEP', time]
        return cmd

    def lock(self,resource,time,client):
        """
        Cria comando lock.
        """
        cmd = [10,resource,time,client]
        return cmd

    def unlock(self,resource,client):
        """
        Cria comando unlock.
        """
        cmd = [20,resource,client]
        return cmd

    def status(self,option,resource):
        """
        Cria comando status.
        """
        if option == 'R':
            cmd = [30]
        else:
            cmd = [40]
        
        cmd.append(resource)
        return cmd

    def stats(self,option):
        """
        Cria comando stats.
        """
        if option == 'Y':
            cmd = [50]
        elif option == 'N':
            cmd = [60]
        else:
            cmd = [70]
        
        return cmd

    def print(self):
        """
        Cria comando print.
        """
        cmd = [80]
        return cmd