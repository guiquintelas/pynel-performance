from client.pynel.helpers import *
from client.pynel.settings import *
import psutil
import os
import os.path
import time


class HdModule(Pynel):
    def __init__(self):
        super().__init__(nome="Disco", use_draw_tick=True)
        self.path = "Carregando..."
        self.pegou_path = False

        self.headers = {
            "Tipo": 40,
            "Nome": 100,
            "Data Modificado": 320,
            "Tamanho (Bytes)": 490
        }

        self.mouse_pos = pygame.mouse.get_pos()
        self.files = []
        self.click = False

    def draw_tick(self):
        self.draw_geral()
        draw_text(self.sur, "Arquivos: {}".format(self.path), self.next_height(), small=True, no_pad=True)

        # headers
        for header in self.headers.keys():
            draw_text(self.sur, header, self.next_height(small=True, same=True), small=True, x=self.headers[header])

        self.add_pad(.7)

        for file in self.files:
            if 50 < self.mouse_pos[0] < WIDTH - 50:
                if self.next_height(same=True) - 5 < self.mouse_pos[1] < get_height(self.index + .6):
                    pygame.draw.rect(self.sur, BLACK_GRAY, (50, get_height(self.index - .1) - 5, WIDTH - 99, 33))
                    if self.click and not file["is_file"]:
                        self.path = os.path.abspath(os.path.join(self.path, file["nome"]))
                        self.click = False

            # tipo de arquivo
            if file["is_file"]:
                self.sur.blit(file_icon, (self.headers["Tipo"] + 35, self.next_height(same=True) - 4))
            else:
                self.sur.blit(folder_icon, (self.headers["Tipo"] + 40, self.next_height(same=True)))

            # nome
            draw_text(self.sur, file["nome"], self.next_height(small=True, same=True), small=True, x=self.headers["Nome"])

            if not file["back"]:
                # data modificado
                draw_text(self.sur, time.strftime('%H:%M:%S %d/%m/%Y ', time.localtime(file["info"].st_mtime)),
                          self.next_height(small=True, same=True), small=True,
                          x=self.headers["Data Modificado"])

                # tamanho
                draw_text(self.sur, file["info"].st_size, self.next_height(small=True, same=True), small=True,
                          x=self.headers["Tamanho (Bytes)"])

            self.add_pad(.6)
            pygame.draw.line(self.sur, BLACK_GRAY, (50, self.next_height(same=True)), (WIDTH - 50, self.next_height(same=True)))
            self.add_pad(.2)

    def draw_geral(self):
        disco = psutil.disk_usage('.')

        total_gb = round(disco.total / (1024 * 1024 * 1024), 2)
        used_gb = round(disco.used / (1024 * 1024 * 1024), 2)

        pygame.draw.rect(self.sur, (150, 0, 0), (0, self.next_height(True), WIDTH, 30))

        hd_perc_used_bar = (disco.used * WIDTH) / disco.total
        hd_perc_used = (disco.used * 100) / disco.total
        pygame.draw.rect(self.sur, (255, 0, 0), (0, self.next_height(True), hd_perc_used_bar, 30))

        draw_text(self.sur, "Disco: {0:.2f}gb / {1:.2f}gb        {2:.2f}%"
                  .format(used_gb, total_gb, hd_perc_used), self.next_height() + 5)

    def update_tick(self, eventos):
        self.click = False

        for event in eventos:
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = True
                break

        self.mouse_pos = pygame.mouse.get_pos()

    def update(self, eventos):
        if not self.pegou_path:
            request_server(PATH_BASE_DIRETORIO, self.on_path_base_diretorio)
        else:
            request_server(LISTA_ARQUIVOS_PATH, self.on_lista_arquivos_path, self.path)

    def on_path_base_diretorio(self, resposta):
        self.path = resposta
        self.pegou_path = True

    def on_lista_arquivos_path(self, files):
        self.files = files
