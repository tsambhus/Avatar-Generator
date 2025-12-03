# Avatar-Generator
is an interactive personality test that generates a unique avatar based on your answers. No two avatars look the same. Your avatar will be added to a gallery that can be accessed [here]([https://app.milanote.com/1VlHUf1AVrjP6W?p=GDAzJHBZq1Q]).
https://app.milanote.com/1VlHUf1AVrjP6W?p=GDAzJHBZq1Q

# Process
I began with a proof of concept in Colab.
<img width="489" height="454" alt="Screenshot 2025-12-03 at 7 55 43 AM" src="https://github.com/user-attachments/assets/c75f7f96-9832-4351-b9be-3f36c87a22a9" />

https://colab.research.google.com/drive/1MWxMykG0b-8Sn6kFAp19QJI1SsEvhFMY?usp=sharing

Then I moved onto a local version that runs tkinter.

# Method
To make the avatar, I used matplotlib to generate custom shapes. I wrote a bezier curve functi

on that kept all shapes organic. Then, I wrote functions for the head, body and legs. The head was made with an organic blob. The body or spine was made with a S shaped curve. The legs were long and flowing lines that tapered at the end.
Then, I wrote a function to define scoring logic. Each trait was assigned a value, that could be plugged into the functions of the avatar shape generator. In Colab, I used ipywidgets to run a basic prototype. Then, I transferred it to my local Python and used Tkinter to write the full quiz code.


# Contributions
I used customtkinter, a library designed by Tom Schimansk. I used chatGPT for help finding the Colab widgets module and for help translating the colab to the confusing parts of customTkinter. 

# Author
My name is Tosha and you can contact me at tsambhus@pratt.edu.
