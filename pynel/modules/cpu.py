from pynel.helpers import pygame, text_width, draw_text, pad_mod, WIDTH, Pynel
import psutil
import platform
from cpuinfo import get_cpu_info

info = ""
if info == "":
    info = get_cpu_info()


class CpuModule(Pynel):
    def __init__(self):
        super().__init__("Cpu")

    def draw(self):
        freq = psutil.cpu_freq()

        self.draw_geral()

        cpus = psutil.cpu_percent(percpu=True)
        cpu_y = self.next_height()
        cpu_index = 6.5

        cpu_bar_margin = 5
        cpu_bar_width = WIDTH / len(cpus) - cpu_bar_margin * 2
        cpu_bar_height = cpu_index * pad_mod

        for idx, cpu_perc in enumerate(cpus):
            cpu_x = idx * (cpu_bar_width + cpu_bar_margin * 2) + cpu_bar_margin
            pygame.draw.rect(self.sur,
                             (150, 0, 0),
                             (cpu_x, cpu_y,
                              cpu_bar_width,
                              cpu_bar_height))
            pygame.draw.rect(self.sur,
                             (255, 0, 0),
                             (cpu_x, cpu_y + (cpu_bar_height / 100 * (100 - cpu_perc)),
                              cpu_bar_width, cpu_bar_height / 100 * cpu_perc))

            perc_text = str(cpu_perc) + "%"
            draw_text(self.sur,
                      perc_text,
                      cpu_y + cpu_bar_height / 2 - 10,
                      x=cpu_x + cpu_bar_width / 2 - text_width(perc_text) / 2,
                      small=True,
                      no_pad=True)

        self.add_pad(cpu_index - .5)

        draw_text(self.sur, "CPU", self.next_height(small=True))
        draw_text(self.sur, "Modelo: %s" % (info["brand"]), self.next_height(small=True), True)
        draw_text(self.sur, "Arquitetura: %s" % (info["arch"]), self.next_height(small=True), True)
        draw_text(self.sur, "Palavra: %s" % (info["bits"]), self.next_height(small=True), True)
        draw_text(self.sur, "Threads: %s" % (psutil.cpu_count()), self.next_height(small=True), True)
        draw_text(self.sur, "Núcleos: %s" % (psutil.cpu_count(logical=False)), self.next_height(small=True), True)
        draw_text(self.sur, "Frequência Atual: %i" % freq.current, self.next_height(small=True), True)
        draw_text(self.sur, "Frequência Total: %i" % freq.max, self.next_height(), True)

        draw_text(self.sur, "Informações", self.next_height(small=True))
        draw_text(self.sur, "Processador: " + platform.processor(), self.next_height(small=True), True)
        draw_text(self.sur, "Nome do computador na rede: " + platform.node(), self.next_height(small=True), True)
        draw_text(self.sur, "Detalhe da Plataforma: " + platform.platform(), self.next_height(small=True), True)
        draw_text(self.sur, "Sistema Operacional: " + platform.system(), self.next_height(), True)

    def draw_geral(self):
        pygame.draw.rect(self.sur, (150, 0, 0), (0, self.next_height(True), WIDTH, 30))
        cpu_usage = psutil.cpu_percent()
        cpu_perc_used_bar = (cpu_usage * WIDTH) / 100
        pygame.draw.rect(self.sur, (255, 0, 0), (0, self.next_height(True), cpu_perc_used_bar, 30))
        draw_text(self.sur, "CPU: {0:.2f} %".format(cpu_usage), self.next_height() + 5)
