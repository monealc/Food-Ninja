import pygame, sys
import os
import random

vidas = 3
pontos = 0
alimentos = ['batata', 'berinjela', 'cebola', 'cenoura', 'coco', 
'laranja', 'lichia', 'pepino', 'pera', 'tomate', 'uva', 'bomba']

pygame.init()
pygame.mixer.init()
BACKGROUND_SOUND = pygame.mixer.Sound('sounds/abertura.mp3')
BACKGROUND_SOUND.play(-1)

LARGURA = pygame.display.Info().current_w
ALTURA = pygame.display.Info().current_h

FPS = 15

BRANCO = (255,255,255)

pygame.display.set_caption('Jogo - Food Ninja')
gameDisplay = pygame.display.set_mode((LARGURA, ALTURA))
tempo = pygame.time.Clock()

fundo = pygame.image.load('images/fundo.jpg')
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

capa = pygame.image.load('images/fundocapa.png')
capa = pygame.transform.scale(capa, (LARGURA, ALTURA))

font = pygame.font.Font(os.path.join(os.getcwd(), './comic.ttf'), 42)
pontuacao = font.render('Pontuação : ' + str(pontos), True, (255, 255, 255))


def gerar_alimentos_aleatorios(alimento):
    alimento_path = os.path.join('images', alimento + ".png")
    data[alimento] = {
        'img': pygame.image.load(alimento_path),
        'x' : random.randint(0, LARGURA - 100),
        'y' : ALTURA - 100,
        'speed_x': random.randint(-10,10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[alimento]['throw'] = True
    else:
        data[alimento]['throw'] = False

data = {}
for alimento in alimentos:
    gerar_alimentos_aleatorios(alimento)

def esconder_vidas(x, y):
    gameDisplay.blit(pygame.image.load('images/vidas_vermelhas.png'), (x, y))

font_name = pygame.font.match_font('comic.ttf')
def desenhar_texto(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BRANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

def desenhar_vidas(display, x, y, vidas, image) :
    for i in range(vidas) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

def tela_jogando():
    gameDisplay.blit(capa, (0, 0))
    if not jogando :
        BACKGROUND_SOUND.play(-1)
        gameDisplay.blit(fundo, (0,0))
        desenhar_texto(gameDisplay, "TENTE NOVAMENTE!", 90, LARGURA / 2, ALTURA / 4)
        desenhar_texto(gameDisplay,"Pontuação : " + str(pontos), 50, LARGURA / 2, ALTURA /2)

    desenhar_texto(gameDisplay, "Tecle para iniciar", 64, LARGURA / 2, ALTURA * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        tempo.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

primeiro_round = True
jogando = True
executando_jogo = True

while executando_jogo :
    if jogando :
        if primeiro_round :
            tela_jogando()
            primeiro_round = False
        jogando = False
        vidas = 3
        desenhar_vidas(gameDisplay, LARGURA - 150, 5, vidas, 'images/vidas_vermelhas.png')
        pontos = 0
        
        BACKGROUND_SOUND.stop()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            executando_jogo = False

    gameDisplay.blit(fundo, (0, 0))
    gameDisplay.blit(pontuacao, (100, 0))
    desenhar_vidas(gameDisplay, LARGURA - 150, 5, vidas,'images/vidas_vermelhas.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= LARGURA:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                gerar_alimentos_aleatorios(key)

            posicao_atual = pygame.mouse.get_pos()

            mouse_x = posicao_atual[0]
            mouse_y = posicao_atual[1]
            fruit_x = value['x']
            fruit_y = value['y']
            fruit_w = value['img'].get_width()
            fruit_h = value['img'].get_height()
            fruit_circle = pygame.Rect(fruit_x, fruit_y, fruit_w, fruit_h)
            mouse_circle = pygame.Rect(mouse_x, mouse_y, 25, 25)
            if fruit_circle.colliderect(mouse_circle) and not value['hit']:
                som = "sounds/corte.mp3"
                if key == 'bomba':
                    vidas -= 1
                    som = "sounds/bomba.mp3"
                    if vidas == 0:
                        esconder_vidas(LARGURA, 15)
                    elif vidas == 1 :
                        esconder_vidas(LARGURA, 15)
                    elif vidas == 2 :
                        esconder_vidas(LARGURA, 15)

                    if vidas <= 0 :
                        tela_jogando()
                        jogando = True
                    
                    metade_alimento_path = os.path.join('images', 'explosao.png')
                else:
                    metade_alimento_path = os.path.join('images', "metade_" + key + ".png") 

                value['img'] = pygame.image.load(metade_alimento_path)
                value['speed_x'] += 10

                som_corte = pygame.mixer.Sound(som)
                som_corte.play()

                if key != 'bomba' :
                    pontos += 1

                pontuacao = font.render('Pontuação : ' + str(pontos), True, (255, 255, 255))
                value['hit'] = True
        else:
            gerar_alimentos_aleatorios(key)

    pygame.display.update()
    tempo.tick(FPS)

pygame.quit()