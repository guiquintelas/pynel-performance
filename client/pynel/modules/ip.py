from client.pynel.helpers import *


class IpModule(Pynel):
    def __init__(self):
        super().__init__("Rede", use_draw_tick=True)

        self.adaptadores = {}
        self.ip = "Selecione um adaptador."
        self.sel_adapdador = False

        self.ips = []
        self.esperando_ips = []
        self.pegando_ip = False

        self.click = False
        self.mouse_pos = []

        request_server(PEGAR_ADAPTADORES, self.on_adaptadores)

    def draw_tick(self):
        if len(self.adaptadores.keys()) == 0:
            draw_text(self.sur, "Pegando interfaces...", self.next_height())
        else:
            draw_text(self.sur, "Selecione uma interface:", self.next_height())

            for index, adaptador in enumerate(self.adaptadores.keys()):
                y = get_height(self.index - .1) - 5
                x = 50 + ((index % 3) * (WIDTH - 100) / 3)
                width = (WIDTH - 100) / 3 - 10
                height = 33

                if x < self.mouse_pos[0] < x + width and \
                        y < self.mouse_pos[1] < y + height:
                    cor_rect = BLACK_GRAY_LIGHT

                    if self.click:
                        self.select_adapter(adaptador)
                else:
                    cor_rect = BLACK_GRAY

                pygame.draw.rect(self.sur, cor_rect, (x, y, width, height))

                if adaptador == self.sel_adapdador:
                    cor_text = RED
                else:
                    cor_text = WHITE

                x_text = (width - text_width(adaptador)) / 2
                draw_text(self.sur, adaptador, y + 9, x=x + x_text, small=True, no_pad=True, color=cor_text)

                if (index + 1) % 3 == 0:
                    self.add_pad(1)
            self.add_pad(1)

        if self.sel_adapdador:
            pygame.draw.rect(self.sur, BLACK_GRAY, (10, self.next_height(small=True), WIDTH - 20, 1))

            draw_text(self.sur, "Informações da interface selecionada:", self.next_height())

            template = "{} {}"
            draw_text(self.sur, template.format("Nome:       ", self.sel_adapdador),
                      self.next_height(small=True),
                      small=True,
                      no_pad=True)

            draw_text(self.sur, template.format("Ip:            ", self.ip),
                      self.next_height(small=True),
                      small=True,
                      no_pad=True)

            draw_text(self.sur, template.format("Máscara:  ", self.adaptadores[self.sel_adapdador][1].netmask),
                      self.next_height(),
                      small=True,
                      no_pad=True)

            pygame.draw.rect(self.sur, BLACK_GRAY, (10, self.next_height(small=True), WIDTH - 20, 1))

            if len(self.ips) > 0:
                draw_text(self.sur, f"Ips da subrede - (quantidade: {len(self.ips)})", self.next_height())

                index_inicial = self.index
                x = 50

                for idx, ip in enumerate(self.ips):
                    draw_text(self.sur, ip, get_height(self.index), small=True, x=x)
                    self.add_pad(.5)

                    if (idx + 1) % 12 == 0:
                        self.index = index_inicial
                        x += 120

            elif self.pegando_ip:
                draw_text(self.sur, "Nenhum ip encontrado :(", self.next_height())

    def update_tick(self, eventos):
        self.click = False

        for event in eventos:
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = True
                break

        self.mouse_pos = pygame.mouse.get_pos()

    def update(self, eventos):
        self.pegar_ips()

    def on_adaptadores(self, resposta):
        self.adaptadores = resposta

    def select_adapter(self, adaptador):
        try:
            self.ips = []
            self.esperando_ips = []
            self.sel_adapdador = adaptador
            self.ip = self.adaptadores[self.sel_adapdador][1].address
            self.sel_adapdador = adaptador
        except:
            self.ip = "Não foi possivel achar o ip"
            self.sel_adapdador = False

        self.pegando_ip = False

    def pegar_ips(self):
        if self.pegando_ip or self.ip == "Selecione um adaptador.":
            return

        self.pegando_ip = True
        self.esperando_ips = [final for final in range(1, 255)]

        for final in range(1, 255):
            request_server(PEGAR_IP, self.on_ip, self.ip, final, multiple_instance=True)

    def on_ip(self, resposta):
        # chamada de um adaptador antigo
        # o usuario trcou de adaptador no meio das chamdas de ip
        if resposta["host"] != ".".join(self.ip.split(".")[:-1]):
            return

        if resposta["result"] == 0:
            if resposta["hostname"] not in self.ips:
                self.ips.append(resposta["hostname"])
        else:
            if resposta["hostname"] in self.ips:
                self.ips.remove(resposta["hostname"])

        self.esperando_ips.remove(int(resposta["hostname"].split(".")[-1]))

        if len(self.esperando_ips) == 0:
            self.pegando_ip = False
