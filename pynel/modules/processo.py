from pynel.helpers import *
from pynel.settings import *
import pygame
import psutil


class ProcessModule(Pynel):
    def __init__(self):
        super().__init__(nome="Processos")
        self.use_update = False

        self.headers = {
            "Nome": 40,
            "Memoria": 200,
            "Memoria %": 300,
            "Threads": 400
        }

        self.pids = self.get_processos()
        self.pids.sort(key=lambda p: p["mem"], reverse=True)

    def draw(self):
        draw_text(self.sur, "15 Processos que mais utilizam Memória:", self.next_height())

        for header in self.headers.keys():
            draw_text(self.sur, header, self.next_height(small=True, same=True), small=True, x=self.headers[header])

        self.add_pad(.7)

        for pid in self.pids[:15]:
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

    def draw_geral(self):
        draw_text(self.sur, "Processos sendo executados: {}".format(len(psutil.pids())), self.next_height())

    @staticmethod
    def get_processos():
        pids = []
        for p in psutil.pids():
            pid = {}
            try:
                p = psutil.Process(p)
                pid["nome"] = p.name()
                pid["mem"] = p.memory_percent()
                pid["mem_c"] = '{:.2f} MB'.format(p.memory_info().rss / 1024 / 1024)
                pid["thr"] = p.num_threads()
            except:
                continue

            pids.append(pid)
        return pids
