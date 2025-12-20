"""System utilities for wallpaper management and system integration"""

import ctypes
import platform
from pathlib import Path
from datetime import datetime
import requests
import json
from typing import Optional, Tuple
import config

class WallpaperManager:
    """Manages Windows wallpaper setting"""
    
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02
    
    @staticmethod
    def check_wallpaper_access() -> bool:
        """
        Check if the application has access to change wallpaper
        
        Returns:
            True if access is available, False otherwise
        """
        try:
            # Try to query current wallpaper
            buffer = ctypes.create_unicode_buffer(260)
            result = ctypes.windll.user32.SystemParametersInfoW(
                0x0073,  # SPI_GETDESKWALLPAPER
                260,
                buffer,
                0
            )
            return result != 0
        except Exception:
            return False
    
    @staticmethod
    def open_windows_personalization_settings():
        """Open Windows personalization settings for wallpaper"""
        try:
            import subprocess
            # Open Windows Settings to Personalization > Background
            subprocess.Popen(['start', 'ms-settings:personalization-background'], shell=True)
            return True
        except Exception as e:
            print(f"Error opening settings: {e}")
            return False
    
    @staticmethod
    def set_wallpaper(image_path: Path, show_error_dialog=False) -> bool:
        """
        Set Windows desktop wallpaper
        
        Args:
            image_path: Path to the image file
            show_error_dialog: Whether to show error dialog on failure
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # First check if we have access
            if not WallpaperManager.check_wallpaper_access():
                if show_error_dialog:
                    from tkinter import messagebox
                    response = messagebox.askyesno(
                        "Wallpaper Access Required",
                        "PolliPaper needs access to change your wallpaper.\n\n"
                        "This might be blocked by:\n"
                        "• Windows Group Policy\n"
                        "• Corporate IT restrictions\n"
                        "• Privacy settings\n\n"
                        "Would you like to open Windows settings to check permissions?"
                    )
                    if response:
                        WallpaperManager.open_windows_personalization_settings()
                return False
            
            # Convert to absolute path string
            abs_path = str(image_path.absolute())
            
            # Verify the file exists
            if not image_path.exists():
                print(f"Wallpaper file does not exist: {abs_path}")
                return False
            
            # Set the wallpaper using Windows API
            result = ctypes.windll.user32.SystemParametersInfoW(
                WallpaperManager.SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                WallpaperManager.SPIF_UPDATEINIFILE | WallpaperManager.SPIF_SENDWININICHANGE
            )
            
            if result == 0 and show_error_dialog:
                from tkinter import messagebox
                response = messagebox.askyesno(
                    "Failed to Set Wallpaper",
                    "Could not change the wallpaper. This may be due to system restrictions.\n\n"
                    "Would you like to open Windows settings to check permissions?"
                )
                if response:
                    WallpaperManager.open_windows_personalization_settings()
            
            return result != 0
            
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
            if show_error_dialog:
                from tkinter import messagebox
                messagebox.showerror(
                    "Error",
                    f"An error occurred while setting the wallpaper:\n{str(e)}"
                )
            return False
    
    @staticmethod
    def get_screen_resolution() -> Tuple[int, int]:
        """Get current screen resolution"""
        try:
            user32 = ctypes.windll.user32
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            return (width, height)
        except Exception:
            return (1920, 1080)  # Default to Full HD

class LocationDetector:
    """Detects user's location for weather and time-based features"""
    
    _cached_location = None
    _cache_time = None
    _cache_duration = 3600  # Cache for 1 hour
    
    @staticmethod
    def get_location() -> Optional[dict]:
        """
        Get user's location using IP geolocation
        
        Returns:
            Dict with keys: city, region, country, lat, lon, timezone
        """
        import time
        
        # Check cache
        if (LocationDetector._cached_location and 
            LocationDetector._cache_time and 
            (time.time() - LocationDetector._cache_time) < LocationDetector._cache_duration):
            print(f"[LOCATION] Using cached: {LocationDetector._cached_location.get('city', 'Unknown')}")
            return LocationDetector._cached_location
        
        try:
            print("[LOCATION] Fetching location data...")
            # Try multiple services for redundancy
            
            # Method 1: ip-api.com (free, no key needed)
            try:
                response = requests.get(
                    "http://ip-api.com/json/",
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        location = {
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('regionName', ''),
                            'country': data.get('country', ''),
                            'lat': data.get('lat', 0),
                            'lon': data.get('lon', 0),
                            'timezone': data.get('timezone', '')
                        }
                        LocationDetector._cached_location = location
                        LocationDetector._cache_time = time.time()
                        print(f"[LOCATION] Detected: {location['city']}, {location['country']}")
                        return location
            except Exception as e:
                print(f"[LOCATION] ip-api.com failed: {e}")
            
            # Method 2: ipapi.co (backup)
            try:
                response = requests.get(
                    "https://ipapi.co/json/",
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    location = {
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('region', ''),
                        'country': data.get('country_name', ''),
                        'lat': data.get('latitude', 0),
                        'lon': data.get('longitude', 0),
                        'timezone': data.get('timezone', '')
                    }
                    LocationDetector._cached_location = location
                    LocationDetector._cache_time = time.time()
                    print(f"[LOCATION] Detected: {location['city']}, {location['country']}")
                    return location
            except Exception as e:
                print(f"[LOCATION] ipapi.co failed: {e}")
            
            print("[LOCATION] All location services failed, using defaults")
            return None
            
        except Exception as e:
            print(f"[LOCATION] Error: {e}")
            return None

class TimeDetector:
    """Detects time of day for dynamic wallpapers"""
    
    @staticmethod
    def get_time_period() -> str:
        """
        Get current time period based on local time
        
        Returns:
            One of: dawn, morning, afternoon, evening, night, midnight
        """
        now = datetime.now()
        hour = now.hour
        
        print(f"[TIME] Current time: {now.strftime('%I:%M %p')} (Hour: {hour})")
        
        if 5 <= hour < 7:
            period = "dawn"
        elif 7 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 17:
            period = "afternoon"
        elif 17 <= hour < 20:
            period = "evening"
        elif 20 <= hour < 23:
            period = "night"
        else:
            period = "midnight"
        
        print(f"[TIME] Period: {period}")
        return period
    
    @staticmethod
    def get_time_prompt() -> str:
        """Get prompt for current time of day"""
        period = TimeDetector.get_time_period()
        prompt = config.TIME_PROMPTS.get(period, config.TIME_PROMPTS["morning"])
        print(f"[TIME] Using prompt for '{period}'")
        return prompt

class WeatherDetector:
    """Detects current weather conditions"""
    
    @staticmethod
    def get_weather() -> Optional[str]:
        """
        Get current weather condition
        
        Returns:
            Weather description or None if failed
        """
        try:
            response = requests.get(
                config.WEATHER_API_URL,
                timeout=5
            )
            response.raise_for_status()
            return response.text.strip()
        except Exception as e:
            print(f"Error getting weather: {e}")
            return None
    
    @staticmethod
    def parse_weather_condition(weather_data: Optional[dict]) -> str:
        """
        Parse weather data to get condition type
        
        Args:
            weather_data: Weather data dict from get_weather()
            
        Returns:
            One of: clear, cloudy, rain, snow, storm, fog
        """
        if not weather_data:
            print("[WEATHER] No weather data, defaulting to 'clear'")
            return "clear"
        
        weather_text = weather_data.get('condition', '') + ' ' + weather_data.get('raw', '')
        weather_lower = weather_text.lower()
        
        print(f"[WEATHER] Parsing: {weather_lower[:50]}")
        
        if any(word in weather_lower for word in ["clear", "sunny"]):
            condition = "clear"
        elif any(word in weather_lower for word in ["rain", "drizzle", "shower", "rainy"]):
            condition = "rain"
        elif any(word in weather_lower for word in ["snow", "sleet", "snowy"]):
            condition = "snow"
        elif any(word in weather_lower for word in ["storm", "thunder", "lightning"]):
            condition = "storm"
        elif any(word in weather_lower for word in ["fog", "mist", "haze", "foggy"]):
            condition = "fog"
        elif any(word in weather_lower for word in ["cloud", "overcast", "cloudy", "partly"]):
            condition = "cloudy"
        else:
            condition = "clear"
        
        print(f"[WEATHER] Condition: {condition}")
        return condition
    
    @staticmethod
    def get_weather_prompt() -> str:
        """Get prompt based on current weather"""
        weather_data = WeatherDetector.get_weather()
        condition = WeatherDetector.parse_weather_condition(weather_data)
        prompt = config.WEATHER_PROMPTS.get(condition, config.WEATHER_PROMPTS["clear"])
        
        # Add location context if available
        if weather_data and weather_data.get('location'):
            location_name = weather_data['location']
            if location_name != 'auto' and not any(char.isdigit() for char in location_name):
                print(f"[WEATHER] Adding location context: {location_name}")
        
        return prompt

class MusicAnalyzer:
    """Analyzes system audio for music-reactive wallpapers"""
    
    def __init__(self):
        self.is_available = False
        try:
            import pyaudio
            self.pyaudio = pyaudio
            self.is_available = True
        except ImportError:
            print("PyAudio not available - music features disabled")
    
    def get_audio_energy(self) -> float:
        """
        Get current audio energy level (0.0 to 1.0)
        
        Returns:
            Audio energy level
        """
        if not self.is_available:
            return 0.5  # Return neutral value
        
        try:
            import numpy as np
            
            # Open audio stream
            p = self.pyaudio.PyAudio()
            stream = p.open(
                format=self.pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
            
            # Read audio data
            data = stream.read(1024, exception_on_overflow=False)
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Calculate energy
            audio_data = np.frombuffer(data, dtype=np.int16)
            energy = np.abs(audio_data).mean() / 32768.0
            
            return min(energy * 10, 1.0)  # Scale and cap at 1.0
            
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return 0.5
    
    def get_music_mood(self) -> str:
        """
        Determine music mood based on audio energy
        
        Returns:
            One of: calm, ambient, energetic, intense
        """
        energy = self.get_audio_energy()
        
        if energy < 0.2:
            return "calm"
        elif energy < 0.4:
            return "ambient"
        elif energy < 0.7:
            return "energetic"
        else:
            return "intense"
    
    def get_music_prompt(self) -> str:
        """Get prompt based on current music mood"""
        mood = self.get_music_mood()
        return config.MUSIC_PROMPTS.get(mood, config.MUSIC_PROMPTS["ambient"])

class SettingsManager:
    """Manages application settings persistence"""
    
    @staticmethod
    def load_settings() -> dict:
        """Load settings from file"""
        try:
            if config.CONFIG_FILE.exists():
                with open(config.CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # Return defaults
        return {
            "mode": "time_based",
            "resolution": "1920x1080",
            "auto_change_interval": 3600,  # 1 hour
            "enhance_prompts": True,
            "custom_prompt": "",
            "auto_start": False,
            "minimize_to_tray": True
        }
    
    @staticmethod
    def save_settings(settings: dict) -> bool:
        """Save settings to file"""
        try:
            with open(config.CONFIG_FILE, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
