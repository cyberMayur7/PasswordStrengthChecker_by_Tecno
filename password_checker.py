import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random
import string
import pyperclip
import time
import os
from datetime import datetime

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
    casual_tips = [
        "Yeh password hacker ko bhagayega! 💪",
        "Casual vibe: Easy to remember, hard to crack! 😎",
        "Stronger than your coffee! ☕🔒",
        "Avoid 'password123' – yeh weak hai! 🚫"
    ]
    
    for i in range(num_passwords):
        password = ''.join(random.choice(chars) for _ in range(length))
        if style == "Casual":
            # Make it slightly memorable (e.g., mix words but secure)
            words = ["secure", "strong", "safe", "lock", "guard"]
            base = random.choice(words) + str(random.randint(10,99)) + random.choice("!@#")
            password = base + ''.join(random.choice(chars) for _ in range(length - len(base)))
        elif style == "Funny":
            # Fun but secure (e.g., add punny chars)
            fun_suffix = random.choice(["HahaSecure!", "CrackMeNot😂", "PwndByMe!"])
            password = ''.join(random.choice(chars) for _ in range(length - len(fun_suffix))) + fun_suffix
            password = password[:length]  # Ensure length
        
        passwords.append(password)
        save_to_history(password, "Generated", f"generated ({style})")
    
    tip = random.choice(casual_tips)
    return passwords, tip

def copy_to_clipboard(text):
    pyperclip.copy(text)
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
        messagebox.showinfo("Exported!", f"History saved to {filename} ✅")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {e}")

# GUI Setup
def create_gui():
    root = tk.Tk()
    root.title("Password Strength Checker - Casual Edition! 😎")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")
    
    # Style for casual look
    style = ttk.Style()
    style.theme_use('clam')
    
    # Input frame
    input_frame = ttk.Frame(root, padding="10")
    input_frame.pack(fill=tk.X)
    
    ttk.Label(input_frame, text="Enter Password:").grid(row=0, column=0, sticky=tk.W)
    password_entry = ttk.Entry(input_frame, show="*", width=40, font=("Arial", 12))
    password_entry.grid(row=0, column=1, padx=5)
    
    ttk.Button(input_frame, text="Check Strength", command=lambda: check_and_show()).grid(row=0, column=2, padx=5)
    
    # Generator frame
    gen_frame = ttk.LabelFrame(root, text="Generate Casual Passwords", padding="10")
    gen_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(gen_frame, text="Length:").grid(row=0, column=0)
    length_var = tk.IntVar(value=12)
    length_spin = ttk.Spinbox(gen_frame, from_=8, to=50, textvariable=length_var, width=5)
    length_spin.grid(row=0, column=1, padx=5)
    
    ttk.Label(gen_frame, text="Style:").grid(row=0, column=2)
    style_var = tk.StringVar(value="Strong")
    style_combo = ttk.Combobox(gen_frame, textvariable=style_var, values=["Casual", "Strong", "Funny"], state="readonly", width=10)
    style_combo.grid(row=0, column=3, padx=5)
    
    num_var = tk.IntVar(value=2)  # Default 2 passwords
    ttk.Label(gen_frame, text="Count:").grid(row=0, column=4)
    num_spin = ttk.Spinbox(gen_frame, from_=1, to=5, textvariable=num_var, width=5)
    num_spin.grid(row=0, column=5, padx=5)
    
    # Fixed: Use grid instead of pack for button
    ttk.Button(gen_frame, text="Generate & Copy", command=lambda: generate_and_show()).grid(row=1, column=0, columnspan=6, pady=5)
    
    # Results frame
    result_frame = ttk.LabelFrame(root, text="Results & Feedback", padding="10")
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    result_text = scrolledtext.ScrolledText(result_frame, height=10, width=70, font=("Arial", 10))
    result_text.pack(fill=tk.BOTH, expand=True)
    
    # History frame
    history_frame = ttk.LabelFrame(root, text="History (Last 10)", padding="10")
    history_frame.pack(fill=tk.X, padx=10, pady=5)
    
    history_list = tk.Listbox(history_frame, height=4)
    history_list.pack(fill=tk.X)
    
    def update_history():
        history = load_history()[-10:]  # Last 10
        history_list.delete(0, tk.END)
        for entry in history:
            history_list.insert(tk.END, entry)
    
    ttk.Button(history_frame, text="Refresh History", command=update_history).pack(side=tk.LEFT)
    ttk.Button(history_frame, text="Export History", command=export_history).pack(side=tk.RIGHT)
    
    # Initial load
    update_history()
    
    def check_and_show():
        password = password_entry.get()
        if not password:
            messagebox.showwarning("Empty", "Enter a password first! 😅")
            return
        score, level, feedback = check_strength(password)
        save_to_history(password, f"{score}/100 ({level})", "checked")
        
        result = f"Strength Score: {score}/100 ({level}) 🎯\n\nFeedback:\n" + "\n".join(feedback)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        update_history()
    
    def generate_and_show():
        length = length_var.get()
        style = style_var.get()
        num = num_var.get()
        passwords, tip = generate_password(length, True, True, True, True, style, num)
        
        result = f"Generated {num} {style} Password(s):\n\n"
        for i, pw in enumerate(passwords, 1):
            result += f"{i}. {pw}\n"
            if i == 1:  # Copy first one auto
                copy_to_clipboard(pw)
        result += f"\nTip: {tip}\n\nCopy the first one – it's ready! 📋"
        
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        update_history()
    
    root.mainloop()

if __name__ == "__main__":
    # Check if Tkinter available (for non-GUI fallback)
    try:
        create_gui()
    except ImportError:
        print("Tkinter not available. Running console mode...")
        # Console fallback code here (original console version if needed)
        pass