#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 3 - database.py
Grupo: 25
Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991
"""

# Zona para fazer importação

import sqlite3
from os.path import isfile

###############################################################################

db_is_created = isfile(r'RateAlbums.db')

if not db_is_created:
    conn = sqlite3.connect(r'RateAlbums.db')
    with open('listagem1.sql') as f:
        conn.executescript(f.read())

    cursor = conn.cursor()

    avaliacoes = [(1, 'M', 'Mediocre'),
                  (2, 'm', 'Mau'),
                  (3, 'S', 'Suficiente'),
                  (4, 'B', 'Bom'),
                  (5, 'MB', 'Muito Bom')]

    cursor.executemany('INSERT INTO avaliacoes VALUES (?,?,?)', avaliacoes)
    conn.commit()

cursor.execute('SELECT * FROM avaliacoes')
aval = cursor.fetchall()
print('Avaliações: ', aval)
                        
