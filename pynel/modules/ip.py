from pynel.helpers import Pynel, draw_text
import psutil


class IpModule(Pynel):
    def __init__(self):
        super().__init__("Ip")
        self.use_update = False

    def draw_geral(self):
        self.draw()

    def draw(self):
        ip = psutil.net_if_addrs()["Ethernet 2"][1].address
        draw_text(self.sur, "Ip da maquina: " + ip, self.next_height())
