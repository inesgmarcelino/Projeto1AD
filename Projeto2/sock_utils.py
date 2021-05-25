#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - sock_utils.py
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

def receive_all(socket,length):
    data = b''
    while (len(data) < length):
        more = socket.recv(length - len(data))
        data += more
    return data