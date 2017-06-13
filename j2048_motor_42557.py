# -*- coding: utf-8 -*-
#
#ISEL - LEIM - MDP
#
#Motor do jogo 2048
#
#Autor: Diogo Milheiro nº:42557
#
#História:
#
#2015-11-10 Implementação da função direita
#2015-11-25 Implementação da função acima
#2015-12-03 Implementação da função abaixo
#           Implementação das funções da aula 7
#2015-12-08 Implementação de pygame
#2015-12-25 Limpeza de código do pygame
#2015-12-28 Aplicar funções da aula 7 à função acima e abaixo
#2016-01-11 Aplicar mais que uma musica e escolher uma delas aleatoriamente
#           Implementacao da funcao lugar que verifica o ranking do jogador
#2016-01-14 Eliminação do bug que devolvia mensagem cloud: jogo inválido
#2016-01-17 Últimos retoques

from random import random
from random import choice

grelha = [[0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0]]

fim = False
vitoria = False
pontos = 0
movimento = False

#função chamada de cada vez que uma tecla é pressionada para actualizar os numeros na grelha e verificar
#se o jogo já acabou
def actualizar_jogo():
    global fim
    if movimento == True:
        inserir_2ou4()
    posicoes_vazias = get_posicoes_vazias()
    if (len(posicoes_vazias)==0) and not(ha_iguais_adjacentes()):
        fim = True
    

def get_posicoes_vazias():
# não é preciso declarar grelha como global porque ela só vai ser lida

    posicoes_vazias = []

    for linha in range(len(grelha)):
        for coluna in range(len(grelha[linha])):
            if grelha[linha][coluna] == 0:
                posicoes_vazias.append([linha, coluna])
    return posicoes_vazias

def ha_iguais_adjacentes(): # aula 07
    ha = False
    # não é preciso testar se cada posição da grelha é diferente de
    # zero porque esta função só vai ser chamada quando a grelha está
    # cheia. Mas testar se cada posição da grelha é diferente de zero
    # facilita os testes
    
    # processar linhas
    for linha in range(len(grelha)):
        for coluna in range(len(grelha[linha])-1):
            if (grelha[linha][coluna] != 0) and (grelha[linha][coluna] == grelha[linha][coluna+1]):
                ha = True
    # processar colunas
    for coluna in range(len(grelha)):
        for linha in range(len(grelha[coluna])-1):
            if (grelha[linha][coluna] != 0) and (grelha[linha][coluna] == grelha[linha+1][coluna]):
                ha = True
    return(ha)

def get_2ou4():
    
    x = random()
    if x > 0.1:
        return 2
    else:
        return 4
                
def inserir_2ou4():
    # não é preciso declarar grelha como global porque a grelha é uma
    # lista e as listas são mutáveis. Como tal, os elementos das listas
    # que são variáveis globais podem ser alterados dentro de uma
    # função.
    
    dois_ou_quatro = get_2ou4()
    posicoes_vazias = get_posicoes_vazias()
    posicao_vazia = choice(posicoes_vazias)
    # índices da posição vazia
    
    indice_linha = posicao_vazia[0]
    indice_coluna = posicao_vazia[1]

    grelha[indice_linha][indice_coluna] = dois_ou_quatro

#função que move os valores para a esquerda sem os somar
def mover_esquerda(uma_lista):
    global movimento
    resultado = []
    for y in range(len(uma_lista)):
        if uma_lista[y] != 0:
            resultado.append(uma_lista[y])
    while len(resultado) < len(uma_lista):
        resultado.append(0)
    for y in range(len(uma_lista)):
        if uma_lista[y] != resultado[y]:
            movimento = True
    return(resultado)

#funcão que soma os valores iguais adjacentes a ser usada apos mover_esquerda()
def somar_esquerda(uma_lista):
    global movimento
    global pontos
    global vitoria
    resultado = []
    indice = 0
    while indice < len(uma_lista)-1:
        if uma_lista[indice] == uma_lista[indice+1]:
            soma = uma_lista[indice] + uma_lista[indice+1]
            resultado.append(soma)
            indice = indice + 2
            if soma > 0:
                movimento = True
                pontos = pontos + soma
                if soma == 2048:
                    vitoria = True
        else:
            resultado.append(uma_lista[indice])
            indice = indice + 1
    if indice == len(uma_lista)-1:
        resultado.append(uma_lista[indice])
    while len(resultado) < len(uma_lista):
        resultado.append(0)
    return(resultado)

#reverte as linhas para usar com a função direita
def reverte_linhas():
    global movimento
    global pontos
    global vitoria
    for i in range(4):
        #grelha[i] = grelha[i][::-1]
        grelha[i].reverse()
    return grelha

#troca as linhas com as colunas para usar com as funções acima e abaixo
def trocar_linhas_com_colunas():
    global grelha
    nova_grelha = []
    for i in range(4):
        nova_grelha.append([])
        for j in range(4):
            nova_grelha[i].append(grelha[j][i])
    grelha = nova_grelha
    return(grelha)

def esquerda():
    global movimento
    movimento = False
    for i in range(4):
        aux = mover_esquerda(grelha[i])
        nova_linha = somar_esquerda(aux)
        grelha[i] = nova_linha  # não é preciso declarar grelha como
                                # global porque grelha é uma
                                # lista. Como as listas são mutáveis,
                                # podem ser alteradas dentro de funções.
    actualizar_jogo() 
        
def direita():
    reverte_linhas()
    esquerda()
    reverte_linhas()

def acima():
    trocar_linhas_com_colunas()
    esquerda()
    trocar_linhas_com_colunas()
    
def abaixo():
    trocar_linhas_com_colunas()
    direita()
    trocar_linhas_com_colunas()

def valor(linha, coluna):
    linha_grelha = grelha[linha]
    return linha_grelha[coluna]

#função que controla o final do jogo. está a ser sempre chamada para verificar se o jogo já terminou
def terminou():
    global fim
    return fim

#função que controla o final do jogo. está a ser sempre chamada para verificar se o jogo já foi ganho
#o jogo é ganho quando um dos valores é 2048
def ganhou_ou_perdeu():
    global vitoria
    for i in range(4):
        for j in range(4):
            if valor(i,j) == 2048:
                vitoria = True
    return vitoria

def pontuacao():
    return pontos

#função chamada no ficheiro do modo gráfico para passar a variável fim a True e por consequente
#com a função terminou() chamar o final do jogo e o ecra de game over.
def terminar_jogo():
    global fim
    fim = True

#reinicialização das variáveis
def novo_jogo():
    global fim
    global vitoria
    global pontos
    global grelha

    grelha = [[0,0,0,0],
              [0,0,0,0],
              [0,0,0,0],
              [0,0,0,0]]
    fim = False
    vitoria = False
    pontos = 0
    

    inserir_2ou4()
    inserir_2ou4()
