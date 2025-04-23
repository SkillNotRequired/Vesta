import tkinter as tk
import Game
import Play
from Play import surprise
from Game import game
from tkinter import messagebox
from playsound import playsound

def greet():
	name = entry.get()
	if name.strip():
		messagebox.showinfo("Greetings", f"Nice to see ya, {name}!")
	else:
		playsound("ErrorBeats.mp3")
		messagebox.showwarning("Oops!","This name is banned.")

def soundtest():
	playsound("ErrorBeats.mp3")

# Main window
root = tk.Tk()
root.title("Say Hello")
root.geometry("300x150")

# Frame making
Hi_Frame = tk.Frame(root)
btn_Frame = tk.Frame(root)

# Label
label = tk.Label(Hi_Frame, text="What's your name?")

# Text entry
entry = tk.Entry(Hi_Frame)

# Buttons
btn = tk.Button(Hi_Frame, text="Hi", command=greet)
btn2 = tk.Button(btn_Frame, text="Test Sound", command=soundtest)
btn3 = tk.Button(
	btn_Frame, 
	text="Ball Game", 
	bg="lightblue", 
	fg="darkblue", 
	command=game
)
btn4 = tk.Button(root, text="????", bg="tomato", fg="darkred", command=surprise)

# Packing

Hi_Frame.pack(side="left", padx=30)
btn_Frame.pack(side="left")
label.pack(pady=10)
entry.pack()
btn.pack(pady=5)
btn2.pack(pady=10)
btn3.pack()
btn4.place(x=350, y=200)

# Start of app
root.mainloop()