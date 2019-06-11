from client.pynel.settings import pygame, WIDTH
from client.pynel.helpers import Pynel, draw_text
import psutil


class MemoryModule(Pynel):
    def __init__(self):
        super().__init__("Memoria")

    def draw_geral(self):
        self.draw()

    def draw(self):
        pygame.draw.rect(self.sur, (150, 0, 0), (0, self.next_height(True), WIDTH, 30))

        mem = psutil.virtual_memory()
        mem_perc_used_bar = (mem.used * WIDTH) / mem.total
        mem_perc_used = (mem.used * 100) / mem.total
        pygame.draw.rect(self.sur, (255, 0, 0), (0, self.next_height(True), mem_perc_used_bar, 30))

        mem_used_gb = mem.used / (1024 * 1024 * 1024)
        mem_total_gb = mem.total / (1024 * 1024 * 1024)
        draw_text(self.sur,
                  "Memoria:   {0:.2f}gb / {1:.2f}gb    {2:.2f} %"
                  .format(mem_used_gb, mem_total_gb, mem_perc_used), self.next_height() + 5)
