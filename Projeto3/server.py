#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 3 - server.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""

# Zona para fazer importação

import sqlite3
import requests
import json
from flask import Flask, request, make_response

###############################################################################

# API
BASE_URL = 'https://api.spotify.com/v1/'

# TOKEN


def token():
    CLIENT_ID = '8c7da52fbb8a4ce182838285ccfaecc2'
    CLIENT_SECRET = 'a88227dd8b4f4cf3ba5277ee460e0e68'

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    authResp = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    authresponse = authResp.json()
    accessToken = authresponse['access_token']

    return {'Authorization': 'Bearer {token}'.format(token=accessToken)}

# CONNECTION


def get_db_connection():
    conn = sqlite3.connect('RateAlbums.db')
    return conn


# RESPONSE HEADER
headers = {'Content-Type': 'application/vnd.collection+json'}

app = Flask(__name__)

# UTILIZADORES

# PESQUISA


@app.route('/utilizadores/search', methods=['GET'])
def searchU():
    conn = get_db_connection()
    if not request.data:
        query = conn.execute('SELECT * FROM utilizadores').fetchall()
        if len(query) != 0:
            lines = []
            for i in range(len(query)):
                id_user = query[i][0]
                nome = query[i][1]
                senha = query[i][2]

                lines.append('ID: %s\nNome: %s\nSenha: %s' %
                             (id_user, nome, senha))

            res = '\n--- ---\n'.join(tuple(lines))
            code = 200

        else:
            res = ''  # Não há resultados
            code = 204

    else:
        data = json.loads(request.data)
        query = conn.execute('SELECT id FROM utilizadores').fetchall()
        ids = []
        for i in range(len(query)):
            ids.append(query[i][0])

        id_user = data['id_user']

        if id_user in ids:
            query = conn.execute(
                'SELECT * FROM utilizadores WHERE id = ' + str(id_user)).fetchall()
            lines = []
            for i in range(len(query)):
                id_user = query[i][0]
                nome = query[i][1]
                senha = query[i][2]

                lines.append('ID: %s\nNome: %s\nSenha: %s' %
                             (id_user, nome, senha))
                res = '\n--- ---\n'.join(tuple(lines))

            code = 200

        else:
            res = 'Utilizador %s não existe.' % id_user
            code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# APAGA


@app.route('/utilizadores/delete', methods=['DELETE'])
def deleteU():
    conn = get_db_connection()
    if not request.data:
        query = conn.execute('SELECT id FROM utilizadores').fetchall()
        if len(query) != 0:
            query = conn.execute('DELETE FROM listas_albuns')
            conn.commit()
            query = conn.execute('DELETE FROM utilizadores')
            conn.commit()
            res = 'Todos os utilizadores foram apagados.'
            code = 200
        else:
            res = 'Não há utilizadores para apagar.'
            code = 200

    else:
        data = json.loads(request.data)
        query = conn.execute('SELECT id FROM utilizadores').fetchall()
        ids = []
        for i in range(len(query)):
            ids.append(query[i][0])

        id_user = data['id_user']

        if id_user in ids:
            query = conn.execute(
                'DELETE FROM listas_albuns WHERE id_user = ' + str(id_user))
            conn.commit()
            query = conn.execute(
                'DELETE FROM utilizadores WHERE id = ' + str(id_user))
            conn.commit()
            res = 'O utilizador %s foi apagado.' % id_user
            code = 200

        else:
            res = 'Utilizador %s não existe.' % id_user
            code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# CRIA


@app.route('/utilizadores/create', methods=['POST'])
def createU():
    conn = get_db_connection()
    data = json.loads(request.data)
    id = conn.execute('SELECT COUNT(id) FROM utilizadores').fetchall()[
        0][0] + 1
    nome = data['nome']
    senha = data['pass']
    query = conn.execute(
        "INSERT INTO utilizadores (id, nome, senha) VALUES (" + str(id)+",'"+nome+"','"+senha+"')")
    conn.commit()
    r = make_response(
        'Novo utilizador adicionado! Nome: %s, ID: %s' % (nome, id), 201)
    conn.close()
    return r

# ATUALIZA


@app.route('/utilizadores/update', methods=['PUT'])
def updateU():
    conn = get_db_connection()
    data = json.loads(request.data)
    query = conn.execute('SELECT id FROM utilizadores').fetchall()
    ids = []
    for i in range(len(query)):
        ids.append(query[i][0])

    id_user = data['id_user']
    if id_user in ids:
        senha = data['pass']
        query = conn.execute(
            "UPDATE utilizadores SET senha = '"+senha+"' WHERE id = "+str(id_user))
        conn.commit()
        res = 'A palavra-passe do utilizador %s foi alterada.' % id_user
        code = 201

    else:
        res = 'Utilizador %s não existe.' % id_user
        code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# ARTISTAS

# PESQUISA


@app.route('/artistas/search', methods=['GET'])
def searchA():
    conn = get_db_connection()
    if not request.data:
        query = conn.execute('SELECT * FROM artistas').fetchall()
        if len(query) != 0:
            lines = []
            for i in range(len(query)):
                id_artista = query[i][0]
                id_spotify = query[i][1]
                nome = query[i][2]

                lines.append('ID: %s\nID Spotify: %s\nNome: %s' %
                             (id_artista, id_spotify, nome))

            res = '\n--- ---\n'.join(tuple(lines))
            code = 200

        else:
            res = ''  # Não há resultados
            code = 204

    else:
        data = json.loads(request.data)
        query = conn.execute('SELECT id FROM artistas').fetchall()
        ids = []
        for i in range(len(query)):
            ids.append(query[i][0])

        id_artista = data['id_artista']
        if id_artista in ids:
            query = conn.execute(
                'SELECT * FROM artistas WHERE id = ' + str(id_artista)).fetchall()
            if len(query) != 0:
                lines = []
                for i in range(len(query)):
                    id_artista = query[i][0]
                    id_spotify = query[i][1]
                    nome = query[i][2]

                    lines.append('ID: %s\nID Spotify: %s\nNome: %s' %
                                 (id_artista, id_spotify, nome))
                res = '\n--- ---\n'.join(tuple(lines))
                code = 200

            else:
                res = ''  # Não há resultados
                code = 204

        else:
            res = 'Artista %s não existe.' % id_artista
            code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# APAGA


@app.route('/artistas/delete', methods=['DELETE'])
def deleteA():
    conn = get_db_connection()
    if not request.data:
        query = conn.execute('DELETE FROM listas_albuns')
        conn.commit()
        query = conn.execute('DELETE FROM albuns')
        conn.commit()
        query = conn.execute('DELETE FROM artistas')
        conn.commit()
        res = 'Todos os artistas foram apagados.'
        code = 200

    else:
        data = json.loads(request.data)
        query = conn.execute('SELECT id FROM artistas').fetchall()
        ids = []
        for i in range(len(query)):
            ids.append(query[i][0])

        id_artista = data['id_artista']
        if id_artista in ids:
            ids_album = conn.execute(
                'SELECT albuns.id FROM albuns WHERE albuns.id_artista = ' + str(id_artista)).fetchall()
            for i in range(len(ids_album)):
                query = conn.execute(
                    'DELETE FROM listas_albuns WHERE id_album = ' + str(ids_album[i][0]))
                conn.commit()
            query = conn.execute(
                'DELETE FROM albuns WHERE id_artista =' + str(id_artista))
            conn.commit()
            query = conn.execute(
                'DELETE FROM artistas WHERE id = ' + str(id_artista))
            conn.commit()
            res = 'O artista %s foi apagado.' % id_artista
            code = 200

        else:
            res = 'Artista %s não existe.' % id_artista
            code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# CRIA


@app.route('/artistas/create', methods=['POST'])
def createA():
    conn = get_db_connection()
    data = json.loads(request.data)
    artista = data['id_spotify']
    query = conn.execute('SELECT id_spotify FROM artistas').fetchall()
    artistas = []
    for i in range(len(query)):
        artistas.append(query[i][0])

    if artista not in artistas:
        id = conn.execute('SELECT COUNT(id) FROM artistas').fetchall()[
            0][0] + 1
        r = requests.get(BASE_URL + 'artists/' + artista, headers=token())
        api = r.json()
        nome = api['name']
        query = conn.execute(
            "INSERT INTO artistas (id, id_spotify, nome) VALUES ("+str(id)+",'"+artista+"','"+nome+"')")
        conn.commit()
        res = 'Novo artista adicionado! Nome: %s, ID: %s, ID Spotify: %s' % (
            nome, id, artista)
        code = 201
    else:
        res = 'Já existe esse artista na base de dados.'
        code = 501

    r = make_response(res, code, headers)
    conn.close()
    return r

# ALBUNS

# PESQUISA


@app.route('/albuns/search', methods=['GET'])
def searchAB():
    conn = get_db_connection()

    query = conn.execute('SELECT * FROM albuns').fetchall()
    if len(query) != 0:
        if not request.data:
            lines = []
            for i in range(len(query)):
                id_album = query[i][0]
                id_spotify = query[i][1]
                nomeAlbum = query[i][2]
                nomeArtista = conn.execute(
                    'SELECT nome FROM artistas WHERE id = ' + str(query[i][3])).fetchall()[0][0]

                lines.append('ID: %s\nID Spotify: %s\nNome: %s\nArtista: %s' % (
                    id_album, id_spotify, nomeAlbum, nomeArtista))

            if len(lines) != 0:
                res = '\n--- ---\n'.join(tuple(lines))
                code = 200
            else:
                res = ''
                code = 204

        else:
            data = json.loads(request.data)
            if 'id_album' in data.keys():
                query = conn.execute('SELECT id from albuns').fetchall()
                ids = []
                for i in range(len(query)):
                    ids.append(query[i][0])

                id_album = data['id_album']
                if id_album in ids:
                    query = conn.execute(
                        'SELECT * FROM albuns WHERE id = ' + str(id_album)).fetchall()
                    if len(query) != 0:
                        lines = []
                        for i in range(len(query)):
                            id_album = query[i][0]
                            id_spotify = query[i][1]
                            nomeAlbum = query[i][2]
                            nomeArtista = conn.execute(
                                'SELECT nome FROM artistas WHERE id = ' + str(query[i][3])).fetchall()[0][0]

                            lines.append('ID: %s\nID Spotify: %s\nNome: %s\nArtista: %s' % (
                                id_album, id_spotify, nomeAlbum, nomeArtista))
                        res = '\n--- ---\n'.join(tuple(lines))
                        code = 200

                    else:
                        res = ''  # Não há resultados
                        code = 204

                else:
                    res = 'Album %s não existe.' % id_album
                    code = 404

            elif 'id_artista' in data.keys():
                query = conn.execute('SELECT id FROM artistas').fetchall()
                ids = []
                for i in range(len(query)):
                    ids.append(query[i][0])

                id_artista = data['id_artista']
                if id_artista in ids:
                    query = conn.execute(
                        'SELECT * FROM albuns WHERE id_artista = ' + str(id_artista)).fetchall()
                    if len(query) != 0:
                        lines = []
                        for i in range(len(query)):
                            id_user = query[i][0]
                            id_spotify = query[i][1]
                            nomeAlbum = query[i][2]
                            nomeArtista = conn.execute(
                                'SELECT nome FROM artistas WHERE id = ' + str(query[i][3])).fetchall()[0][0]

                            lines.append('ID: %s\nID Spotify: %s\nNome: %s\nArtista: %s' % (
                                id_user, id_spotify, nomeAlbum, nomeArtista))
                        res = '\n--- ---\n'.join(tuple(lines))
                        code = 200

                    else:
                        res = ''  # Não há resultados
                        code = 204

                else:
                    res = 'Artista %s não existe.' % id_artista
                    code = 404

            elif 'id_user' in data.keys():
                query = conn.execute(
                    'SELECT DISTINCT id_user FROM listas_albuns').fetchall()
                ids = []
                for i in range(len(query)):
                    ids.append(query[i][0])

                id_user = data['id_user']
                if id_user in ids:
                    query = conn.execute(
                        'SELECT albuns.* FROM listas_albuns l, albuns WHERE l.id_user = %s AND albuns.id = l.id_album' % id_user).fetchall()
                    if len(query) != 0:
                        lines = []
                        for i in range(len(query)):
                            id_user = query[i][0]
                            id_spotify = query[i][1]
                            nomeAlbum = query[i][2]
                            nomeArtista = conn.execute(
                                'SELECT nome FROM artistas WHERE id = ' + str(query[i][3])).fetchall()[0][0]

                            lines.append('ID: %s\nID Spotify: %s\nNome: %s\nArtista: %s' % (
                                id_user, id_spotify, nomeAlbum, nomeArtista))
                        res = '\n--- ---\n'.join(tuple(lines))
                        code = 200

                    else:
                        res = ''  # Não há resultados
                        code = 204

                else:
                    res = 'Utilizador %s ainda não fez nenhuma avaliação.' % id_user
                    code = 404

            else:
                query = conn.execute(
                    'SELECT DISTINCT avaliacoes.sigla FROM avaliacoes, listas_albuns WHERE listas_albuns.id_avaliacao = avaliacoes.id').fetchall()
                avals = []
                for i in range(len(query)):
                    avals.append(query[i][0])

                aval = data['aval']
                if aval in avals:
                    query = conn.execute("SELECT albuns.* FROM avaliacoes, listas_albuns l, albuns WHERE avaliacoes.sigla = '" +
                                         aval+"' AND l.id_avaliacao = avaliacoes.id AND albuns.id = l.id_album").fetchall()
                    if len(query) != 0:
                        lines = []
                        for i in range(len(query)):
                            id_user = query[i][0]
                            id_spotify = query[i][1]
                            nomeAlbum = query[i][2]
                            nomeArtista = conn.execute(
                                'SELECT nome FROM artistas WHERE id = ' + str(query[i][3])).fetchall()[0][0]

                            lines.append('ID: %s\nID Spotify: %s\nNome: %s\nArtista: %s' % (
                                id_user, id_spotify, nomeAlbum, nomeArtista))
                        res = '\n--- ---\n'.join(tuple(lines))
                        code = 200

                    else:
                        res = ''  # Não há resultados
                        code = 204

                else:
                    res = 'Não há nenhum álbum avaliado com %s' % aval
                    code = 404

    else:
        res = 'Não há albuns para pesquisar.'
        code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# APAGA


@app.route('/albuns/delete', methods=['DELETE'])
def deleteAB():
    conn = get_db_connection()
    query = conn.execute('SELECT * FROM albuns').fetchall()
    if len(query) != 0:
        if not request.data:
            query = conn.execute('DELETE FROM listas_albuns')
            conn.commit()
            query = conn.execute('DELETE FROM albuns')
            conn.commit()
            res = 'Todos os álbuns foram apagados.'
            code = 200

        else:
            data = json.loads(request.data)
            if 'id_album' in data.keys():
                query = conn.execute('SELECT id FROM albuns').fetchall()
                ids = []
                for i in range(len(query)):
                    ids.append(query[i][0])

                id_album = data['id_album']

                if id_album in ids:
                    query = conn.execute(
                        'DELETE FROM listas_albuns WHERE id_album = ' + str(id_album))
                    conn.commit()
                    query = conn.execute(
                        'DELETE FROM albuns WHERE id = ' + str(id_album))
                    conn.commit()
                    res = 'O álbum %s foi apagado.' % id_album
                    code = 200

                else:
                    res = 'Álbum %s não existe.' % id_album
                    code = 404

            elif 'id_artista' in data.keys():
                query = conn.execute('SELECT id FROM artistas').fetchall()
                ids = []
                for i in range(len(query)):
                    ids.append(query[i][0])

                id_artista = data['id_artista']
                if id_artista in ids:
                    ids_album = conn.execute(
                        'SELECT albuns.id FROM albuns WHERE albuns.id_artista = ' + str(id_artista)).fetchall()
                    for i in range(len(ids_album)):
                        query = conn.execute(
                            'DELETE FROM listas_albuns WHERE id_album = ' + str(ids_album[i][0]))
                        conn.commit()
                    query = conn.execute(
                        'DELETE FROM albuns WHERE id_artista =' + str(id_artista))
                    conn.commit()
                    res = 'Todos os albuns do artista %s foram apagados.' % id_artista
                    code = 200
                else:
                    res = 'Artista %s não existe.'
                    code = 404

            elif 'id_user' in data.keys():
                query = conn.execute(
                    'SELECT DISTINCT id_user FROM listas_albuns').fetchall()
                ids = []
                for i in range(len(query)):
                    ids.append(query[i][0])

                id_user = data['id_user']

                if id_user in ids:
                    ids_album = conn.execute(
                        'SELECT listas_albuns.id_album FROM listas_albuns WHERE listas_albuns.id_user = ' + str(id_user)).fetchall()
                    for i in range(len(ids_album)):
                        query = conn.execute(
                            'DELETE FROM listas_albuns WHERE id_album = ' + str(ids_album[i][0]))
                        conn.commit()
                        query = conn.execute(
                            'DELETE FROM albuns WHERE id =' + str(ids_album[i][0]))
                        conn.commit()

                    res = 'Todos os álbuns avaliados pelo utilizador %s foram apagados.' % id_user
                    code = 200

                else:
                    res = 'Utilizador %s ainda não fez nenhuma avaliação.' % id_user
                    code = 404

            else:
                query = conn.execute(
                    'SELECT DISTINCT avaliacoes.sigla FROM avaliacoes, listas_albuns WHERE listas_albuns.id_avaliacao = avaliacoes.id').fetchall()
                avals = []
                for i in range(len(query)):
                    avals.append(query[i][0])

                aval = data['aval']
                if aval in avals:
                    id_aval = conn.execute(
                        'SELECT id FROM avaliacoes WHERE sigla = ' + aval)
                    ids_album = conn.execute(
                        'SELECT listas_albuns.id_album FROM listas_albuns WHERE listas_albuns.id_avaliacao = ' + str(id_aval)).fetchall()
                    for i in range(len(ids_album)):
                        query = conn.execute(
                            'DELETE FROM listas_albuns WHERE id_album = ' + str(ids_album[i][0]))
                        conn.commit()
                        query = conn.execute(
                            'DELETE FROM albuns WHERE id =' + str(ids_album[i][0]))
                        conn.commit()

                    res = 'Todos os álbuns com avaliação %s foram apagados.' % aval
                    code = 200

                else:
                    res = 'Não há nenhum álbum avaliado com %s' % aval
                    code = 404

    else:
        res = 'Não há álbuns para apagar.'
        code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# CRIA


@app.route('/albuns/create', methods=['POST'])
def createAB():
    conn = get_db_connection()
    data = json.loads(request.data)
    if len(data) == 1:
        album = data['id_spotify']
        query = conn.execute('SELECT id_spotify FROM albuns').fetchall()
        albuns = []
        for i in range(len(query)):
            albuns.append(query[i][0])

        if album not in albuns:
            r = requests.get(BASE_URL + 'albums/' + album, headers=token())
            api = r.json()
            nome = api['name']
            artista = api['artists'][0]['name']
            id = conn.execute('SELECT COUNT(id) FROM albuns').fetchall()[
                0][0] + 1
            query = conn.execute('SELECT nome FROM artistas').fetchall()
            artistas = []
            for i in range(len(query)):
                artistas.append(query[i][0])

            if artista in artistas:
                id_artista = conn.execute(
                    "SELECT id FROM artistas WHERE nome = '" + artista + "'").fetchall()[0][0]
                query = conn.execute(
                    'INSERT INTO albuns VALUES (?,?,?,?)', (id, album, nome, id_artista))
                conn.commit()
                res = 'Novo álbum adicionado! ID: %s, Nome: %s, ID Spotify: %s, Artista: %s' % (
                    id, nome, album, id_artista)
                code = 201

            else:
                res = 'Artista %s não existe.' % artista
                code = 404

        else:
            res = 'Já existe esse álbum na Base de Dados.'
            code = 501

    else:
        id_user = data['id_user']
        id_album = data['id_album']

        query = conn.execute(
            'SELECT * FROM listas_albuns l WHERE l.id_user = %s AND l.id_album = %s' % (id_user, id_album)).fetchall()

        if len(query) == 0:
            aval = data['aval']
            id_aval = conn.execute(
                "SELECT id FROM avaliacoes WHERE  sigla = '" + aval + "'").fetchall()[0][0]
            query = conn.execute(
                'INSERT INTO listas_albuns VALUES (?, ?, ?)', (id_user, id_album, id_aval))
            conn.commit()
            res = 'Nova avaliação foi adicionada! ID: %s, Álbum: %s, Avaliação: %s' % (
                id_user, id_album, aval)
            code = 201
        else:
            res = 'Utilizador %s já avaliou o álbum %s' % (id_user, id_album)
            code = 501

    r = make_response(res, code, headers)
    conn.close()
    return r

# ATUALIZA


@app.route('/albuns/update', methods=['PUT'])
def updateAB():
    conn = get_db_connection()
    data = json.loads(request.data)
    query = conn.execute('SELECT id FROM albuns').fetchall()
    albuns = []
    for i in range(len(query)):
        albuns.append(query[i][0])

    id_album = data['id_album']

    if id_album in albuns:
        query2 = conn.execute(
            'SELECT DISTINCT avaliacoes.sigla FROM avaliacoes, listas_albuns WHERE listas_albuns.id_avaliacao = avaliacoes.id').fetchall()
        avals = []
        for i in range(len(query2)):
            avals.append(query2[i][0])

        aval = data['aval']

        if aval in avals:
            query3 = conn.execute(
                'SELECT DISTINCT id_user FROM listas_albuns').fetchall()
            users = []
            for i in range(len(query3)):
                users.append(query3[i][0])

            id_user = data['id_user']

            if id_user in users:
                id_aval = conn.execute(
                    "SELECT id FROM avaliacoes WHERE  sigla = '" + aval + "'").fetchall()[0][0]
                query = conn.execute('UPDATE listas_albuns SET id_avaliacao = %s WHERE id_user = %s AND id_album = %s' % (
                    id_aval, id_user, id_album))
                conn.commit()
                res = 'A avaliação do utilizador %s ao álbum %s foi alterada para %s.' % (
                    id_user, id_album, aval)
                code = 201

            else:
                res = 'Utilizador %s ainda não fez nenhuma avaliação' % id_user
                code = 404

        else:
            res = 'Avaliação %s não existe.' % aval
            code = 404

    else:
        res = 'Álbum %s não existe.' % id_album
        code = 404

    r = make_response(res, code, headers)
    conn.close()
    return r

# ERRORS


@app.route('/400')
def BadRequest400():
    return make_response('Comando desconhecido.', 400, headers)


if __name__ == '__main__':
    app.run(debug=True)
