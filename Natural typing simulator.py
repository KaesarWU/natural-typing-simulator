import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import random
import threading
import pyautogui

class NaturalTypingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Natural Typing Simulator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.is_typing = False
        self.typing_thread = None
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Natural Typing Simulator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Instructions
        instructions = ("Paste your text below and click 'Start Typing'. "
                       "The app will type it out naturally with variable speed and pauses. "
                       "Make sure your cursor is in the target application!")
        instruction_label = ttk.Label(main_frame, text=instructions, wraplength=580)
        instruction_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Text area
        text_label = ttk.Label(main_frame, text="Text to type:")
        text_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.text_area = scrolledtext.ScrolledText(main_frame, width=70, height=15)
        self.text_area.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Settings frame
        settings_frame = ttk.Frame(main_frame)
        settings_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # WPM settings
        wpm_label = ttk.Label(settings_frame, text="Average WPM:")
        wpm_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.wpm_var = tk.StringVar(value="50")
        wpm_entry = ttk.Entry(settings_frame, textvariable=self.wpm_var, width=5)
        wpm_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        # Delay before start
        delay_label = ttk.Label(settings_frame, text="Start delay (seconds):")
        delay_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        self.delay_var = tk.StringVar(value="3")
        delay_entry = ttk.Entry(settings_frame, textvariable=self.delay_var, width=5)
        delay_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Start button
        self.start_button = ttk.Button(buttons_frame, text="Start Typing", command=self.start_typing)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.stop_typing, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready. Paste your text above.")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
    def start_typing(self):
        if self.is_typing:
            return
            
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.status_var.set("Please enter some text to type.")
            return
            
        try:
            wpm = int(self.wpm_var.get())
            if wpm < 10 or wpm > 120:
                raise ValueError("WPM should be between 10 and 120")
        except ValueError:
            self.status_var.set("Please enter a valid WPM (10-120).")
            return
            
        try:
            delay = int(self.delay_var.get())
            if delay < 0:
                raise ValueError("Delay should be a positive number")
        except ValueError:
            self.status_var.set("Please enter a valid delay.")
            return
            
        self.is_typing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set(f"Starting in {delay} seconds... Move cursor to target application!")
        
        # Start typing in a separate thread to keep UI responsive
        self.typing_thread = threading.Thread(
            target=self.type_text, 
            args=(text, wpm, delay)
        )
        self.typing_thread.daemon = True
        self.typing_thread.start()
        
    def stop_typing(self):
        self.is_typing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Typing stopped.")
        
    def type_text(self, text, wpm, delay):
        # Wait for the specified delay
        time.sleep(delay)
        
        if not self.is_typing:
            return
            
        self.root.after(0, lambda: self.status_var.set("Typing in progress..."))
        
        # Calculate base time per character (in seconds)
        base_time_per_char = 60.0 / (wpm * 5)  # Assuming 5 characters per word
        
        # Type the text character by character
        for i, char in enumerate(text):
            if not self.is_typing:
                break
                
            # Type the character
            pyautogui.write(char)
            
            # Calculate delay with natural variations
            if char in '.!?':  # Longer pause after sentences
                delay_time = base_time_per_char * random.uniform(8, 15)
            elif char in ',;:':  # Medium pause after clauses
                delay_time = base_time_per_char * random.uniform(3, 6)
            elif char == ' ':  # Slight pause after words
                delay_time = base_time_per_char * random.uniform(1.2, 2.5)
            else:  # Normal typing with slight variations
                delay_time = base_time_per_char * random.uniform(0.8, 1.5)
                
            # Occasionally add a slightly longer pause (simulating thinking)
            if random.random() < 0.02:  # 2% chance of a thinking pause
                delay_time *= random.uniform(2, 4)
                
            time.sleep(delay_time)
            
            # Update status occasionally
            if i % 20 == 0:
                progress = int((i / len(text)) * 100)
                self.root.after(0, lambda p=progress: self.status_var.set(f"Typing... {p}% complete"))
        
        if self.is_typing:
            self.root.after(0, lambda: self.status_var.set("Typing completed!"))
            self.is_typing = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))

if __name__ == "__main__":
    root = tk.Tk()
    app = NaturalTypingSimulator(root)
    root.mainloop()