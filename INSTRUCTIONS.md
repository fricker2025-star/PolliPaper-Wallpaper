# 🚀 PolliPaper - Build & Distribution Instructions

## 📋 Prerequisites

### Required Software
1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Inno Setup** - [Download](https://jrsoftware.org/isdl.php) (for creating installer)

### Optional (for development)
- **Visual Studio Code** - Recommended IDE
- **Git** - For version control

---

## 🔧 Development Setup

### 1. Install Dependencies

Open Command Prompt or PowerShell in the project directory:

```batch
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Icon

```batch
python create_icon.py
```

This creates `icon.ico` used for the application and installer.

### 3. Run in Development Mode

**Option A: Using the script**
```batch
run.bat
```

**Option B: Manual**
```batch
venv\Scripts\activate
python main.py
```

---

## 🏗️ Building the Executable

### Method 1: Using Build Script (Recommended)

```batch
build.bat
```

This will:
1. Create/activate virtual environment
2. Install all dependencies
3. Build the executable using PyInstaller
4. Output: `dist\PolliPaper.exe`

### Method 2: Manual Build

```batch
# Activate environment
venv\Scripts\activate

# Build with PyInstaller
pyinstaller build.spec --clean --noconfirm
```

### Testing the EXE

After building, test the executable:

```batch
cd dist
PolliPaper.exe
```

Verify:
- Application launches without errors
- UI displays correctly
- Wallpaper generation works
- Settings save/load properly
- System tray integration works
- Auto-start toggle functions

---

## 📦 Creating the Installer

### Prerequisites
Install **Inno Setup**: https://jrsoftware.org/isdl.php

### Steps

1. **Build the executable first** (see above)

2. **Open Inno Setup Compiler**

3. **Load the script:**
   - File → Open → Select `installer.iss`

4. **Compile:**
   - Build → Compile (or press Ctrl+F9)

5. **Output:**
   - Installer created in `installer_output\`
   - File name: `PolliPaper_Setup_v1.0.0.exe`

### Testing the Installer

1. Run the installer as a normal user
2. Install to default location
3. Create desktop/start menu shortcuts (optional)
4. Launch the application
5. Test all features
6. Uninstall and verify clean removal

---

## 🎨 Customization

### Changing Colors

Edit `config.py`:

```python
COLORS = {
    "primary": "#6366f1",      # Main accent color
    "secondary": "#8b5cf6",    # Secondary accent
    "bg_dark": "#0f172a",      # Dark background
    # ... etc
}
```

### Adding Generation Modes

1. Add to `config.py`:
```python
MODES = {
    "your_mode": "Your Mode Name",
    # ...
}
```

2. Add prompts:
```python
YOUR_PROMPTS = {
    "condition1": "prompt text...",
    # ...
}
```

3. Update `main.py` → `generate_wallpaper()` method

### Changing Default Settings

Edit `config.py` or modify default returns in `system_utils.py` → `SettingsManager.load_settings()`

---

## 🐛 Troubleshooting

### Build Issues

**Problem: PyInstaller fails**
- Solution: Update PyInstaller: `pip install --upgrade pyinstaller`
- Check Python version (3.9+ required)

**Problem: Missing modules in built EXE**
- Solution: Add to `hiddenimports` in `build.spec`

**Problem: Icon not embedding**
- Solution: Ensure `icon.ico` exists, run `create_icon.py`

### Runtime Issues

**Problem: App won't start**
- Run from command line to see errors: `dist\PolliPaper.exe`
- Check Windows Event Viewer for details

**Problem: Wallpaper not setting**
- Ensure image paths are absolute
- Check Windows permissions
- Try running as administrator

**Problem: API errors**
- Verify internet connection
- Check API key in `config.py`
- Ensure Pollen credits remain

### Installer Issues

**Problem: Inno Setup won't compile**
- Verify `dist\PolliPaper.exe` exists
- Check file paths in `installer.iss`
- Update Inno Setup to latest version

---

## 📝 Release Checklist

Before creating a release:

- [ ] Update version in `config.py`
- [ ] Update version in `installer.iss`
- [ ] Update version in `version_info.txt`
- [ ] Update `README.md` with changes
- [ ] Test all features thoroughly
- [ ] Build fresh executable
- [ ] Test executable on clean system
- [ ] Create installer
- [ ] Test installer on clean system
- [ ] Create release notes
- [ ] Tag release in Git (if using)

---

## 🚀 Distribution

### Files to Distribute

**For End Users:**
- `PolliPaper_Setup_v1.0.0.exe` (installer)
- `README.md` (usage instructions)

**For Developers:**
- Source code (all `.py` files)
- `requirements.txt`
- `build.spec`
- `installer.iss`
- Documentation files

### Recommended Distribution Methods

1. **GitHub Releases**
   - Create release with installer
   - Include README and changelog
   - Tag version properly

2. **Direct Download**
   - Host installer on website
   - Include installation guide
   - Provide support contact

3. **Microsoft Store** (Advanced)
   - Package as MSIX
   - Submit for review
   - Follow MS Store guidelines

---

## 🔐 Security Notes

### API Key Management

**For Distribution:**
- Consider removing hardcoded API key
- Implement user key input on first launch
- Or use environment variable: `os.getenv('POLLINATIONS_API_KEY')`

**For Production:**
```python
# In config.py
POLLINATIONS_API_KEY = os.getenv('POLLINATIONS_API_KEY', '')
```

Then users set it via:
- Settings UI
- Environment variable
- Config file

---

## 📞 Support

For build or distribution issues:
1. Check this guide thoroughly
2. Review error messages carefully
3. Test on clean Windows installation
4. Check Python and package versions

---

**Happy Building! 🎉**
