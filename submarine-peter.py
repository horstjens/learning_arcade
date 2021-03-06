"""
submarine game
"""
import random
import arcade
import os
import math


class Torpedo(arcade.Sprite):

    def __init__(self):
        super().__init__(os.path.join("images", "laserRed16.png"), 1.0)
        self.center_x = MyGame.player.center_x
        self.center_y = MyGame.player.center_y
        self.change_x = 5
        MyGame.torpedo_list.append(self)

    def update(self):
        super().update()
        # make bubble
        if random.random() < 0.3:
            Bubble(center_x = self.center_x, center_y=self.center_y)

        if self.left > MyGame.screenwidth:
            print("killing torpedo")
            self.remove_from_sprite_lists()

class Bubble(arcade.Sprite):

    def __init__(self, center_x, center_y):
        super().__init__(os.path.join("images", "pool_cue_ball.png"), 0.1)
        self.center_x = center_x
        self.center_y = center_y
        self.age = 0
        self.max_age = 2 + random.random() * 3 # minimum 2 seconds, maximum 2+3=5 seconds
        self.start_ascending = random.random()*2.5  # 0 - 2.5
        MyGame.bubble_list.append(self)

    def on_update(self, delta_time):

        self.age += delta_time
        if self.age > self.start_ascending:
            self.change_y = 0.01 + random.random() * 0.2
        self.change_y *= 1.01
        self.change_y = min(3.5, self.change_y)
        super().update()
        super().on_update(delta_time)
        if self.center_y > MyGame.screenheight or self.age > self.max_age:
            self.remove_from_sprite_lists()

class Worm(arcade.Sprite):

    textures = []

    def __init__(self):
        super().__init__() #MyGame.textures["worm1"], 1.0)    # os.path.join("images", "wormGreen.png"), 1.0)
        self.texture = MyGame.textures["worm1"]
        self.center_x = MyGame.screenwidth + random.randint(100,200)
        self.center_y = random.randint(15, MyGame.screenheight - 15)
        self.change_x = - 0.1 - random.random() * 3
        self.age = 0
        self.i = 0
        self.animation_interval = 0.22

        MyGame.enemy_list.append(self)

    def on_update(self, delta_time):
        self.age += delta_time # self age in seconds

        i = int(self.age  / self.animation_interval) % 2 # because we have 2 images in the animation
        self.texture = (MyGame.textures["worm1"], MyGame.textures["worm2"])[i]
        #print("age", self.age, i)

        super().update()
        super().on_update(delta_time)
        self.change_y = math.sin(self.age)
        #pass

class Player(arcade.Sprite):

   def __init__(self):
       super().__init__(os.path.join("images", "uboot.png"), 0.3)
       self.center_x = 50
       self.center_y = 50
       MyGame.player_list.append(self)
       self.change_x = 0
       self.change_y = 0

   def update(self):
       super().update()
       #self.change_y *= 0.9
       #self.change_x *= 0.9
        # self.change_x += 0.1#Strömung
        # self.change_y *= 1.01#beschi**** Äh.... Beschleunigung >1
        # self.change_x *= 1.01
        # self.change_y *= 0.9#beschi**** Äh.... Bremsung <1
        # self.change_x *= 0.9


class MyGame(arcade.Window):
    """
    Main application class.
    """
    player_list = None
    #coin_list = None
    bubble_list = None
    torpedo_list = None
    enemy_list = None
    player = None
    screenwidth = 0
    screenheight = 0
    textures = {}

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)
        MyGame.screenwidth = width
        MyGame.screenheight = height

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Background image will be stored in this variable
        self.background = None

        # Variables that will hold sprite lists


        # Set up the player info
        #self.player_sprite = None
        self.score = 0
        self.score_text = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        MyGame.textures["worm1"] = arcade.load_texture(os.path.join("images", "wormGreen.png"))
        MyGame.textures["worm2"] = arcade.load_texture(os.path.join("images", "wormGreen_move.png"))
        #Worm.textures = [arcade.load_texture(os.path.join("images", "wormGreen.png")),
        #                 arcade.load_texture(os.path.join("images", "wormGreen_move.png"))]


    def setup(self):
        """ Set up the game and initialize the variables. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        # Image from:
        # http://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html
        # self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        self.background = arcade.load_texture(os.path.join("images", "wallpaper_b.jpg"))

        # Sprite lists
        MyGame.player_list = arcade.SpriteList()
        MyGame.enemy_list = arcade.SpriteList()
        #MyGame.coin_list = arcade.SpriteList()
        MyGame.bubble_list = arcade.SpriteList()
        MyGame.torpedo_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        MyGame.player = Player()
        # saturn_image = a   load_texture(os.path.join("images", "saturn.gif"))
        #for i in range(50):
            # Create the coin instance
            # coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            #coin = arcade.Sprite(os.path.join("images", "saturn.gif"), COIN_SCALING)
            ##coin = arcade.Sprite(textures = saturn_image, scale=COIN_SCALING)

            # Position the coin
            #coin.center_x = random.randrange(SCREEN_WIDTH)
            #coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            #self.coin_list.append(coin)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        scale = MyGame.screenwidth  / self.background.width
        #arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                    SCREEN_WIDTH, SCREEN_HEIGHT,
        #                                    self.background)

        # Draw all the sprites.d
        #self.coin_list.draw()
        self.player_list.draw()
        self.bubble_list.draw()
        self.torpedo_list.draw()
        self.enemy_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

    # def on_mouse_motion(self, x, y, dx, dy):
    #   """
    #  Called whenever the mouse moves.
    # """
    # self.player_sprite.center_x = x
    # self.player_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        print(button)

    def on_key_press(self, symbol, modifiers):
        print("key pressed", symbol)

        if symbol == arcade.key.SPACE:
            # fire torpedo
            Torpedo()

        if symbol == arcade.key.W: # or symbol == arcade.key.UP:
            self.player.change_y += 10
            #print("rauf")
            # arcade.play_sound(self.move_up_sound)
        if symbol == arcade.key.S : # or symbol == arcade.key.DOWN:
            self.player.change_y -= 10
        if symbol == arcade.key.A: # or symbol == arcade.key.LEFT:
            self.player.change_x -= 10
        if symbol == arcade.key.D: # or symbol == arcade.key.RIGHT:
            self.player.change_x += 10

    def on_key_release(self, symbol: int, modifiers: int):
        print("key released:", symbol)
        if symbol == arcade.key.W: # or symbol == arcade.key.UP:
            self.player.change_y -= 10
        if symbol == arcade.key.S:
            self.player.change_y += 10
        if symbol == arcade.key.A:  # or symbol == arcade.key.UP:
            self.player.change_x += 10
        if symbol == arcade.key.D:
            self.player.change_x -= 10

        #if symbol == arcade.key.W:
        #    self.player.cange_y = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on the coin sprites (The sprites don't do much in this
        # example though.)
        #self.coin_list.update()
        self.bubble_list.on_update(delta_time)
        self.torpedo_list.update()
        self.player_list.update()
        self.enemy_list.on_update(delta_time)
        # aging


        if random.random() < 0.01:
            Worm()
            print("Worm created")
        # Generate a list of all sprites that collided with the player.
        #hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        #for coin in hit_list:
            # create particles
        #    for _ in range(random.randint(3, 8)):
        #        particle = Particle(os.path.join("images", "sun.gif"),
        #                            random.random() * 0.15 + 0.03)  # scaling 0.01 ... 0.21
        #        particle.center_x = coin.center_x
        #        particle.center_y = coin.center_y
        #        particle.change_x = random.random() * 50 - 25
        #        particle.change_y = random.random() * 50 - 25
        #        particle.age = 0
        #        self.dust_list.append(particle)

        #    coin.remove_from_sprite_lists()
        #    self.score += 1


def main(width, height, title):
    """ Main method """
    window = MyGame(width, height, title)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main(width=1024, height=800, title="Peter's Submarine game")
