from tkinter import *
from tkinter import ttk


class BlankFrame:
    def __init__(self, master):
        #=== Create Base Frame ===#
        self.start_frame = Frame(master)
        self.start_frame.grid(row=0, column=0, sticky=NSEW)

        return self


class StartFrame(BlankFrame):
    def add_player(self, name):
        test_label = Label(self.player_wrapper,
                           text=name, background="#fcdc92",
                           font=('Courier', 24))
        test_label.pack(fill=BOTH, expand="yes", pady=20)

    def __init__(self, master):
        super().__init__(master)

        #===Frame===#
        start_frame_title = Label(
            self.start_frame, text="Simon Says", height=3, font=('Courier', 45))
        start_frame_title.pack(fill='x')

        def on_btn_press():
            global gameRunning
            gameRunning = True

        start_frame_btn = Button(
            self.start_frame, text="Begin!", command=on_btn_press)
        start_frame_btn.pack(side=BOTTOM)

        #===Player List===#
        self.player_wrapper = LabelFrame(self.start_frame)
        self.player_wrapper.pack(
            fill="both", expand="yes", padx=20, pady=50)

        player_canvas = Canvas(self.player_wrapper)
        player_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        player_scrollbar = ttk.Scrollbar(
            self.player_wrapper, orient="vertical", command=player_canvas.yview)
        player_scrollbar.pack(side=RIGHT, fill="y")

class GameFrame(BlankFrame):
    def __init__(self, master):
        super().__init__(master)

        


frames_list = {
    'start': StartFrame
}


def get_frame(frame):
    if frame in frames_list:
        return frames_list.get(frame)
