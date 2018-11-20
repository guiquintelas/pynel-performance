
import pygame
import psutil
import platform
import cpuinfo

if __name__ != "__main__":
    exit(0)

info = cpuinfo.get_cpu_info()

WIDTH = 700
HEIGHT = 700
HEIGHT_SUR = 670
HEIGHT_MENU = 30
MARGIN = 20

BLACK = (0, 0, 0)

rectSize = 10
init_height = 30
pad_mod = 40

pygame.init()
pygame.display.set_caption('Pynel de Performance')

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fim = False

fonte = pygame.font.SysFont('Verdana', 15)
small_fonte = pygame.font.SysFont('Verdana', 12)
small_fonte_bold = pygame.font.SysFont('Verdana', 12, bold=True)

# surfaces
cpu_sur = pygame.surface.Surface((WIDTH, HEIGHT_SUR))
hd_sur = pygame.surface.Surface((WIDTH, HEIGHT_SUR))
memoria_sur = pygame.surface.Surface((WIDTH, HEIGHT_SUR))
menu_sur = pygame.surface.Surface((WIDTH, HEIGHT_SUR))
ip_sur = pygame.surface.Surface((WIDTH, HEIGHT_SUR))

geral = True

pintar_count = 0

# menu sel sera iniciado em 0
primeira_tecla = True
menu_sel = 0


def draw_text(tela, text, y, small=False, x=50.0, no_pad=False):

    if small:
        global small_fonte
        textsurface = small_fonte.render(text, False, (255, 255, 255))
        if not no_pad:
            x += 40
    else:
        global fonte
        textsurface = fonte.render(text, False, (255, 255, 255))

    tela.blit(textsurface, (x, y))


def text_width(text):
    return small_fonte.render(text, False, (255, 255, 255)).get_width()


def next_height(menu_index, same=False, small=False):
    global init_height
    global pad_mod

    y = init_height + pad_mod * menus[menu_index]["index"]

    if not same:
        if small:
            menus[menu_index]["index"] += .5
        else:
            menus[menu_index]["index"] += 1
    return y


def add_pad(menu_index, pad):
    menus[menu_index]["index"] += pad


def draw_memoria():

    pygame.draw.rect(memoria_sur, (150, 0, 0), (0, next_height(1, True), WIDTH, 30))

    mem = psutil.virtual_memory()
    mem_perc_used_bar = (mem.used * WIDTH) / mem.total
    mem_perc_used = (mem.used * 100) / mem.total
    pygame.draw.rect(memoria_sur, (255, 0, 0), (0, next_height(1, True), mem_perc_used_bar, 30))

    mem_used_gb = mem.used / (1024 * 1024 * 1024)
    mem_total_gb = mem.total / (1024 * 1024 * 1024)
    draw_text(memoria_sur,
              "Memoria:   {0:.2f}gb / {1:.2f}gb    {2:.2f} %"
              .format(mem_used_gb, mem_total_gb, mem_perc_used), next_height(1) + 5)


def draw_cpu_geral():
    pygame.draw.rect(cpu_sur, (150, 0, 0), (0, next_height(0, True), WIDTH, 30))
    cpu_usage = psutil.cpu_percent()
    cpu_perc_used_bar = (cpu_usage * WIDTH) / 100
    pygame.draw.rect(cpu_sur, (255, 0, 0), (0, next_height(0, True), cpu_perc_used_bar, 30))
    draw_text(cpu_sur, "CPU: {0:.2f} %".format(cpu_usage), next_height(0) + 5)


def draw_cpu_detail():
    freq = psutil.cpu_freq()

    draw_cpu_geral()

    cpus = psutil.cpu_percent(percpu=True)
    cpu_y = next_height(0)
    cpu_index = 6.5

    cpu_bar_margin = 5
    cpu_bar_width = WIDTH / len(cpus) - cpu_bar_margin * 2
    cpu_bar_height = cpu_index * pad_mod

    for idx, cpu_perc in enumerate(cpus):
        cpu_x = idx * (cpu_bar_width + cpu_bar_margin * 2) + cpu_bar_margin
        pygame.draw.rect(cpu_sur, (150, 0, 0), (cpu_x, cpu_y, cpu_bar_width, cpu_bar_height))
        pygame.draw.rect(cpu_sur, (255, 0, 0), (cpu_x, cpu_y + (cpu_bar_height / 100 * (100 - cpu_perc)), cpu_bar_width, cpu_bar_height / 100 * cpu_perc))

        perc_text = str(cpu_perc) + "%"
        draw_text(cpu_sur, perc_text, cpu_y + cpu_bar_height / 2 - 10, x=cpu_x + cpu_bar_width / 2 - text_width(perc_text) / 2, small=True, no_pad=True)

    add_pad(0, cpu_index - .5)

    draw_text(cpu_sur, "CPU", next_height(0, small=True))
    draw_text(cpu_sur, "Modelo: %s" % (info["brand"]), next_height(0, small=True), True)
    draw_text(cpu_sur, "Arquitetura: %s" % (info["arch"]), next_height(0, small=True), True)
    draw_text(cpu_sur, "Palavra: %s" % (info["bits"]), next_height(0, small=True), True)
    draw_text(cpu_sur, "Núcleos: %s" % (psutil.cpu_count()), next_height(0, small=True), True)
    draw_text(cpu_sur, "Núcleos Físicos: %s" % (psutil.cpu_count(logical=False)), next_height(0, small=True), True)
    draw_text(cpu_sur, "Frequência Atual: %i" % freq.current, next_height(0, small=True), True)
    draw_text(cpu_sur, "Frequência Total: %i" % freq.max, next_height(0), True)

    draw_text(cpu_sur, "Informações", next_height(0, small=True))
    draw_text(cpu_sur, "Processador: " + platform.processor(), next_height(0, small=True), True)
    draw_text(cpu_sur, "Nome do computador na rede: " + platform.node(), next_height(0, small=True), True)
    draw_text(cpu_sur, "Detalhe da Plataforma: " + platform.platform(), next_height(0, small=True), True)
    draw_text(cpu_sur, "Sistema Operacional: " + platform.system(), next_height(0), True)


def draw_hd():
    disco = psutil.disk_usage('.')

    total_gb = round(disco.total / (1024 * 1024 * 1024), 2)
    used_gb = round(disco.used / (1024 * 1024 * 1024), 2)

    pygame.draw.rect(hd_sur, (150, 0, 0), (0, next_height(2, True), WIDTH, 30))

    hd_perc_used_bar = (disco.used * WIDTH) / disco.total
    hd_perc_used = (disco.used * 100) / disco.total
    pygame.draw.rect(hd_sur, (255, 0, 0), (0, next_height(2, True), hd_perc_used_bar, 30))
    draw_text(hd_sur, "Disco: {0:.2f}gb / {1:.2f}gb        {2:.2f}%"
              .format(used_gb, total_gb, hd_perc_used), next_height(2) + 5)


def draw_ip():
    ip = psutil.net_if_addrs()["Ethernet 2"][1].address
    draw_text(ip_sur, "Ip da maquina: " + ip, next_height(3))


def draw_menu():
    menu_sur.fill(BLACK)

    pygame.draw.rect(menu_sur, (255, 255, 255), (0, 0, WIDTH, .5))

    for idx, menu in enumerate(menus):
        sector = WIDTH//len(menus)
        draw_text(menu_sur, menu['nome'], 3, x=sector*idx + WIDTH//(len(menus)*2) - text_width(menu["nome"])/2)
        if menu_sel == idx and not geral:
            pygame.draw.rect(menu_sur, (255, 0, 0), (sector*idx, HEIGHT_MENU - 3, sector, 3))

    if geral:
        pygame.draw.rect(menu_sur, (255, 0, 0), (0, HEIGHT_MENU - 3, WIDTH, 3))

    DISPLAY.blit(menu_sur, (0, HEIGHT_SUR))


def draw_menu_sel():
    if geral:
        draw_geral()
    else:
        menus[menu_sel]['sur'].fill(BLACK)
        menus[menu_sel]['funcao']()
        DISPLAY.blit(menus[menu_sel]['sur'], (0, 0))


def draw_geral():
    # tira a height inicial para não repetir em cada surface
    global init_height
    init_height_value = init_height
    init_height = 0

    # soma de todos os indexes para agir como uma surface só
    index_off = 1

    draw_text(DISPLAY, "Visão Geral (SPACE Para sair da visão geral  |  <- -> Para navegar)", 10)

    for menu in menus:
        menu['sur'].fill(BLACK)
        menu['funcao_geral']()
        DISPLAY.blit(menu['sur'], (0, index_off * (pad_mod + 10)))
        index_off += menu["index"]

    init_height = init_height_value


menus = [
    {
        "nome": "Cpu",
        "funcao": draw_cpu_detail,
        "funcao_geral": draw_cpu_geral,
        "sur": cpu_sur,
        "index": 0
    },
    {
        "nome": "Memoria",
        "funcao": draw_memoria,
        "funcao_geral": draw_memoria,
        "sur": memoria_sur,
        "index": 0
    },
    {
        "nome": "Disco",
        "funcao": draw_hd,
        "funcao_geral": draw_hd,
        "sur": hd_sur,
        "index": 0
    },
    {
        "nome": "Ip",
        "funcao": draw_ip,
        "funcao_geral": draw_ip,
        "sur": ip_sur,
        "index": 0
    },
]




while not fim:
    # resetar os indexes para não acumular infinitamente no loop
    for men in menus:
        men["index"] = 0

    # configurando o clock para 30 vezes por segundo
    clock.tick(30)

    # pintando as surfaces somente quando o count for <= zero
    if pintar_count <= 0:
        DISPLAY.fill((0, 0, 0))
        draw_menu_sel()

    draw_menu()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            fim = True
            exit(0)
            break

        if event.type == pygame.KEYDOWN:
            pintar_count = -3

            if event.key == pygame.K_RIGHT:
                geral = False
                menu_sel += 1

                if menu_sel >= len(menus):
                    menu_sel = 0

            if event.key == pygame.K_LEFT:
                geral = False
                menu_sel -= 1

                if menu_sel < 0:
                    menu_sel = len(menus) - 1

            if event.key == pygame.K_SPACE:
                geral = not geral

            if primeira_tecla:
                menu_sel = 0
                primeira_tecla = False

    # incrementa o clock
    pintar_count += 1

    # faz com que as surfaces sejam pintadas duas vezes por segundo
    if pintar_count >= 15:
        pintar_count = 0
