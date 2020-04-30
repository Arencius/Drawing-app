import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
import random as r
from PIL import Image, ImageTk, ImageGrab
import io
import os
import ghostscript
import time

PATH = '{}/Desktop'.format(os.environ['USERPROFILE'])
COLORS = ['red', 'orange', 'yellow', 'green', 'blue', '#eee', 'gray', 'black']


class DrawApp:
    def __init__(self):
        self.main()

    def main(self):
        global root, canvas
        root = tk.Tk()
        root.geometry('600x600')
        root.resizable(False, False)
        root.title('Paint')

        canvas = tk.Canvas(root, bg='#eee', width=600, height=550)
        canvas.grid(pady=(50, 0))

        # Frame containing all the buttons
        upper_frame = tk.Frame(root, height=50)
        upper_frame.grid(row=0, sticky='n')

        # If user choose 'yes', the word to draw is randomly picked
        if messagebox.askyesno('Question', 'Do you want the app to pick the word to draw?'):
            word_to_guess = tk.Label(
                upper_frame, text=self.pick_word(), font=Font(size=18))
            word_to_guess.grid(row=0, column=0, padx=(10, 15), pady=15)

        # Adds a drawing method to canvas and setting default color to black.
        self.stroke_color('#000')

        # button erasing all unsaved drawings
        clear_button = tk.Button(
            upper_frame, text='X', command=self.clear_canvas)
        clear_button.grid(row=0, column=1, padx=5, pady=15)

        color_buttons = []

        # loop for creating and placing all buttons at once
        for i in range(len(COLORS)):
            button = tk.Button(upper_frame, width=3, bg=COLORS[i])
            button.grid(row=0, column=i+2, padx=1)
            color_buttons.append(button)

        # loop made to change dynamically a stroke color
        for b in color_buttons:
            c = b.cget('bg')
            b.configure(command=lambda x=c: self.stroke_color(x))

        photo = Image.open('images/save_icon.png').resize((20, 20))
        photo_sized = ImageTk.PhotoImage(photo)

        # button to save users' current work to a file
        save_button = tk.Button(upper_frame, width=20,
                                image=photo_sized, command=lambda s=PATH:
                                self.save_drawing(s))
        save_button.grid(row=0, column=len(COLORS)+2, padx=5)

        root.mainloop()

    def pick_word(self):
        '''
        Returns a random word for the user to draw. String
        '''
        with open('words.txt') as f:
            words = f.read().split(',')
            picked = r.randint(0, len(words)-1)
            return words[picked].upper()

    def draw(self, event, color):
        x1, y1 = (event.x-1), (event.y-1)
        x2, y2 = (event.x+1), (event.y+1)
        canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def clear_canvas(self):
        canvas.delete('all')

    def stroke_color(self, color):
        '''
        Binds a draw function to a canvas and sets color of line
        '''
        canvas.bind('<B1-Motion>', lambda event,
                    arg=color: self.draw(event, arg))

    def save_drawing(self, path):
        '''
        Saves picture in the directory (Desktop/My drawing)
        '''
        ps = canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))

        picture_time = time.strftime("%Y%m%d_%H%M%S")
        path_to_save = '{}/My drawings'.format(path)

        if not os.path.exists(path_to_save):
            os.mkdir(path_to_save)
        img.save('{}/IMG_{}.jpg'.format(path_to_save, picture_time), 'jpeg')


if __name__ == '__main__':
    DrawApp()
