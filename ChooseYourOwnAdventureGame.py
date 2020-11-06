# This is a python game in which you can choose your own adventure.
# The choices you make will affect the story you get.
# Created by Erica Travers

import arcade
import pathlib
import time


class ChooseYourOwn(arcade.Window):

    def __init__(self):
        super().__init__(1200, 800, "Choose Your Own Adventure Game")
        self.cursor = None
        self.story_path = None
        self.background = None
        self.start_button = None
        self.left_box = None
        self.right_box = None
        self.story_box = None
        self.level = None
        self.set_mouse_visible(False)
        self.choices_appear_time = None
        self.timer = None
        self.story_text = None

    def setup(self):
        self.cursor = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Images" / "cursor.png")
        self.story_path = ""
        self.background = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Backgrounds" / "start.png", 1.2,
                                        center_x=600, center_y=400)
        self.start_button = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Images" / "start_button.png", 0.5,
                                          center_x=600, center_y=200)
        self.left_box = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Images" / "Boxes" / "choice_box.png", 1.5,
                                      center_x=300, center_y=200)
        self.right_box = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Images" / "Boxes" / "choice_box.png", 1.5,
                                       center_x=900, center_y=200)
        self.story_box = arcade.Sprite()
        self.level = "start"
        self.choices_appear_time = 7
        self.timer = time.time()
        self.story_text = ""

    def update(self, delta_time: float):
        if self.story_path != "":
            self.setup_next_window(self.story_path)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()

        if self.level == "start":
            arcade.draw_text("Choose Your Own", 300, 550, arcade.color.BLACK, 60, font_name='GARA')
            arcade.draw_text("Adventure Game", 320, 450, arcade.color.BLACK, 60, font_name='GARA')
            self.start_button.draw()

        if self.level == "game in progress" and self.timer >= self.choices_appear_time:
            self.story_box.draw()
            self.left_box.draw()
            self.right_box.draw()
            self.setup_story_text(self.story_path)

        self.cursor.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.cursor.center_x = x + 15
        self.cursor.center_y = y - 15

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and arcade.check_for_collision(self.cursor, self.start_button):
            self.story_path += "1"
            self.level = "game in progress"
        elif button == arcade.MOUSE_BUTTON_LEFT and arcade.check_for_collision(self.cursor, self.left_box):
            self.story_path += "1"
        elif button == arcade.MOUSE_BUTTON_LEFT and arcade.check_for_collision(self.cursor, self.right_box):
            self.story_path += "2"

    def setup_next_window(self, level):
        file = open(pathlib.Path.cwd() / "Stories" / f"{level}.txt")
        first_line = file.readline()
        first_line.rstrip("\n")
        window_visuals = first_line.split()
        scale = float(window_visuals[1])
        self.background = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Backgrounds" / f"{window_visuals[0]}.png",
                                        scale, center_x=600, center_y=400)
        self.story_box = arcade.Sprite(pathlib.Path.cwd() / "Resources" / "Images" / "Boxes" /
                                       f"{window_visuals[2]}_box.png", 3, center_x=600, center_y=500)
        sound = arcade.load_sound(pathlib.Path.cwd() / "Resources" / "Sounds" / "phone-ringing.wav")
        arcade.play_sound(sound)
        # alarm-clock close-car-door open-car-door coffee_pour dial-tone gasp all not working

    def setup_story_text(self, level):
        file = open(pathlib.Path.cwd() / "Stories" / f"{level}.txt")
        file.readline()
        choice_line = file.readline()
        choices = choice_line.split('|')
        arcade.draw_text(f"{choices[0]}", 200, 200, arcade.color.BLACK, 20)
        arcade.draw_text(f"{choices[1]}", 810, 175, arcade.color.BLACK, 20)
        lines = file.readlines()
        line_y = 575
        for line in lines:
            line.rstrip("\n")
            arcade.draw_text(f"{line}", 300, line_y, arcade.color.BLACK, 20)
            line_y -= 30


def main():
    window: ChooseYourOwn = ChooseYourOwn()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
