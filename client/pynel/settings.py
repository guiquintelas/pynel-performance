import pygame
import os

WIDTH = 700
HEIGHT = 680
HEIGHT_SUR = 650
HEIGHT_MENU = 30
MARGIN = 20

pygame.init()
pygame.display.set_caption('Pynel de Performance')

fonte = pygame.font.SysFont('Verdana', 15)
small_fonte = pygame.font.SysFont('Verdana', 12)
small_fonte_bold = pygame.font.SysFont('Verdana', 12, bold=True)

folder_icon = pygame.image.load(os.path.join(os.getcwd(), '../assets', 'folder_icon.png'))
file_icon = pygame.image.load(os.path.join(os.getcwd(), '../assets', 'file_icon.png'))

BLACK_GRAY = (76, 76, 76)
BLACK_GRAY_LIGHT = (96, 96, 96)
BLACK = (28, 28, 28)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

rectSize = 10
init_height = 30
pad_mod = 40


