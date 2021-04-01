# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""

# zona para fazer importação

from sock_utils import create_tcp_client_socket
import pickle
from sock_utils import receive_all

# definição da classe server 

class server:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.host = address
        self.port = port
        self.sock = None
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        self.sock = create_tcp_client_socket(self.host, self.port)
        return self.sock

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        #send
        msg = pickle.dumps(data,-1)
        self.sock.sendall(msg)
        #receive
        r = receive_all(self.sock,1024)
        if r:
            resposta = pickle.loads(r)
            return resposta
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
