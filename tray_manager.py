"""System tray integration for PolliPaper"""

import pystray
from PIL import Image, ImageDraw
import threading
import sys
from pathlib import Path

import config

class TrayManager:
    """Manages system tray icon and menu"""
    
    def __init__(self, app):
        self.app = app
        self.icon = None
        self.is_running = False
        
    def create_icon_image(self):
        """Create tray icon image"""
        # Create a simple icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=config.COLORS["primary"])
        dc = ImageDraw.Draw(image)
        
        # Draw a simple wallpaper symbol
        dc.rectangle([10, 10, 54, 54], fill=config.COLORS["bg_dark"], outline=config.COLORS["text_primary"], width=2)
        dc.rectangle([15, 15, 49, 49], fill=config.COLORS["secondary"])
        
        return image
    
    def create_menu(self):
        """Create tray menu"""
        return pystray.Menu(
            pystray.MenuItem("PolliPaper", self.show_window, default=True),
            pystray.MenuItem("Generate Now", self.generate_wallpaper),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Time-Based", lambda: self.quick_generate("time")),
            pystray.MenuItem("Weather-Based", lambda: self.quick_generate("weather")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", self.show_settings),
            pystray.MenuItem("Exit", self.quit_app)
        )
    
    def show_window(self, icon=None, item=None):
        """Show main window"""
        self.app.deiconify()
        self.app.lift()
        self.app.focus_force()
    
    def generate_wallpaper(self, icon=None, item=None):
        """Generate wallpaper from tray"""
        self.app.generate_wallpaper()
    
    def quick_generate(self, mode: str):
        """Quick generation from tray"""
        self.app.quick_generate(mode)
    
    def show_settings(self, icon=None, item=None):
        """Show settings window"""
        self.show_window()
        # Settings are in the main window, just show it
    
    def quit_app(self, icon=None, item=None):
        """Quit application properly - IMMEDIATE EXIT"""
        print("[TRAY] Quit requested from system tray")
        
        # Stop the icon immediately
        if self.icon:
            try:
                self.icon.stop()
                self.is_running = False
                print("[TRAY] Icon stopped")
            except Exception as e:
                print(f"[TRAY] Error stopping icon: {e}")
        
        # Call cleanup directly (don't use after() - might not work if mainloop stopping)
        try:
            self.app.cleanup_and_exit()
        except:
            # If cleanup fails, force exit anyway
            import os
            print("[TRAY] Cleanup failed, forcing exit")
            os._exit(0)
    
    def run(self):
        """Run tray icon"""
        if self.is_running:
            return
        
        self.is_running = True
        image = self.create_icon_image()
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            config.APP_NAME,
            image,
            config.APP_NAME,
            menu
        )
        
        # Run in separate thread
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop tray icon"""
        if self.icon:
            self.icon.stop()
        self.is_running = False
