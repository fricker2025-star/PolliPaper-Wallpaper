"""Windows startup management"""

import winreg
import sys
from pathlib import Path

class StartupManager:
    """Manages Windows startup registry entries"""
    
    REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "PolliPaper"
    
    @staticmethod
    def is_enabled() -> bool:
        """Check if startup is enabled"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REG_PATH,
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, StartupManager.APP_NAME)
                winreg.CloseKey(key)
                return True
            except WindowsError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @staticmethod
    def enable():
        """Enable startup"""
        try:
            # Get executable path
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                exe_path = sys.executable
            else:
                # Running as script - use pythonw to hide console
                exe_path = f'pythonw.exe "{Path(__file__).parent / "main.py"}"'
            
            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Set value
            winreg.SetValueEx(
                key,
                StartupManager.APP_NAME,
                0,
                winreg.REG_SZ,
                f'"{exe_path}" --minimized'
            )
            
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            print(f"Error enabling startup: {e}")
            return False
    
    @staticmethod
    def disable():
        """Disable startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            
            try:
                winreg.DeleteValue(key, StartupManager.APP_NAME)
            except WindowsError:
                pass  # Value doesn't exist
            
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            print(f"Error disabling startup: {e}")
            return False
    
    @staticmethod
    def toggle(enable: bool) -> bool:
        """Toggle startup"""
        if enable:
            return StartupManager.enable()
        else:
            return StartupManager.disable()
