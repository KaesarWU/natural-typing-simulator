import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import random
import threading
import pyautogui
import json
import os

class NaturalTypingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Natural Typing Simulator")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        
        # Variables
        self.is_typing = False
        self.typing_thread = None
        self.config_file = "typing_config.json"
        
        # Load configuration
        self.config = self.load_config()
        
        # Create UI
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
        # Focus on text area for easy pasting
        self.root.after(100, lambda: self.text_area.focus())
        
    def load_config(self):
        """Load configuration from file or create default"""
        default_config = {
            "shortcuts": {
                "start": "F5",
                "stop": "F6",
                "clear": "Ctrl+L"
            },
            "default_wpm": 50,
            "default_delay": 3,
            "default_typo_prob": 3,
            "default_synonym_prob": 2,
            "default_mode": "natural"
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
            
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
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
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Instructions
        instructions = ("Paste your text below and click 'Start Typing'. "
                       "Natural mode: realistic with inconsistencies, typos, synonyms, bursts. "
                       "Competition mode: pure WPM typing. "
                       "Custom shortcuts available in settings.")
        instruction_label = ttk.Label(main_frame, text=instructions, wraplength=730)
        instruction_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Text area
        text_label = ttk.Label(main_frame, text="Text to type:")
        text_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.text_area = scrolledtext.ScrolledText(main_frame, width=80, height=12)
        self.text_area.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Settings frame
        settings_frame = ttk.Frame(main_frame)
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mode selection
        mode_label = ttk.Label(settings_frame, text="Typing Mode:")
        mode_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.mode_var = tk.StringVar(value=self.config["default_mode"])
        self.mode_combo = ttk.Combobox(settings_frame, textvariable=self.mode_var, 
                                      values=["natural", "competition"], width=12, state="readonly")
        self.mode_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        self.mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
        
        # WPM settings
        wpm_label = ttk.Label(settings_frame, text="Target WPM:")
        wpm_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        self.wpm_var = tk.StringVar(value=str(self.config["default_wpm"]))
        wpm_entry = ttk.Entry(settings_frame, textvariable=self.wpm_var, width=5)
        wpm_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 15))
        
        # Delay before start
        delay_label = ttk.Label(settings_frame, text="Start delay (seconds):")
        delay_label.grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        
        self.delay_var = tk.StringVar(value=str(self.config["default_delay"]))
        delay_entry = ttk.Entry(settings_frame, textvariable=self.delay_var, width=5)
        delay_entry.grid(row=0, column=5, sticky=tk.W)
        
        # Typo probability (only for natural mode)
        self.typo_label = ttk.Label(settings_frame, text="Typo probability (%):")
        self.typo_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        
        self.typo_var = tk.StringVar(value=str(self.config["default_typo_prob"]))
        self.typo_entry = ttk.Entry(settings_frame, textvariable=self.typo_var, width=5)
        self.typo_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 15))
        
        # Synonym probability (only for natural mode)
        self.synonym_label = ttk.Label(settings_frame, text="Synonym probability (%):")
        self.synonym_label.grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        
        self.synonym_var = tk.StringVar(value=str(self.config["default_synonym_prob"]))
        self.synonym_entry = ttk.Entry(settings_frame, textvariable=self.synonym_var, width=5)
        self.synonym_entry.grid(row=1, column=3, sticky=tk.W, padx=(0, 15))
        
        # Settings button
        settings_btn = ttk.Button(settings_frame, text="⚙️", width=3, command=self.open_settings)
        settings_btn.grid(row=1, column=5, sticky=tk.E)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        # Start button
        self.start_button = ttk.Button(buttons_frame, text=f"Start Typing ({self.config['shortcuts']['start']})", 
                                      command=self.start_typing)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(buttons_frame, text=f"Stop ({self.config['shortcuts']['stop']})", 
                                     command=self.stop_typing, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(buttons_frame, text=f"Clear ({self.config['shortcuts']['clear']})", 
                                 command=self.clear_text)
        clear_button.grid(row=0, column=2, padx=(0, 10))
        
        # Status label
        shortcut_info = f"Shortcuts: {self.config['shortcuts']['start']}=Start, {self.config['shortcuts']['stop']}=Stop, {self.config['shortcuts']['clear']}=Clear"
        self.status_var = tk.StringVar(value=f"Ready. {shortcut_info}")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        # Initialize mode-specific UI state
        self.on_mode_change()
        
    def on_mode_change(self, event=None):
        """Enable/disable natural mode specific controls"""
        is_natural_mode = self.mode_var.get() == "natural"
        
        # Update typo controls
        self.typo_label.config(state=tk.NORMAL if is_natural_mode else tk.DISABLED)
        self.typo_entry.config(state=tk.NORMAL if is_natural_mode else tk.DISABLED)
        
        # Update synonym controls
        self.synonym_label.config(state=tk.NORMAL if is_natural_mode else tk.DISABLED)
        self.synonym_entry.config(state=tk.NORMAL if is_natural_mode else tk.DISABLED)
        
        # Visual feedback
        disabled_color = "gray"
        normal_color = "black"
        
        self.typo_label.config(foreground=normal_color if is_natural_mode else disabled_color)
        self.synonym_label.config(foreground=normal_color if is_natural_mode else disabled_color)
        
        # Update status
        mode_name = "Natural" if is_natural_mode else "Competition"
        features = "with typos, synonyms, and variations" if is_natural_mode else "pure consistent WPM"
        self.status_var.set(f"Mode: {mode_name} - {features}")
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts based on configuration"""
        # Unbind any existing bindings
        self.root.unbind('<Key>')
        
        # Bind configured shortcuts
        start_key = self.config['shortcuts']['start'].lower()
        stop_key = self.config['shortcuts']['stop'].lower()
        clear_key = self.config['shortcuts']['clear'].lower()
        
        # Map common keys to their event names
        key_map = {
            'f5': '<F5>', 'f6': '<F6>', 'f7': '<F7>', 'f8': '<F8>', 'f9': '<F9>', 'f10': '<F10>',
            'f11': '<F11>', 'f12': '<F12>', 'escape': '<Escape>', 'enter': '<Return>',
            'space': '<space>', 'ctrl+l': '<Control-l>', 'ctrl+s': '<Control-s>',
            'ctrl+x': '<Control-x>', 'ctrl+c': '<Control-c>', 'ctrl+v': '<Control-v>'
        }
        
        start_event = key_map.get(start_key, f'<{start_key}>')
        stop_event = key_map.get(stop_key, f'<{stop_key}>')
        clear_event = key_map.get(clear_key, f'<{clear_key}>')
        
        self.root.bind(start_event, lambda event: self.start_typing())
        self.root.bind(stop_event, lambda event: self.stop_typing())
        self.root.bind(clear_event, lambda event: self.clear_text())
        
    def open_settings(self):
        """Open settings window for custom shortcuts"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Typing Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        ttk.Label(settings_window, text="Custom Shortcuts", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Shortcut settings frame
        shortcut_frame = ttk.Frame(settings_window)
        shortcut_frame.pack(fill="x", padx=20, pady=10)
        
        # Start shortcut
        ttk.Label(shortcut_frame, text="Start Typing:").grid(row=0, column=0, sticky="w", pady=5)
        start_shortcut = ttk.Entry(shortcut_frame, width=15)
        start_shortcut.insert(0, self.config['shortcuts']['start'])
        start_shortcut.grid(row=0, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Stop shortcut
        ttk.Label(shortcut_frame, text="Stop Typing:").grid(row=1, column=0, sticky="w", pady=5)
        stop_shortcut = ttk.Entry(shortcut_frame, width=15)
        stop_shortcut.insert(0, self.config['shortcuts']['stop'])
        stop_shortcut.grid(row=1, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Clear shortcut
        ttk.Label(shortcut_frame, text="Clear Text:").grid(row=2, column=0, sticky="w", pady=5)
        clear_shortcut = ttk.Entry(shortcut_frame, width=15)
        clear_shortcut.insert(0, self.config['shortcuts']['clear'])
        clear_shortcut.grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))
        
        ttk.Label(shortcut_frame, text="Examples: F5, F6, Escape, Ctrl+L, Ctrl+S", 
                 foreground="gray", font=("Arial", 8)).grid(row=3, column=0, columnspan=2, pady=10)
        
        def save_settings():
            self.config['shortcuts'] = {
                'start': start_shortcut.get().strip(),
                'stop': stop_shortcut.get().strip(),
                'clear': clear_shortcut.get().strip()
            }
            self.config['default_wpm'] = int(self.wpm_var.get())
            self.config['default_delay'] = int(self.delay_var.get())
            self.config['default_typo_prob'] = float(self.typo_var.get())
            self.config['default_synonym_prob'] = float(self.synonym_var.get())
            self.config['default_mode'] = self.mode_var.get()
            
            self.save_config()
            self.bind_shortcuts()
            self.update_button_text()
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings saved successfully!")
        
        ttk.Button(settings_window, text="Save Settings", command=save_settings).pack(pady=20)
        
    def update_button_text(self):
        """Update button text with current shortcuts"""
        self.start_button.config(text=f"Start Typing ({self.config['shortcuts']['start']})")
        self.stop_button.config(text=f"Stop ({self.config['shortcuts']['stop']})")
        
    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        
    def start_typing(self):
        if self.is_typing:
            return
            
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.status_var.set("Please enter some text to type.")
            return
            
        try:
            wpm = int(self.wpm_var.get())
            if wpm < 10 or wpm > 500:
                raise ValueError("WPM should be between 10 and 500")
        except ValueError:
            self.status_var.set("Please enter a valid WPM (10-500).")
            return
            
        try:
            delay = int(self.delay_var.get())
            if delay < 0:
                raise ValueError("Delay should be a positive number")
        except ValueError:
            self.status_var.set("Please enter a valid delay.")
            return
            
        # Only validate natural mode settings if in natural mode
        if self.mode_var.get() == "natural":
            try:
                typo_prob = float(self.typo_var.get())
                if typo_prob < 0 or typo_prob > 20:
                    raise ValueError("Typo probability should be between 0 and 20")
            except ValueError:
                self.status_var.set("Please enter a valid typo probability (0-20).")
                return
                
            try:
                synonym_prob = float(self.synonym_var.get())
                if synonym_prob < 0 or synonym_prob > 20:
                    raise ValueError("Synonym probability should be between 0 and 20")
            except ValueError:
                self.status_var.set("Please enter a valid synonym probability (0-20).")
                return
        else:
            # Competition mode - force no typos or synonyms
            typo_prob = 0
            synonym_prob = 0
            
        self.is_typing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set(f"Starting in {delay} seconds... Move cursor to target application!")
        
        # Start typing in a separate thread to keep UI responsive
        self.typing_thread = threading.Thread(
            target=self.type_text, 
            args=(text, wpm, delay, typo_prob/100.0, synonym_prob/100.0, self.mode_var.get())
        )
        self.typing_thread.daemon = True
        self.typing_thread.start()
        
    def stop_typing(self):
        self.is_typing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Typing stopped.")
        
    def get_synonyms(self):
        """Return a comprehensive dictionary of synonyms for NATURAL MODE ONLY"""
        return {
            'happy': ['joyful', 'cheerful', 'delighted', 'pleased', 'content', 'ecstatic', 'elated', 'glad', 'jubilant', 'thrilled'],
            'sad': ['unhappy', 'depressed', 'melancholy', 'gloomy', 'miserable', 'sorrowful', 'dejected', 'downcast', 'despondent', 'heartbroken'],
            'big': ['large', 'huge', 'enormous', 'gigantic', 'massive', 'colossal', 'immense', 'substantial', 'considerable', 'spacious'],
            'small': ['tiny', 'little', 'miniature', 'petite', 'compact', 'minuscule', 'microscopic', 'mini', 'diminutive', 'pocket-sized'],
            'good': ['excellent', 'great', 'wonderful', 'fantastic', 'superb', 'outstanding', 'marvelous', 'splendid', 'terrific', 'first-rate'],
            'bad': ['poor', 'terrible', 'awful', 'horrible', 'dreadful', 'lousy', 'inferior', 'substandard', 'unsatisfactory', 'defective'],
            'beautiful': ['gorgeous', 'stunning', 'lovely', 'attractive', 'pretty', 'handsome', 'exquisite', 'breathtaking', 'magnificent', 'elegant'],
            'ugly': ['unattractive', 'hideous', 'unsightly', 'repulsive', 'disgusting', 'grotesque', 'monstrous', 'horrid', 'frightful', 'unpleasant'],
            'smart': ['intelligent', 'clever', 'bright', 'brilliant', 'knowledgeable', 'wise', 'sharp', 'astute', 'perceptive', 'brainy'],
            'stupid': ['foolish', 'dumb', 'unintelligent', 'ignorant', 'simple-minded', 'slow', 'dense', 'obtuse', 'dim-witted', 'moronic'],
            'fast': ['quick', 'rapid', 'swift', 'speedy', 'brisk', 'hasty', 'expeditious', 'fleet', 'accelerated', 'high-speed'],
            'slow': ['sluggish', 'leisurely', 'gradual', 'unhurried', 'plodding', 'languid', 'deliberate', 'measured', 'creeping', 'snail-like'],
            'important': ['significant', 'crucial', 'vital', 'essential', 'critical', 'paramount', 'major', 'momentous', 'weighty', 'consequential'],
            'unimportant': ['insignificant', 'trivial', 'minor', 'negligible', 'inconsequential', 'petty', 'paltry', 'meaningless', 'worthless', 'frivolous'],
            'difficult': ['hard', 'challenging', 'tough', 'arduous', 'demanding', 'strenuous', 'laborious', 'grueling', 'formidable', 'complicated'],
            'easy': ['simple', 'effortless', 'straightforward', 'uncomplicated', 'elementary', 'painless', 'undemanding', 'facile', 'basic', 'clear-cut'],
            'rich': ['wealthy', 'affluent', 'prosperous', 'well-off', 'moneyed', 'opulent', 'flush', 'loaded', 'well-to-do', 'comfortable'],
            'poor': ['poverty-stricken', 'destitute', 'impoverished', 'needy', 'penniless', 'broke', 'bankrupt', 'insolvent', 'indigent', 'underprivileged'],
            'angry': ['mad', 'furious', 'enraged', 'irate', 'incensed', 'wrathful', 'infuriated', 'livid', 'outraged', 'heated'],
            'calm': ['peaceful', 'serene', 'tranquil', 'placid', 'composed', 'collected', 'unruffled', 'cool', 'relaxed', 'untroubled'],
            'hot': ['warm', 'heated', 'scorching', 'blazing', 'boiling', 'sizzling', 'torrid', 'sweltering', 'fiery', 'burning'],
            'cold': ['chilly', 'cool', 'freezing', 'frigid', 'icy', 'frosty', 'bitter', 'nippy', 'glacial', 'wintry'],
            'new': ['fresh', 'novel', 'modern', 'current', 'recent', 'up-to-date', 'brand-new', 'latest', 'contemporary', 'innovative'],
            'old': ['aged', 'ancient', 'elderly', 'vintage', 'antique', 'outdated', 'obsolete', 'archaic', 'timeworn', 'hoary'],
            'young': ['youthful', 'juvenile', 'adolescent', 'immature', 'childish', 'babyish', 'tender', 'green', 'callow', 'inexperienced'],
            'brave': ['courageous', 'fearless', 'bold', 'heroic', 'valiant', 'intrepid', 'dauntless', 'gallant', 'audacious', 'stouthearted'],
            'cowardly': ['timid', 'fearful', 'fainthearted', 'spineless', 'pusillanimous', 'craven', 'gutless', 'chicken-hearted', 'timorous', 'yellow'],
            'strong': ['powerful', 'mighty', 'forceful', 'robust', 'sturdy', 'tough', 'muscular', 'athletic', 'strapping', 'brawny'],
            'weak': ['feeble', 'frail', 'fragile', 'delicate', 'puny', 'powerless', 'impotent', 'debilitated', 'enervated', 'infirm'],
            'funny': ['humorous', 'amusing', 'comical', 'hilarious', 'entertaining', 'witty', 'droll', 'jocular', 'laughable', 'side-splitting'],
            'serious': ['solemn', 'grave', 'earnest', 'sober', 'staid', 'sedate', 'thoughtful', 'pensive', 'humorless', 'stern'],
            'loud': ['noisy', 'deafening', 'thunderous', 'booming', 'resounding', 'piercing', 'shrill', 'earsplitting', 'clamorous', 'vociferous'],
            'quiet': ['silent', 'hushed', 'muted', 'soft', 'low', 'faint', 'subdued', 'peaceful', 'tranquil', 'noiseless'],
            'bright': ['shiny', 'brilliant', 'radiant', 'luminous', 'dazzling', 'glowing', 'vivid', 'intense', 'sparkling', 'gleaming'],
            'dark': ['dim', 'gloomy', 'shadowy', 'murky', 'obscure', 'black', 'somber', 'dusky', 'unlit', 'tenebrous'],
            'clean': ['spotless', 'immaculate', 'pristine', 'unsullied', 'hygienic', 'sanitary', 'sterile', 'pure', 'unpolluted', 'tidy'],
            'dirty': ['filthy', 'soiled', 'grimy', 'stained', 'unclean', 'muddy', 'dusty', 'squalid', 'foul', 'polluted'],
            'dry': ['arid', 'parched', 'dehydrated', 'moistureless', 'waterless', 'rainless', 'thirsty', 'desiccated', 'barren', 'bone-dry'],
            'wet': ['damp', 'moist', 'soggy', 'soaked', 'drenched', 'saturated', 'waterlogged', 'sodden', 'clammy', 'humid'],
            'empty': ['vacant', 'void', 'hollow', 'unfilled', 'deserted', 'unoccupied', 'bare', 'blank', 'depleted', 'exhausted'],
            'full': ['filled', 'packed', 'crowded', 'brimming', 'overflowing', 'loaded', 'stuffed', 'crammed', 'teeming', 'replete'],
            'high': ['tall', 'elevated', 'lofty', 'soaring', 'towering', 'sky-high', 'steep', 'raised', 'uplifted', 'ascending'],
            'low': ['short', 'small', 'little', 'squat', 'stubby', 'diminished', 'reduced', 'sunken', 'depressed', 'subdued'],
            'long': ['lengthy', 'extended', 'prolonged', 'elongated', 'stretched', 'extensive', 'sustained', 'enduring', 'persistent', 'running'],
            'short': ['brief', 'concise', 'succinct', 'abbreviated', 'curtailed', 'truncated', 'fleeting', 'momentary', 'transient', 'ephemeral'],
            'wide': ['broad', 'expansive', 'spacious', 'roomy', 'extensive', 'ample', 'capacious', 'voluminous', 'commodious', 'sweeping'],
            'narrow': ['thin', 'slender', 'slim', 'tight', 'confined', 'restricted', 'constricted', 'cramped', 'limited', 'close'],
            'heavy': ['weighty', 'burdensome', 'substantial', 'massive', 'hefty', 'ponderous', 'cumbersome', 'unwieldy', 'leaden', 'oppressive'],
            'light': ['weightless', 'airy', 'ethereal', 'feathery', 'buoyant', 'floaty', 'insubstantial', 'delicate', 'graceful', 'nimble'],
            'expensive': ['costly', 'dear', 'high-priced', 'valuable', 'precious', 'exorbitant', 'steep', 'pricey', 'upmarket', 'lavish'],
            'cheap': ['inexpensive', 'affordable', 'reasonable', 'economical', 'budget', 'low-cost', 'cut-rate', 'bargain', 'discount', 'modest'],
            'simple': ['easy', 'uncomplicated', 'straightforward', 'elementary', 'basic', 'plain', 'unadorned', 'modest', 'unpretentious', 'minimal'],
            'complex': ['complicated', 'intricate', 'involved', 'convoluted', 'sophisticated', 'elaborate', 'byzantine', 'tangled', 'knotty', 'multifaceted'],
            'clear': ['transparent', 'see-through', 'limpid', 'crystalline', 'pellucid', 'lucid', 'distinct', 'obvious', 'evident', 'unambiguous'],
            'vague': ['unclear', 'indistinct', 'obscure', 'ambiguous', 'nebulous', 'hazy', 'fuzzy', 'indefinite', 'imprecise', 'woolly'],
            'common': ['ordinary', 'usual', 'typical', 'standard', 'regular', 'conventional', 'everyday', 'prevalent', 'widespread', 'ubiquitous'],
            'rare': ['uncommon', 'unusual', 'infrequent', 'scarce', 'sparse', 'exceptional', 'unique', 'singular', 'extraordinary', 'unparalleled'],
            'real': ['genuine', 'authentic', 'true', 'actual', 'legitimate', 'bona fide', 'veritable', 'factual', 'tangible', 'concrete'],
            'fake': ['false', 'counterfeit', 'imitation', 'forged', 'fraudulent', 'sham', 'bogus', 'spurious', 'phony', 'ersatz'],
            'right': ['correct', 'accurate', 'true', 'exact', 'precise', 'proper', 'appropriate', 'suitable', 'fitting', 'apt'],
            'wrong': ['incorrect', 'inaccurate', 'false', 'mistaken', 'erroneous', 'faulty', 'flawed', 'improper', 'inappropriate', 'unsuitable'],
            'dangerous': ['risky', 'hazardous', 'perilous', 'unsafe', 'precarious', 'treacherous', 'threatening', 'menacing', 'ominous', 'dire'],
            'safe': ['secure', 'protected', 'guarded', 'shielded', 'harmless', 'innocuous', 'benign', 'non-threatening', 'reliable', 'dependable'],
            'early': ['premature', 'advance', 'forward', 'untimely', 'precocious', 'punctual', 'timely', 'seasonable', 'opportune', 'ahead'],
            'late': ['tardy', 'delayed', 'overdue', 'belated', 'behind', 'slow', 'dilatory', 'unpunctual', 'last-minute', 'eleventh-hour'],
            'true': ['accurate', 'correct', 'right', 'valid', 'genuine', 'real', 'authentic', 'factual', 'verifiable', 'undeniable'],
            'false': ['untrue', 'incorrect', 'wrong', 'inaccurate', 'erroneous', 'faulty', 'invalid', 'spurious', 'misleading', 'deceptive'],
            'open': ['unlocked', 'accessible', 'available', 'unrestricted', 'unobstructed', 'clear', 'free', 'receptive', 'welcoming', 'inviting'],
            'closed': ['shut', 'locked', 'sealed', 'blocked', 'obstructed', 'inaccessible', 'unavailable', 'restricted', 'private', 'exclusive'],
            'begin': ['start', 'commence', 'initiate', 'launch', 'inaugurate', 'originate', 'embark', 'activate', 'trigger', 'instigate'],
            'end': ['finish', 'conclude', 'terminate', 'complete', 'cease', 'stop', 'halt', 'discontinue', 'culminate', 'finalize'],
            'create': ['make', 'produce', 'generate', 'fabricate', 'construct', 'build', 'develop', 'form', 'establish', 'invent'],
            'destroy': ['demolish', 'ruin', 'wreck', 'devastate', 'annihilate', 'obliterate', 'eradicate', 'eliminate', 'shatter', 'smash'],
            'increase': ['grow', 'expand', 'enlarge', 'augment', 'amplify', 'escalate', 'multiply', 'intensify', 'boost', 'enhance'],
            'decrease': ['reduce', 'diminish', 'lessen', 'lower', 'shrink', 'decline', 'dwindle', 'subside', 'abate', 'curtail'],
            'help': ['assist', 'aid', 'support', 'facilitate', 'serve', 'benefit', 'advise', 'guide', 'counsel', 'succor'],
            'hinder': ['impede', 'obstruct', 'hamper', 'block', 'thwart', 'frustrate', 'inhibit', 'restrict', 'curb', 'stifle'],
            'love': ['adore', 'cherish', 'treasure', 'worship', 'idolize', 'esteem', 'admire', 'revere', 'prize', 'hold dear'],
            'hate': ['despise', 'loathe', 'detest', 'abhor', 'abominate', 'execrate', 'disdain', 'scorn', 'dislike', 'resent'],
            'win': ['triumph', 'succeed', 'prevail', 'conquer', 'vanquish', 'overcome', 'surmount', 'achieve', 'accomplish', 'attain'],
            'lose': ['fail', 'miscarry', 'flounder', 'fold', 'collapse', 'decline', 'deteriorate', 'weaken', 'falter', 'succumb'],
            'give': ['donate', 'contribute', 'bestow', 'grant', 'present', 'award', 'confer', 'impart', 'provide', 'supply'],
            'take': ['receive', 'accept', 'acquire', 'obtain', 'get', 'gain', 'secure', 'procure', 'collect', 'gather'],
            'say': ['state', 'declare', 'announce', 'proclaim', 'assert', 'affirm', 'aver', 'allege', 'claim', 'maintain'],
            'ask': ['inquire', 'question', 'query', 'interrogate', 'quiz', 'probe', 'investigate', 'examine', 'request', 'solicit'],
            'see': ['look', 'watch', 'observe', 'view', 'behold', 'witness', 'perceive', 'discern', 'notice', 'spot'],
            'hear': ['listen', 'overhear', 'eavesdrop', 'attend', 'heed', 'catch', 'perceive', 'discern', 'detect', 'ascertain'],
            'know': ['understand', 'comprehend', 'grasp', 'fathom', 'apprehend', 'realize', 'recognize', 'discern', 'perceive', 'cognize'],
            'think': ['ponder', 'consider', 'contemplate', 'reflect', 'meditate', 'muse', 'ruminate', 'cogitate', 'deliberate', 'reason'],
            'feel': ['sense', 'perceive', 'experience', 'undergo', 'endure', 'suffer', 'enjoy', 'relish', 'savor', 'appreciate'],
            'want': ['desire', 'wish', 'crave', 'long', 'yearn', 'covet', 'fancy', 'prefer', 'choose', 'elect'],
            'need': ['require', 'necessitate', 'demand', 'call for', 'entail', 'involve', 'lack', 'want', 'miss', 'require'],
            'come': ['arrive', 'approach', 'advance', 'near', 'reach', 'attain', 'enter', 'appear', 'materialize', 'show up'],
            'go': ['leave', 'depart', 'exit', 'withdraw', 'retire', 'retreat', 'vanish', 'disappear', 'evaporate', 'fade'],
            'work': ['labor', 'toil', 'strive', 'endeavor', 'exert', 'operate', 'function', 'perform', 'act', 'serve'],
            'play': ['recreate', 'amuse', 'entertain', 'divert', 'sport', 'frolic', 'gambol', 'romp', 'caper', 'cavort'],
            'live': ['exist', 'survive', 'subsist', 'endure', 'persist', 'remain', 'continue', 'abide', 'dwell', 'reside'],
            'die': ['perish', 'expire', 'succumb', 'depart', 'pass away', 'cease', 'terminate', 'end', 'vanish', 'fade away'],
            'find': ['discover', 'locate', 'uncover', 'detect', 'spot', 'identify', 'recognize', 'notice', 'observe', 'discern'],
            'lose': ['misplace', 'mislay', 'forfeit', 'surrender', 'yield', 'relinquish', 'sacrifice', 'abandon', 'desert', 'forsake'],
            'change': ['alter', 'modify', 'transform', 'convert', 'adapt', 'adjust', 'revise', 'amend', 'reform', 'remodel'],
            'stay': ['remain', 'continue', 'persist', 'endure', 'last', 'abide', 'dwell', 'reside', 'inhabit', 'occupy'],
            'move': ['proceed', 'advance', 'progress', 'travel', 'journey', 'voyage', 'trek', 'migrate', 'relocate', 'transfer'],
            'stop': ['cease', 'halt', 'discontinue', 'terminate', 'conclude', 'finish', 'end', 'quit', 'desist', 'refrain'],
            'continue': ['persist', 'endure', 'last', 'remain', 'stay', 'abide', 'proceed', 'advance', 'progress', 'persevere'],
            'try': ['attempt', 'endeavor', 'strive', 'struggle', 'labor', 'toil', 'work', 'exert', 'apply', 'seek'],
            'succeed': ['triumph', 'prevail', 'prosper', 'flourish', 'thrive', 'achieve', 'accomplish', 'attain', 'realize', 'fulfill'],
            'fail': ['miscarry', 'abort', 'collapse', 'founder', 'flop', 'fizzle', 'misfire', 'backfire', 'underachieve', 'disappoint'],
            'understand': ['comprehend', 'grasp', 'fathom', 'apprehend', 'realize', 'recognize', 'discern', 'perceive', 'cognize', 'know'],
            'confuse': ['bewilder', 'perplex', 'puzzle', 'baffle', 'mystify', 'fluster', 'disconcert', 'nonplus', 'disorient', 'addle'],
            'remember': ['recall', 'recollect', 'reminisce', 'retain', 'memorize', 'engrave', 'imprint', 'treasure', 'cherish', 'value'],
            'forget': ['overlook', 'neglect', 'disregard', 'ignore', 'omit', 'skip', 'miss', 'bypass', 'dismiss', 'abandon'],
            'hope': ['desire', 'wish', 'want', 'aspire', 'dream', 'long', 'yearn', 'crave', 'covet', 'fancy'],
            'fear': ['dread', 'apprehend', 'anticipate', 'forebode', 'worry', 'fret', 'agonize', 'torment', 'trouble', 'distress'],
            'like': ['enjoy', 'appreciate', 'relish', 'savor', 'fancy', 'prefer', 'choose', 'elect', 'select', 'pick'],
            'dislike': ['hate', 'detest', 'despise', 'loathe', 'abhor', 'abominate', 'execrate', 'scorn', 'disdain', 'shun'],
            'believe': ['trust', 'credit', 'accept', 'buy', 'swallow', 'endorse', 'support', 'advocate', 'champion', 'defend'],
            'doubt': ['question', 'challenge', 'dispute', 'contest', 'oppose', 'resist', 'protest', 'object', 'demur', 'hesitate'],
            'show': ['display', 'exhibit', 'present', 'demonstrate', 'illustrate', 'manifest', 'reveal', 'disclose', 'unveil', 'expose'],
            'hide': ['conceal', 'cover', 'mask', 'disguise', 'camouflage', 'veil', 'shroud', 'obscure', 'screen', 'bury'],
            'lead': ['guide', 'direct', 'conduct', 'steer', 'pilot', 'navigate', 'usher', 'escort', 'accompany', 'shepherd'],
            'follow': ['pursue', 'chase', 'track', 'trail', 'shadow', 'stalk', 'accompany', 'attend', 'escort', 'serve'],
            'teach': ['instruct', 'educate', 'tutor', 'coach', 'train', 'drill', 'school', 'enlighten', 'illuminate', 'edify'],
            'learn': ['study', 'research', 'investigate', 'explore', 'examine', 'scrutinize', 'analyze', 'dissect', 'probe', 'inquire'],
            'buy': ['purchase', 'acquire', 'obtain', 'procure', 'secure', 'gain', 'get', 'score', 'snap up', 'pick up'],
            'sell': ['vend', 'market', 'merchandise', 'trade', 'barter', 'exchange', 'auction', 'retail', 'wholesale', 'distribute'],
            'send': ['dispatch', 'forward', 'transmit', 'convey', 'deliver', 'ship', 'mail', 'post', 'express', 'remit'],
            'receive': ['accept', 'get', 'obtain', 'acquire', 'gain', 'secure', 'collect', 'gather', 'accumulate', 'amass'],
            'build': ['construct', 'erect', 'assemble', 'fabricate', 'manufacture', 'create', 'make', 'form', 'establish', 'found'],
            'destroy': ['demolish', 'raze', 'level', 'flatten', 'wreck', 'ruin', 'devastate', 'annihilate', 'obliterate', 'eradicate'],
            'agree': ['concur', 'assent', 'consent', 'accede', 'comply', 'acquiesce', 'endorse', 'support', 'approve', 'ratify'],
            'disagree': ['differ', 'dissent', 'object', 'protest', 'oppose', 'resist', 'contest', 'challenge', 'dispute', 'contest'],
            'allow': ['permit', 'let', 'authorize', 'sanction', 'license', 'enable', 'empower', 'entitle', 'qualify', 'warrant'],
            'forbid': ['prohibit', 'ban', 'bar', 'exclude', 'prevent', 'hinder', 'obstruct', 'block', 'veto', 'outlaw'],
            'include': ['incorporate', 'embrace', 'encompass', 'contain', 'comprise', 'involve', 'entail', 'imply', 'mean', 'signify'],
            'exclude': ['omit', 'eliminate', 'remove', 'eject', 'expel', 'evict', 'dismiss', 'discharge', 'oust', 'banish'],
            'start': ['begin', 'commence', 'initiate', 'launch', 'inaugurate', 'originate', 'embark', 'activate', 'trigger', 'instigate'],
            'finish': ['complete', 'conclude', 'terminate', 'end', 'cease', 'stop', 'halt', 'discontinue', 'culminate', 'finalize'],
            'arrive': ['come', 'reach', 'attain', 'achieve', 'accomplish', 'gain', 'get', 'obtain', 'secure', 'procure'],
            'depart': ['leave', 'go', 'exit', 'withdraw', 'retire', 'retreat', 'vanish', 'disappear', 'evaporate', 'fade'],
            'enter': ['access', 'penetrate', 'pierce', 'perforate', 'puncture', 'invade', 'infiltrate', 'intrude', 'trespass', 'violate'],
            'exit': ['leave', 'depart', 'withdraw', 'retreat', 'retire', 'vacate', 'evacuate', 'abandon', 'desert', 'forsake'],
            'rise': ['ascend', 'climb', 'mount', 'scale', 'escalate', 'surge', 'soar', 'rocket', 'skyrocket', 'spiral'],
            'fall': ['descend', 'drop', 'plummet', 'plunge', 'sink', 'dive', 'tumble', 'collapse', 'crumble', 'topple'],
            'win': ['triumph', 'succeed', 'prevail', 'conquer', 'vanquish', 'overcome', 'surmount', 'achieve', 'accomplish', 'attain'],
            'lose': ['fail', 'miscarry', 'flounder', 'fold', 'collapse', 'decline', 'deteriorate', 'weaken', 'falter', 'succumb'],
            'save': ['preserve', 'conserve', 'protect', 'guard', 'defend', 'shield', 'safeguard', 'secure', 'rescue', 'deliver'],
            'waste': ['squander', 'dissipate', 'fritter', 'lavish', 'misspend', 'misuse', 'abuse', 'exploit', 'deplete', 'exhaust'],
            'join': ['unite', 'connect', 'link', 'couple', 'attach', 'fasten', 'secure', 'fix', 'affix', 'append'],
            'separate': ['divide', 'split', 'cleave', 'sever', 'disconnect', 'detach', 'disengage', 'disunite', 'dissociate', 'isolate'],
            'meet': ['encounter', 'confront', 'face', 'experience', 'undergo', 'suffer', 'endure', 'bear', 'tolerate', 'withstand'],
            'avoid': ['evade', 'elude', 'dodge', 'escape', 'flee', 'shun', 'eschew', 'abstain', 'refrain', 'forbear'],
            'accept': ['receive', 'take', 'get', 'obtain', 'acquire', 'gain', 'secure', 'procure', 'collect', 'gather'],
            'reject': ['refuse', 'decline', 'deny', 'rebuff', 'spurn', 'scorn', 'disdain', 'dismiss', 'repudiate', 'renounce'],
            'approve': ['endorse', 'support', 'back', 'champion', 'advocate', 'promote', 'further', 'advance', 'forward', 'foster'],
            'disapprove': ['condemn', 'denounce', 'criticize', 'censure', 'reprimand', 'rebuke', 'reprove', 'admonish', 'chide', 'scold'],
            'support': ['back', 'champion', 'advocate', 'promote', 'further', 'advance', 'forward', 'foster', 'nurture', 'cultivate'],
            'oppose': ['resist', 'contest', 'challenge', 'dispute', 'confront', 'counter', 'defy', 'contradict', 'gainsay', 'refute'],
            'attack': ['assault', 'charge', 'storm', 'besiege', 'bombard', 'barrage', 'strafe', 'blitz', 'invade', 'raid'],
            'defend': ['protect', 'guard', 'shield', 'safeguard', 'secure', 'preserve', 'conserve', 'maintain', 'uphold', 'sustain'],
            'encourage': ['inspire', 'motivate', 'stimulate', 'energize', 'invigorate', 'vitalize', 'animate', 'enliven', 'exhilarate', 'electrify'],
            'discourage': ['dishearten', 'dispirit', 'demoralize', 'depress', 'deter', 'dissuade', 'daunt', 'intimidate', 'frighten', 'scare'],
            'praise': ['commend', 'applaud', 'acclaim', 'extol', 'laud', 'eulogize', 'glorify', 'magnify', 'aggrandize', 'dignify'],
            'criticize': ['censure', 'condemn', 'denounce', 'decry', 'deplore', 'disparage', 'deprecate', 'derogate', 'belittle', 'diminish'],
            'reward': ['compensate', 'remunerate', 'recompense', 'require', 'repay', 'refund', 'reimburse', 'indemnify', 'satisfy', 'content'],
            'punish': ['penalize', 'discipline', 'chastise', 'castigate', 'scourge', 'flagellate', 'torture', 'torment', 'afflict', 'smite'],
            'forgive': ['pardon', 'excuse', 'absolve', 'exonerate', 'acquit', 'vindicate', 'clear', 'release', 'discharge', 'liberate'],
            'blame': ['accuse', 'charge', 'indict', 'impeach', 'arraign', 'incriminate', 'inculpate', 'implicate', 'involve', 'entangle'],
            'thank': ['gratitude', 'appreciation', 'recognition', 'acknowledgment', 'credit', 'praise', 'commendation', 'accolade', 'tribute', 'homage'],
            'apologize': ['regret', 'repent', 'rue', 'lament', 'bemoan', 'bewail', 'deplore', 'mourn', 'grieve', 'sorrow'],
        }
        
    def get_adjacent_key(self, char):
        """Return a commonly mistyped adjacent key for the given character"""
        # QWERTY keyboard layout adjacent keys
        adjacent_keys = {
            'a': ['q', 'w', 's', 'z', 'x'],
            'b': ['v', 'g', 'h', 'n', ' '],
            'c': ['x', 'd', 'f', 'v', ' '],
            'd': ['s', 'e', 'r', 'f', 'c', 'x'],
            'e': ['w', 's', 'd', 'r', 'f'],
            'f': ['d', 'r', 't', 'g', 'v', 'c'],
            'g': ['f', 't', 'y', 'h', 'b', 'v'],
            'h': ['g', 'y', 'u', 'j', 'n', 'b'],
            'i': ['u', 'j', 'k', 'o', 'l'],
            'j': ['h', 'u', 'i', 'k', 'm', 'n'],
            'k': ['j', 'i', 'o', 'l', ',', 'm'],
            'l': ['k', 'o', 'p', ';', '.', ','],
            'm': ['n', 'j', 'k', ',', '.'],
            'n': ['b', 'h', 'j', 'm', ' '],
            'o': ['i', 'k', 'l', 'p', ';'],
            'p': ['o', 'l', ';', '[', ']'],
            'q': ['1', '2', 'w', 'a', 's'],
            'r': ['e', 'd', 'f', 't', '4', '5'],
            's': ['a', 'w', 'e', 'd', 'x', 'z'],
            't': ['r', 'f', 'g', 'y', '5', '6'],
            'u': ['y', 'h', 'j', 'i', '7', '8'],
            'v': ['c', 'f', 'g', 'b', ' '],
            'w': ['q', '2', '3', 'e', 's', 'a'],
            'x': ['z', 's', 'd', 'c', ' '],
            'y': ['t', 'g', 'h', 'u', '6', '7'],
            'z': ['1', 'a', 's', 'x', ' '],
            ' ': ['c', 'v', 'b', 'n', 'm', 'x', 'z'],
        }
        
        char_lower = char.lower()
        if char_lower in adjacent_keys:
            return random.choice(adjacent_keys[char_lower])
        return char
        
    def type_text(self, text, target_wpm, delay, typo_probability, synonym_probability, mode):
        """Fixed timing system that strictly follows target WPM"""
        # Wait for the specified delay
        time.sleep(delay)
        
        if not self.is_typing:
            return
            
        self.root.after(0, lambda: self.status_var.set("Typing in progress..."))
        
        # Calculate base time per character (seconds per character)
        # FIXED: Proper calculation for high WPM
        base_time_per_char = 60.0 / (target_wpm * 5) if target_wpm > 0 else 0.1
        
        i = 0
        synonyms = self.get_synonyms() if mode == "natural" else {}
        start_time = time.time()
        characters_typed = 0
        
        while i < len(text) and self.is_typing:
            char = text[i]
            
            # Handle word boundaries for synonym replacement (Natural mode only)
            if mode == "natural" and char.isalpha() and synonym_probability > 0:
                # Extract the current word
                j = i
                current_word = ""
                while j < len(text) and (text[j].isalpha() or text[j] == "'"):
                    current_word += text[j]
                    j += 1
                
                # Check if we should replace with synonym
                if (len(current_word) > 3 and 
                    current_word.lower() in synonyms and 
                    random.random() < synonym_probability):
                    
                    synonym = random.choice(synonyms[current_word.lower()])
                    
                    # Type the synonym quickly
                    for syn_char in synonym:
                        pyautogui.write(syn_char)
                        time.sleep(base_time_per_char * 0.1)  # Very fast typing
                    
                    # Wait a bit then delete the synonym
                    time.sleep(base_time_per_char * 0.3)
                    for _ in range(len(synonym)):
                        pyautogui.press('backspace')
                        time.sleep(base_time_per_char * 0.05)
                    
                    # Type the correct word
                    for word_char in current_word:
                        pyautogui.write(word_char)
                        # Use consistent timing for the correct word
                        time.sleep(base_time_per_char)
                    
                    i = j
                    characters_typed += len(current_word)
                    continue
            
            # Handle typos (Natural mode only)
            if mode == "natural" and (char.isalpha() or char == ' ') and random.random() < typo_probability:
                # Make a typo
                typo_char = self.get_adjacent_key(char)
                pyautogui.write(typo_char)
                time.sleep(base_time_per_char * 0.3)
                
                # Correct the typo
                pyautogui.press('backspace')
                time.sleep(base_time_per_char * 0.2)
                
                # Type correct character
                pyautogui.write(char)
                delay_time = base_time_per_char
                
            else:
                # Normal typing - COMPETITION MODE: 100% consistent, NATURAL: with variations
                pyautogui.write(char)
                if mode == "competition":
                    # Competition mode: perfectly consistent timing
                    delay_time = base_time_per_char
                else:
                    # Natural mode: variations around the target WPM
                    if char in '.!?':  # Longer pause after sentences
                        delay_time = base_time_per_char * random.uniform(3, 6)
                    elif char in ',;:':  # Medium pause after clauses
                        delay_time = base_time_per_char * random.uniform(1.5, 2.5)
                    elif char == ' ':  # Slight pause after words
                        delay_time = base_time_per_char * random.uniform(1.0, 1.5)
                    elif char == '\n':  # Pause for new lines
                        delay_time = base_time_per_char * random.uniform(2, 4)
                    else:  # Normal typing with slight variations
                        delay_time = base_time_per_char * random.uniform(0.8, 1.2)
                    
                    # Occasional bursts of speed (fast typing)
                    if random.random() < 0.1:  # 10% chance of burst
                        delay_time *= random.uniform(0.3, 0.6)  # 1.6x to 3.3x faster
                    
                    # Occasional thinking pauses
                    if random.random() < 0.03:  # 3% chance of thinking pause
                        delay_time *= random.uniform(2, 5)
            
            time.sleep(delay_time)
            i += 1
            characters_typed += 1
            
            # Calculate and display real-time WPM
            if characters_typed % 10 == 0 or i == len(text):
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    current_wpm = (characters_typed / 5) / (elapsed_time / 60)
                    progress = int((i / len(text)) * 100)
                    mode_status = f" - Current: {int(current_wpm)} WPM" if mode == "natural" else f" - Target: {target_wpm} WPM"
                    self.root.after(0, lambda p=progress, m=mode_status: 
                                  self.status_var.set(f"Typing... {p}% complete{m}"))
        
        if self.is_typing:
            total_time = time.time() - start_time
            final_wpm = (characters_typed / 5) / (total_time / 60) if total_time > 0 else 0
            self.root.after(0, lambda: self.status_var.set(f"Typing completed! Final WPM: {int(final_wpm)}"))
            self.is_typing = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))

if __name__ == "__main__":
    root = tk.Tk()
    app = NaturalTypingSimulator(root)
    root.mainloop()
