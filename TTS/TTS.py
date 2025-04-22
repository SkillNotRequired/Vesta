import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import io
import threading
from pydub import AudioSegment
import simpleaudio as sa
from cryptography.fernet import Fernet

# === Load encrypted secrets file ===
DECRYPTION_KEY = b'x9s0oZv-1c1z_abiYW-kMbmLkM6UVCTU__KCq25X1PM='  # Replace with your key from encryption script

try:
    with open("secrets.enc", "rb") as f:
        encrypted_data = f.read()

    decrypted_data = Fernet(DECRYPTION_KEY).decrypt(encrypted_data)
    secrets = json.loads(decrypted_data.decode())

    API_KEY = secrets["ELEVEN_API_KEY"]
except Exception as e:
    raise RuntimeError(f"Failed to decrypt secrets: {e}")

# === Allowed voice names ===
ALLOWED_VOICES = [
    "Gabe", "Andrew Garfield", "QOP", "Vash", "Voice Spirit",
    "Halo", "Legion Commander", "Counter Strike", "Shaxx", "Glados", "DMZ Warzone"
]

# === Fetch allowed voices from ElevenLabs ===
def fetch_voices():
    headers = {"xi-api-key": API_KEY}
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    if response.status_code == 200:
        all_voices = response.json()["voices"]
        return [v for v in all_voices if v["name"] in ALLOWED_VOICES]
    else:
        messagebox.showerror("Error", f"Could not fetch voices:\n{response.text}")
        return []

# === ElevenLabs TTS function ===
def synthesize_text(text, voice_id):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        return AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    else:
        messagebox.showerror("Error", f"API Error: {response.status_code}\n{response.text}")
        return None

# === Main App ===
class DubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ElevenLabs Dub App")
        self.audio = None
        self.play_obj = None
        self.playing = False
        self.update_slider = True
        self.position_ms = 0

        self.voices = fetch_voices()
        self.voice_options = {v["name"]: v["voice_id"] for v in self.voices}

        # === Voice Dropdown
        self.voice_var = tk.StringVar(value=list(self.voice_options.keys())[0])
        ttk.Label(root, text="Select a voice:").pack(pady=(10, 0))
        self.voice_menu = ttk.Combobox(root, textvariable=self.voice_var, values=list(self.voice_options.keys()), state="readonly")
        self.voice_menu.pack()

        # === Text Box
        ttk.Label(root, text="Enter text (max 500 chars):").pack(pady=(10, 0))
        self.text_entry = tk.Text(root, height=5, width=50)
        self.text_entry.pack()
        self.text_entry.bind("<KeyRelease>", self.limit_text)

        # === Speak Button
        ttk.Button(root, text="🔊 Speak", command=self.speak).pack(pady=5)

        # === Audio Controls
        self.slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=400, command=self.slider_moved)
        self.slider.pack(pady=5)

        self.play_pause_btn = ttk.Button(root, text="▶️ Play", command=self.toggle_play_pause)
        self.play_pause_btn.pack()

        self.slider_label = ttk.Label(root, text="0.0 / 0.0 sec")
        self.slider_label.pack()

    def limit_text(self, event=None):
        current = self.text_entry.get("1.0", "end-1c")
        if len(current) > 500:
            self.text_entry.delete("1.0", "end")
            self.text_entry.insert("1.0", current[:500])

    def speak(self):
        text = self.text_entry.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Empty", "Please enter some text.")
            return

        voice_id = self.voice_options[self.voice_var.get()]
        self.audio = synthesize_text(text, voice_id)

        if self.audio:
            self.position_ms = 0
            self.slider.config(to=len(self.audio))
            self.slider.set(0)
            self.slider_label.config(text=f"0.0 / {len(self.audio)/1000:.1f} sec")
            self.play_audio()

    def play_audio(self):
        if not self.audio:
            return
        self.stop_audio()
        slice = self.audio[self.position_ms:]
        raw = slice.raw_data
        self.play_obj = sa.play_buffer(
            raw,
            num_channels=slice.channels,
            bytes_per_sample=slice.sample_width,
            sample_rate=slice.frame_rate
        )
        self.playing = True
        self.play_pause_btn.config(text="⏸️ Pause")
        threading.Thread(target=self.track_progress, daemon=True).start()

    def stop_audio(self):
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
        self.playing = False

    def toggle_play_pause(self):
        if not self.audio:
            return
        if self.playing:
            self.stop_audio()
            self.play_pause_btn.config(text="▶️ Play")
        else:
            self.play_audio()

    def track_progress(self):
        total = len(self.audio)
        while self.playing and self.play_obj and self.play_obj.is_playing():
            self.position_ms += 100
            if self.position_ms >= total:
                break
            self.update_slider = False
            self.slider.set(self.position_ms)
            self.update_slider = True
            self.slider_label.config(text=f"{self.position_ms/1000:.1f} / {total/1000:.1f} sec")
            self.root.update_idletasks()
            self.root.after(100)
        self.playing = False
        self.play_pause_btn.config(text="▶️ Play")

    def slider_moved(self, value):
        if not self.audio or not self.update_slider:
            return
        self.position_ms = int(float(value))
        self.stop_audio()
        self.slider_label.config(text=f"{self.position_ms/1000:.1f} / {len(self.audio)/1000:.1f} sec")

# === Launch App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = DubApp(root)
    root.mainloop()
