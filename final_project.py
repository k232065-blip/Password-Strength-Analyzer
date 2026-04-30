import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
import random
import string
import winsound

# Load dictionary of frequently used passwords
def load_common_passwords():
    try:
        with open("common_passwords.txt", "r") as file:
            return {line.strip() for line in file}
    except FileNotFoundError:
        return {"123456", "password", "123456789", "12345678", "12345", "qwerty", "abc123", "111111", "123123"}

COMMON_PASSWORDS = load_common_passwords()

# Evaluate password strength
def evaluate_password_strength(password):
    length = len(password)
    contains_upper = any(char.isupper() for char in password)
    contains_lower = any(char.islower() for char in password)
    contains_number = any(char.isdigit() for char in password)
    contains_special = any(not char.isalnum() for char in password)
    is_in_dictionary = password in COMMON_PASSWORDS

    score = 0
    if length >= 8:
        score += 1
    if contains_upper:
        score += 1
    if contains_lower:
        score += 1
    if contains_number:
        score += 1
    if contains_special:
        score += 1
    if is_in_dictionary:
        score -= 2

    return max(score, 0), is_in_dictionary

# Simulate a common password check
def check_against_common_passwords(password):
    if password in COMMON_PASSWORDS:
        return "Your password is weak: Found in common password lists."
    return "Your password is secure: Not found in common password lists."

# Create a secure random password
def create_password():
    password_length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(random.choice(characters) for _ in range(password_length))
    password_var.set(secure_password)

# Update the displayed strength score
def update_password_score(*args):
    current_password = password_var.get()
    score, is_common = evaluate_password_strength(current_password)
    if is_common:
        score_label.config(text=f"Strength Score: {score} (Weak, Common Password)", fg="red")
    else:
        score_label.config(text=f"Strength Score: {score}", fg="black")

# Switch between visible and hidden password states
def toggle_visibility():
    if show_password_var.get():
        password_entry.config(show="")
        visibility_button.config(text="Hide Password")
    else:
        password_entry.config(show="*")
        visibility_button.config(text="Show Password")

# Show a loading animation before displaying feedback
def display_loading_animation():
    loading_frame = tk.Frame(root, bg="lightblue")
    loading_frame.pack(pady=10)

    progress = Progressbar(loading_frame, orient="horizontal", length=200, mode="determinate")
    progress.pack(pady=10)

    def increment_progress(value):
        progress["value"] = value
        if value < 100:
            loading_frame.after(20, increment_progress, value + 1)
        else:
            loading_frame.destroy()
            show_feedback()

    increment_progress(0)

# Provide feedback on password strength
def show_feedback():
    winsound.PlaySound('sound.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
    password = password_var.get()
    score, is_common = evaluate_password_strength(password)

    if score == 5:
        feedback_label.config(text="Strong password! Excellent work!", fg="green")
    elif score >= 3:
        feedback_label.config(text="Moderate password. Try using more diverse characters.", fg="orange")
    else:
        feedback_label.config(text="Weak password. Combine uppercase, lowercase, numbers, and symbols.", fg="red")

    if is_common:
        feedback_label.config(text=f"{feedback_label.cget('text')} Avoid common passwords.")

# Tips for better password practices
def display_password_tips():
    tips_window = tk.Toplevel(root)
    tips_window.title("Password Tips")
    tips_window.configure(bg="lightblue")

    tips = """Guidelines for Strong Passwords:
1. Use 12 or more characters.
2. Combine uppercase, lowercase, digits, and symbols.
3. Avoid using common passwords.
4. Use unrelated words in a passphrase.
5. A password manager can simplify secure password storage."""
    tk.Label(tips_window, text=tips, font=("Arial", 12), bg="lightblue", wraplength=400).pack(pady=10)

# GUI layout and setup
root = tk.Tk()
root.title("Password Strength Analyzer")
root.configure(bg="lightblue")

font_style = ("Arial", 12)

tk.Label(root, text="Enter a password:", font=font_style, bg="lightblue").pack(pady=10)
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, show="*", font=font_style)
password_entry.pack(pady=5)
password_var.trace_add("write", update_password_score)

score_label = tk.Label(root, text="Strength Score: 0", font=font_style, bg="lightblue")
score_label.pack(pady=10)

show_password_var = tk.BooleanVar()
visibility_button = tk.Checkbutton(root, text="Show Password", variable=show_password_var, command=toggle_visibility, bg="lightblue")
visibility_button.pack(pady=5)

ttk.Button(root, text="Analyze Password", command=display_loading_animation).pack(pady=10)
ttk.Button(root, text="Generate Secure Password", command=create_password).pack(pady=10)
ttk.Button(root, text="View Tips", command=display_password_tips).pack(pady=10)

feedback_label = tk.Label(root, text="", font=font_style, bg="lightblue")
feedback_label.pack(pady=10)

root.mainloop()