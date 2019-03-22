from server.main import HOST, PORT
from inspect import signature
import pickle
import socket
import threading
import time

CHAMADAS_RODANDO = []
SOCKET_ABERTOS = []


def dispatch(chamada, callback, args, multiple_instance):
    tempo_inicial = time.time()

    chamada_str = chamada.decode('utf-8')
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCKET_ABERTOS.append(socket_client)

    if len(args) > 0:
        socket_client.sendto(pickle.dumps([chamada, *args]), (HOST, PORT))
    else:
        socket_client.sendto(chamada, (HOST, PORT))

    try:
        resposta, addr = socket_client.recvfrom(10000)
    except Exception:
        print(f"Sem conexao com o servidor... ({chamada_str})")
        return
    finally:
        CHAMADAS_RODANDO.remove(chamada_str)
        SOCKET_ABERTOS.remove(socket_client)
        socket_client.close()

    tempo_decorrido = time.time() - tempo_inicial
    if not multiple_instance:
        print("Respondeu - {} ({:.2f}s)".format(chamada_str, tempo_decorrido))

    if len(signature(callback).parameters) > 1:
        callback(pickle.loads(resposta), tempo_decorrido)
    else:
        callback(pickle.loads(resposta))


def request_server(chamada, callback, *args, multiple_instance=False):
    chamada_str = chamada.decode('utf-8')

    # checa se ja existe uma chamada desse tipo pendente
    if chamada_str in CHAMADAS_RODANDO and not multiple_instance:
        return False

    thread = threading.Thread(target=dispatch,
                              args=[chamada, callback, args, multiple_instance],
                              daemon=True,
                              name=chamada_str)
    thread.start()
    CHAMADAS_RODANDO.append(chamada_str)
    return True
