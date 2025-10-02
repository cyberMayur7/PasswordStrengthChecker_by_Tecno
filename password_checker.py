import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random
import string
import pyperclip
import time
import os
from datetime import datetime
import pygame  # For sound effects

# Initialize pygame mixer for sounds
pygame.mixer.init()

# Simple sound functions (tones without files – pygame generates)
def play_beep(frequency=800, duration=0.2):
    try:
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = pygame.sndarray.make_sound(pygame.sndarray.array(pygame.mixer.Sound(buffer=b'\x00\x7f' * frames)))  # Simple beep
        arr = arr * (frequency / 440)  # Adjust pitch
        sound = pygame.sndarray.make_sound(arr)
        sound.play()
    except:
        pass  # Silent if error

def play_scan_sound():
    play_beep(600, 0.1)  # Low scan beep
    time.sleep(0.05)
    play_beep(800, 0.1)

def play_success_sound():
    play_beep(1000, 0.3)  # High success

# History file path
HISTORY_FILE = "password_history.txt"

def load_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    history.append(line.strip())
        except Exception as e:
            print(f"Error loading history: {e}")
    return history

def save_to_history(password, strength="Unknown", action="checked"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action.capitalize()}: '{password}' (Strength: {strength})"
    history = load_history()
    history.append(entry)
    try:
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(entry + '\n')
    except Exception as e:
        print(f"Error saving history: {e}")

def check_strength(password):
    score = 0
    feedback = []
    
    # Length
    if len(password) >= 12:
        score += 30
        feedback.append("Length: Strong! 💪")
    elif len(password) >= 8:
        score += 20
        feedback.append("Length: Good 👍")
    else:
        score += 0
        feedback.append("Length: Too short! Add more chars.")
    
    # Uppercase
    if any(c.isupper() for c in password):
        score += 15
        feedback.append("Uppercase: Included! 🔒")
    else:
        feedback.append("Add uppercase letters.")
    
    # Lowercase
    if any(c.islower() for c in password):
        score += 15
        feedback.append("Lowercase: Good! 📝")
    else:
        feedback.append("Add lowercase letters.")
    
    # Numbers
    if any(c.isdigit() for c in password):
        score += 20
        feedback.append("Numbers: Secure! 🔢")
    else:
        feedback.append("Add numbers for strength.")
    
    # Symbols
    if any(c in string.punctuation for c in password):
        score += 20
        feedback.append("Symbols: Extra protection! ⚡")
    else:
        feedback.append("Add symbols like !@#.")
    
    # Common patterns (basic check)
    common_weak = ["123", "abc", "password", "qwerty"]
    if any(weak in password.lower() for weak in common_weak):
        score -= 20
        feedback.append("Warning: Common pattern detected! Change it. 🚨")
    
    # Brute-force estimate (simple entropy-based)
    chars = len(set(password))
    entropy = len(password) * 4.7  # Approx bits per char
    guesses_per_sec = 10**9  # Modern GPU speed
    crack_time_years = (2 ** entropy) / (guesses_per_sec * 60 * 60 * 24 * 365 * 10**6)  # Rough calc
    if crack_time_years > 10**12:
        time_str = "Eternity! (Trillions of years) 🌌"
    elif crack_time_years > 100:
        time_str = f"{int(crack_time_years):,} years 😎"
    else:
        time_str = f"{int(crack_time_years * 365 * 24 * 3600)} seconds ⚠️"
    
    feedback.append(f"Crack Time: {time_str}")
    
    strength_level = "Very Strong" if score >= 80 else "Strong" if score >= 60 else "Medium" if score >= 40 else "Weak"
    return score, strength_level, feedback

def generate_password(length=12, include_upper=True, include_lower=True, include_digits=True, include_symbols=True, style="Strong", num_passwords=2):
    chars = ""
    if include_lower:
        chars += string.ascii_lowercase
    if include_upper:
        chars += string.ascii_uppercase
    if include_digits:
        chars += string.digits
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        return ["No characters selected!"], "No chars? Select options! 😅"
    
    passwords = []
    meme_tips = [  # More fun memes!
        "This password is stronger than Thanos! 🦸‍♂️ No snap needed.",
        "Don't be like this: '123456' – RIP your security 😂💀",
        "Hacker approved: Uncrackable like a vault! 🔐🕵️‍♂️",
        "Casual mode: Easy peasy, but hackers hate it! 🤪🚫",
        "Generated like a boss – copy & conquer! 👑📋"
    ]
    
    for i in range(num_passwords):
        password = ''.join(random.choice(chars) for _ in range(length))
        if style == "Casual":
            words = ["secure", "strong", "safe", "lock", "guard"]
            base = random.choice(words) + str(random.randint(10,99)) + random.choice("!@#")
            password = base + ''.join(random.choice(chars) for _ in range(length - len(base)))
        elif style == "Funny":
            fun_suffix = random.choice(["HahaSecure!", "CrackMeNot😂", "PwndByMe!"])
            password = ''.join(random.choice(chars) for _ in range(length - len(fun_suffix))) + fun_suffix
            password = password[:length]
        
        passwords.append(password)
        save_to_history(password, "Generated", f"generated ({style})")
    
    tip = random.choice(meme_tips)
    return passwords, tip

def copy_to_clipboard(text):
    pyperclip.copy(text)
    play_success_sound()
    messagebox.showinfo("Copied!", "Password copied to clipboard! 📋")

def export_history():
    history = load_history()
    if not history:
        messagebox.showwarning("Empty", "No history to export!")
        return
    
    filename = f"password_history_{int(time.time())}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(history))
        play_success_sound()
        messagebox.showinfo("Exported!", f"History saved to {filename} ✅")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {e}")

# Typing animation function (hacker-style)
def type_text(widget, text, speed=0.05):
    widget.delete(1.0, tk.END)
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        time.sleep(speed)
    widget.insert(tk.END, "\n")  # New line

# Flashing animation for score
def flash_score(label, color="green", times=3):
    original_color = label.cget("foreground")
    for _ in range(times):
        label.config(foreground=color)
        label.update()
        time.sleep(0.2)
        label.config(foreground=original_color)
        label.update()
        time.sleep(0.2)

# GUI Setup
def create_gui():
    root = tk.Tk()
    root.title("Hacker Mode: Password Strength Checker - TECNO_MAYUR Edition! 🕵️‍♂️💻")
    root.geometry("700x600")
    root.configure(bg="black")  # Hacker black bg
    
    # Style for hacker theme
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", foreground="lime", background="black", font=("Courier", 10))  # Monospace green
    style.configure("TButton", foreground="black", background="green", font=("Courier", 10, "bold"))
    style.configure("TEntry", foreground="lime", fieldbackground="black")
    style.configure("TCombobox", foreground="lime", fieldbackground="black")
    style.configure("TSpinbox", foreground="lime", fieldbackground="black")
    
    # Title label with animation
    title_label = tk.Label(root, text="Hacker Mode Activated! 🔓", font=("Courier", 16, "bold"), fg="lime", bg="black")
    title_label.pack(pady=10)
    
    # Input frame (green theme)
    input_frame = ttk.Frame(root, padding="10")
    input_frame.pack(fill=tk.X)
    
    ttk.Label(input_frame, text="Enter Password:").grid(row=0, column=0, sticky=tk.W)
    password_entry = ttk.Entry(input_frame, show="*", width=40, font=("Courier", 12))
    password_entry.grid(row=0, column=1, padx=5)
    
    check_btn = ttk.Button(input_frame, text="Scan Strength", command=lambda: check_and_show())
    check_btn.grid(row=0, column=2, padx=5)
    
    # Generator frame
    gen_frame = ttk.LabelFrame(root, text="Generate Hacker Passwords", padding="10")
    gen_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(gen_frame, text="Length:").grid(row=0, column=0)
    length_var = tk.IntVar(value=12)
    length_spin = ttk.Spinbox(gen_frame, from_=8, to=50, textvariable=length_var, width=5)
    length_spin.grid(row=0, column=1, padx=5)
    
    ttk.Label(gen_frame, text="Style:").grid(row=0, column=2)
    style_var = tk.StringVar(value="Strong")
    style_combo = ttk.Combobox(gen_frame, textvariable=style_var, values=["Casual", "Strong", "Funny"], state="readonly", width=10)
    style_combo.grid(row=0, column=3, padx=5)
    
    num_var = tk.IntVar(value=2)
    ttk.Label(gen_frame, text="Count:").grid(row=0, column=4)
    num_spin = ttk.Spinbox(gen_frame, from_=1, to=5, textvariable=num_var, width=5)
    num_spin.grid(row=0, column=5, padx=5)
    
    gen_btn = ttk.Button(gen_frame, text="Generate & Hack It! 💥", command=lambda: generate_and_show())
    gen_btn.grid(row=1, column=0, columnspan=6, pady=5)
    
    # Results frame
    result_frame = ttk.LabelFrame(root, text="Hack Results", padding="10")
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80, font=("Courier", 10), fg="lime", bg="black", insertbackground="lime")
    result_text.pack(fill=tk.BOTH, expand=True)
    
    # Score label for flashing
    score_label = tk.Label(result_frame, text="", font=("Courier", 14, "bold"), fg="red", bg="black")
    score_label.pack(pady=5)
    
    # History frame
    history_frame = ttk.LabelFrame(root, text="Hack History (Last 10)", padding="10")
    history_frame.pack(fill=tk.X, padx=10, pady=5)
    
    history_list = tk.Listbox(history_frame, height=4, fg="lime", bg="black", font=("Courier", 9), selectbackground="green")
    history_list.pack(fill=tk.X)
    
    def update_history():
        history = load_history()[-10:]
        history_list.delete(0, tk.END)
        for entry in history:
            history_list.insert(tk.END, entry)
    
    ttk.Button(history_frame, text="Refresh Logs", command=update_history).pack(side=tk.LEFT)
    export_btn = ttk.Button(history_frame, text="Export Data", command=export_history)
    export_btn.pack(side=tk.RIGHT)
    
    # Watermark: TECNO_MAYUR
    watermark = tk.Label(root, text="Created by TECNO_MAYUR 🛡️", font=("Courier", 8), fg="gray", bg="black")
    watermark.pack(side=tk.BOTTOM, pady=5)
    
    # Initial load
    update_history()
    
    def check_and_show():
        play_scan_sound()
        password = password_entry.get()
        if not password:
            messagebox.showwarning("Alert!", "Enter a password first! 😅")
            return
        score, level, feedback = check_strength(password)
        save_to_history(password, f"{score}/100 ({level})", "checked")
        
        result = f"Strength Score: {score}/100 ({level}) 🎯\n\nFeedback:\n"
        for fb in feedback:
            result += fb + "\n"
        
        # Typing animation
        root.after(0, lambda: type_text(result_text, result, 0.03))  # Hacker typing speed
        
        # Flash score
        score_label.config(text=f"Score: {score}/100 - {level}")
        root.after(500, lambda: flash_score(score_label, "lime" if score >= 60 else "red", 4))
        
        update_history()
    
    def generate_and_show():
        play_beep(500, 0.1)  # Loading sound
        length = length_var.get()
        style = style_var.get()
        num = num_var.get()
        passwords, tip = generate_password(length, True, True, True, True, style, num)
        
        result = f"Generated {num} {style} Password(s):\n\n"
        for i, pw in enumerate(passwords, 1):
            result += f"{i}. {pw}\n"
            if i == 1:
                copy_to_clipboard(pw)
        result += f"\nMeme Tip: {tip}\n\nFirst one copied – Hack on! 🕶️"
        
        # Typing animation for results
        root.after(300, lambda: type_text(result_text, result, 0.04))
        
        # Success flash
        score_label.config(text="Generation Complete! 💻")
        root.after(800, lambda: flash_score(score_label, "green", 3))
        
        update_history()
        play_success_sound()
    
    root.mainloop()

if __name__ == "__main__":
    try:
        create_gui()
    except ImportError as e:
        print(f"Error: {e}. Install missing libs: pip install pygame pyperclip")
        # Console fallback if needed
        pass