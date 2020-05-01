from tkinter import *
from math import *
import os
import pygame.mixer

PATH_SOUND = "./sounds/"


class AppClass():
    def __init__(self):
        self.Fen = Tk()

        self.Item = {"Canvas": {}}

        self.width = self.Fen.winfo_screenwidth()
        self.height = self.Fen.winfo_screenheight()
        self.min_hw = min(self.width, self.height)

        self.Fen.geometry("%ix%i" % (self.width, self.height))
        self.Fen.overrideredirect(True)
        self.Fen.wm_attributes("-transparentcolor", "SystemButtonFace")
        self.Fen.wm_attributes("-topmost", "1")

        self.Fen.grid_rowconfigure(1, weight = 1)
        self.Fen.grid_columnconfigure(1, weight = 1)

        self.ButtonQuit = Button(self.Fen, text = "X", command = lambda: self.Fen.quit(), bg = "white")
        self.ButtonQuit.grid(row = 1, column = 50)

        self.mult_wheel_size = 0.4
        self.mult_wheel_center_size = 0.2
        self.mult_wheel_text = (self.mult_wheel_size + self.mult_wheel_center_size) / 2

        self.Canvas = Canvas(self.Fen, width = self.min_hw, height = self.min_hw)
        self.Canvas.grid(row = 1, column = 1)

        self.Canvas_wheelborder = self.Canvas.create_oval(
            (self.min_hw / 2) - self.min_hw * self.mult_wheel_size,
            (self.min_hw / 2) - self.min_hw * self.mult_wheel_size,
            (self.min_hw / 2) + self.min_hw * self.mult_wheel_size,
            (self.min_hw / 2) + self.min_hw * self.mult_wheel_size,
            width = 5) # Cercle exterieur


        self.Canvas_wheelcenterborder = self.Canvas.create_oval(
            (self.min_hw / 2) - self.min_hw * self.mult_wheel_center_size,
            (self.min_hw / 2) - self.min_hw * self.mult_wheel_center_size,
            (self.min_hw / 2) + self.min_hw * self.mult_wheel_center_size,
            (self.min_hw / 2) + self.min_hw * self.mult_wheel_center_size,
            width = 5, fill = "SystemButtonFace")


        self.VolumeScale = Scale(self.Fen, from_ = 0, to_ = 100, orient = HORIZONTAL,
                                 width = self.min_hw / 40, length = self.min_hw / 2,
                                 sliderlength = self.min_hw / 20, bg = "gray45", label = "Volume",
                                 activebackground = "gray65", command = self.update_volume)
        self.VolumeScale.grid(row = 2, column = 1)
        self.VolumeScale.set(70)


        self.Fen.after(0, self.main_menu)
        pygame.mixer.init()

        self.Fen.mainloop()


    def menu(self, Possibility = {}):
        for item in self.Item["Canvas"]:
            self.Canvas.delete(self.Item["Canvas"][item])

        for index, keys in enumerate(Possibility):
            self.Item["Canvas"]["Arc%i" % index] = self.Canvas.create_arc(
                (self.min_hw / 2) - self.min_hw * self.mult_wheel_size,
                (self.min_hw / 2) - self.min_hw * self.mult_wheel_size,
                (self.min_hw / 2) + self.min_hw * self.mult_wheel_size,
                (self.min_hw / 2) + self.min_hw * self.mult_wheel_size,

                start = (360 * index) / len(Possibility),
                extent = 359.9 / len(Possibility),
                width = 5, fill = "gray45")


            self.Item["Canvas"]["Text%i" % index] = self.Canvas.create_text(
                self.min_hw / 2 + self.min_hw * self.mult_wheel_text * cos(pi * 2 * index / len(Possibility) - pi / len(Possibility)),
                self.min_hw / 2 + self.min_hw * self.mult_wheel_text * sin(pi * 2 * index / len(Possibility) - pi / len(Possibility)),
                text = keys, font = ("Purisa", 30)
                )

            self.Canvas.tag_bind(self.Item["Canvas"]["Arc%i" % index], "<Button-1>", Possibility[keys])
            self.Canvas.tag_bind(self.Item["Canvas"]["Text%i" % index], "<Button-1>", Possibility[keys])


        for index, keys in enumerate(Possibility): self.Canvas.tag_raise(self.Item["Canvas"]["Text%i" % index])
        self.Canvas.tag_raise(self.Canvas_wheelcenterborder)

    def main_menu(self):
        self.menu(
            Possibility = {"Quitter": lambda x: self.Fen.quit(),
                           "Paramètre": lambda x: print("paramètre"),
                           "Jouer": lambda x: self.play_menu()}
        )

    def play_menu(self):
        Possibility = {file.split(".")[0]: lambda x, file = file: self.play_music(file) for file in os.listdir(PATH_SOUND)}
        Possibility.update({"Retour": lambda x: self.main_menu()})
        self.menu(
            Possibility = Possibility
        )

    def play_music(self, file):
        pygame.mixer.music.load(PATH_SOUND + file)
        pygame.mixer.music.play()

    def update_volume(self, event):
        pygame.mixer.music.set_volume(self.VolumeScale.get() / 100)

App = AppClass()