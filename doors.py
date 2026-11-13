"""
    author: Ronald Kaiser
    e-mail: raios DOT catodicos AT gmail DOT com
"""

import random

import arcade


# CONSTANTS
VIRTUAL_WIDTH  = 1280 
VIRTUAL_HEIGHT = 720
VIRTUAL_ASPECT = VIRTUAL_WIDTH / VIRTUAL_HEIGHT
SCREEN_TITLE  = "doors"

SPRITE_SCALING        = 1
PLAYER_RADIUS         = 13
PLAYER_VELOCITY_X     = 7
PLAYER_VELOCITY_Y     = 7 
LEFT_BORDER           = 50
RIGHT_BORDER          = VIRTUAL_WIDTH - 50
TOP_BORDER            = VIRTUAL_HEIGHT - 100
BOTTOM_BORDER         = 50
KEY_WIDTH             = 15
KEY_HEIGHT            = 20 
WALL_VERTICAL_WIDTH   = 25
WALL_VERTICAL_HEIGHT  = 25
WALL_HORIZONTAL_WIDTH = 25
WALL_HORIZONTAL_HEIGHT= 25
TILE_SIZE             = 100 
PORTAL_RADIUS         = 20
WALL_COLOR            = (100, 100, 230, 255)
BORDER_COLOR          = WALL_COLOR
DIAMOND_COLOR         = arcade.color.CYAN
DIAMOND_SIZE          = 15



class MainMenu(arcade.View):
    def on_show_view(self):
        """Called once when we switch to this view."""
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        arcade.resources.load_kenney_fonts()

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(
            arcade.rect.XYWH(500, 900, 500, 600), 
            (76,35,101, 255)
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(0, 300, 100, 600), 
            (76,35,101, 255)
        )

        arcade.draw_text(
            "d", 
            self.window.width / 2 - 250, 
            self.window.height / 2 - 50,
            arcade.color.YELLOW,
            rotation=10,
            font_size=200, 
            bold=True,
            anchor_x="center",
            font_name="Kenney Pixel"
        )

        arcade.draw_text(
            "o", 
            self.window.width / 2 - 100, 
            self.window.height / 2 - 50,
            arcade.color.RED,
            rotation=5,
            font_size=200, 
            bold=True,
            anchor_x="center",
            font_name="Kenney Pixel"
        )

        arcade.draw_text(
            "o", 
            self.window.width / 2 + 50, 
            self.window.height / 2 - 50,
            arcade.color.GREEN,
            rotation=-10,
            font_size=200, 
            bold=True,
            anchor_x="center",
            font_name="Kenney Pixel"
        )

        arcade.draw_text(
            "r", 
            self.window.width / 2 + 120, 
            self.window.height / 2 - 50,
            arcade.color.BLUE,
            rotation=10,
            font_size=200, 
            bold=True,
            anchor_x="center",
            font_name="Kenney Pixel"
        )

        arcade.draw_text(
            "s", 
            self.window.width / 2 + 230, 
            self.window.height / 2 - 50,
            arcade.color.PURPLE,
            rotation=5,
            font_size=200, 
            bold=True,
            anchor_x="center",
            font_name="Kenney Pixel"
        )

        arcade.draw_text(
            "by Ronald Kaiser",
            self.window.width / 2 + 200,
            self.window.height / 2 - 80,
            arcade.color.GRAY, 
            font_size=15, 
            anchor_x="center",
            font_name="helvetica"
        )
        
        arcade.draw_text(
            "press \"return\" to start",
            self.window.width / 2,
            self.window.height / 2 - 250,
            arcade.color.WHITE, 
            font_size=20, 
            anchor_x="center",
            font_name="helvetica"
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(400, 200, 100, 50), 
            arcade.color.RED
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(650, 200, 100, 50), 
            arcade.color.BLUE
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(900, 200, 100, 50), 
            arcade.color.GREEN
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            game_view = get_next_level(1) 
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            self.window.close()


class FloatingText:
    def __init__(self, text, x, y, size=14, duration=1.0):
        self.text = text
        self.x = x
        self.y = y
        self.change_y = 0.5  # Speed at which it floats up
        self.alpha = 255  # Opacity for fading effect (255 = solid, 0 = invisible)
        self.timer = duration  # Duration in seconds before it disappears
        self.size = size

    def update(self, delta_time):
        self.y += self.change_y
        self.timer -= delta_time
        # Fade out gradually as timer drops
        if self.timer <= 0.5:
            self.alpha = max(0, int(255 * (self.timer / 0.5)))

    def draw(self):
        # Color with alpha for fading (R, G, B, Alpha)
        color = (255, 255, 255, self.alpha)
        arcade.draw_text(self.text, self.x, self.y, color, font_size=self.size, bold=True, font_name="Montserrat")


class Player(arcade.SpriteCircle):
    def update(self, delta_time):
        pass


class KeySprite(arcade.SpriteSolidColor):
    def __init__(self, width, height, center_x, center_y, color):
        super().__init__(width, height)
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.positions = [center_y, center_y - 2, center_y, center_y + 2]
        self.cur_position = 0
        self.last_time = None
        self.animation_timer = 0

    def update(self, delta):
        self.animation_timer += delta

        if self.animation_timer >= 0.1:
            self.cur_position = (self.cur_position + 1) % 4
            self.center_y = self.positions[self.cur_position]

            self.animation_timer -= 0.1


class DiamondSprite(arcade.SpriteSolidColor):
    def __init__(self, width, height, center_x, center_y, color, angle, visible):
        super().__init__(width, height)
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.widths = [width, width - 5, width, width + 5]
        self.angle = angle
        self.visible = visible
        self.cur_position = random.randrange(0, len(self.widths))
        self.last_time = None
        self.animation_timer = 0

    def update(self, delta):
        self.animation_timer += delta

        if self.animation_timer >= 0.1:
            self.cur_position = (self.cur_position + 1) % 4
            self.width = self.widths[self.cur_position]

            self.animation_timer -= 0.1


class KeyCollectedSprite(arcade.SpriteSolidColor):
    def __init__(self, width, height, center_x, center_y, color):
        super().__init__(width, height)
        self.center_x = center_x
        self.center_y = center_y
        self.color = color


class Level(arcade.View):
    def __init__(self, level, data):
        super().__init__()

        self.data = data

        # flags
        self.game_over = False
        self.starting = True

        # keys pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # music/sounds
        self.music = arcade.Sound(":resources:music/1918.mp3", streaming=True)
        self.music_player = self.music.play()
        self.key_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        self.diamond_sound = arcade.load_sound(":resources:sounds/coin3.wav")
        self.portal_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover3.wav")

        # level
        self.set_level(level)

        # sprites
        # background
        self.background_list = arcade.SpriteList()
        self.populate_background()

        # border
        self.border_list = arcade.shape_list.ShapeElementList()
        self.populate_border()

        # walls
        self.wall_list = arcade.SpriteList()
        positions = self.data["walls"] 
        self.populate_walls(positions)

        # blue doors
        self.blue_doors = arcade.SpriteList()
        positions = self.data["blue_doors"] 
        self.populate_blue_doors(positions)

        # red doors
        self.red_doors = arcade.SpriteList()
        positions = self.data["red_doors"] 
        self.populate_red_doors(positions)

        # green doors
        self.green_doors = arcade.SpriteList()
        positions = self.data["green_doors"] 
        self.populate_green_doors(positions)

        # player
        self.player_list = arcade.SpriteList()
        position = self.data["player"] 
        self.player_list = arcade.SpriteList()
        self.populate_player(position)

        # portals
        self.portals_list = arcade.SpriteList()
        positions = self.data["portals"] 
        self.portals_list = arcade.SpriteList()
        self.populate_portals(positions)

        # keys
        self.keys_list = arcade.SpriteList()
        # red key
        position = self.data["red_key"]
        self.populate_red_key(position)

        # blue key
        position = self.data["blue_key"]
        self.populate_blue_key(position)

        # green key
        position = self.data["green_key"]
        self.populate_green_key(position)

        # keys collected
        self.keys_collected_list = arcade.SpriteList()
        self.populate_keys_collected()

        # goal
        position = self.data["goal"]
        self.populate_goal(position)

        # diamonds
        self.diamonds_list = arcade.SpriteList()
        positions = self.data["diamonds"] 
        self.populate_diamonds(positions)

        # text
        self.floating_texts_list = [] 

    def setup(self):
        self.score = 0

    def set_level(self, level):
        self.level = level

    def populate_border(self):
        rect_outline = arcade.shape_list.create_rectangle_outline(
            center_x=VIRTUAL_WIDTH // 2, center_y=VIRTUAL_HEIGHT // 2 - 25, 
            width=VIRTUAL_WIDTH - 50, height=VIRTUAL_HEIGHT - 100, 
            color=BORDER_COLOR, 
            border_width=25
        )
        self.border_list.append(rect_outline)

    def populate_background(self):
        # background
        i = 0
        for x in range(75, VIRTUAL_WIDTH-40, TILE_SIZE):
            j = 0 if i % 2 == 0 else 1
            for y in range(75, VIRTUAL_HEIGHT-75, TILE_SIZE):
                tile = arcade.SpriteSolidColor(
                    width=TILE_SIZE,
                    height=TILE_SIZE,
                    color=(25,25,112,100) if j % 2 == 0 else (40,40,100,100) 
                )
                tile.angle = 45
                tile.center_x = x
                tile.center_y = y
                self.background_list.append(tile)
                j += 1
            i += 1

    def populate_walls(self, positions):
        for (x, y) in positions:
            wall = arcade.SpriteSolidColor(
                width=WALL_VERTICAL_WIDTH,
                height=WALL_VERTICAL_HEIGHT,
                color=WALL_COLOR
            )
            wall.center_x = x
            wall.center_y = y
            self.wall_list.append(wall)

    def populate_blue_doors(self, positions):
        for (x, y) in positions:
            door = arcade.SpriteSolidColor(
                width=WALL_VERTICAL_WIDTH,
                height=WALL_VERTICAL_HEIGHT,
                color=arcade.color.BLUE
            )
            door.center_x = x
            door.center_y = y
            self.blue_doors.append(door)

    def populate_red_doors(self, positions):
        for (x, y) in positions:
            door = arcade.SpriteSolidColor(
                width=WALL_VERTICAL_WIDTH,
                height=WALL_VERTICAL_HEIGHT,
                color=arcade.color.RED
            )
            door.center_x = x
            door.center_y = y
            self.red_doors.append(door)

    def populate_green_doors(self, positions):
        for (x, y) in positions:
            door = arcade.SpriteSolidColor(
                width=WALL_VERTICAL_WIDTH,
                height=WALL_VERTICAL_HEIGHT,
                color=arcade.color.GREEN
            )
            door.center_x = x
            door.center_y = y
            self.green_doors.append(door)

    def populate_player(self, position):
        self.player_sprite = Player(
            radius=PLAYER_RADIUS,
            color=arcade.color.YELLOW,
            soft_gradient=True,
        ) 
        self.player_sprite.center_x = position[0] 
        self.player_sprite.center_y = position[1] 
        self.player_list.append(self.player_sprite)

    def populate_portals(self, positions):
        # portal 1
        self.portal1_sprite = arcade.SpriteCircle(
            radius=PORTAL_RADIUS,
            color=arcade.color.ORANGE,
            soft_gradient=True
        )
        self.portal1_inner_sprite = arcade.SpriteCircle(
            radius=PORTAL_RADIUS - 5,
            color=arcade.color.BLACK,
            soft_gradient=True
        )
        self.portal1_sprite.center_x = positions[0][0]
        self.portal1_sprite.center_y = positions[0][1]
        self.portal1_inner_sprite.center_x = positions[0][0] 
        self.portal1_inner_sprite.center_y = positions[0][1]
        self.portals_list.append(self.portal1_sprite)
        self.portals_list.append(self.portal1_inner_sprite)

        # portal 2
        self.portal2_sprite = arcade.SpriteCircle(
            radius=PORTAL_RADIUS,
            color=arcade.color.CYAN,
            soft_gradient=True
        )
        self.portal2_inner_sprite = arcade.SpriteCircle(
            radius=PORTAL_RADIUS - 5,
            color=arcade.color.BLACK,
            soft_gradient=True
        )
        self.portal2_sprite.center_x = positions[1][0] 
        self.portal2_sprite.center_y = positions[1][1]
        self.portal2_inner_sprite.center_x = positions[1][0]
        self.portal2_inner_sprite.center_y = positions[1][1]
        self.portals_list.append(self.portal2_sprite)
        self.portals_list.append(self.portal2_inner_sprite)
        self.portal1_available = True
        self.portal2_available = True

    def populate_red_key(self, position):
        self.red_key_sprite = KeySprite(
            width=KEY_WIDTH,
            height=KEY_HEIGHT,
            color=arcade.color.RED,
            center_x = position[0],
            center_y = position[1]
        )
        self.red_key_sprite.visible = True 
        self.keys_list.append(self.red_key_sprite)

    def populate_green_key(self, position):
        self.green_key_sprite = KeySprite(
            width=KEY_WIDTH,
            height=KEY_HEIGHT,
            color=arcade.color.GREEN,
            center_x = position[0],
            center_y = position[1]
        )
        self.green_key_sprite.visible = True 
        self.keys_list.append(self.green_key_sprite)

    def populate_blue_key(self, position):
        self.blue_key_sprite = KeySprite(
            width=KEY_WIDTH,
            height=KEY_HEIGHT,
            color=arcade.color.BLUE,
            center_x = position[0],
            center_y = position[1]
        )
        self.blue_key_sprite.visible = True 
        self.keys_list.append(self.blue_key_sprite)

    def populate_keys_collected(self):
        # red key
        self.red_key_collected_sprite = KeyCollectedSprite(
            width=KEY_WIDTH,
            height=KEY_HEIGHT,
            center_x = 270,
            center_y = VIRTUAL_HEIGHT - 35,
            color=arcade.color.GRAY
        )
        self.keys_collected_list.append(self.red_key_collected_sprite)

        # blue key
        self.blue_key_collected_sprite = KeyCollectedSprite(
            width=KEY_WIDTH,
            height=KEY_HEIGHT,
            color=arcade.color.GRAY,
            center_x = 320,
            center_y = VIRTUAL_HEIGHT - 35
        )
        self.keys_collected_list.append(self.blue_key_collected_sprite)

        # green_key
        self.green_key_collected_sprite = KeyCollectedSprite(
            width=KEY_WIDTH,
            height=KEY_HEIGHT,
            color=arcade.color.GRAY,
            center_x = 370,
            center_y = VIRTUAL_HEIGHT - 35
        )
        self.keys_collected_list.append(self.green_key_collected_sprite)

    def populate_goal(self, position):
        self.goal_sprite = arcade.SpriteCircle(
            radius=PORTAL_RADIUS,
            color=arcade.color.PURPLE,
            soft_gradient=True
        )
        self.goal_inner_sprite = arcade.SpriteCircle(
            radius=PORTAL_RADIUS - 5,
            color=arcade.color.BLACK,
            soft_gradient=True
        )
        self.goal_sprite.center_x = position[0]
        self.goal_sprite.center_y = position[1]
        self.goal_inner_sprite.center_x = position[0] 
        self.goal_inner_sprite.center_y = position[1]
        self.portals_list.append(self.goal_sprite)
        self.portals_list.append(self.goal_inner_sprite)

    def populate_diamonds(self, positions):
        for (x, y) in positions:
            diamond = DiamondSprite(
                width=DIAMOND_SIZE,
                height=DIAMOND_SIZE,
                color=DIAMOND_COLOR,
                angle=45,
                center_x=x,
                center_y=y,
                visible=True
            )
            self.diamonds_list.append(diamond)

    def on_key_press(self, key, modifiers):
        """Switch back to the main menu if ESC is pressed."""
        if key == arcade.key.ESCAPE:
            menu_view = MainMenu()
            self.music.stop(self.music_player)
            self.window.show_view(menu_view)

        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        print(f"mouse position: ({x}, {y})")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        if self.starting:
            floating_text = FloatingText(f"Level {self.level}", VIRTUAL_WIDTH // 2 - 150, VIRTUAL_HEIGHT // 2, size=50, duration=1.5)
            self.floating_texts_list.append(floating_text)
            self.starting = False

        self.clear()
        arcade.draw_text(
            f"score: {self.score}", 20, self.window.height - 40, arcade.color.WHITE, 14
        )
        arcade.draw_text(
            "keys:", 200, self.window.height - 40, arcade.color.WHITE, 14
        )
        self.background_list.draw()
        self.blue_doors.draw()
        self.green_doors.draw()
        self.red_doors.draw()
        self.keys_collected_list.draw()
        self.wall_list.draw()
        self.keys_list.draw()
        self.portals_list.draw()
        self.diamonds_list.draw()
        self.player_list.draw()
        self.border_list.draw()
        for floating_text in self.floating_texts_list:
            floating_text.draw()

    def on_update(self, delta_time):
        if self.game_over:
            all_sprites = []
            for _, attr_value in vars(self).items():
                if isinstance(attr_value, arcade.SpriteList):
                    for sprite in attr_value:
                        all_sprites.append(sprite)

            if all_sprites:
                sprite = all_sprites.pop()
                sprite.remove_from_sprite_lists()
            else:
                new_level = get_next_level(self.level + 1) 
                if not new_level:
                    new_level = MainMenu()
                    self.window.show_view(new_level)
                    return
                new_level.setup()
                self.window.show_view(new_level)
            return
        
        went_left = False
        went_right = False
        went_up = False
        went_down = False
        if self.left_pressed and not self.right_pressed:
            went_left = True
            self.player_sprite.center_x -= PLAYER_VELOCITY_X 
        if self.right_pressed and not self.left_pressed:
            went_right = True
            self.player_sprite.center_x += PLAYER_VELOCITY_X
        if self.up_pressed and not self.down_pressed:
            went_up = True
            self.player_sprite.center_y += PLAYER_VELOCITY_Y
        if self.down_pressed and not self.up_pressed:
            went_down = True
            self.player_sprite.center_y -= PLAYER_VELOCITY_Y

        if arcade.check_for_collision_with_list(self.player_sprite, self.wall_list):
            if went_up: self.player_sprite.center_y -= PLAYER_VELOCITY_Y
            if went_down: self.player_sprite.center_y += PLAYER_VELOCITY_Y
            if went_left: self.player_sprite.center_x += PLAYER_VELOCITY_X 
            if went_right: self.player_sprite.center_x -= PLAYER_VELOCITY_X

        if arcade.check_for_collision_with_lists(self.player_sprite, [self.blue_doors, self.red_doors, self.green_doors]):
            if went_up: self.player_sprite.center_y -= PLAYER_VELOCITY_Y
            if went_down: self.player_sprite.center_y += PLAYER_VELOCITY_Y
            if went_left: self.player_sprite.center_x += PLAYER_VELOCITY_X 
            if went_right: self.player_sprite.center_x -= PLAYER_VELOCITY_X
            
        if self.player_sprite.center_y > TOP_BORDER:
            self.player_sprite.center_y = TOP_BORDER
        if self.player_sprite.center_y < BOTTOM_BORDER:
            self.player_sprite.center_y = BOTTOM_BORDER
        if self.player_sprite.center_x > RIGHT_BORDER:
            self.player_sprite.center_x = RIGHT_BORDER
        if self.player_sprite.center_x < LEFT_BORDER:
            self.player_sprite.center_x = LEFT_BORDER

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.diamonds_list)
        for diamond in hit_list:
            if diamond.visible:
                self.score += 100
                floating_text = FloatingText("+100", diamond.center_x, diamond.center_y)
                self.floating_texts_list.append(floating_text)
                arcade.play_sound(self.diamond_sound)
                diamond.remove_from_sprite_lists()
            diamond.visible = False

        for text in self.floating_texts_list[:]:
            text.update(delta_time)
            if text.timer <= 0:
                self.floating_texts_list.remove(text)

        if self.red_key_sprite.visible and arcade.check_for_collision(self.player_sprite, self.red_key_sprite):
            self.red_key_sprite.remove_from_sprite_lists()
            for door in self.red_doors[:]:
                door.remove_from_sprite_lists()
            arcade.play_sound(self.key_sound)
            self.red_key_sprite.visible = False
            self.red_key_collected_sprite.color = arcade.color.RED

        if self.blue_key_sprite.visible and arcade.check_for_collision(self.player_sprite, self.blue_key_sprite):
            self.blue_key_sprite.remove_from_sprite_lists()
            for door in self.blue_doors[:]:
                door.remove_from_sprite_lists()
            arcade.play_sound(self.key_sound)
            self.blue_key_sprite.visible = False
            self.blue_key_collected_sprite.color = arcade.color.BLUE

        if self.green_key_sprite.visible and arcade.check_for_collision(self.player_sprite, self.green_key_sprite):
            self.green_key_sprite.remove_from_sprite_lists()
            for door in self.green_doors[:]:
                door.remove_from_sprite_lists()
            arcade.play_sound(self.key_sound)
            self.green_key_sprite.visible = False 
            self.green_key_collected_sprite.color = arcade.color.GREEN

        if arcade.check_for_collision(self.player_sprite, self.portal1_sprite):
            if self.portal1_available:
                arcade.play_sound(self.portal_sound)
                self.player_sprite.center_x = self.portal2_sprite.center_x
                self.player_sprite.center_y = self.portal2_sprite.center_y
                self.portal2_available = False
                self.portal1_available = False
        else:
            self.portal1_available = True

        if arcade.check_for_collision(self.player_sprite, self.portal2_sprite):
            if self.portal2_available:
                arcade.play_sound(self.portal_sound)
                self.player_sprite.center_x = self.portal1_sprite.center_x
                self.player_sprite.center_y = self.portal1_sprite.center_y
                self.portal1_available = False
                self.portal2_available = False
        else:
            self.portal2_available = True

        if not self.game_over and arcade.check_for_collision(self.player_sprite, self.goal_sprite):
            self.music.stop(self.music_player)
            self.game_over_sound.play()
            self.game_over = True

        self.keys_list.update()
        self.diamonds_list.update()


levels = [
    {
        # green key tutorial
        "walls": [(425, 200), (450, 200), (475, 200), (500, 200), (525, 200), (550, 200), (575, 200), (600, 200), (625, 200), (650, 200), (675, 200), (700, 200), (725, 200), (750, 200), (775, 200), (800, 200), (800, 225), (800, 250), (800, 275), (800, 300), (800, 325), (800, 350), (800, 375), (800, 400), (800, 425), (800, 450), (800, 475), (425, 200), (425, 225), (425, 250), (425, 275), (425, 300), (425, 325), (425, 350), (425, 375), (425, 400), (425, 425), (425, 450), (425, 475), (425, 475), (450, 475), (475, 475), (500, 475), (525, 475), (550, 475), (575, 475), (600, 475), (625, 475), (650, 475), (675, 475), (700, 475), (725, 475), (750, 475), (775, 475), (650, 200), (650, 225), (650, 250), (650, 325), (650, 350), (650, 375), (650, 400), (650, 425), (650, 450), (650, 475)],
        "blue_doors": [(-500, -500), (-500, -500)],
        "red_doors": [(-500, -500), (-500, -500)],
        "green_doors" : [(650, 275), (650, 300)],
        "player": (VIRTUAL_WIDTH // 2 - 150, VIRTUAL_HEIGHT // 2 - 100 ),
        "portals": [(-500, -500), (-500, -500)],
        "red_key": (-500, -500),
        "blue_key": (-500, -500),
        "green_key": (590, 300),
        "goal": (750, 350),
        "diamonds": []
    },
    {
        # red key tutorial
        "walls": [(425, 200), (450, 200), (475, 200), (500, 200), (525, 200), (550, 200), (575, 200), (600, 200), (625, 200), (650, 200), (675, 200), (700, 200), (725, 200), (750, 200), (775, 200), (800, 200), (800, 225), (800, 250), (800, 275), (800, 300), (800, 325), (800, 350), (800, 375), (800, 400), (800, 425), (800, 450), (800, 475), (425, 200), (425, 225), (425, 250), (425, 275), (425, 300), (425, 325), (425, 350), (425, 375), (425, 400), (425, 425), (425, 450), (425, 475), (425, 475), (450, 475), (475, 475), (500, 475), (525, 475), (550, 475), (575, 475), (600, 475), (625, 475), (650, 475), (675, 475), (700, 475), (725, 475), (750, 475), (775, 475), (650, 200), (650, 225), (650, 250), (650, 325), (650, 350), (650, 375), (650, 400), (650, 425), (650, 450), (650, 475)],
        "blue_doors": [(-500, -500), (-500, -500)],
        "green_doors": [(-500, -500), (-500, -500)],
        "red_doors" : [(650, 275), (650, 300)],
        "player": (VIRTUAL_WIDTH // 2 - 150, VIRTUAL_HEIGHT // 2 - 100 ),
        "portals": [(-500, -500), (-500, -500)],
        "green_key": (-500, -500),
        "blue_key": (-500, -500),
        "red_key": (590, 300),
        "goal": (750, 350),
        "diamonds": [] 
    },
    {
        # blue key tutorial
        "walls": [(425, 200), (450, 200), (475, 200), (500, 200), (525, 200), (550, 200), (575, 200), (600, 200), (625, 200), (650, 200), (675, 200), (700, 200), (725, 200), (750, 200), (775, 200), (800, 200), (800, 225), (800, 250), (800, 275), (800, 300), (800, 325), (800, 350), (800, 375), (800, 400), (800, 425), (800, 450), (800, 475), (425, 200), (425, 225), (425, 250), (425, 275), (425, 300), (425, 325), (425, 350), (425, 375), (425, 400), (425, 425), (425, 450), (425, 475), (425, 475), (450, 475), (475, 475), (500, 475), (525, 475), (550, 475), (575, 475), (600, 475), (625, 475), (650, 475), (675, 475), (700, 475), (725, 475), (750, 475), (775, 475), (650, 200), (650, 225), (650, 250), (650, 325), (650, 350), (650, 375), (650, 400), (650, 425), (650, 450), (650, 475)],
        "red_doors": [(-500, -500), (-500, -500)],
        "green_doors": [(-500, -500), (-500, -500)],
        "blue_doors" : [(650, 275), (650, 300)],
        "player": (VIRTUAL_WIDTH // 2 - 150, VIRTUAL_HEIGHT // 2 - 100 ),
        "portals": [(-500, -500), (-500, -500)],
        "green_key": (-500, -500),
        "red_key": (-500, -500),
        "blue_key": (590, 300),
        "goal": (750, 350),
        "diamonds": [] 
    },
    {
        # portal tutorial
        "walls": [(425, 200), (450, 200), (475, 200), (500, 200), (525, 200), (550, 200), (575, 200), (600, 200), (625, 200), (650, 200), (675, 200), (700, 200), (725, 200), (750, 200), (775, 200), (800, 200), (800, 225), (800, 250), (800, 275), (800, 300), (800, 325), (800, 350), (800, 375), (800, 400), (800, 425), (800, 450), (800, 475), (425, 200), (425, 225), (425, 250), (425, 275), (425, 300), (425, 325), (425, 350), (425, 375), (425, 400), (425, 425), (425, 450), (425, 475), (425, 475), (450, 475), (475, 475), (500, 475), (525, 475), (550, 475), (575, 475), (600, 475), (625, 475), (650, 475), (675, 475), (700, 475), (725, 475), (750, 475), (775, 475), (650, 200), (650, 225), (650, 250), (650, 325), (650, 350), (650, 375), (650, 400), (650, 425), (650, 450), (650, 475), (650, 275), (650, 300)],
        "red_doors": [(-500, -500), (-500, -500)],
        "green_doors": [(-500, -500), (-500, -500)],
        "blue_doors" : [(-500, -500), (-500, -500)],
        "player": (VIRTUAL_WIDTH // 2 - 150, VIRTUAL_HEIGHT // 2 - 100 ),
        "portals": [(500, 400), (700, 250)],
        "green_key": (-500, -500),
        "red_key": (-500, -500),
        "blue_key": (-500, -500),
        "goal": (750, 350),
        "diamonds": [] 
    },
    {
        # portal tutorial 2
        "walls": [(50, 200), (75, 200), (100, 200), (125, 200), (150, 200), (175, 200), (200, 200), (225, 200), (250, 200), (275, 200), (300, 200), (325, 200), (350, 200), (375, 200), (400, 200), (425, 200), (450, 200), (475, 200), (500, 200), (525, 200), (550, 200), (575, 200), (600, 200), (625, 200), (650, 200), (675, 200), (700, 200), (725, 200), (750, 200), (775, 200), (800, 200), (825, 200), (850, 200), (875, 200), (900, 200), (925, 200), (950, 200), (975, 200), (1000, 200), (1025, 200), (1050, 200), (1075, 200), (1100, 200), (1125, 200), (1150, 200), (1175, 200), (1200, 200), (1225, 200), (1250, 200), (1000, 625), (1000, 600), (1000, 575), (1000, 550), (1000, 525), (1000, 500), (1000, 475), (1000, 450), (1000, 425), (1000, 400), (1000, 325), (1000, 300), (1000, 275), (1000, 250), (1000, 225), (800, 625), (800, 600), (800, 575), (800, 550), (800, 525), (800, 500), (800, 475), (800, 450), (800, 425), (800, 400), (800, 325), (800, 300), (800, 275), (800, 250), (800, 225), (600, 625), (600, 600), (600, 575), (600, 550), (600, 525), (600, 500), (600, 475), (600, 450), (600, 425), (600, 400), (600, 325), (600, 300), (600, 275), (600, 250), (600, 225)],
        "blue_doors": [(1000, 375), (1000, 350)],
        "red_doors": [(600, 375), (600, 350)],
        "green_doors" : [(800, 375), (800, 350)],
        "player": (1100, 400),
        "portals": [(100, 100), (1100, 600)],
        "blue_key": (1100, 100),
        "green_key": (900, 100),
        "red_key": (800, 100),
        "goal": (120, 500),
        "diamonds": [] 
    },
    {
        "walls": [(300, 630), (300, 605), (300, 580), (300, 555), (300, 530), (300, 505), (300, 480), (300, 455), (300, 430), (300, 405), (300, 380), (608, 292), (608, 267), (608, 242), (608, 217), (608, 192), (608, 167), (608, 142), (608, 117), (608, 92), (608, 67), (608, 42), (358, 284), (358, 259), (358, 234), (358, 209), (358, 184), (358, 159), (358, 134), (358, 109), (358, 84), (358, 59), (358, 34), (810, 632), (810, 607), (810, 582), (810, 557), (810, 532), (810, 507), (810, 482), (810, 457), (810, 432), (810, 407), (810, 382), (810, 357), (810, 332), (810, 307), (810, 282), (810, 257), (810, 232), (810, 157), (810, 132), (810, 107), (810, 82), (810, 57), (810, 32), (944, 285), (944, 261), (944, 237), (944, 213), (944, 189), (944, 165), (1094, 285), (1094, 261), (1094, 237), (1094, 213), (1094, 189), (1094, 165), (300, 375), (275, 375), (250, 375), (225, 375), (200, 375), (175, 375), (150, 375), (125, 375), (100, 375), (358, 300), (383, 300), (408, 300), (483, 300), (508, 300), (533, 300), (558, 300), (583, 300), (608, 300), (815, 300), (840, 300), (865, 300), (890, 300), (915, 300), (940, 300), (965, 300), (1040, 300), (1065, 300), (1090, 300), (1115, 300), (1140, 300), (1165, 300), (1190, 300), (1215, 300), (1240, 300), (944, 150), (969, 150), (994, 150), (1019, 150), (1044, 150), (1069, 150), (1094, 150)],
        "blue_doors": [(810, 207), (810, 182)],
        "red_doors": [(433, 300), (458, 300)],
        "green_doors" : [(990, 300), (1015, 300)],
        "player": (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2),
        "portals": [(VIRTUAL_WIDTH - 100, 200), (VIRTUAL_WIDTH - 300, VIRTUAL_HEIGHT - 200)],
        "red_key": (200, 400),
        "blue_key": (500, 100),
        "green_key": (1100, 600),
        "goal": (1015, 188),
        "diamonds": [(332, 615), (367, 615), (332, 575), (332, 535), (367, 575), (407, 615), (58, 100), (58, 60), (98, 60), (774, 615), (734, 615), (650, 52), (690, 52), (1015, 125), (1055, 125), (1159, 346), (1209, 346)] 
    },
    {
        "walls": [(500, 625), (500, 600), (500, 575), (500, 550), (475, 550), (450, 550), (425, 550), (425, 525), (425, 500), (400, 500), (375, 500), (350, 500), (325, 500), (300, 500), (275, 500), (250, 500), (250, 475), (250, 450), (250, 425), (225, 425), (200, 425), (175, 425), (150, 425), (75, 425), (50, 425), (250, 400), (250, 375), (250, 350), (250, 325), (325, 325), (350, 325), (350, 350), (350, 375), (350, 400), (350, 425), (350, 450), (350, 475), (700, 625), (700, 625), (700, 600), (700, 575), (700, 550), (700, 525), (700, 450), (700, 425), (700, 400), (700, 375), (700, 350), (700, 325), (700, 300), (700, 275), (700, 250), (700, 225), (700, 200), (700, 175), (700, 150), (700, 125), (700, 100), (700, 75), (700, 50), (50, 250), (50, 250), (75, 250), (100, 250), (125, 250), (150, 250), (175, 250), (200, 250), (225, 250), (250, 250), (275, 250), (300, 250), (325, 250), (350, 250), (375, 250), (400, 250), (425, 250), (450, 250), (475, 250), (500, 250), (525, 250), (550, 250), (575, 250), (600, 250), (625, 250), (650, 250), (675, 250), (900, 625)],
        "blue_doors": [(700, 500), (700, 475)],
        "red_doors": [(125, 425), (100, 425)],
        "green_doors" : [(275, 325), (300, 325)],
        "player": (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2),
        "portals": [(100, 200), (1100, 400)],
        "red_key": (600, 600),
        "blue_key": (100, 525),
        "green_key": (610, 110),
        "goal": (300, 400),
        "diamonds": [(60, 475), (60, 515), (60, 555), (740, 60), (740, 60), (740, 100), (740, 140), (740, 180), (740, 220), (740, 260), (740, 300), (740, 340), (740, 380), (740, 420), (740, 460), (740, 500), (740, 540), (740, 580), (780, 60), (780, 100), (780, 140), (780, 180), (780, 220), (780, 260), (780, 300), (780, 340), (780, 380), (780, 420), (780, 460), (780, 500), (780, 540), (820, 60), (820, 100), (820, 140), (820, 180), (820, 220), (820, 260), (820, 300), (820, 340), (820, 380), (820, 420), (820, 460), (820, 500)] 
    },
]


def get_next_level(level):
    pos = level - 1

    if pos < len(levels):
        return Level(level=level, data=levels[pos])
    return None


def main():
    window = arcade.Window(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, SCREEN_TITLE)
    
    start_view = MainMenu()
    window.show_view(start_view)
    
    arcade.run()


if __name__ == "__main__":
    main()
