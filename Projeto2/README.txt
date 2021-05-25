Aplicações distribuídas - Projeto 2 - README.txt
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991

Neste projeto 2, foram feitas alterações em quase todos os ficheiros
e ainda adicionados mais 2 (lock_stub.py e lock_skeleton.py). No ficheiro lock_client.py
as alterações que feitas foram apenas adaptações para a implementação da classe Stub do
ficheiro lock_stub.py. No ficheiro lock_server.py foram feitas grandes alterações devida 
á implementação da classe Skeleton do ficheiro lock_skeleton.py, sendo assim as classes
lock_pool e resource_lock agora estão num ficheiro á parte lock_pool.py, ou seja, no ficheiro
lock_client apenas está implementada a inicialização da class Skeleton do ficheiro 
lock_skeleton.py e a implentação do módulo select para suporte de múltiplos clientes, foi
ainda alterada o método send_data e adicionada um método send_data.
No ficheiro sock_utils.py foi melhorado o método receive_all para mensagens fragmentadas.
Os únicos ficheiros que não sofreram qualquer alteração foram net_client.py e sock_utils.py.

A única dificuldade que encontramos e não conseguimos resolver foi o facto de quando fazemos
EXIT no cliente, não aparece 'Cliente fechou ligação' automaticamente, só se fizermos Ctrl+c 
no servidor. Tentamos ver de várias formas e não conseguimos.
