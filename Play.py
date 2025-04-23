import tkinter as tk
import time
import random

# Phase 1: Face animation
faces = [":|", ":)", ";)", ":D"]
face_duration = 10  # seconds
bomb_duration = 5   # seconds

def surprise():
	root1 = tk.Tk()
	root1.title("Face to Bomb")
	root1.geometry("300x200")  # initial size
	
	face_label = tk.Label(root1, text="", font=("Helvetica", 48))
	face_label.pack(pady=20)
	
	timer_label = tk.Label(root1, text="", font=("Helvetica", 20))
	timer_label.pack()
	
	face_index = 0
	start_time = time.time()
	
	def move_window(times_left):
	    if times_left > 0:
	        x = random.randint(100, 1000)
	        y = random.randint(100, 600)
	        root1.geometry(f"+{x}+{y}")
	        root1.after(200, lambda: move_window(times_left - 1))
	    else:
	        root1.destroy()
	
	def fake_delete_system32(progress=0):
	    if progress <= 100:
	        face_label.config(font=("Courier", 16), text=f"Deleting system32... {progress}%")
	        root1.update_idletasks()
	        root1.geometry("")  # auto-resize window to fit contents
	        root1.after(100, lambda: fake_delete_system32(progress + 5))
	    else:
	        face_label.config(text="System32 successfully deleted! 💀")
	        timer_label.config(text="")
	        root1.update_idletasks()
	        root1.geometry("")
	        root1.after(1000, lambda: move_window(20))
	
	def update_bomb(time_left):
	    if time_left > 0:
	        fuse = "=" * time_left
	        face_label.config(text=f"💣{fuse}")
	        timer_label.config(text=f"Time left: {time_left}s")
	        root1.update_idletasks()
	        root1.geometry("")
	        root1.after(1000, lambda: update_bomb(time_left - 1))
	    else:
	        face_label.config(text="💥 BOOM!")
	        timer_label.config(text="")
	        root1.update_idletasks()
	        root1.geometry("")
	        root1.after(1000, fake_delete_system32)
	
	def update_face():
	    nonlocal face_index
	    elapsed = time.time() - start_time
	    remaining = max(0, int(face_duration - elapsed))
	
	    face_label.config(text=faces[face_index % len(faces)])
	    timer_label.config(text=f"Time left: {remaining}s")
	    face_index += 1
	
	    root1.update_idletasks()
	    root1.geometry("")
	
	    if remaining > 0:
	        root1.after(500, update_face)
	    else:
	        start_bomb()
	
	def start_bomb():
	    face_label.config(font=("Helvetica", 36))
	    update_bomb(bomb_duration)
	
	# Start the face animation
	update_face()
	
	root1.mainloop()	