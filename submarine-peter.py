"""
Sprite Collect Coins with Background

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins_background
"""
import random
import arcade
import os

PLAYER_SCALING = 0.5
COIN_SCALING = 1.0  # 0.25

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Submarine Peter"
MAXAGE = 1.3

class Torpedo(arcade.Sprite):

    def update(self):
        super().update()
        # kill self if reaching right screen border
        if self.left > 1200:
            self.remove_from_sprite_lists()



class Particle(arcade.Sprite):

    def update(self):
        #f self.age > 1:
        super().update()

        self.change_y += 0.1  # gravitation
        # self.change_y *= 1.01#beschi***** Äh.... Beschleunigung >1
        # self.change_x *= 1.01
        self.change_y *= 0.9  # beschi***** Äh.... Beschleunigung <1
        self.change_x *= 0.9
        # after 1 second, start climbing
        if self.age > MAXAGE:
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):


   def update(self):
       super().update()
       self.change_y *= 0.9
       self.change_x *= 0.9
        # self.change_x += 0.1#Strömung
        # self.change_y *= 1.01#beschi**** Äh.... Beschleunigung >1
        # self.change_x *= 1.01
        # self.change_y *= 0.9#beschi**** Äh.... Bremsung <1
        # self.change_x *= 0.9


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Background image will be stored in this variable
        self.background = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.dust_list = None
        self.torpedo_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        # Image from:
        # http://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html
        # self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        self.background = arcade.load_texture(os.path.join("images", "wallpaper_b.jpg"))

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.dust_list = arcade.SpriteList()
        self.torpedo_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player = Player(os.path.join("images", "uboot.png"), PLAYER_SCALING)
        self.player.center_x = 50
        self.player.center_y = 50
        self.player_list.append(self.player)
        # saturn_image = a   load_texture(os.path.join("images", "saturn.gif"))
        for i in range(50):
            # Create the coin instance
            # coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin = arcade.Sprite(os.path.join("images", "saturn.gif"), COIN_SCALING)
            ##coin = arcade.Sprite(textures = saturn_image, scale=COIN_SCALING)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        scale = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Draw all the sprites.
        self.coin_list.draw()
        self.player_list.draw()
        self.dust_list.draw()
        self.torpedo_list.draw()

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
            torpedo = Torpedo(os.path.join("images", "laserRed16.png"))
            torpedo.center_x = self.player.center_x + 50
            torpedo.center_y = self.player.center_y
            torpedo.change_x = 5
            torpedo.change_y = 0
            self.torpedo_list.append(torpedo)

        if symbol == arcade.key.W: # or symbol == arcade.key.UP:

            self.player.change_y = 10
            #print("rauf")
            # arcade.play_sound(self.move_up_sound)

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -50
            # arcade.play_sound(self.move_down_sound)


        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -50

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 50

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W: # or symbol == arcade.key.UP:

            self.player.change_y = 0


        #if symbol == arcade.key.W:
        #    self.player.cange_y = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on the coin sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.dust_list.update()
        self.torpedo_list.update()
        self.player_list.update()
        for p in self.dust_list:
            p.age += delta_time

        for torpedo in self.torpedo_list:
            # create bubbles
            if random.random() < 0.1:
                bubble = Particle(os.path.join("images", "sun.gif"),
                         random.random() * 0.15 + 0.03)  # scaling 0.01 ... 0.21
                bubble.center_x = torpedo.center_x
                bubble.center_y = torpedo.center_y
                bubble.change_x = 0
                bubble.change_y = random.random() * 10 + 5
                bubble.age = 0
                self.dust_list.append(bubble)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            # create particles
            for _ in range(random.randint(3, 8)):
                particle = Particle(os.path.join("images", "sun.gif"),
                                    random.random() * 0.15 + 0.03)  # scaling 0.01 ... 0.21
                particle.center_x = coin.center_x
                particle.center_y = coin.center_y
                particle.change_x = random.random() * 50 - 25
                particle.change_y = random.random() * 50 - 25
                particle.age = 0
                self.dust_list.append(particle)

            coin.remove_from_sprite_lists()
            self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
