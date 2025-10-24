# Natural Typing Simulator

A sophisticated Python application that simulates human-like typing with customizable realism. Perfect for demonstrations, testing, accessibility, or practicing typing with realistic variations.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%2C%20macOS%2C%20Linux-lightgrey)

## 🌟 Features

### 🎯 Dual Typing Modes
- **Natural Mode**: Ultra-realistic human typing with inconsistencies, typos, and thinking pauses
- **Competition Mode**: Pure, consistent WPM typing for speed practice

### 🎮 Customizable Realism (Natural Mode)
- **Adjustable Typos**: 0-20% typo probability with QWERTY-based key errors
- **Synonym Substitutions**: 0-20% chance of word substitutions with automatic correction
- **Speed Variations**: Natural bursts (100+ WPM) mixed with thinking pauses
- **Intelligent Pausing**: Longer pauses after sentences, medium pauses after clauses

### ⚙️ Fully Customizable
- **WPM Range**: 10-500 WPM support
- **Custom Shortcuts**: Rebind start/stop/clear to any keys
- **Start Delay**: Configurable countdown before typing begins
- **Persistent Settings**: Saves your preferences between sessions

### 🚀 Technical Excellence
- **Lightweight**: Minimal resource usage
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Threaded Design**: Responsive UI during typing
- **Real-time Feedback**: Live WPM and progress tracking

## 📦 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/KaesarWU/natural-typing-simulator.git
cd natural-typing-simulator
```

2. **Install dependencies**:
```bash
pip install pyautogui
```

3. **Run the application**:
```bash
python natural_typing_simulator.py
```

## 🎮 Usage

### Basic Operation
1. Paste your text into the text area
2. Select your preferred mode (Natural/Competition)
3. Adjust settings as needed
4. Click "Start Typing" or use your custom shortcut
5. Quickly move cursor to target application
6. Watch the magic happen!

### Custom Shortcuts
Access settings (⚙️) to rebind:
- **Start Typing**: Default F5 (configurable)
- **Stop Typing**: Default F6/Escape (configurable)  
- **Clear Text**: Default Ctrl+L (configurable)

### Mode Comparison
| Feature | Natural Mode | Competition Mode |
|---------|--------------|------------------|
| Typos | ✅ Customizable (0-20%) | ❌ None |
| Synonyms | ✅ Customizable (0-20%) | ❌ None |
| Speed Variations | ✅ Realistic bursts & pauses | ❌ Consistent |
| Thinking Pauses | ✅ Intelligent pauses | ❌ None |
| Best For | Demonstrations, realism | Speed practice, testing |

## ⚙️ Configuration Examples

### 🎭 Ultra-Realistic Setup
```yaml
Mode: Natural
WPM: 60
Typos: 5%
Synonyms: 3%
Shortcuts: F5=Start, F6=Stop, Ctrl+L=Clear
```

### 🏆 Competition Setup  
```yaml
Mode: Competition  
WPM: 120
Typos: 0%
Synonyms: 0%
Shortcuts: F1=Start, F2=Stop, Ctrl+C=Clear
```

### 🚀 Fast but Human Setup
```yaml
Mode: Natural
WPM: 100  
Typos: 2%
Synonyms: 1%
Shortcuts: F8=Start, F9=Stop, Ctrl+X=Clear
```

## 🛠️ Technical Details

### Architecture
- **Frontend**: Tkinter for lightweight, cross-platform GUI
- **Automation**: PyAutoGUI for cross-platform input simulation
- **Threading**: Separate typing thread to maintain UI responsiveness
- **Configuration**: JSON-based settings persistence

### Algorithm
The typing engine uses sophisticated probability models:
- **Typos**: QWERTY adjacency mapping with realistic correction flow
- **Synonyms**: Dictionary-based substitution with rapid correction
- **Timing**: Gaussian distribution around target WPM with burst detection
- **Pausing**: Context-aware pauses based on punctuation and random thinking

## 🎯 Use Cases

### 🎬 Content Creation
- Make automated typing look human in videos/demos
- Create realistic screen recordings for tutorials

### 🧪 Testing & Development
- Test applications that monitor typing patterns
- Evaluate typing tutors and learning software
- Benchmark text input systems

### ♿ Accessibility
- Assist users with motor impairments
- Provide typing assistance for temporary injuries

### 🎓 Education
- Demonstrate proper typing rhythm
- Show realistic vs robotic typing patterns
- Practice maintaining speed with distractions

## 🐛 Troubleshooting

**Typing doesn't start?**
- Ensure cursor is in target application
- Check pyautogui installation
- Some applications block automated input

**Installation issues?**
- Verify Python 3.6+ is installed
- On Linux, install tkinter separately: `sudo apt-get install python3-tk`

**Shortcuts not working?**
- Check key conflicts with your system
- Try different key combinations in settings

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional keyboard layouts (AZERTY, QWERTZ)
- More sophisticated typo patterns
- Enhanced synonym databases
- Performance optimizations

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

Use responsibly and only in environments where you have permission to automate typing. The developer is not responsible for any misuse.

---

**Created by [KaesarWU](https://github.com/KaesarWU)** 

*Making automated typing beautifully human since 2025* 🚀

---

## 🎉 Quick Start

```python
# Just run it!
python natural_typing_simulator.py
```

Experience the most realistic typing simulation available - perfect for any scenario where you want automated typing to appear genuinely human!
