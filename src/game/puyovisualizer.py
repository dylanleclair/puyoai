import sys
import pygame
import puyoenv
import random
import copy

def get_finished_player_count(players):
    playersDone = 0
    for player in players:
        if player.finished:
            playersDone+=1
    return playersDone

class Player(puyoenv.PuyoEnv):
    controller = {'left': pygame.K_LEFT,
                  'down': pygame.K_DOWN,
                  'right': pygame.K_RIGHT,
                  'roll': pygame.K_a}
    
class Game:
    
    def __init__(self, screen=(864, 480)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen)
        self.puyo = {'1': pygame.transform.scale(pygame.image.load('resource/r.png').convert_alpha(), (24, 24)),
                     '2': pygame.transform.scale(pygame.image.load('resource/g.png').convert_alpha(), (24, 24)),
                     '3': pygame.transform.scale(pygame.image.load('resource/b.png').convert_alpha(), (24, 24)),
                     '4': pygame.transform.scale(pygame.image.load('resource/y.png').convert_alpha(), (24, 24))}
        self.x = pygame.image.load('resource/x.png').convert_alpha()
        

        self.players = []

        for i in range(6):
            self.players.append(Player(x_offset= i * 6 * 24, y_offset=0))

        # draws a white background for each player
        self.screen.fill((255, 255, 255),
                         (self.players[0].offset[0], self.players[0].offset[1],
                          self.players[0].w * 24 * len(self.players), self.players[0].h * 24))

        for p in self.players:
            self.draw(p)

        pygame.display.update()
        self.clock = pygame.time.Clock()

    def draw(self, p):
        x_offset, y_offset = p.offset
        self.screen.blit(self.x, (x_offset + 2 * 24, y_offset + 1 * 24))
        for y, row in enumerate(p.board):
            for x, colour in enumerate(row):
                if colour != ' ':
                    self.screen.blit(self.puyo[colour], (x_offset + x * 24, y_offset + y * 24))
        if p.falling:
            for i in range(2):
                y, x = p.falling[i]['pos']
                if y >= 0 and x >= 0:
                    self.screen.blit(self.puyo[p.falling[i]['colour']], (x_offset + x * 24, y_offset + y * 24))

    def play(self):
        counter = 0
        # primary game loop
        while True:
            counter += 1 # counts ticks
            self.clock.tick(60) # 60ms between calls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if get_finished_player_count(self.players) < 3:
                for player in self.players:
                    if player.falling and not (counter % 3):
                        actions = player.act()
                        
                        col1, row1 = player.falling[0]['pos']
                        col2, row2 = player.falling[1]['pos']
                        if actions['left']:
                            if (row1 > 0 and player.board[col1][row1 - 1] == ' ') and (
                                    row2 > 0 and player.board[col2][row2 - 1] == ' '):
                                player.falling[0]['pos'] = (col1, row1 - 1)
                                player.falling[1]['pos'] = (col2, row2 - 1)
                        if actions['right']:
                            if (row1 < player.w - 1 and player.board[col1][row1 + 1] == ' ') and (
                                    row2 < player.w - 1 and player.board[col2][row2 + 1] == ' '):
                                player.falling[0]['pos'] = (col1, row1 + 1)
                                player.falling[1]['pos'] = (col2, row2 + 1)
                        if actions['down']:
                            if (col1 < player.h - 1 and player.board[col1 + 1][row1] == ' ') and (
                                    col2 < player.h - 1 and player.board[col2 + 1][row2] == ' '):
                                player.falling[0]['pos'] = (col1 + 1, row1)
                                player.falling[1]['pos'] = (col2 + 1, row2)
                        if actions['roll']:
                            col1, row1 = player.falling[0]['pos']
                            col2, row2 = player.falling[1]['pos']
                            a1 = col1 - col2
                            a2 = row1 - row2
                            if (row1 + a1 in (-1, player.w)) or col1 - a2 == player.h or \
                                    player.board[col1 - a2][row1 + a1] != ' ':
                                pass
                            else:
                                player.falling[1]['pos'] = (col1 - a2, row1 + a1)
                    if not (counter % 50): # updates the board
                        player.update(display=True)
                    # draws the screen
                    self.screen.fill((255, 255, 255),
                                    (player.offset[0],
                                    player.offset[1],
                                    player.w * 24,
                                    player.h * 24)
                                    )
                    # draws the player
                    self.draw(player)
                    pygame.display.update()
                    # reset frame counter
                    if counter == 300:
                        counter = 0
            else:

                for player in self.players:
                    player.net.set_fitness(player.score)

                # next generation baby
                self.players.sort(key=lambda x: x.net.fitness, reverse=False)

                # mutate
                midpoint = len(self.players) // 2
                
                fit = self.players[:midpoint]
                fit[0].net.save()
                index = midpoint
                # assign new values to nets
                while index < len(self.players):
                    # replace each unfit network with either a mutated or crossed-over copy of the fitter networks
                    local_player = random.choice(fit)
                    self.players[index].net =  copy.deepcopy(local_player.net)
                    self.players[index].net.mutate()
                
                # run again
                

if __name__ == '__main__':
    Game().play()

