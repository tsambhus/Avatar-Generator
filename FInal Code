# Python 3.14.0 (v3.14.0:ebf955df7a8, Oct  7 2025, 8:20:14) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
# Enter "help" below or click "Help" above for more information.
import customtkinter as ctk
import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import random
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt



# question + scoring setup


QUESTIONS = [
    ("What is your favorite season?", ["Winter", "Spring", "Summer", "Autumn"]),
    ("It's a Friday night. Would you rather...", ["Go to a party where you only know the host", "Hang out with your friends at their place", "Watch your favorite show at home"]),
    ("Which color do you prefer?", ["Black", "Sage green", "Bright Red"]),
    ("How fast do you make decisions?", ["On the spot", "A day or two", "One month minimum"]),
    ("How often do you cry?", ["Once a month or less", "Once a week", "Once a day"]),
    ("You've just been offered a chance to travel the world for 2 years. Would you do it?", ["No, I have a home where I am.", "Maximum, 2 weeks", "Yes, without a doubt."]),
    ("How routine-driven are you?", ["Minute by minute plan", "Loose plans, but I can deviate", "No routine at all"]),
    ("Which obscure skill would you master?", ["Perfect calligraphy", "Playing a rare instrument of your choice", "Understanding 3 random languages"]),
    ("How do you react to the unknown?", ["Excitement", "Suspicion", "Anxiety", "Indifference"]),
    ("How do you process your emotions?", ["Introspection", "Talking", "Creating"]),
]

# map each multiple choice text to a numeric trait (0.0, 0.5, 1.0)
ANSWER_SCORES = {
    0: {"Winter": 0.6 , "Spring": 0.85, "Autumn": 0.7, "Summer": 1.0},
    1: {"Go to a party where you just know the host": 0.0, "Hang out with your friends at their place": 0.5, "Watch your favorite show at home": 1.0},
    2: {"Black": 0.0, "Sage green": 0.5, "Bright Red": 1.0},
    3: {"On the spot": 0.0, "A day or two": 0.5, "One month minimum": 1.0},
    4: {"Once a month or less": 0.0, "Once a week": 0.5, "Once a day": 1.0},
    5: {"No, I have a home where I am.": 0.0, "Maximum, 2 weeks": 0.5, "Yes, without a doubt.": 1.0},
    6: {"Minute by minute plan": 0.0, "Loose plans, but I can deviate": 0.5, "No routine at all": 1.0},
    7: {"Perfect calligraphy": 0.0, "Playing a rare instrument of your choice": 0.5, "Understanding 3 random languages": 1.0},
    8: {"Indifference": 0.0, "Excitement": 0.25, "Suspicion": 0.75, "Anxiety": 1.0},
    9: {"Introspection": 0.0, "Talking": 0.5, "Creating": 1.0},
}


# avatar drawing functions

def bezier_curve(ax, pts, lw=3): #frommatplotlib bezier curves demo
    Path = mpath.Path
    path_data = [(Path.MOVETO, pts[0])]
    for i in range(1, len(pts), 3):
        segment = pts[i:i+3]
        if len(segment) == 3:
            path_data.append((Path.CURVE4, segment[0]))
            path_data.append((Path.CURVE4, segment[1]))
            path_data.append((Path.CURVE4, segment[2]))

    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, fill=False, lw=lw, color="black")
    ax.add_patch(patch)


def draw_head(ax, x, y, size, energy, abstractness): #"electric flower using Python" from rudix technology on instagram
    
    #head shape controlled by energy.

    #energy: 0–20, controls how many lobes / oscillations the outline has.

    θ = np.linspace(0, 2 * np.pi, 300)  # angles
    # scale by `size` 
    r = size * (1 + 0.3 * np.cos(energy * θ)) #radial

    xs = x + r * np.cos(θ)
    ys = y + r * np.sin(θ)

    ax.plot(xs, ys, color='black', linewidth=2)

    #fill
    if abstractness < 0.5:
        ax.fill(xs, ys, color='black')
    else:
        ax.plot(xs, ys, color='black', linewidth=2)


def draw_body(ax, x, y, height, width, openness):

    if openness < 0.33:
        # super-open shape: long vertical line + arc
        ax.plot([x, x], [y-height/2, y+height/2], color='black', linewidth=3)
        theta = np.linspace(-np.pi/2, np.pi/2, 50)
        ax.plot(x + width*np.cos(theta), y+height/2 + width*np.sin(theta), color='black', linewidth=3)

    elif openness < 0.66:
        # abstract trapezoid body
        shape = np.array([
            [x-width, y-height/2],
            [x+width, y-height/2],
            [x+0.5*width, y+height/2],
            [x-0.5*width, y+height/2]
        ])
        ax.plot(shape[:,0], shape[:,1], color='black', linewidth=3)
    else:
        # central S-curve spine, frommatplotlib spine curves demo
        spine_x = x
        top = y + height / 2
        bottom = y - height / 2
        bezier_curve(ax, [
        (spine_x, bottom),
        (spine_x - width * 0.3, y - height * 0.2),
        (spine_x + width * (openness - 0.5), y + height * 0.2),
        (spine_x, top),
    ], lw=4)

    # left body outline
        bezier_curve(ax, [
        (x - width, bottom),
        (x - width * 1.4, y - height * 0.2),
        (x - width * 1.2, y + height * 0.1),
        (x - width, top),
    ], lw=3)

    # right body outline
        bezier_curve(ax, [
        (x + width, bottom),
        (x + width * 1.4, y - height * 0.1),
        (x + width * 1.2, y + height * 0.2),
        (x + width, top),
    ], lw=3)



def draw_legs(ax, x, y, length, curvature, regulation):
    #flat legs
    if regulation == 1:
        # lengths
        left_len  = length
        right_len = length * 1   # slightly longer than before

        # left leg
        ax.plot(
            [x - left_len * 0.7, x - left_len * 0.2],
            [y, y],
            color='black',
            linewidth=2
        )

        # right leg
        ax.plot(
            [x + right_len * 0.1, x + right_len * 0.85],
            [y, y],
            color='black',
            linewidth=2
        )
        return
    #flowing legs that taper at the ends
    spread = length * 0.3

    for side in [-1, 1]:
        ctrl1 = (x + side * spread, y - length * 0.3)
        ctrl2 = (x + side * (spread + curvature * 0.5), y - length * 0.7)
        foot = (x + side * (spread * 0.8), y - length)

        bezier_curve(ax, [
            (x, y),
            ctrl1,
            ctrl2,
            foot
        ], lw=4)
    

def draw_noise(ax, intro_extro):
    #add noise
    n = int(intro_extro * 40)
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1.5, 1.5)
        ax.plot(x, y, 'o', color='black', markersize=random.random() * 2)



# UI for quiz (multiple choice questions, sliders and buttons), used chatGPT for the frame 


class AvatarApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Personality Avatar Generator")
        self.geometry("700x700")

        self.current_page = 0  # 0 = start, 1-5 = questions, 6 = sliders+avatar

        # hold widgets/state
        self.main_frame = None
        self.question_vars = []
        self.slider_energy = None
        self.slider_warmth = None
        self.slider_focus = None
        self.avatar_canvas = None

        # initialize StringVars for questions
        for i, (text, options) in enumerate(QUESTIONS):
            var = ctk.StringVar(value=options[1])  # default to middle option
            self.question_vars.append(var)

        self.show_start_screen()

    # screen management, used chatGPT to help

    def clear_main_frame(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_start_screen(self):
        self.current_page = 0
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Generate your Avatar",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=40)

        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Answer a few questions and we’ll draw a unique personality avatar.",
            font=ctk.CTkFont(size=14)
        )
        subtitle.pack(pady=10)

        btn = ctk.CTkButton(
            self.main_frame,
            text="Get Started",
            command=self.next_page
        )
        btn.pack(pady=30)

    def show_question_page(self, page_index):

        #page_index: 1–5, each page shows 2 questions:
        #page 1 to Q0, Q1
        #page 2 to Q2, Q3
        
        self.clear_main_frame()

        start_q = (page_index - 1) * 2
        end_q = start_q + 2

        header = ctk.CTkLabel(
            self.main_frame,
            text=f"Questions {start_q + 1}–{end_q}",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        header.pack(pady=20)

        inner = ctk.CTkFrame(self.main_frame)
        inner.pack(pady=20, fill="both", expand=True)

        for q_idx in range(start_q, end_q):
            q_text, options = QUESTIONS[q_idx]

            q_frame = ctk.CTkFrame(inner)
            q_frame.pack(pady=10, fill="x")

            label = ctk.CTkLabel(
                q_frame,
                text=q_text,
                anchor="w",
                font=ctk.CTkFont(size=14, weight="normal")
            )
            label.pack(side="top", anchor="w", pady=4)

            opt_menu = ctk.CTkOptionMenu(
                q_frame,
                values=options,
                variable=self.question_vars[q_idx],
                width=220
            )
            opt_menu.pack(side="top", anchor="w", pady=4)

        next_btn_text = "Next"
        btn = ctk.CTkButton(
            self.main_frame,
            text=next_btn_text,
            command=self.next_page
        )
        btn.pack(pady=20)

    def show_slider_page(self):
        self.clear_main_frame()

        header = ctk.CTkLabel(
            self.main_frame,
            text="Final step: tune your sliders",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        header.pack(pady=10)

        sub = ctk.CTkLabel(
            self.main_frame,
            text="These sliders fine-tune the energy, warmth, and focus of your avatar.",
            font=ctk.CTkFont(size=13)
        )
        sub.pack(pady=5)

        slider_frame = ctk.CTkFrame(self.main_frame)
        slider_frame.pack(pady=10, fill="x", expand=False)

        # energy sliders 0-20
        self.slider_energy = ctk.CTkSlider(slider_frame, from_=0, to=20, number_of_steps=40)

        # other sliders 0-255
        self.slider_warmth = ctk.CTkSlider(slider_frame, from_=0, to=255, number_of_steps=255)
        self.slider_focus = ctk.CTkSlider(slider_frame, from_=0, to=255, number_of_steps=255)

        self.slider_energy.set(128)
        self.slider_warmth.set(128)
        self.slider_focus.set(128)

        def add_slider_row(parent, label_text, slider_widget):
            row = ctk.CTkFrame(parent)
            row.pack(pady=10, fill="x")
            lbl = ctk.CTkLabel(row, text=label_text, width=150, anchor="w")
            lbl.pack(side="left", padx=10)
            slider_widget.pack(side="left", fill="x", expand=True, padx=10)

        add_slider_row(slider_frame, "Countryside or big city?", self.slider_energy)
        add_slider_row(slider_frame, "Your confidence today?", self.slider_warmth)
        add_slider_row(slider_frame, "Average focus levels?", self.slider_focus)

        btn = ctk.CTkButton(
            self.main_frame,
            text="Complete Avatar",
            command=self.generate_and_show_avatar
        )
        btn.pack(pady=15)

        # frame where the matplotlib canvas (avatar) will live
        self.avatar_frame = ctk.CTkFrame(self.main_frame)
        self.avatar_frame.pack(fill="both", expand=True, pady=10)

    def next_page(self):

        #Global navigation:
        #0 to start
        #1–5 to question pages
        #6 to sliders

        if self.current_page == 0:
            self.current_page = 1
            self.show_question_page(1)
        elif 1 <= self.current_page <= 4:
            self.current_page += 1
            self.show_question_page(self.current_page)
        elif self.current_page == 5:
            self.current_page = 6
            self.show_slider_page()

    #translating answers to generate avatar 

    def compute_traits(self):
        #function to get the question answers in, used chatgpt
        trait_values = []
        for i, var in enumerate(self.question_vars):
            text = var.get()
            score = ANSWER_SCORES[i].get(text, 0.5)
            trait_values.append(score)

        # sliders: map 0–255 to 0–1
        
        warmth = self.slider_warmth.get() / 255.0
        focus = self.slider_focus.get() / 255.0

        #keep energy from 0-20
        energy = self.slider_energy.get()
        #combine into one list
        return np.array(trait_values + [energy, warmth, focus])

    def generate_and_show_avatar(self):
        traits = self.compute_traits()

        seasons = traits[0]
        intro_extro = traits[1]
        color = traits[2]
        spontaneity = traits[3]
        cryfrequency = traits[4]
        openness = traits[5]
        flexibility = traits[6]
        abstractness = traits[7]
        regulation = traits[8]
        consientiousness = traits[9]

        energy = traits[10]
        warmth = traits[11]
        focus = traits[12]

        # map traits to visual parameters
        body_height = seasons + intro_extro * 1.5
        body_width = 0.15 + cryfrequency * 0.2 * (1 + warmth * 0.5)
        head_size = 0.09 + color * 0.08
        leg_length = 0.6 + focus * 0.7
        curve = (consientiousness - 0.5) * (regulation * 3)
        noise_amount = flexibility

        # Clear previous avatar canvas if exists, used chatGPT here to debug
        if self.avatar_canvas is not None:
            self.avatar_canvas.get_tk_widget().destroy()
            self.avatar_canvas = None

        # create matplotlib figure
        fig = Figure(figsize=(4, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1.5, 1.5)
        ax.axis("off")

        # draw avatar
        
        draw_body(ax, 0, 0.2, body_height, body_width, openness)
        draw_head(ax, 0, body_height / 2 + 0.35, head_size, energy, abstractness)
        draw_legs(ax, 0, -body_height / 2, leg_length, curve, regulation)

        # embed figure in Tkinter
        self.avatar_canvas = FigureCanvasTkAgg(fig, master=self.avatar_frame)
        self.avatar_canvas.draw()
        self.avatar_canvas.get_tk_widget().pack()




# run APP


if __name__ == "__main__":
    app = AvatarApp()
    app.mainloop()

