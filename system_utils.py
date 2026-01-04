"""System utilities for wallpaper management and system integration"""

import ctypes
import platform
from pathlib import Path
from datetime import datetime
import requests
import json
import psutil
import time
import random
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
                        "- Windows Group Policy\n"
                        "- Corporate IT restrictions\n"
                        "- Privacy settings\n\n"
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
    
    _cached_weather = None
    _cache_time = None
    _cache_duration = 900  # Cache for 15 minutes
    
    @staticmethod
    def get_weather() -> Optional[dict]:
        """
        Get current weather condition with caching
        
        Returns:
            Weather data dict or None if failed
        """
        # Check cache
        if (WeatherDetector._cached_weather and 
            WeatherDetector._cache_time and 
            (time.time() - WeatherDetector._cache_time) < WeatherDetector._cache_duration):
            print(f"[WEATHER] Using cached weather: {WeatherDetector._cached_weather.get('condition', 'Unknown')}")
            return WeatherDetector._cached_weather
            
        try:
            # Method 1: Get detailed JSON from wttr.in
            # Using 'auto' or detecting city from LocationDetector
            location = LocationDetector.get_location()
            city = location.get('city', 'auto') if location else 'auto'
            
            # format=j1 gives a nice JSON response
            response = requests.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if 'current_condition' in data and data['current_condition']:
                current = data['current_condition'][0]
                
                # More robust extraction
                weather_desc = current.get('weatherDesc', [{}])
                condition_val = weather_desc[0].get('value', '') if weather_desc else ''
                
                weather_info = {
                    'condition': condition_val,
                    'temp': current.get('temp_C', ''),
                    'location': data.get('nearest_area', [{}])[0].get('areaName', [{}])[0].get('value', '') if data.get('nearest_area') else '',
                    'raw': condition_val
                }
                
                # Update cache
                WeatherDetector._cached_weather = weather_info
                WeatherDetector._cache_time = time.time()
                return weather_info
                
            return None
        except Exception as e:
            print(f"[WEATHER] Detailed fetch failed: {e}")
            # Fallback to simple format
            try:
                response = requests.get(
                    "https://wttr.in/?format=%C",
                    timeout=5
                )
                if response.status_code == 200:
                    condition = response.text.strip()
                    weather_info = {
                        'condition': condition,
                        'raw': condition
                    }
                    # Update cache even for fallback
                    WeatherDetector._cached_weather = weather_info
                    WeatherDetector._cache_time = time.time()
                    return weather_info
            except:
                pass
            return None
    
    @staticmethod
    def parse_weather_condition(weather_data: Optional[dict]) -> str:
        """
        Parse weather data to get condition type
        
        Args:
            weather_data: Weather data dict
            
        Returns:
            One of: clear, cloudy, rain, snow, storm, fog
        """
        if not weather_data:
            print("[WEATHER] No weather data, defaulting to 'clear'")
            return "clear"
        
        condition_text = weather_data.get('condition', '').lower()
        raw_text = weather_data.get('raw', '').lower()
        weather_lower = f"{condition_text} {raw_text}"
        
        print(f"[WEATHER] Parsing: {weather_lower[:50]}")
        
        if any(word in weather_lower for word in ["clear", "sunny", "fair"]):
            condition = "clear"
        elif any(word in weather_lower for word in ["rain", "drizzle", "shower", "rainy", "light rain"]):
            condition = "rain"
        elif any(word in weather_lower for word in ["snow", "sleet", "snowy", "ice"]):
            condition = "snow"
        elif any(word in weather_lower for word in ["storm", "thunder", "lightning", "thundery"]):
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
                print(f"[WEATHER] Found location: {location_name}")
                # We could append location to prompt if we wanted, but the presets are usually better
        
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
            "minimize_to_tray": True,
            "api_key": "",
            "model": "flux"
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

class GameDetector:
    """Detects currently running games and generates dynamic prompts"""
    
    # Common game process keywords to look for
    GAME_KEYWORDS = [
        "valorant", "leagueoflegends", "minecraft", "fortnite", "roblox", 
        "csgo", "cs2", "cyberpunk2077", "overwatch", "apex", "genshin",
        "starrail", "dota2", "pubg", "eldenring", "stardew", "terraria"
    ]
    
    @staticmethod
    def get_running_game() -> Optional[str]:
        """
        Detect if a game is currently running
        
        Returns:
            Game name or None if no game detected
        """
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name'].lower()
                    # Check for .exe or other common extensions
                    clean_name = name.replace(".exe", "").replace("-", "").replace("_", "")
                    
                    for keyword in GameDetector.GAME_KEYWORDS:
                        if keyword in clean_name:
                            # Map back to a nice name
                            mapping = {
                                "leagueoflegends": "League of Legends",
                                "csgo": "Counter-Strike: Global Offensive",
                                "cs2": "Counter-Strike 2",
                                "cyberpunk2077": "Cyberpunk 2077",
                                "starrail": "Honkai: Star Rail",
                                "apex": "Apex Legends",
                                "pubg": "PUBG: BATTLEGROUNDS",
                                "eldenring": "Elden Ring",
                                "stardew": "Stardew Valley"
                            }
                            return mapping.get(keyword, keyword.capitalize())
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            return None
        except Exception as e:
            print(f"[GAME] Detection error: {e}")
            return None

    @staticmethod
    def get_game_prompt() -> str:
        """
        Detect running game and generate a dynamic prompt
        """
        game_name = GameDetector.get_running_game()
        
        if not game_name:
            print("[GAME] No game detected, using default gaming prompt")
            return "Professional gaming setup with vibrant RGB lighting, futuristic mechanical keyboard, dual monitor setup, cinematic atmosphere, 8k resolution, photorealistic"
            
        print(f"[GAME] Detected: {game_name}")
        
        # Dynamic prompt construction
        base_prompt = f"Epic high-quality wallpaper inspired by the game {game_name}. "
        style_elements = "Cinematic lighting, vibrant colors, iconic aesthetic, highly detailed environment, 8k resolution, masterpiece, digital art style."
        
        # Add some variety based on the game name for better results
        if any(word in game_name.lower() for word in ["minecraft", "roblox", "stardew", "terraria"]):
            style_elements = "Vibrant stylized art style, beautiful lighting, atmospheric world, sharp detail, 8k, digital painting."
        elif any(word in game_name.lower() for word in ["cyberpunk", "valorant", "apex", "overwatch"]):
            style_elements = "Futuristic sci-fi aesthetic, neon accents, sharp geometric lines, cinematic atmosphere, high-octane energy, 8k."
            
        return f"{base_prompt}{style_elements}"
