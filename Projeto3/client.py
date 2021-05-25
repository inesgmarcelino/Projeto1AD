#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 3 - client.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""

# Zona para fazer importação

import requests
import json

###############################################################################

BASE_URL ='http://localhost:5000/'
headers = {'Content-Type': 'application/vnd.collection+json'}

def erro():
    """
    Resquest para devolver erro BAD REQUEST quando o cliente introduz um comando desconhecido.
    """
    return requests.get(BASE_URL + '400', data=None, headers=headers)

###############################################################################
while True:
    comando = input('Pedido: ')
    cmdTokens = comando.split(' ')

    try:
        if cmdTokens[0] == 'CREATE':
            if len(cmdTokens) > 1:
                if cmdTokens[1] == 'UTILIZADOR':
                    if len(cmdTokens) == 4:
                        params = {'nome': cmdTokens[2], 'pass': cmdTokens[3]}
                        r = requests.post(
                            BASE_URL + 'utilizadores/create', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()
                        
                elif cmdTokens[1] == 'ARTISTA':
                    if len(cmdTokens) == 3:
                        params = {'id_spotify': cmdTokens[2]}
                        r = requests.post(
                            BASE_URL + 'artistas/create', data=json.dumps(params), headers=headers)
                    
                    else:
                        r = erro()

                elif cmdTokens[1] == 'ALBUM':
                    if len(cmdTokens) == 3:
                        params = {'id_spotify': cmdTokens[2]}
                        r = requests.post(
                            BASE_URL + 'albuns/create', data=json.dumps(params), headers=headers)
                        
                    else:
                        r = erro()

                else:
                    if len(cmdTokens) == 4:
                        params = {'id_user': int(cmdTokens[1]), 'id_album': int(cmdTokens[2]), 'aval': cmdTokens[3]}
                        r = requests.post(
                            BASE_URL + 'albuns/create', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()
            
            else:
                r = erro()

        elif cmdTokens[0] == 'READ':
            if len(cmdTokens) > 1:
                if cmdTokens[1] == 'ALL':
                    if len(cmdTokens) == 3:
                        if cmdTokens[2] == 'UTILIZADORES':
                            r = requests.get(
                                BASE_URL + 'utilizadores/search', data=None, headers=headers)
                    
                        elif cmdTokens[2] == 'ARTISTAS':
                            r = requests.get(
                                BASE_URL + 'artistas/search', data=None, headers=headers)
                
                        elif cmdTokens[2] == 'ALBUNS':
                            r = requests.get(
                                BASE_URL + 'albuns/search', data=None, headers=headers)

                        else:
                            r = erro()

                    elif len(cmdTokens) == 4:
                        if cmdTokens[2] == 'ALBUNS_A' or cmdTokens[2] == 'ALBUNS_U' or cmdTokens[2] == 'ALBUNS':
                            if cmdTokens[2] == 'ALBUNS_A':
                                params = {'id_artista': int(cmdTokens[3])}

                            elif cmdTokens[2] == 'ALBUNS_U':
                                params = {'id_user': int(cmdTokens[3])}

                            else:
                                params = {'aval': cmdTokens[3]}

                            r = requests.get(
                                BASE_URL + 'albuns/search', data=json.dumps(params), headers=headers)

                        else:
                            r = erro()

                    else:
                        r = erro()

                elif cmdTokens[1] == 'UTILIZADOR':
                    if len(cmdTokens) == 3:
                        params = {'id_user': int(cmdTokens[2])}
                        r = requests.get(
                            BASE_URL + 'utilizadores/search', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                elif cmdTokens[1] == 'ARTISTA':
                    if len(cmdTokens) == 3:
                        params = {'id_artista': int(cmdTokens[2])}
                        r = requests.get(
                            BASE_URL + 'artistas/search', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                elif cmdTokens[1] == 'ALBUM':
                    if len(cmdTokens) == 3:
                        params = {'id_album': int(cmdTokens[2])}
                        r = requests.get(
                            BASE_URL + 'albuns/search', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                else:
                    r = erro()
            
            else:
                r = erro()

        elif cmdTokens[0] == 'DELETE':
            if len(cmdTokens) > 1:
                if cmdTokens[1] == 'ALL':
                    if len(cmdTokens) == 3:
                        if cmdTokens[2] == 'UTILIZADORES':
                            r = requests.delete(
                                BASE_URL + 'utilizadores/delete', data=None, headers=headers)  

                        elif cmdTokens[2] == 'ARTISTAS':
                            r = requests.delete(
                                BASE_URL + 'artistas/delete', data=None, headers=headers)

                        elif cmdTokens[2] == 'ALBUNS':
                            r = requests.delete(
                                BASE_URL + 'albuns/delete', data=None)

                        else:
                            r = erro()

                    elif len(cmdTokens) == 4:
                        if cmdTokens[2] == 'ALBUNS_A' or cmdTokens[2] == 'ALBUNS_U' or cmdTokens[2] == 'ALBUNS':
                            if cmdTokens[2] == 'ALBUNS_A':
                                params = {'id_artista': int(cmdTokens[3])}

                            elif cmdTokens[2] == 'ALBUNS_U':
                                params = {'id_user': int(cmdTokens[3])}

                            else:
                                params = {'aval': cmdTokens[3]}

                            r = requests.delete(
                                BASE_URL + 'albuns/delete', data=json.dumps(params), headers=headers)

                        else:
                            r = erro()

                    else:
                        r = erro()

                elif cmdTokens[1] == 'UTILIZADOR':
                    if len(cmdTokens) == 3:
                        params = {'id_user': int(cmdTokens[2])}
                        r = requests.delete(
                            BASE_URL + 'utilizadores/delete', data=json.dumps(params), headers=headers)
                    
                    else:
                        r = erro()

                elif cmdTokens[1] == 'ARTISTA':
                    if len(cmdTokens) == 3:
                        params = {'id_artista': int(cmdTokens[2])}
                        r = requests.delete(
                            BASE_URL + 'artistas/delete', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                elif cmdTokens[1] == 'ALBUM':
                    if len(cmdTokens) == 3:
                        params = {'id_album': int(cmdTokens[2])}
                        r = requests.delete(
                            BASE_URL + 'albuns/delete', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                else:
                    r = erro()
            
            else:
                r = erro()

        elif cmdTokens[0] == 'UPDATE':
            if len(cmdTokens) > 1:
                if cmdTokens[1] == 'UTILIZADOR':
                    if len(cmdTokens) == 4:
                        params = {'id_user': int(cmdTokens[2]), 'pass': cmdTokens[3]}
                        r = requests.put(
                            BASE_URL + 'utilizadores/update', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                elif cmdTokens[1] == 'ALBUM':
                    if len(cmdTokens) == 5:
                        params = {'id_album': int(cmdTokens[2]), 'aval': cmdTokens[3], 'id_user': int(cmdTokens[4])}
                        r = requests.put(
                            BASE_URL + 'albuns/update', data=json.dumps(params), headers=headers)

                    else:
                        r = erro()

                else:
                    r = erro()

            else: 
                r = erro()

        else:
            r = erro()

        print(r.status_code, r.reason)
        print('***')
        if r.status_code != 204 :
            print(r.content.decode())
        print('***')
        print(r.headers)
        print('***')
    
    except ValueError:
        print('Argumentos inválidos.')

    except TypeError:
        print('Incapaz de realizar a serialização dos dados inseridos.')

    except requests.exceptions.RequestException as e:
        raise exit()
