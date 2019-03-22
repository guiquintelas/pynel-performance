from client.pynel.helpers import *
import pygame
import threading
import time


class ProcessModule(Pynel):
    def __init__(self):
        super().__init__(nome="Processos")

        self.headers = {
            "Nome": 40,
            "Memoria": 300,
            "Memoria %": 400,
            "Threads": 500
        }

        self.processos = []
        self.pegando_processos = False

        self.pids_para_tratar = []
        self.tratar_pids_tempo_inicial = 0

        self.tempo_medio_get_processos = 0
        self.tempo_medio_get_processo = 0
        self.tempo_medio_get_processos_count = 0
        self.tempo_medio_get_processo_count = 0

        self.numeros_processos = "Carregando..."

    def draw(self):
        draw_text(self.sur, "15 Processos que mais utilizam Memória:", self.next_height())

        for header in self.headers.keys():
            draw_text(self.sur, header, self.next_height(small=True, same=True), small=True, x=self.headers[header])

        self.add_pad(.7)

        for pid in self.processos[:15]:
            draw_text(self.sur, pid["nome"], self.next_height(small=True, same=True), small=True,
                      x=self.headers["Nome"])

            draw_text(self.sur, pid["mem_c"], self.next_height(small=True, same=True), small=True,
                      x=self.headers["Memoria"])

            draw_text(self.sur, "{:.2f}%".format(pid["mem"]), self.next_height(small=True, same=True), small=True,
                      x=self.headers["Memoria %"])

            draw_text(self.sur, pid["thr"], self.next_height(small=True, same=True), small=True,
                      x=self.headers["Threads"])

            self.add_pad(.6)
            pygame.draw.line(self.sur, BLACK_GRAY, (50, self.next_height(same=True)),
                             (WIDTH - 50, self.next_height(same=True)))
            self.add_pad(.2)

        self.add_pad(.2)
        draw_text(self.sur,
                  "Número de threads nesse processo: {}".format(threading.active_count()),
                  self.next_height(small=True),
                  small=True, no_pad=True)

        draw_text(self.sur,
                  "Tempo médio para pegar as informações de um processo:           {:.3f} s".format(
                      self.tempo_medio_get_processo),
                  self.next_height(small=True),
                  small=True, no_pad=True)

        draw_text(self.sur,
                  "Tempo médio para pegar as informações de todos os processo:  {:.3f} s".format(
                      self.tempo_medio_get_processos),
                  self.next_height(small=True),
                  small=True, no_pad=True)

    def draw_geral(self):
        draw_text(self.sur, "Processos sendo executados: {}".format(self.numeros_processos), self.next_height())

    def update(self, eventos):
        self.get_processos()

    def update_tick(self, eventos):
        self.request_detalha_processo()

    def get_processos(self):
        if self.pegando_processos:
            return

        request_server(LISTAR_PROCESSOS, self.on_pids_response)

    def on_pids_response(self, pids):
        print("pegando processos...")
        self.pegando_processos = True
        self.pids_para_tratar = pids
        self.tratar_pids_tempo_inicial = time.time()

    def request_detalha_processo(self):
        if not self.pegando_processos:
            return

        if len(self.pids_para_tratar) <= 0:
            self.tratar_processos_completo()
            return

        if request_server(DETALHAR_PROCESSO, self.tratar_processo, self.pids_para_tratar[0]):
            self.pids_para_tratar.pop(0)

    def tratar_processo(self, processo, tempo_decorrido):
        if isinstance(processo, int):
            # self.processos.remove(processo)
            return

        ja_existe = False

        for idx, pid_atual in enumerate(self.processos):
            if pid_atual['pid'] == processo["pid"]:
                self.processos[idx] = processo
                ja_existe = True
                break

        if not ja_existe:
            self.processos.append(processo)

        self.processos.sort(key=lambda p: p["mem"], reverse=True)

        if len(self.pids_para_tratar) == 0:
            self.tratar_processos_completo()

        # atualizando tempo medio
        self.tempo_medio_get_processo_count += 1
        self.tempo_medio_get_processo = self.tempo_medio_get_processo * (self.tempo_medio_get_processo_count - 1) + tempo_decorrido
        self.tempo_medio_get_processo /= self.tempo_medio_get_processo_count

    def tratar_processos_completo(self):
        self.pegando_processos = False

        # atualizando tempo medio
        tempo_decorrido = time.time() - self.tratar_pids_tempo_inicial
        self.tempo_medio_get_processos_count += 1
        self.tempo_medio_get_processos = self.tempo_medio_get_processos * (self.tempo_medio_get_processos_count - 1) + tempo_decorrido
        self.tempo_medio_get_processos /= self.tempo_medio_get_processos_count
        print("Pegou todos! ({:.2f}s)".format(tempo_decorrido))

    def update_geral(self, eventos):
        request_server(NUMERO_PROCESSOS, self.on_numeros_processos)

    def on_numeros_processos(self, resposta):
        self.numeros_processos = resposta
