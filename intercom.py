# -*- coding: utf-8 -*-
"""Modulo receptor emisor de audio.

Usamos upd para estas dos tareas con dos hilos simultaneos
"""
from pyaudio import paInt16
from pyaudio import PyAudio
import socket
import threading
# import sys

CHUNK = 1024
FORMAT = paInt16
CHANNELS = 1
RATE = 44100


def receiver(port_receiv):
    """Receptor de datos.

    Usado como un hilo recibe el puerto por el que se desea escuchar
    """
    sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('0.0.0.0', int(port_receiv))
    sock_receiver.bind(server_address)

    p = PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    while True:
        data, addr = sock_receiver.recvfrom(2048)
        # recibir datos, descomprimirlos y etc. luego reproducir
        stream.write(data)

def transmiter(ip_transm, port_transm):
    """Emisor de datos.

    Usado como un segundo hilo recibe como parametros la ip del compañero
    al que enviar datos y el puerto por el que lo hace
    """
    sock_transmiter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    p = PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while True:
        # grabar sonido comprimirlo y etc y enviarlo.
        data = stream.read(1024)
        sock_transmiter.sendto(data, (ip_transm, int(port_transm)))
        
        # mostrar el audio por pantalla con enteros
        for i in range(0, 1024):
            frames.append(data[i])
        print(frames)

if __name__ == '__main__':
    # establecemos puerto de escucha
    port_receiv = input("Introduce el puerto para recibir: ")

    # iniciamos el hilo reporoductor que lee lo que entra de udp
    r = threading.Thread(target=receiver, args=(port_receiv,))
    r.daemon = True
    r.start()

    # solicitamos los datos del "peer"
    host_transm = input("Introduce la ip del host: ")
    port_transm = input("Introduce el puerto del host: ")

    # hilo para enviar udp de lo que se graba
    t = threading.Thread(target=transmiter, args=(host_transm, port_transm,))
    t.daemon = True
    t.start()

    esperandoEntradaDatos = input("Introduce algo mas: ")
