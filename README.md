# 💜 PolliPaper

**Your AI-Powered Wallpaper Generation Companion**

PolliPaper is a beautiful desktop application that generates stunning AI wallpapers using the Pollinations.ai API. Transform your desktop with dynamic, context-aware wallpapers that adapt to time of day, weather, music, and more!

---

## ✨ Features

### 🎨 **10 Generation Modes**
- **Time of Day** - Dynamic wallpapers matching current time
- **Weather Live** - Reacts to your local weather conditions  
- **Music Sync** - Visualizes your currently playing music
- **Aesthetic** - Trendy vaporwave and modern art styles
- **Nature** - Serene landscapes and natural beauty
- **Space** - Cosmic scenes and celestial wonders
- **Abstract** - Digital art patterns and shapes
- **Cyberpunk** - Neon-lit futuristic cityscapes
- **Fantasy** - Magical worlds and mythical scenes
- **Custom** - Your own creative prompts

### ⚡ **Smart Features**
- 🔄 **Auto-Change** - Automatically refresh wallpapers (1-240 minutes)
- 🎯 **Quick Generate** - Double-click any mode for instant generation
- 💾 **Auto-Save** - All wallpapers saved to Pictures folder
- 🚀 **System Tray** - Minimize to background, always accessible
- ⌨️ **Keyboard Shortcuts** - Fast workflow with hotkeys

### 🎨 **Beautiful UI**
- Modern purple-pink gradient theme
- Smooth animations and transitions
- Responsive side panels (Help, Settings, Support)
- High-contrast, accessible design

---

## 🚀 Quick Start

### For Users
1. Download `PolliPaper.exe` from [Releases](../../releases)
2. Run the application
3. Select a generation mode
4. Click **GENERATE NOW** or press Enter
5. Enjoy your AI-generated wallpaper!

### For Developers

#### Prerequisites
- Python 3.12+
- Windows 10/11
- Git

#### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pollipaper.git
cd pollipaper

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
# Copy security.py.example to security.py and add your Pollinations API key
copy security.py.example security.py
# Edit security.py and replace YOUR_API_KEY_HERE with your actual key

# Run the application
python main.py
```

#### Building EXE
```bash
# Build with PyInstaller
venv\Scripts\pyinstaller build.spec --noconfirm

# Output will be in dist/PolliPaper.exe
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` / `Space` | Generate wallpaper |
| `Escape` | Minimize to tray |
| `Ctrl + Q` | Quit application |

---

## 🛠️ Project Structure

```
pollipaper/
├── main.py              # Main application entry
├── config.py            # Configuration & prompts
├── api_client.py        # Pollinations API client
├── security.py          # API key obfuscation
├── mode_selector.py     # Mode selection UI
├── tray_manager.py      # System tray integration
├── setup_wizard.py      # First-run setup
├── startup_manager.py   # Auto-start functionality
├── system_utils.py      # System utilities
├── build.spec           # PyInstaller build configuration
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🔧 Configuration

Settings are stored in `%APPDATA%/PolliPaper/settings.json`:

```json
{
  "resolution": "1920x1080",
  "auto_start": false,
  "enhance_prompts": true,
  "last_mode": "aesthetic"
}
```

---

## 🎨 Supported Resolutions

- 1920×1080 (Full HD)
- 2560×1440 (2K)
- 3840×2160 (4K)
- 1366×768 (Laptop)
- 1280×720 (HD)

---

## 🔐 Security

- API keys are obfuscated using XOR cipher and base64 encoding
- Compiled EXE makes key extraction significantly harder
- No sensitive data stored in plaintext
- All settings saved locally, no telemetry

---

## 📝 Dependencies

- **customtkinter** - Modern UI framework
- **Pillow** - Image processing
- **requests** - HTTP client
- **psutil** - System utilities
- **pyaudio** - Audio detection (Music Sync mode)
- **pystray** - System tray integration

See `requirements.txt` for full list.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💜 Acknowledgments

- **Pollinations.ai** - For providing the amazing AI image generation API
- **Flux Model** - High-quality AI image generation
- **CustomTkinter** - Beautiful modern UI framework
- All contributors and users who support this project!

---

## 📧 Support

- 🐛 **Bug Reports**: [GitHub Issues](../../issues)
- 💡 **Feature Requests**: [GitHub Discussions](../../discussions)
- 💬 **Questions**: Open an issue with the `question` label

---

**Made with 💜 by the PolliPaper Team**

*Transform your desktop, one AI wallpaper at a time!*
