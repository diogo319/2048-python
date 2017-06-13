# -*- coding: iso-8859-15 -*-
#
#ISEL - LEIM - MDP
#
#Modo gráfico (Pygame) do jogo 2048
#
#Autor: Diogo Milheiro nº:42557
#

from j2048_motor_42557 import novo_jogo, valor, terminou, esquerda, direita, acima, abaixo, pontuacao, terminar_jogo, ganhou_ou_perdeu
from j2048_gestor_42557 import inicializa_semente, le_identificacao, regista_grelha_inicial, regista_jogada, regista_pontos, escreve_registo
from random import choice

#inicializa o pygame e o mixer para reproduzir música
import pygame
pygame.init()
pygame.mixer.init()

#definicoes gerais do pygame, tais como o tamanho da janelsa a ser apresentada,
#carregamento de algumas imagens para fazer blit mais a frente, definicao da frame rate a
#ser usada no jogo, definicao de algumas cores e fonts para texto a ser apresentado
#importacao de musicas de fundo
#Janela:
largura = 400
altura = 500
tamanho = (largura, altura)
janela = pygame.display.set_mode(tamanho)

novo_jogo_back = pygame.image.load("novo_jogo_back.png")

#Tempos:
frame_rate = 10
last_screen = 5000
first_screen = 3000
clock = pygame.time.Clock()
nova_frame = None


#Cores principais:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BACKGROUND = (0, 204, 255)
antialias = True


#Musicas de fundo:
string_musicas = []
for i in range(8):
    string_musicas.append(pygame.mixer.Sound("musica_fundo"+str(i+1)+".ogg"))


#Fonts:
novo_jogo_size = 14
novo_jogo_font = pygame.font.Font("numbers.ttf", novo_jogo_size)

numbers_size = 25
numbers_font = pygame.font.Font("numbers.ttf", numbers_size)

text_size = 20
text_font = pygame.font.Font("numbers.ttf", text_size)

titulo_size = 50
titulo_font = pygame.font.Font("numbers.ttf", titulo_size)


#Posições na janela dos varios valores
posicoes = []
for i in [150, 250, 350, 450]:
    for j in [40, 140, 240, 340]:
        posicoes.append((j,i))

#cria uma lista com todos os valores a imprimir       
valores = []
for i in range(4):
    for j in range(4):
        valores.append((i,j))

#cria uma lista com tuplos das possibilidades de valores e respectivas cores
#255,255,0 é vermelho. 255,0,0 é amarelo. Nesta função faz-se variar o valor de Green de forma a ter 12 valores entre o vermelho e o amarelo
colors = []
P = []
for i in range(12):
    colors.append((255,int(23.18*i),0))
    P.append(2**i)
colors = colors[::-1]

what_color = []
for i in range(11):
    what_color.append((colors[i],P[i+1]))


#retorna a que cor o numero é renderizado
def which_color(valor):
    if valor == 0:
        return BLACK
    else:
        for i in range(11):
            if valor == what_color[i][1]:
                return what_color[i][0]

#funcao que faz todas as operacoes de novo jogo associadas ao pygame e gestor,
#sendo assim mais facil chamar esta funcao de cada vez que se faz um novo jogo em vez
#de ter um bloco de codigo repetido inumeras vezes com o mesmo efeito.
def novo_jogo_pygame():
    nova_musica()
    inicializa_semente(None)
    novo_jogo()

    regista_grelha_inicial(valor(0,0),valor(0,1),valor(0,2),valor(0,3),
                           valor(1,0),valor(1,1),valor(1,2),valor(1,3),
                           valor(2,0),valor(2,1),valor(2,2),valor(2,3),
                           valor(3,0),valor(3,1),valor(3,2),valor(3,3))

#define a nova musica apartir das varias importadas no inicio do programa
def nova_musica():
    global aMusic
    aMusic = choice(string_musicas)
    aMusic.set_volume(0.5)
    aMusic.play(-1)

#funcao que faz todas as operacoes de fim de jogo associadas ao pygame e gestor,
#sendo assim mais facil chamar esta funcao de cada vez que se termina um jogo em vez
#de ter um bloco de codigo repetido inumeras vezes com o mesmo efeito.
#esta funcao faz tambem a renderizacao do ultimo ecra do jogo, que mostra uma mensagem
#de final de jogo e a pontuacao final do jogador e o ranking do mesmo.
def termina_jogo_pygame():
    global nova_frame
    global aMusic

    aMusic.fadeout(4000)
    regista_pontos(pontuacao())
    mensagem_cloud = escreve_registo()
    print(mensagem_cloud)
    nova_frame.fill(BACKGROUND)
    nova_frame.blit((numbers_font.render("Game Over", antialias, RED)),(125,215))
    nova_frame.blit((numbers_font.render(lugar(mensagem_cloud)+"º lugar!",antialias,RED)),(145,275))
    nova_frame.blit((numbers_font.render("Pontuação = "+str(pontuacao()),antialias,BLACK)),(30,450))
    janela.blit(nova_frame, (0,0))
    pygame.display.flip()
    pygame.time.delay(last_screen)


#funcao que verifica se o ranking do jogador tem um ou dois digitos e retorna o mesmo consoante o caso
def lugar(mensagem_cloud):
    if mensagem_cloud[44] == ' ':
        return str(mensagem_cloud[43])
    else:
        return (str(mensagem_cloud[43])+str(mensagem_cloud[44]))


#funcao que renderiza o primeiro ecra do jogo (splash screen). tem o titulo do jogo, instrucoes e
#uma mensagem de boa sorte. apos isto, faz um delay de 3 segundos de modo a esta mensagem aparecer
#essa duracao.
def primeiro_ecra():
    global nova_frame

    nova_frame = pygame.Surface(tamanho)
    nova_frame.fill(BACKGROUND)
    nova_frame.blit((titulo_font.render("2048", antialias, BLACK)),(125,200))
    nova_frame.blit((text_font.render("Use W, A, S, D para jogar", antialias, BLACK)),(60, 275))
    nova_frame.blit((text_font.render("Boa Sorte!", antialias, BLACK)),(145, 300))
    janela.blit(nova_frame, (0,0))
    pygame.display.flip()
    pygame.time.delay(first_screen)
                
#inicializa um novo jogo ao correr o programa
le_identificacao()
primeiro_ecra()
novo_jogo_pygame()

#funcao que faz a renderizacao de tudo o que aparece na janela de jogo excepto os valores
def print_HUD():
    global nova_frame

    nova_frame.fill(BACKGROUND)
    pontuacao_render = text_font.render("Pontuação = "+str(pontuacao()),antialias,BLACK)
    nova_frame.blit(pontuacao_render,(35,50))  
    nova_frame.blit(novo_jogo_back,(250,45))
    nova_frame.blit((novo_jogo_font.render("Novo Jogo",antialias,BACKGROUND)),(257,52))
    pygame.draw.line(nova_frame,BLACK,(25,215),(375,215),5)
    pygame.draw.line(nova_frame,BLACK,(25,315),(375,315),5)
    pygame.draw.line(nova_frame,BLACK,(25,415),(375,415),5)
    pygame.draw.line(nova_frame,BLACK,(100,150),(100,485),5)
    pygame.draw.line(nova_frame,BLACK,(200,150),(200,485),5)
    pygame.draw.line(nova_frame,BLACK,(300,150),(300,485),5)


#funcao que faz a renderizacao dos valores da grelha de jogo
def print_grelha():
    global nova_frame
       
    for i in range(16):
        nova_frame.blit((numbers_font.render(str(valor(valores[i][0],valores[i][1])), antialias, which_color(valor(valores[i][0],valores[i][1])))),posicoes[i])

def controlo():
    global fim
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminar_jogo()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] < 350 and pos[0] > 250:
                if pos[1] < 75 and pos[1] > 45:
                    termina_jogo_pygame()
                    novo_jogo_pygame()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                terminar_jogo()
            if event.key == pygame.K_a:
                esquerda()
                regista_jogada('a')
            if event.key == pygame.K_d:
                direita()
                regista_jogada('d')
            if event.key == pygame.K_w:
                acima()
                regista_jogada('w')
            if event.key == pygame.K_s:
                abaixo()
                regista_jogada('s')
            if event.key == pygame.K_n:
                termina_jogo_pygame()
                novo_jogo_pygame()


while not(terminou()):
    if (ganhou_ou_perdeu()):
        termina_jogo_pygame()
    else:    
        print_HUD()
        print_grelha()
        controlo()
        janela.blit(nova_frame, (0,0))
        pygame.display.flip()
        clock.tick(frame_rate)


if(terminou()):
    termina_jogo_pygame()

pygame.quit()
