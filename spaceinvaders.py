# coding: utf-8
from random import choice, randint
from math import ceil
import pygame
import os
   
  

####     Cores     ####
#       (R, G, B)
WHITE = (150, 150, 150)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
SPRINGREEN = (0, 250, 154)


####     TELA     ####
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


####     DIRETÓRIO     ####
# Comando para pegar o caminho onde a pasta do jogo está
DIRECTORY = os.getcwd()

####     FONTE     ####
FONT = DIRECTORY + "/fonts/space_invaders.ttf"


class Edge(pygame.sprite.Sprite):
    """
    Estrutura criada para facilitar a análise de colisões com as bordas.
    """

    def __init__(self, width, height, x, y):
        """
        Cria as bordas do jogo.

        width: largura da borda.
        height: altura da borda.
        x: posição no eixo x.
        y: posição no eixo y.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Block(pygame.sprite.Sprite):
    """
    Responsável por criar barreiras que protegem a nave.
    """

    def __init__(self, color = WHITE, size = 10):
        """
        Cria cada bloco com uma determinada cor e tamanho.

        color: cor que o bloco terá.
        size: tamanho de cada quadrado.
        """
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.size = size
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Ship(pygame.sprite.Sprite):
    """
    Classe que representa a nave do jogador.
    """
    
    def __init__(self, path, pos_x, pos_y, speed = 5):
        """
        Cria uma nave.
        
        path: caminho onde está a imagem que representa a nave.
        pos_x: posição inicial da nave no eixo x.
        pos_y: posição inicial da nave no eixo y.
        speed: velocidade que a nave se deslocará. Por padrão ela é 5px.
        """
        pygame.sprite.Sprite.__init__(self)
        self.__initial_position = (pos_x, pos_y)
        # Carregando a imagem da nave
        self.__image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.__image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        # A nave inicia com 3 vidas
        self.lifes = 3
        # Sons que a nave possui quando atira ou quando é atingida
        self.__sound_shot = pygame.mixer.Sound(DIRECTORY + "/sounds/shoot.wav")
        self.__ship_explosion = pygame.mixer.Sound(DIRECTORY + "/sounds/shipexplosion.wav")

    def initial_position(self):
        """
        Define as posições iniciais da nave.
        """
        self.rect.x = self.__initial_position[0]
        self.rect.y = self.__initial_position[1]

    def die(self):
        """
        Assim que a nave é atingida esse método é chamado para realizar as devidas
        ações que são necessárias. 
        As ações são: reproduzir o som de explosão definido na construção do objeto,
        retornar a nave à posição inicial e reduzir a sua quantidade de vidas.
        """
        self.__ship_explosion.play()
        self.initial_position()
        self.lifes -= 1

    def shoot(self):
        """
        Método que permite a nave atirar.
        Ao ser chamado é liberado o som de tiro e criado um projétil.
        """
        self.__sound_shot.play()
        bullet = Bullet(self.rect.midtop, 1)
        return bullet

    def update(self, *args):
        """
        Método que realiza a atualização da posição da nave à medida que o
        jogador a movimenta.
        """
        # Se estiver pressionando o botão da seta da direita
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.rect.right < (SCREEN_WIDTH - self.speed):
                self.rect.x += self.speed
        # Se estiver pressionando o botão da seta da esquerda
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.rect.left > self.speed:
                self.rect.x -= self.speed

    def __str__(self):
        """
        Representação textual do objeto, indicando a sua posição atual.
        """
        return "Ship in (%s, %s)" % (self.rect.x, self.rect.y)

class Invader(pygame.sprite.Sprite):
    """
    Classe que representa os invasores.
    """

    def __init__(self, sprite, pos_x, pos_y, speed = 1):
        """
        Método responsável por criar cada invasor.
        sprite: imagem que representa cada invasor.
        pos_x: posição inicial do invasor no eixo x.
        pos_y: posição inicial do invasor no eixo y.
        speed: velocidade em que cada objeto se movimenta.
         """  
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
     
    def shoot(self):
        """
        Metódo que permite cada invasor disparar.
        """
        bullet = Bullet(self.rect.midtop, -1, speed = 4, color = RED)
        return bullet
    
    def up_speed(self):
        """
        Aumenta a velocidade com que cada invasor se movimenta.
        """
        self.speed += 0.5
    
    def down_invader(self):
        """
        Método que movimenta as sprites ao longo do eixo y.
        """
        self.rect.y += 20

    def update(self, direction):
        """
        Método que movimentas as sprites ao longo do eixo x.
        """
        self.rect = self.rect.move(self.speed * direction, 0)

    def __str__(self):
        """
        Representação textual do objeto, indicando a sua posição atual.
        """
        return "Invader in (%s, %s)" % (self.rect.x, self.rect.y)


class Mystery(pygame.sprite.Sprite):
    """
    Classe que representa a Mystery do jogo tradicional.
    """

    def __init__(self, sprite, pos_x, pos_y, speed = 2.7):
        """
        Método responsável por criar a nave-mãe.

        sprite: imagem que representa a nave.
        pos_x: posição inicial da nave no eixo x.
        pos_y: posição inicial da nave no eixo y.
        speed: velocidade em que a nave se movimenta.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
        self.speed = speed
    
    def update(self, *args):
        if (self.rect.x >= (SCREEN_WIDTH + 200)):
            self.kill()
        else:
            self.rect = self.rect.move(self.speed, 0)

class Bullet(pygame.sprite.Sprite):
    """
    Classe que representa as balas de todos os objetos que realizam disparos.
    """

    def __init__(self, pos_xy, direction, color = SPRINGREEN, speed = 8):
        """
        Constrói um objeto do tipo Bullet.

        pos_xy: é o ponto (x, y) que é o ponto médio da borda superior
                da sprite.
        direction: direção que o objeto se deslocará.
        speed: velocidade que o objeto se deslocará.
                Por padrão é 8px.
        color: cor do objeto. 
                Por padrão é azul-marinho.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_xy[0]
        self.rect.y = pos_xy[1]
        self.direction = direction
        self.speed = speed * direction

    def update(self, *args):
        """
        Atualiza o objeto durante o seu deslocamento.
        """
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()


class SpaceInvaders():
    """
    Classe que comanda os principais comandos do jogo.
    """
    
    def __init__(self):
        """
        Permite criar uma instância do jogo.
        """
        # Definindo os caminhos dos arquivos necessários para o jogo
        self.ship_shot = pygame.sprite.GroupSingle()
        self.invader_shot = pygame.sprite.Group()

        """
        Para colocar em tela cheia usa o comando:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        """
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Coloca uma legenda para a janela
        pygame.display.set_caption("iNVASORES DO ESPACO")
        # Coloca um ícone na janela
        logo = pygame.image.load(DIRECTORY + "/images/logo.png")
        pygame.display.set_icon(logo)
        self.score = 0
        self.level = 0
        self.speed = 0
        '''
        Criando um objeto do tipo pygame.font.Font, onde é passada a fonte e o tamanho
        se a fonte for passada como None é utilizada a padrão do sistema.
        '''
        self.font = self.create_font(60)
        self.score_font = self.create_font(15)
        self.explosion_sound = pygame.mixer.Sound(DIRECTORY + "/sounds/invaderkilled.wav")
        
        # Carregando imagens necessárias
        self.path_image_ship = DIRECTORY + "/images/ship.png"
        background_image = pygame.image.load(DIRECTORY + "/images/back.png")
        explosion_image = pygame.image.load(DIRECTORY + "/images/explosion.png")
        lifes_image = pygame.image.load(DIRECTORY + "/images/heart.png")

        self.ship = pygame.sprite.GroupSingle(
                                Ship(self.path_image_ship, (SCREEN_WIDTH - 50) // 2, 
                                        (SCREEN_HEIGHT - 110)))
        self.ship_sprite = self.ship.sprites()[0]
        mystery_image = pygame.image.load(DIRECTORY + "/images/boss3.png")
        self.mystery_image = pygame.transform.scale(mystery_image, [71, 39])
        self.mystery = pygame.sprite.GroupSingle(
                                Mystery(self.mystery_image, self.random_position(), 15))
        self.background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.lifes_image = pygame.transform.scale(lifes_image, (25, 25))
        self.explosion_image = pygame.transform.scale(explosion_image, (
                                    (SCREEN_WIDTH // 20), (SCREEN_WIDTH // 20)))
        self.clock = pygame.time.Clock()
        self.invaders = pygame.sprite.OrderedUpdates()
    
        self.invaders_direction = 1
        self.increment_speed = False
        
        self.left_edge = pygame.sprite.GroupSingle(Edge(5, SCREEN_HEIGHT, 0, 0))
        self.right_edge = pygame.sprite.GroupSingle(Edge(5, SCREEN_HEIGHT, 795, 0))
        self.bottom_edge = pygame.sprite.GroupSingle(Edge(SCREEN_WIDTH, 5, 0, 560))
        self.groups = pygame.sprite.Group(self.ship_shot, self.invader_shot, 
                                    self.invaders, self.mystery)

     
    def random_position(self):
        """
        Escolhe aleatoriamente uma posição inicial no eixo x
        para a nave-mãe.
        """
        return choice([-1700, -1900, -2200, -2500, -1500])

    def home_screen(self):
        """
        Cria a tela inicial do jogo.
        """
        menu = True
        music_menu = pygame.mixer.Sound(DIRECTORY + "/sounds/menu.wav")
        music_menu.play(-1)
        
        text = self.font.render("SPACE INVADERS", True, RED)
        self.font = self.create_font(20)
        command1 = self.font.render(" TECLE ENTER  PARA INICIAR O JOGO ", True, WHITE, None)
        command2 = self.font.render(" PRESSIONE  ESC  PARA SAIR      ", True, WHITE, None)
        command1_rect = command1.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        command2_rect = command2.get_rect(center = ((SCREEN_WIDTH + 15) // 2, SCREEN_HEIGHT - 50))
        
        mystery = pygame.image.load(DIRECTORY + "/images/boss1.png")
        mystery = pygame.transform.scale(mystery, [110, 60])
        speed = [-5, 5]
        rect_mystery = mystery.get_rect()

        self.window.fill(BLACK)
        self.window.blit(text, [(SCREEN_WIDTH - 570) // 2, 50])
        self.window.blit(command1, command1_rect)
        self.window.blit(command2, command2_rect)
        pygame.display.update()

        while menu:
            # Mudando a direção que a nave se movimenta.
            if rect_mystery.left < 0 or rect_mystery.right > SCREEN_WIDTH:
                speed[0] = -speed[0]
            if rect_mystery.top < 0 or rect_mystery.bottom > SCREEN_HEIGHT:
                speed[1] = -speed[1]
            
            rect_mystery.x += speed[0]
            rect_mystery.y += speed[1]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    music_menu.stop()
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.start_game()
                        music_menu.stop()
                        return True

                    if event.key == pygame.K_ESCAPE:
                        music_menu.stop()
                        return False

            self.window.fill(BLACK)
            self.window.blit(mystery, rect_mystery)
            self.window.blit(text, [(SCREEN_WIDTH - 570) // 2, 50])
            self.window.blit(command1, command1_rect)
            self.window.blit(command2, command2_rect)
            self.clock.tick(60)
            pygame.display.update()
    
    def final_screen(self):
        """
        Cria a tela final do jogo.
        """
        music_menu = pygame.mixer.Sound(DIRECTORY + "/sounds/menu.wav")
        music_menu.play(-1)
        self.game_over_screen()

        self.font50 = self.create_font(50)
        self.font20 = self.create_font(20)

        text1 = self.font50.render("SEU PLACAR: %d" % self.score, True, GOLD)
        text2 = self.font20.render("PRESIONE  ENTER  PARA  JOGAR NOVAMENTE", True, WHITE)
        text3 = self.font20.render("PRESSIONE  ESC  PARA  ENCERRAR", True, WHITE)

        text1_rect = text1.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 350))
        text2_rect = text2.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        text3_rect = text3.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))

        self.window.fill(BLACK)
        self.window.blit(text1, text1_rect)
        self.window.blit(text2, text2_rect)
        self.window.blit(text3, text3_rect)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    music_menu.stop()
                    pygame.quit()
                    exit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        music_menu.stop()
                        self.level = 0
                        self.speed = 0
                        self.ship = pygame.sprite.GroupSingle(
                                Ship(self.path_image_ship, (SCREEN_WIDTH) // 2, (SCREEN_HEIGHT - 110)))
                        self.ship_sprite = self.ship.sprites()[0]
                        self.start_game()
                        return
						
                    if event.key == pygame.K_ESCAPE:
                        music_menu.stop()
                        pygame.quit()
                        exit()
        
    def level_screen(self):
        """
        Cria a tela que indica o nível que irá iniciar.
        Ela dura 1 segundo (1000 milisegundos).
        """
        self.level += 1
        if (self.level > 1 and self.level < 6):
            self.speed += 0.3
        elif (self.level == 1):
            self.speed += 1
        
        font = self.create_font(100)
        text = font.render('NIVEL : ' + str(self.level), True, GOLD)
        self.time = pygame.time.get_ticks()

        while ((pygame.time.get_ticks() - self.time) < 1000):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.window.blit(self.background, [0, 0])
            self.window.blit(text, [(SCREEN_WIDTH - 450) // 2, 220])
            pygame.display.update()
    
    def game_over_screen(self):
        """
        Cria a tela de game over.
        Ela dura 1.5 segundo (1500 milisegundos).
        """
        font = self.create_font(100)
        text = font.render('GAME OVER', True, RED)
        time = pygame.time.get_ticks()

        while ((pygame.time.get_ticks() - time) < 1500):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.window.blit(self.background, [0, 0])
            self.window.blit(text, [(SCREEN_WIDTH - 600) // 2, 220])
            pygame.display.update()

    def start_game(self):
        """
        Limpa todas as variáveis para que se possa iniciar o jogo.
        """
        self.groups.add(self.ship)
        self.invaders_direction = 1
        self.blocks = pygame.sprite.Group(self.build_blocks(0),
                                            self.build_blocks(1),
                                            self.build_blocks(2))
        self.invaders.empty()
        self.mystery.empty()
        self.invader_shot.empty()
        self.ship_shot.empty()
        self.level_screen()
        self.create_invaders()
        self.ship_sprite.initial_position()
        self.update()
	
    def build_blocks(self, number):
        """
        Constrói cada bloco que fica entre os invasores e a nave.
        Cada bloco é constituído de diversos pequenos blocos, o que facilita
        analisar as colisões.

        number: é o número do bloco, isso ajuda a indicar a posição
                que ele será construído.
        """
        aux = pygame.sprite.Group()
        for row in range(4):
            for column in range(10):
                blocker = Block()
                blocker.rect.x = 45 + (300 * number) + (column * blocker.size)
                blocker.rect.y = 400 + (row * blocker.size)
                aux.add(blocker)
        return aux

    def create_invaders(self):
        """
        Cria os invasores e coloca todos em um grupo.
        """
        enemy_types = []

        for i in range(1, 8):
            enemy_types.append(pygame.image.load(DIRECTORY + ("/images/invader%d.png" % (i % 2))))

        x = 25

        # Preenchendo os invasores pelas colunas.
        for j in range(7):
            y = 60
            for i in range(5):
                sprite = pygame.transform.scale(enemy_types[i], 
                                ((SCREEN_WIDTH // 20), (SCREEN_WIDTH // 20)))
                self.invaders.add(Invader(sprite, x, y, self.speed))
                y += 45
            x += 62

    def showShipLives(self):
        """
        Mostra na tela as vidas que a nave possui.
        """
        y = 10
        for i in range(self.ship_sprite.lifes):
            self.window.blit(self.lifes_image, (y, 570))
            y += 40

    def enemy_shot(self):
        """
        Escolhe aleatoriamente um invasor para que ele realize algum disparo.
        """
        enemy = [i for i in self.invaders]
        
        for i in range(2):
            invader = choice(enemy)
            self.invader_shot.add(invader.shoot())

    def update(self):
        """
        Realiza todas as atualizações necessárias para o jogo.
        """
        score = self.score_font.render("PLACAR : %d" % self.score, True, WHITE)

        current_time = pygame.time.get_ticks()

        if (current_time % 2000.0 < 20):
            self.enemy_shot()
        
        if ((len(self.mystery) == 0)):
            self.mystery.add(Mystery(self.mystery_image, self.random_position(), 15))

        self.window.blit(self.background, [0, 0])
        self.window.blit(score, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))
        self.groups.draw(self.window)
        self.blocks.draw(self.window)

        self.groups.update(self.invaders_direction)
        self.update_direction()
        self.check_collisions()
        self.showShipLives()

        self.groups = pygame.sprite.Group(self.ship, self.ship_shot, self.invader_shot, self.invaders, 
                                    self.left_edge, self.bottom_edge, self.right_edge, self.mystery)
        self.clock.tick(60)
        pygame.display.update()
    
    def check_collisions(self):
        """
        Realiza todas as checagens de colisões do jogo e as suas 
        consequências.
        """

        """
        Se ocorrer uma colisão entre os projéteis da nave e de algum
        invasor ambas são mortas e ocorre um acréscimo de um valor entre
        5 e 20 na pontuação do jogador.
        """
        if pygame.sprite.groupcollide(self.ship_shot, self.invader_shot, True, True):
            self.score += randint(5, 20)
        
        # Colisão entre as balas e a borda inferior, apenas os disparos são mortos.
        pygame.sprite.groupcollide(self.invader_shot, self.bottom_edge, True, False)
        # Colisão entre os disparos dos invasores e os blocos, ambos morrem.
        pygame.sprite.groupcollide(self.invader_shot, self.blocks, True, True)
        # Colisão entre o disparo da nave e os blocos, ambos morrem.
        pygame.sprite.groupcollide(self.ship_shot, self.blocks, True, True)
        # Colisão entre os blocos e os invasores, apenas os blocos morrem.
        pygame.sprite.groupcollide(self.blocks, self.invaders, True, False)
        
        # Colisão entre a nave e os invasores
        if pygame.sprite.groupcollide(self.ship, self.invaders, False, False):
            self.ship_sprite.die()
        
        # Colisão entre a nave-mãe e o tiro da nave. A pontuação será um valor entre 25 e 55.
        if pygame.sprite.groupcollide(self.mystery, self.ship_shot, True, True):
            self.score += choice([25, 35, 45, 55])


        
        '''
        Colisão entre os disparos da nave e os invasores, ambos morrem.
        Além disso é colocado a imagem, o som de explosão e um acréscimo
        na pontuação podendo ser [10, 15, 20, 25, 30, 35, 40].
        '''
        
        for atingidos in pygame.sprite.groupcollide(self.ship_shot, self.invaders, True, True).values():
            self.explosion_sound.play()
            
            self.window.blit(self.explosion_image, (240, 240))
                     
            for invasor in atingidos:
                #explosion_image = pygame.image.load(DIRECTORY + "/images/explosion.png")
                #self.window.blit(self.explosion_image, (invasor.rect.x, invasor.rect.y))
                self.explosion_sound.play()
                #self.window.blit(self.explosion_image, (invasor.rect.x, invasor.rect.y))
                self.score += choice([10, 15, 20, 25, 30, 35, 40])
        
        # Verifica a colisão dos disparos realizados pelos invasores e a nave. Apenas o tiro morre.
        if (pygame.sprite.groupcollide(self.ship, self.invader_shot, False, True)):
            self.explosion_sound.play()
            #self.window.blit(self.explosion_image, (self.ship_sprite.rect.x, self.ship_sprite.rect.y))
            self.ship_sprite.die()

    def update_direction(self):
        """
        Atualiza a direção dos invasores.
        Já que os invasores são colocados na tela coluna a coluna é possível 
        saber quem são os primeiros e os últimos que foram inseridos para poder
        controlar os limites da tela.
        """
        arr = self.invaders.sprites()
        first = arr[0]
        last = arr[-1]
        
        if ((last.rect.x > (SCREEN_WIDTH - last.rect.width - 10)) or (first.rect.x < 10)):
            self.invaders_direction *= -1
            current_time = pygame.time.get_ticks()
            if (current_time - self.time > (8000 // self.speed)):
                self.down_invader(arr)
    
    def down_invader(self, arr):
        """
        Movimenta cada invasor pelo eixo y.
        """
        up_speed = (len(self.invaders) <= 8)

        for enemy in arr:
            if up_speed:
                enemy.up_speed()
            enemy.down_invader()

    def create_font(self, size):
        return pygame.font.Font(FONT, size)

    def main(self):
        """
        Método principal do jogo.
        """

        # Variável necessária para que o loop onde o jogo ocorre dure o tempo necessário.
        run = True
        menu = True
        
        while menu:
            command = self.home_screen()

            if not command:
                menu = False
                pygame.quit()
                exit()
        
            while run:
                if self.ship_sprite.lifes <= 0:
                    self.final_screen()
                    self.score = 0
                elif len(self.invaders) == 0:
                    self.start_game()
                else:
                    for event in pygame.event.get():
                        # Verificando se o usuário clicou na opção de fechar a janela.
                        if event.type == pygame.QUIT:
                            run, menu = False, False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                run, menu = False, False
                            if ((event.key == pygame.K_UP or event.key == pygame.K_SPACE) and not self.ship_shot):
                                self.ship_shot.add(self.ship_sprite.shoot())

                    self.update()

if __name__ == "__main__":
    # Comando necessário para se inicializar os módulos do Pygame
    pygame.init()
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.mixer.init(22050, -16, 2, 1024)
    game = SpaceInvaders()
    game.main()
    explosion_image = pygame.image.load(DIRECTORY + "/images/explosion.png")
    self.window.blit(explosion_image, 40, 40)
  
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # Comando que encerra os módulos do Pygame
    pygame.quit()
