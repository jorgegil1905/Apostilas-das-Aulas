#!/usr/bin/env python
# -*- coding: utf-8 -*-1


def menu():

    continuar = 1

    while continuar:

        continuar = int(input("0. Sair \n"+
                          "1. Jogar novamente\n" + "\nQual sua opção  : "))
        
        print('\n ')                      
        if continuar > 1:
            print("Voce saiu do Jogo...")
            print(' ')
            return

        if continuar:
            game()  
        else:
            print("Voce saiu do Jogo...")
            print(' ')
            return
def game(): 
    jogada=0

    while ganhou() == 0:
        print("\nJogador ", jogada%2 + 1)
        print(' ')
        exibe()
        linha  = int(input("\nLinha  : "))
        coluna = int(input("Coluna : "))

        if linha < 4:
            if coluna < 4:          
                if board[linha-1][coluna-1] == 0:
                    if(jogada%2+1)==1:
                        board[linha-1][coluna-1]=1
                    else:
                        board[linha-1][coluna-1]=-1
                else:
                    print("Local nao esta vazio")
                    jogada -=1
            else:        
                print("Colona inválida, tente novamente...")
                jogada -=1
        else:
            print("Linha inválida, tente novamente...")
            jogada -=1
        if ganhou():
            if(jogada%2+1)==1:
             board[linha-1][coluna-1]=1
            else:
             board[linha-1][coluna-1]=-1
            print(' ')
            exibe()
            print(' ')
            print("Jogador ",jogada%2 + 1," ganhou apos ", jogada+1," rodadas")
            print(' ' )
        jogada +=1
def ganhou():

#checando linhas
    for i in range(3):
        soma = board[i][0]+board[i][1]+board[i][2]
        if soma==3 or soma ==-3:
            return 1

 #checando colunas
    for i in range(3):
        soma = board[0][i]+board[1][i]+board[2][i]
        if soma==3 or soma ==-3:
            return 1

#checando diagonais
    diagonal1 = board[0][0]+board[1][1]+board[2][2]
    diagonal2 = board[0][2]+board[1][1]+board[2][0]
    if diagonal1==3 or diagonal1==-3 or diagonal2==3 or diagonal2==-3:
        return 1

    return 0
def exibe():
 
    linha = ' '
    for i in range(3):
    
        for j in range(3):
            
            if board[i][j] == 0:
                linha = linha + str(" _ ") 
            elif board[i][j] == 1:
                linha = linha + str(" X ")
            elif board[i][j] == -1:
                linha = linha + str(" 0 ")
        print(linha)
        linha = ' '
board= [ [0,0,0], [0,0,0], [0,0,0] ]


print(' ') 
menu()