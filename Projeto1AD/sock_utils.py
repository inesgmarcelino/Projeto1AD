#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""
import socket

def create_tcp_server_socket(address,port):
    """
    Cria uma tcp socket de servidor
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((address,port))
    sock.listen(1)
    return sock

def create_tcp_client_socket(address,port):
    """
    Cria uma tcp socket de cliente
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address,port))
    return sock

def receive_all(socket,lenght):
    """
    Recebe dados a partir da socket
    """
    dados = socket.recv(lenght)
##    dados = ''
##    while len(dados) < lenght:
##        novosDados = socket.recv(lenght-(len(dados)))
##        if not novosDados:
##            raise EOFError('socket closed %d bytes into a %d-byte message')
##        dados += novosDados
    return dados
