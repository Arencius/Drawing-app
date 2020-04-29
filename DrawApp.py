import tkinter as tk
from tkinter.font import Font
import random as r
import threading


class DrawApp:
    def __init__(self):
        self.main()

    def main(self):
        global root, canvas
        root = tk.Tk()
        root.geometry('600x600')
        root.resizable(False, False)
        root.title('Paint')

        canvas = tk.Canvas(root, bg='#eee')
        canvas.place(width=600, height=600)

        # Adds a drawing method to canvas and setting default color to black.
        self.stroke_color('#000')

        word_to_guess = tk.Label(
            canvas, text=self.pick_word(), font=Font(size=18))
        word_to_guess.grid(row=0, column=0, padx=15, pady=15)

        seconds = 5
        #self.time = tk.Label(canvas, font=Font(size=20))
        #self.time.grid(row=0, column=1, pady=15)
        self.count_down(seconds)

        clear_button = tk.Button(canvas, text='X', command=self.clear_canvas)
        clear_button.grid(row=0, column=1, padx=5)

        colors = ['red', 'yellow', 'green', 'blue', 'black', 'gray', '#eee']
        color_buttons = []
        for i in range(len(colors)):
            button = tk.Button(canvas, width=3, bg=colors[i])
            button.grid(row=0, column=i+2, padx=1)
            color_buttons.append(button)

        # loop made for dynamically changing stroke color
        for b in color_buttons:
            c = b.cget('bg')
            b.configure(command=lambda x=c: self.stroke_color(x))

        save_button = tk.Button(canvas)
        save_button.grid(row=5, column=5, sticky='s')

        root.mainloop()

    def pick_word(self):
        '''
        Returns a random word for the user to draw. String
        '''
        with open('words.txt') as f:
            words = f.read().split(',')
            picked = r.randint(0, len(words)-1)
            return "You're drawing: {}".format(words[picked])

    def count_down(self, seconds):
        mins, secs = seconds // 60, seconds % 60
        while mins >= 0 and secs >= 0:
            secs -= 1
            if secs < 0:
                mins -= 1
                secs = 59
            time_format = '{}:{num:02d}'.format(mins, num=secs)
            self.change_text(time_format)

    def draw(self, event, color):
        x1, y1 = (event.x-1), (event.y-1)
        x2, y2 = (event.x+1), (event.y+1)
        canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def clear_canvas(self):
        canvas.delete('all')

    def stroke_color(self, color):
        canvas.bind('<B1-Motion>', lambda event,
                    arg=color: self.draw(event, arg))

    def change_text(self, s):
        # self.time.configure(text=s)
        print(s)
        #root.after(1000, lambda x=s: self.change_text(x))


if __name__ == '__main__':
    DrawApp()
