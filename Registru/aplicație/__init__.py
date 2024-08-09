import json
import random
import requests
import os
import time

from flask import Flask, jsonify, request

from Registru.portofel.portofel import Portofel
from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.mină import Mină
from Registru.sistem import Registrul
from Registru.pubsub import PubSub

from multiprocessing import Process

import threading
import time
import queue

aplicație = Flask(__name__)

registru = Registrul()

cheie_geneză_privată = Portofel.din_cheie(Portofel,f"C:\\Users\\Calin\\Documents\\GitHub\\nod\\Registru\\utile\\chei\\cheie_privată.pem")
cheie_geneză_publică = cheie_geneză_privată.public_key()
portofel = Portofel(registru)
portofel.cheie_privată = cheie_geneză_privată
portofel.cheie_publică = cheie_geneză_publică
portofel.serializează_cheie_publică()

mină = Mină()
pubsub = PubSub(registru, mină)

data_queue = queue.Queue()

URL = 'https://5692-82-77-240-24.ngrok-free.app'

@aplicație.route('/')
def default():
    PORT_RĂDĂCINĂ=5000

    rezultat = requests.get(f'https://5692-82-77-240-24.ngrok-free.app/registru')

    rezultat_registru = registru.din_json(rezultat.json())

    try:
        registru.înlocuiește_listă(rezultat_registru.listă)
        print('\nRegistrul s-a sincronizat !')
    except Exception as e:
        print(f'\nRegistrul nu s-a sincronizat, eroare {e}')

    return f"Welcome To Individual Freedom ! REGISTRUL ARE {len(str(rezultat_registru.to_json()).encode('utf-8'))/1000}"


@aplicație.route('/registru')
def route_registru():
    return jsonify(registru.to_json())

@aplicație.route('/registru/minează')
def route_adăugare_bloc():

    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    informații = mină.informații_tranzacții()

    informații.append(Tranzacție.răsplătește_tranzacție(portofel).to_json())

    registru.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue), informații])
    pubsub.transmite_bloc(registru.listă[-1])

    return jsonify(registru.listă[-1].to_json())

@aplicație.route('/registru/minează/consensus', methods=['POST'])
def route_adăugare_bloc_consensus():

    start = time.time()

    informații_tranzacție = request.get_json()

    portofel = informații_tranzacție['plătitor']
    portofel = Portofel.din_json(Portofel,portofel)
    portofel.registru = Registrul.din_json(portofel.registru)

    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    informații = mină.informații_tranzacții()
    informații.append(Tranzacție.răsplătește_tranzacție(portofel).to_json())
    registru.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue), informații])
    print({f'durată_consensus: {time.time()-start}'})
    return {'status': 200}


@aplicație.route('/portofel/trimite', methods=['POST'])
def route_portofel_transact():
    
    informații_tranzacție = request.get_json()

    portofel = informații_tranzacție['plătitor']
    portofel = Portofel.din_json(Portofel,portofel)
    portofel.registru = Registrul.din_json(portofel.registru)
    tranzacția = mină.tranzacție_existentă(portofel.adresă)
    

    if tranzacția:
        tranzacția.actualizează(portofel, informații_tranzacție['beneficiar'], informații_tranzacție['sumă'])
    elif 'plătitor' in informații_tranzacție.keys():
        if informații_tranzacție['plătitor'] == informații_tranzacție['beneficiar']:
            tranzacția = Tranzacție(informații_tranzacție['plătitor'],informații_tranzacție['beneficiar'],informații_tranzacție['sumă'] )
        else:
            tranzacția = Tranzacție(portofel, informații_tranzacție['beneficiar'], informații_tranzacție['sumă'])
    else: 
        tranzacția = Tranzacție(portofel, informații_tranzacție['beneficiar'], informații_tranzacție['sumă'])

    pubsub.transmitere_trazacție(tranzacția)
    e_necesar_îndeplinitor = mină.e_necesar_îndeplinitor()

    if e_necesar_îndeplinitor:
        îndeplinitor = registru.următor_îndeplinitor()
        portofel = Portofel(registru)
        portofel.registru = portofel.registru.to_json()
        portofel.cheie_privată = []
        portofel.cheie_publică = îndeplinitor
        portofel.serializează_cheie_publică()

        bloc = requests.post(f'{URL}/registru/minează/consensus', json={'plătitor': portofel.to_json()}).json()

    return jsonify(tranzacția.to_json())


def transmitere_date():
    
    pubsub.transmitere_tranzacție(Tranzacție.din_json(data_queue.get()))

def pornire_threads():
    
    [threading.Thread(target=transmitere_date).start() for i in range(8)]

@aplicație.route('/portofel/trimite/tranzacții', methods=['POST'])
def route_portofel_tranzacții():

    start = time.time()
    informații_tranzacție = request.get_json()

    [data_queue.put(trx) for trx in informații_tranzacție['tranzacții']]
    print(f'date procesate {time.time()-start}')  
    pornire_threads()
    
    e_necesar_îndeplinitor = mină.e_necesar_îndeplinitor()

    if e_necesar_îndeplinitor:
        îndeplinitor = registru.următor_îndeplinitor()
        portofel = Portofel(registru)
        portofel.registru = portofel.registru.to_json()
        portofel.cheie_privată = []
        portofel.cheie_publică = îndeplinitor
        portofel.serializează_cheie_publică()

        bloc = requests.post(f'{URL}/registru/minează/consensus', json={'plătitor': portofel.to_json()}).json()
    
    print({'durată_tranzacții': time.time() - start})
    return {'status': 200}

@aplicație.route('/portofel/info')
def route_portofel_info():
    return jsonify({'adresă': portofel.adresă, 'total': portofel.sumă})

@aplicație.route('/registru/actualizare')
def route_portofel_info():
    return jsonify({'adresă': portofel.adresă, 'total': portofel.sumă})


PORT_RĂDĂCINĂ = 5000
PORT = PORT_RĂDĂCINĂ
if 'True' in os.environ.get('PEER'):
    PORT = random.randint(5001,35000)

    rezultat = requests.get(f'https://5692-82-77-240-24.ngrok-free.app/registru')

    rezultat_registru = registru.din_json(rezultat.json())

    try:
        registru.înlocuiește_listă(rezultat_registru.listă)
        print('\nRegistrul s-a sincronizat !')
    except Exception as e:
        print(f'\nRegistrul nu s-a sincronizat, eroare {e}')

aplicație.run(port=PORT)