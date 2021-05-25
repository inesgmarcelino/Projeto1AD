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
import struct

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
        try:
            data_bytes = pickle.dumps(data,-1)
            size_bytes = struct.pack('i',len(data_bytes))
            self.sock.sendall(size_bytes)
            self.sock.sendall(data_bytes)
            #receive
            # r = receive_all(self.sock,1024)
            size_bytes = receive_all(self.sock,4)
            if size_bytes:
                size = struct.unpack('i',size_bytes)[0]
                resp_bytes = receive_all(self.sock,size)
                resposta = pickle.loads(resp_bytes)
                return resposta

        except pickle.PickleError:
            print('PICKLING FAILED')
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
