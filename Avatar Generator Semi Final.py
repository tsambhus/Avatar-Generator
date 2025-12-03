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

# -----------------------------
# QUESTION + SCORING SETUP
# -----------------------------

QUESTIONS = [
    ("How do you recharge?", ["Introvert", "Both", "Extrovert"]),
    ("Which do you value more?", ["Logic", "Balance", "Intuition"]),
    ("How playful are you?", ["Very serious", "Neutral", "Very playful"]),
    ("How fast do you make decisions?", ["Slow", "Medium", "Fast"]),
    ("How emotional is your thinking?", ["Low", "Medium", "High"]),
    ("How open to new experiences are you?", ["Closed", "Neutral", "Open"]),
    ("How routine-driven are you?", ["Rigid", "Comfy", "Flexible"]),
    ("How abstract is your imagination?", ["Concrete", "Mixed", "Abstract"]),
    ("Your general mood tone?", ["Calm", "Neutral", "Intense"]),
    ("How chaotic/creative are you?", ["Minimalist", "Balanced", "Chaotic"]),
]

# Map each answer text → numeric trait (0.0, 0.5, 1.0)
ANSWER_SCORES = {
    0: {"Introvert": 0.0, "Both": 0.5, "Extrovert": 1.0},
    1: {"Logic": 0.0, "Balance": 0.5, "Intuition": 1.0},
    2: {"Very serious": 0.0, "Neutral": 0.5, "Very playful": 1.0},
    3: {"Slow": 0.0, "Medium": 0.5, "Fast": 1.0},
    4: {"Low": 0.0, "Medium": 0.5, "High": 1.0},
    5: {"Closed": 0.0, "Neutral": 0.5, "Open": 1.0},
    6: {"Rigid": 0.0, "Comfy": 0.5, "Flexible": 1.0},
    7: {"Concrete": 0.0, "Mixed": 0.5, "Abstract": 1.0},
    8: {"Calm": 0.0, "Neutral": 0.5, "Intense": 1.0},
    9: {"Minimalist": 0.0, "Balanced": 0.5, "Chaotic": 1.0},
}


# -----------------------------
# AVATAR DRAWING HELPERS
# -----------------------------

def bezier_curve(ax, pts, lw=3):
    """Draw a smooth bezier curve using control points."""
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


def organic_blob(ax, center, size, irregularity=0.2, fill=True):
    """Draw a filled or outline organic blob for the head."""
    x0, y0 = center
    t = np.linspace(0, 2*np.pi, 200)
    r = size * (1 + irregularity * np.sin(5*t + random.random()*3))

    xs = x0 + r * np.cos(t)
    ys = y0 + r * np.sin(t)

    if fill:
        ax.fill(xs, ys, "black")
    else:
        ax.plot(xs, ys, color="black", lw=2)


def draw_body(ax, x, y, height, width, openness):
    """Organic S-curve spine + curved outline body."""
    spine_x = x
    top = y + height / 2
    bottom = y - height / 2

    # Central S-curve spine
    bezier_curve(ax, [
        (spine_x, bottom),
        (spine_x - width * 0.3, y - height * 0.2),
        (spine_x + width * (openness - 0.5), y + height * 0.2),
        (spine_x, top),
    ], lw=4)

    # Left body outline
    bezier_curve(ax, [
        (x - width, bottom),
        (x - width * 1.4, y - height * 0.2),
        (x - width * 1.2, y + height * 0.1),
        (x - width, top),
    ], lw=3)

    # Right body outline
    bezier_curve(ax, [
        (x + width, bottom),
        (x + width * 1.4, y - height * 0.1),
        (x + width * 1.2, y + height * 0.2),
        (x + width, top),
    ], lw=3)


def draw_legs(ax, x, y, length, curvature):
    """Long flowing bent legs that taper at the ends."""
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


def draw_head(ax, x, y, size, abstractness):
    """Filled head blobs."""
    if abstractness < 0.33:
        # simple filled circle
        circ = mpatches.Circle((x, y), size, color='black')
        ax.add_patch(circ)
    elif abstractness < 0.66:
        # stretched oval
        circ = mpatches.Ellipse((x, y), 2*size*1.3, 2*size, color='black')
        ax.add_patch(circ)
    else:
        # organic blob
        organic_blob(ax, (x, y), size, irregularity=0.4, fill=True)


def draw_noise(ax, intensity):
    """Adds background texture based on creativity/chaos."""
    n = int(intensity * 40)
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1.5, 1.5)
        ax.plot(x, y, 'o', color='black', markersize=random.random() * 2)


# -----------------------------
# MAIN APP CLASS
# -----------------------------

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

    # ------- SCREEN MANAGEMENT -------

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
        """
        page_index: 1–5, each page shows 2 questions:
        page 1 → Q0, Q1
        page 2 → Q2, Q3
        ...
        """
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

        # Energy slider 0–255
        self.slider_energy = ctk.CTkSlider(slider_frame, from_=0, to=255, number_of_steps=255)
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

        add_slider_row(slider_frame, "Energy (0–255)", self.slider_energy)
        add_slider_row(slider_frame, "Warmth (0–255)", self.slider_warmth)
        add_slider_row(slider_frame, "Focus (0–255)", self.slider_focus)

        btn = ctk.CTkButton(
            self.main_frame,
            text="Complete Avatar",
            command=self.generate_and_show_avatar
        )
        btn.pack(pady=15)

        # Frame where the matplotlib canvas (avatar) will live
        self.avatar_frame = ctk.CTkFrame(self.main_frame)
        self.avatar_frame.pack(fill="both", expand=True, pady=10)

    def next_page(self):
        """
        Global navigation:
        0 → start
        1–5 → question pages
        6 → sliders
        """
        if self.current_page == 0:
            self.current_page = 1
            self.show_question_page(1)
        elif 1 <= self.current_page <= 4:
            self.current_page += 1
            self.show_question_page(self.current_page)
        elif self.current_page == 5:
            self.current_page = 6
            self.show_slider_page()

    # ------- TRAITS + AVATAR -------

    def compute_traits(self):
        # Convert question answers → numeric traits
        trait_values = []
        for i, var in enumerate(self.question_vars):
            text = var.get()
            score = ANSWER_SCORES[i].get(text, 0.5)
            trait_values.append(score)

        # sliders: map 0–255 → 0–1
        energy = self.slider_energy.get() / 255.0
        warmth = self.slider_warmth.get() / 255.0
        focus = self.slider_focus.get() / 255.0

        return np.array(trait_values + [energy, warmth, focus])

    def generate_and_show_avatar(self):
        traits = self.compute_traits()

        intro_extro = traits[0]
        intuition = traits[1]
        playfulness = traits[2]
        speed = traits[3]
        emotionality = traits[4]
        openness = traits[5]
        flexibility = traits[6]
        abstractness = traits[7]
        mood = traits[8]
        chaos = traits[9]

        energy = traits[10]
        warmth = traits[11]
        focus = traits[12]

        # Map traits → visual parameters
        body_height = 0.6 + openness * 1.2
        body_width = 0.15 + emotionality * 0.2 * (1 + warmth * 0.5)
        head_size = 0.09 + playfulness * 0.07
        leg_length = 0.6 + energy * 0.7
        curve = (flexibility - 0.5) * (1 + focus * 0.5)
        noise_amount = chaos

        # Clear previous avatar canvas if exists
        if self.avatar_canvas is not None:
            self.avatar_canvas.get_tk_widget().destroy()
            self.avatar_canvas = None

        # Create matplotlib figure
        fig = Figure(figsize=(4, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1.5, 1.5)
        ax.axis("off")

        # Draw avatar
        draw_noise(ax, noise_amount)
        draw_body(ax, 0, 0.2, body_height, body_width, openness)
        draw_head(ax, 0, body_height / 2 + 0.35, head_size, abstractness)
        draw_legs(ax, 0, -body_height / 2, leg_length, curve)

        # Embed figure in Tkinter
        self.avatar_canvas = FigureCanvasTkAgg(fig, master=self.avatar_frame)
        self.avatar_canvas.draw()
        self.avatar_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app = AvatarApp()
    app.mainloop()

