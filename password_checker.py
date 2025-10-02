import secrets
import string
import pyperclip
import time  # For history timestamp
import os    # For file operations

# New Feature: Password history file
HISTORY_FILE = "password_history.txt"

def calculate_strength(password):
    """
    Password strength calculate karta hai.
    Score based on: length, uppercase, lowercase, numbers, special chars.
    Returns: (strength_level, score, details)
    """
    score = 0
    details = []
    
    # Length check
    length = len(password)
    if length < 8:
        details.append("Length < 8: Weak")
    elif length <= 12:
        score += 1
        details.append("Length 8-12: Medium")
    else:
        score += 2
        details.append(f"Length {length}: Strong")
    
    # Lowercase
    if any(c.islower() for c in password):
        score += 1
        details.append("Has lowercase: Good")
    else:
        details.append("No lowercase: Weak")
    
    # Uppercase
    if any(c.isupper() for c in password):
        score += 1
        details.append("Has uppercase: Good")
    else:
        details.append("No uppercase: Weak")
    
    # Numbers
    if any(c.isdigit() for c in password):
        score += 1
        details.append("Has numbers: Good")
    else:
        details.append("No numbers: Weak")
    
    # Special characters
    special = string.punctuation
    if any(c in special for c in password):
        score += 1
        details.append("Has special chars: Strong")
    else:
        details.append("No special chars: Weak")
    
    # Strength level
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"
    
    return strength, score, details

def estimate_crack_time(password):
    """
    New Feature: Brute force cracking time estimate.
    Assumes 10^8 attempts/second (average GPU speed).
    For demo only - real cracking depends on hash type, etc.
    """
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32  # Approx special chars
    
    if charset_size == 0:
        return "Invalid password"
    
    length = len(password)
    attempts = charset_size ** length
    seconds = attempts / 1e8  # 10^8 attempts/sec
    
    if seconds < 60:
        return f"~{seconds:.2f} seconds (Very fast to crack!)"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"~{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"~{hours:.2f} hours"
    else:
        days = seconds / 86400
        return f"~{days:.2f} days (Still crackable with dictionary/rainbow if weak)"

def generate_strong_password(length=16):
    """
    Secure random password generate karta hai using secrets.
    Includes all char types for strength.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def save_to_history(password):
    """
    New Feature: Password ko history file mein save karta hai with timestamp.
    Last 5 only keep karta hai.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp}: {password}\n"
    
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            lines = f.readlines()
        lines.insert(0, entry)  # Add at top
        if len(lines) > 5:  # Keep last 5
            lines = lines[:5]
        with open(HISTORY_FILE, 'w') as f:
            f.writelines(lines)
    else:
        with open(HISTORY_FILE, 'w') as f:
            f.write(entry)

def export_history(filename="exported_passwords.txt"):
    """
    New Feature: History ko external file mein export.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as src, open(filename, 'w') as dst:
            dst.write(src.read())
        print(f"History exported to {filename}")
    else:
        print("No history to export.")

def main():
    print("=== Password Strength Checker ===")
    print("Password Cracking Concepts (Educational):")
    print("- Brute Force: Har possible combo try karta hai (slow for long passwords).")
    print("- Dictionary: Common words list se try karta hai (fast for weak passwords).")
    print("- Rainbow Tables: Pre-computed hashes use karta hai (fast for unsalted hashes).")
    print("Yeh tool ethical use ke liye hai - strong passwords banao to avoid cracking!\n")
    
    while True:
        choice = input("1. Check Password Strength\n2. Generate Strong Password\n3. View History\n4. Export History\n5. Exit\nEnter choice: ")
        
        if choice == '1':
            password = input("Enter password to check: ")
            if not password:
                print("No password entered!")
                continue
            strength, score, details = calculate_strength(password)
            crack_time = estimate_crack_time(password)
            print(f"\nStrength: {strength} (Score: {score}/5)")
            for detail in details:
                print(f"- {detail}")
            print(f"Estimated Brute Force Crack Time: {crack_time}")
        
        elif choice == '2':
            length = int(input("Enter length (default 16): ") or 16)
            password = generate_strong_password(length)
            strength, score, _ = calculate_strength(password)  # Verify it's strong
            print(f"\nGenerated Password: {password}")
            print(f"Strength: {strength} (Score: {score}/5)")
            copy = input("Copy to clipboard? (y/n): ").lower()
            if copy == 'y':
                pyperclip.copy(password)
                print("Copied to clipboard!")
            save_to_history(password)  # Save to history
        
        elif choice == '3':
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    print("\nPassword History:")
                    print(f.read())
            else:
                print("No history yet.")
        
        elif choice == '4':
            export_history()
        
        elif choice == '5':
            print("Bye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()