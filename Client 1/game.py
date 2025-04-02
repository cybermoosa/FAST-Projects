import pygame
from network import Network
import time

tile_size = 25

class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(0,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 3
        self.color = color
        self.role = " " #runner or seeker

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
        if self.role == "seeker":
            pygame.draw.rect(g, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)  # 2 is the width of the outline
        elif self.role == "runner":
            pygame.draw.rect(g, (0, 0, 255), (self.x, self.y, self.width, self.height), 2)  # 2 is the width of the outline

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(100, 400, color = (0,0,0)) #
        self.player2 = Player(50,50) 
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.dirt_blocks = [(col * tile_size, row * tile_size) for row, data in enumerate(data) for col, tile in enumerate(data) if tile == 1]

    def display_start_message(self):
        """
        Display a message at the beginning of the game with player's role and color.
        """
        # Define messages based on player's role and color
        if self.player.role == "seeker":
            role_message = "You are the SEEKER      Colour is RED"
        elif self.player.role == "runner":
            role_message = "You are the RUNNER      Colour is BLUE"

        # Calculate the position to center the messages on the screen
        role_x = 20
        role_y = 0

        # Display messages on the canvas
        self.canvas.draw_text(role_message, 15, role_x, role_y)
        self.canvas.update()

    def run(self):
        clock = pygame.time.Clock()
        run = True
        game_over = False
        game_won = False
        
        role = self.receive_data()

        if role == "seeker":
            self.player.role = "seeker"
            self.player2.role = "runner"
        else:
            self.player.role = "runner"
            self.player2.role = "seeker"

        

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break

            if not game_over and not game_won:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_RIGHT]:
                    if self.player.x <= self.width - self.player.velocity:
                        self.player.move(0)

                if keys[pygame.K_LEFT]:
                    if self.player.x >= self.player.velocity:
                        self.player.move(1)

                if keys[pygame.K_UP]:
                    if self.player.y >= self.player.velocity:
                        self.player.move(2)

                if keys[pygame.K_DOWN]:
                    if self.player.y <= self.height - self.player.velocity:
                        self.player.move(3)


                if self.player.x < self.player2.x + self.player2.width and \
                    self.player.x + self.player.width > self.player2.x and \
                    self.player.y < self.player2.y + self.player2.height and \
                    self.player.y + self.player.height > self.player2.y:
            
                    if self.player.role == 'runner':
                        game_over = True
                     
                    if self.player.role == 'seeker':
                        game_won = True


                # Check for collision with dirt blocks
                for dirt_pos in self.dirt_blocks:
                    if self.player.x < dirt_pos[0] + tile_size and self.player.x + self.player.width > dirt_pos[0] and self.player.y < dirt_pos[1] + tile_size and self.player.y + self.player.height > dirt_pos[1]:
                        game_over = True
                    elif self.player2.x < dirt_pos[0] + tile_size and self.player2.x + self.player2.width > dirt_pos[0] and self.player2.y < dirt_pos[1] + tile_size and self.player2.y + self.player2.height > dirt_pos[1]:
                        game_won = True
                
                # Check for collision with grass blocks

                for tile in self.canvas.tile_list:
                    if tile[0] == self.canvas.grass_img:
                        if self.player.x < tile[1].x + tile_size and self.player.x + self.player.width > tile[1].x and self.player.y < tile[1].y + tile_size and self.player.y + self.player.height > tile[1].y:
                            #if self.player.role == 'runner':
                            game_over = True
                            
                        elif self.player2.x < tile[1].x + tile_size and self.player2.x + self.player2.width > tile[1].x and self.player2.y < tile[1].y + tile_size and self.player2.y + self.player2.height > tile[1].y:
                            #if self.player2.role == 'runner':
                            game_won = True
                            
                # Send Network Stuff
                self.player2.x, self.player2.y = self.parse_data(self.send_data())

                # Update Canvas

                self.canvas.draw_background()
                self.canvas.draw()
                self.player.draw(self.canvas.get_canvas())
                self.player2.draw(self.canvas.get_canvas())
                self.display_start_message()
                
                self.canvas.update()

            else:
                if game_over:
                    self.canvas.draw_text("Game Over", 40, self.width // 2 - 100, self.height // 2)
                    self.canvas.update()
                elif game_won:
                    self.canvas.draw_text("Game Won!", 40, self.width // 2 - 100, self.height // 2)
                    self.canvas.update()

        pygame.quit()
    

    def receive_data(self):

        reply = self.net.receive()
        print(reply)
        return reply.decode('utf-8')

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

        self.tile_list = []
        # Load images
        self.dirt_img = pygame.image.load('D:\\cn\\dirt.png')
        self.dirt_img = pygame.transform.scale(self.dirt_img, (tile_size, tile_size))

        self.grass_img = pygame.image.load('D:\\cn\\grass.png')
        self.grass_img = pygame.transform.scale(self.grass_img, (tile_size, tile_size))

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img_rect = self.dirt_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (self.dirt_img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    img_rect = self.grass_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (self.grass_img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))
        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])

    def draw_background(self):
        self.sky_img = pygame.image.load('D:\\cn\\sky.png')
        self.sky_img = pygame.transform.scale(self.sky_img, (500, 500))
        self.screen.blit(self.sky_img, (0, 0))
