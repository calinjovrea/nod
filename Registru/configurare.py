import socket

NANOSECUNDE = 1
MICROSECUNDE = 1000 * NANOSECUNDE
MILISECUNDE = 1000 * MICROSECUNDE
SECUNDE = 1000 * MILISECUNDE

RATA = 4 * SECUNDE

TOTAL = 1000

RĂSPLĂTIRE = 50
RĂSPLĂTIRE_ = {'adresă': '*--oficială-răsplătire--*'}

SECURIZEAZĂ_ = {'adresă': '*--oficială-securizare--*'}

IP = socket.gethostbyname(socket.gethostname())