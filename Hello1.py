import tkinter as tk
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

# Label
label = tk.Label(root, text="What's your name?")
label.pack(pady=10)

# Text entry
entry = tk.Entry(root)
entry.pack()

# Button
button = tk.Button(root, text="Hi", command=greet)
button.pack(pady=10)

# Button 2
button2 = tk.Button(root, text="Test Sound", command=soundtest)
button2.pack(pady=10)

# Start of app
root.mainloop()