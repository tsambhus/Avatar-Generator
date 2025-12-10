# Avatar-Generator
is an interactive personality test that generates a unique avatar based on your answers. No two avatars look the same. Previous avatars have been added to a gallery that can be accessed [here](https://app.milanote.com/1VqOfZ1WwknkwQ?p=0uQVSkhlN3u).

## Licensing
Open Source

# Process
I began with sketches for how I wanted my final avatars to look.

<img width="476" height="756" alt="Screenshot 2025-12-10 at 10 04 44 AM" src="https://github.com/user-attachments/assets/158f1b2e-a3e7-4006-b6c9-064e4e9e5f63" />

Then I built a proof of concept in Colab.

<img width="489" height="454" alt="Screenshot 2025-12-03 at 7 55 43 AM" src="https://github.com/user-attachments/assets/c75f7f96-9832-4351-b9be-3f36c87a22a9" />


https://colab.research.google.com/drive/1MWxMykG0b-8Sn6kFAp19QJI1SsEvhFMY?usp=sharing

Then I moved onto a local version that runs tkinter.

# Method
To make the avatar, I used matplotlib to generate custom shapes. I wrote a bezier curve function that kept all shapes organic. Then, I wrote functions for the head, body and legs. The head was made with an oscillating cos shape. The body or spine were made with S shaped curves, and . The legs were long and flowing lines that tapered at the end.
Then, I wrote a function to define scoring logic. Each trait was assigned a value, that could be plugged into the functions of the avatar shape generator. In Colab, I used ipywidgets to run a basic prototype. Then, I transferred it to my local Python and used Tkinter to write the full quiz code.

# Prototype
I also designed an ideal working prototype in figma. This demonstrates what the UI will look like (when I have the time to figure Tkinter out).
[Prototype](https://www.figma.com/proto/ZE003m9Kh7Loik8TVISks7/Spiro-App?page-id=0%3A1&node-id=33-1760&p=f&viewport=100%2C-585%2C0.17&t=bzMYsy0pcW269KbN-1&scaling=min-zoom&content-scaling=fixed&starting-point-node-id=33%3A1760)

# Contributions
I used customtkinter, a library designed by Tom Schimansk. I used the matplotlib user guide to understand how to plot beziel curves. 
(https://matplotlib.org/stable/gallery/shapes_and_collections/quad_bezier.html), spines (https://matplotlib.org/stable/gallery/spines/index.html) I used a design from rudixtechnology on Instagram for one of my shapes. (https://www.instagram.com/reels/DRn_ul4kcVB/) I used chatGPT for help coding the Colab widgets library, and with Tkinter's UI generation.

# Author
My name is Tosha Sambhus and you can contact me at toshasambhus@gmail.com
