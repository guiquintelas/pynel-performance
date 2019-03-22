from server.chamadas import *
import socket
import time
import threading
import pickle
import psutil
import os

HOST = '127.0.0.1'
PORT = 65432


def listar_processo():
    return pickle.dumps(psutil.pids())


def numero_processos():
    return pickle.dumps(len(psutil.pids()))


def detalhar_processo(pid):
    try:
        processo = {}
        p = psutil.Process(pid)
        processo["pid"] = pid
        processo["nome"] = p.name()
        processo["mem"] = p.memory_percent()
        processo["mem_c"] = '{:.2f} MB'.format(p.memory_info().rss / 1024 / 1024)
        processo["thr"] = p.num_threads()

    except:
        return pickle.dumps(pid)

    return pickle.dumps(processo)


def path_base_diretorio():
    return pickle.dumps(os.getcwd())


def lista_arquivos_path(path):
    # listando os arquivos no diretório e agrupando por arquivos e pastas
    files = [{"nome": file, "is_file": os.path.isfile(os.path.join(path, file))} for file in
                  os.listdir(path)]
    files.sort(key=lambda a: a["is_file"])

    for file in files:
        file["info"] = os.stat(os.path.join(path, file["nome"]))
        file["back"] = False

    files.insert(0, {"nome": "..", "is_file": False, "back": True})
    return pickle.dumps(files)


def receber_solicitacao():
    try:
        message, address = server_socket.recvfrom(10000)
    except Exception:
        print("Conexao perdida")
        criar_novo_thread()
        return

    # cria um novo thread para lidar com a proxima chamada
    criar_novo_thread()

    args = []

    # recebeu uma sol e comeca outro thread para continuar ouvindo
    tempo_inicial = time.time()
    try:
        # tenta fazer o decode em utf para saber se é uma string
        # ou uma lista no caso de argumentos
        # message.decode('utf-8')
        print(f"Recebeu   - {message.decode('utf-8')}")

    except Exception:
        # separa a chamada (primeira posicao da lista de arguemtnos)
        # e seta a message com seu valor
        pacote = pickle.loads(message)
        message = pacote[0]
        print(f"Recebeu   - {message.decode('utf-8')}")

        # retira a chamada dos args para poder fazer o spread no metodo
        args = pacote[1:]

    # trata a solicitacao
    if message == LISTAR_PROCESSOS:
        resposta = listar_processo()

    elif message == NUMERO_PROCESSOS:
        resposta = numero_processos()

    elif message == DETALHAR_PROCESSO:
        resposta = detalhar_processo(*args)

    elif message == PATH_BASE_DIRETORIO:
        resposta = path_base_diretorio()

    elif message == LISTA_ARQUIVOS_PATH:
        resposta = lista_arquivos_path(*args)

    else:
        print("solicitacao invalida! ", message)
        resposta = "solicitacao invalida!".encode("utf")

    print("Respondeu - {} ({:.2f}s)".format(message.decode('utf-8'), time.time() - tempo_inicial))
    server_socket.sendto(resposta, address)


def criar_novo_thread():
    thread = threading.Thread(target=receber_solicitacao)
    thread.start()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    criar_novo_thread()


