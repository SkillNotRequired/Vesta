import tkinter as tk
from tkinter import scrolledtext
import subprocess
import platform
import socket
import uuid
import getpass
import psutil
import threading
import time
import re
import random
import os

try:
    import wmi
except ImportError:
    wmi = None

try:
    import speedtest
except ImportError:
    speedtest = None

def get_system_info():
    info = []

    info.append("🔒 USER INFO")
    info.append(f"Username: {getpass.getuser()}")
    info.append(f"Computer Name: {platform.node()}")

    info.append("\n💥 SYSTEM INFO")
    info.append(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    info.append(f"CPU: {platform.processor()}")
    info.append(f"CPU Cores: {psutil.cpu_count(logical=False)} physical / {psutil.cpu_count()} logical")
    info.append(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")

    uptime_sec = time.time() - psutil.boot_time()
    uptime_str = time.strftime('%H:%M:%S', time.gmtime(uptime_sec))
    uptime_hours = uptime_sec / 3600
    info.append(f"Uptime: {uptime_str}")

    mood = "🍼 Just booted, still waking up..." if uptime_hours < 1 else (
        "🙂 Warmed up and cruising." if uptime_hours < 5 else "🔥 Been grinding. Respect the uptime!")
    info.append(f"System Mood: {mood}")

    if wmi:
        try:
            gpu = wmi.WMI().Win32_VideoController()[0]
            info.append(f"GPU: {gpu.Name}")
        except:
            info.append("GPU: Not available")
    else:
        info.append("GPU: WMI not installed")

    info.append("\n🌐 NETWORK INFO")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                    for i in range(0, 8 * 6, 8)][::-1])
    info.append(f"Local IP: {local_ip}")
    info.append(f"MAC Address: {mac}")

    try:
        system = platform.system()
        cmd = ["ping", "google.com", "-n", "5"] if system == "Windows" else ["ping", "google.com", "-c", "5"]
        ping_output = subprocess.check_output(cmd, universal_newlines=True)

        avg_ping = "?"
        if system == "Windows":
            match = re.search(r"Average = (\d+ms)", ping_output)
            if match:
                avg_ping = match.group(1)
        else:
            match = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)", ping_output)
            if match:
                avg_ping = f"{match.group(1)} ms"

        info.append(f"My current Ping to google.com (avg): {avg_ping}")
    except:
        info.append("Ping: Failed or not supported")

    if speedtest:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = round(st.download() / 1_000_000, 2)
            upload = round(st.upload() / 1_000_000, 2)
            info.append(f"Download Speed: {download} Mbps")
            info.append(f"Upload Speed: {upload} Mbps")
        except:
            info.append("Speed test: Error running test")
    else:
        info.append("Speed test: Not installed")

    info.append("\n💾 DRIVES")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            info.append(f"{part.device} ({part.mountpoint}): {round(usage.used / (1024**3), 2)} GB used of {round(usage.total / (1024**3), 2)} GB")
        except:
            continue

    info.append("\n⚙️ RUNNING PROCESSES (Top 5 by memory)")
    processes = sorted(psutil.process_iter(['pid', 'name', 'memory_info']),
                       key=lambda p: p.info['memory_info'].rss if p.info['memory_info'] else 0,
                       reverse=True)[:5]
    for p in processes:
        try:
            mem_mb = p.info['memory_info'].rss / (1024 ** 2)
            info.append(f"{p.info['name']} (PID {p.info['pid']}): {mem_mb:.1f} MB")
        except:
            pass

    quotes = [
        "“There are only two hard things in Computer Science: cache invalidation and naming things.”",
        "“It's not a bug – it's an undocumented feature.”",
        "“To understand recursion, you must first understand recursion.”",
        "“The code that is the hardest to debug is the code that you know cannot possibly be wrong.”",
        "“Computers make very fast, very accurate mistakes.”"
    ]
    quote = random.choice(quotes)
    info.append("\n💡 TECH WISDOM")
    info.append(quote)

    return "\n".join(info)

def refresh_info():
    def collect():
        info = get_system_info()
        output_box.after(0, lambda: output_box.delete("1.0", tk.END))
        output_box.after(0, lambda: output_box.insert(tk.END, info))

    threading.Thread(target=collect).start()

def launch_game():
    try:
        game_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Game.py")
        subprocess.Popen(["pythonw", game_path], shell=True)
    except Exception as e:
        output_box.insert(tk.END, f"\n❌ Failed to launch game: {e}\n")

# GUI Setup
root = tk.Tk()
root.title("ProgramV2")
root.geometry("700x720")

refresh_btn = tk.Button(root, text="🔄 Refresh Info", font=("Arial", 14), command=refresh_info)
refresh_btn.pack(pady=5)

game_btn = tk.Button(root, text="🕹 Launch Game", font=("Arial", 12), command=launch_game)
game_btn.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), width=90, height=34)
output_box.pack(padx=10, pady=10)

refresh_info()
root.mainloop()
