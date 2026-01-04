"""Configuration and constants for PolliPaper"""

import os
from pathlib import Path
from security import get_api_key

# API Configuration
POLLINATIONS_API_KEY = get_api_key()  # Obfuscated for security
POLLINATIONS_BASE_URL = "https://gen.pollinations.ai/image"
DEFAULT_MODEL = "flux"  # Flux model - High quality AI images

# Available models for custom API key users
POLLINATIONS_MODELS = [
    "flux",
    "flux-realism",
    "flux-coke",
    "flux-schizo",
    "flux-pro",
    "flux-dev",
    "turbo",
    "midjourney",
    "dalle",
    "any-dark"
]

# Weather API (using free wttr.in service)
WEATHER_API_URL = "https://wttr.in/?format=%C+%t"

# Application Settings
APP_NAME = "PolliPaper"
APP_VERSION = "1.0.0"
APP_DIR = Path(os.getenv('APPDATA')) / APP_NAME
CACHE_DIR = APP_DIR / "cache"
CONFIG_FILE = APP_DIR / "settings.json"

# UI Colors - Professional High-Contrast Purple-Pink Theme
COLORS = {
    # Primary Colors - Bold Purple
    "primary": "#8b5cf6",           # Sharp Purple
    "primary_hover": "#a78bfa",     # Lighter Purple Hover
    "primary_dark": "#6d28d9",      # Dark Purple
    
    # Secondary Colors - Vibrant Pink
    "secondary": "#ec4899",         # Bold Pink
    "secondary_hover": "#f472b6",   # Light Pink Hover
    
    # Status Colors
    "success": "#10b981",           # Emerald
    "danger": "#ef4444",            # Red
    "warning": "#f59e0b",           # Amber
    "info": "#3b82f6",              # Blue
    
    # Background - Deep Purple-Black with Contrast
    "bg_app": "#0d0118",            # Deepest Purple-Black (App BG)
    "bg_dark": "#1a0b2e",           # Dark Purple-Black
    "bg_medium": "#2a1a4a",         # Medium Purple
    "bg_light": "#3d2667",          # Light Purple
    "bg_card": "#251447",           # Card Background
    
    # Text - High Contrast
    "text_primary": "#ffffff",      # Pure White
    "text_secondary": "#e2e8f0",    # Light Gray
    "text_muted": "#94a3b8",        # Muted Gray
    
    # Accents - Gold & Borders
    "accent_gold": "#fbbf24",       # Sharp Gold
    "border": "#6d28d9",            # Purple Border
    "border_light": "#4c1d95",      # Light Purple Border
    "divider": "#2d1b4e",           # Subtle Divider
    
    # Gradients
    "gradient_purple": "#8b5cf6",   # Purple Start
    "gradient_pink": "#ec4899",     # Pink End
    
    # Interactive States
    "hover_overlay": "#1f1735",     # Hover State
    "active": "#a78bfa",            # Active State
    "disabled": "#475569",          # Disabled State
}

# Mode Themes - Dynamic UI Tinting
MODE_THEMES = {
    "time_based": {
        "name": "Time of Day",
        "accent": "#f59e0b",  # Amber
        "gradient": ["#f59e0b", "#d97706"],
        "desc": "Generates wallpapers matching your local time and sun position."
    },
    "weather_based": {
        "name": "Weather Reactive",
        "accent": "#0ea5e9",  # Sky Blue
        "gradient": ["#0ea5e9", "#0284c7"],
        "desc": "Reacts to your local weather: sunny, rainy, or stormy visuals."
    },
    "music_based": {
        "name": "Music Reactive",
        "accent": "#ec4899",  # Pink
        "gradient": ["#ec4899", "#db2777"],
        "desc": "Visualizes your currently playing music into abstract art."
    },
    "gaming": {
        "name": "Game Sense",
        "accent": "#10b981",  # Emerald
        "gradient": ["#10b981", "#059669"],
        "desc": "Detects running games and adapts themes to match the genre."
    },
    "aesthetic": {
        "name": "Aesthetic Vibe",
        "accent": "#8b5cf6",  # Purple
        "gradient": ["#8b5cf6", "#7c3aed"],
        "desc": "Trendy vaporwave, synthwave, and modern aesthetic art styles."
    },
    "nature": {
        "name": "Nature Focus",
        "accent": "#22c55e",  # Green
        "gradient": ["#22c55e", "#16a34a"],
        "desc": "Serene landscapes, forests, and natural wonders of the world."
    },
    "space": {
        "name": "Space & Cosmos",
        "accent": "#6366f1",  # Indigo
        "gradient": ["#6366f1", "#4f46e5"],
        "desc": "Cosmic scenes, nebulas, and the deep mysteries of the universe."
    },
    "abstract": {
        "name": "Abstract Art",
        "accent": "#f43f5e",  # Rose
        "gradient": ["#f43f5e", "#e11d48"],
        "desc": "Digital patterns, shapes, and complex abstract compositions."
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "accent": "#06b6d4",  # Cyan
        "gradient": ["#06b6d4", "#0891b2"],
        "desc": "Neon-lit futuristic cityscapes and high-tech dystopias."
    },
    "fantasy": {
        "name": "Fantasy World",
        "accent": "#a855f7",  # Purple-Pink
        "gradient": ["#a855f7", "#9333ea"],
        "desc": "Magical worlds, mythical creatures, and epic fantasy scenes."
    },
    "manual": {
        "name": "Manual Mode",
        "accent": "#64748b",  # Slate
        "gradient": ["#64748b", "#475569"],
        "desc": "Your creative vision. Type anything and let PolliPaper build it."
    }
}

# Prompt Placeholders
PROMPT_EXAMPLES = [
    "ethereal forest at sunset with floating bioluminescent spores",
    "cyberpunk street market in the rain with neon reflections",
    "minimalist geometric abstract art with gold and marble textures",
    "majestic nebula with swirling cosmic dust and distant stars",
    "vaporwave sunset with palm trees and retro grid horizon",
    "hyper-realistic mountain landscape with clear turquoise lake",
    "fantasy castle floating among the clouds at dawn",
    "macro photography of a mechanical butterfly with clockwork wings"
]

# Wallpaper Settings
# Flux model supports flexible resolutions
DEFAULT_RESOLUTION = "1920x1080"
SUPPORTED_RESOLUTIONS = [
    "1920x1080",  # Full HD
    "2560x1440",  # 2K
    "3840x2160",  # 4K
    "1366x768",   # Laptop
    "1280x720",   # HD
]

# Generation Settings
ENHANCE_DEFAULT = True

# Time of Day Prompts
TIME_PROMPTS = {
    "dawn": "Beautiful serene dawn landscape, soft pink and orange sky, peaceful morning atmosphere, cinematic, 8k, photorealistic",
    "morning": "Bright cheerful morning scene, clear blue sky, vibrant colors, energetic atmosphere, beautiful sunlight, 8k, photorealistic",
    "afternoon": "Warm afternoon landscape, golden sunlight, peaceful scene, clear skies, vibrant nature, 8k, photorealistic",
    "evening": "Stunning sunset scene, golden hour lighting, warm orange and purple sky, peaceful atmosphere, 8k, photorealistic",
    "night": "Beautiful night sky with stars, moonlight, serene nocturnal landscape, deep blues and purples, 8k, photorealistic",
    "midnight": "Mystical midnight scene, starry sky, moonlit landscape, dreamy atmosphere, dark blues and silvers, 8k, photorealistic"
}

# Weather Prompts
WEATHER_PROMPTS = {
    "clear": "Crystal clear sky, beautiful sunny day, vibrant landscape, perfect weather, 8k, photorealistic",
    "cloudy": "Dramatic cloudy sky, moody atmosphere, beautiful cloud formations, scenic landscape, 8k, photorealistic",
    "rain": "Rainy day atmosphere, water droplets, moody sky, cozy rainy scene, beautiful reflections, 8k, photorealistic",
    "snow": "Beautiful snowy landscape, winter wonderland, pristine white snow, peaceful winter scene, 8k, photorealistic",
    "storm": "Dramatic storm clouds, powerful weather, lightning in distance, epic atmospheric scene, 8k, photorealistic",
    "fog": "Mysterious foggy landscape, ethereal atmosphere, soft diffused light, dreamy scene, 8k, photorealistic"
}

# Music Mood Prompts
MUSIC_PROMPTS = {
    "energetic": "Dynamic energetic abstract art, vibrant neon colors, motion blur, exciting patterns, high energy visualization, 8k, digital art",
    "calm": "Peaceful serene abstract patterns, soft pastel colors, flowing shapes, meditative atmosphere, zen-like, 8k, digital art",
    "intense": "Intense dramatic abstract visualization, bold contrasting colors, sharp geometric patterns, powerful energy, explosive, 8k, digital art",
    "ambient": "Ethereal ambient visual patterns, soft glowing colors, dreamy atmosphere, flowing organic forms, mystical, 8k, digital art"
}

# Aesthetic Prompts
AESTHETIC_PROMPTS = {
    "vaporwave": "Vaporwave aesthetic, retro 80s vibes, pink and cyan colors, palm trees, geometric shapes, nostalgic, 8k",
    "minimalist": "Minimalist landscape, simple clean design, limited color palette, peaceful composition, modern aesthetic, 8k",
    "cottagecore": "Cozy cottagecore aesthetic, wildflowers, rustic cottage, warm sunlight, peaceful countryside, vintage feel, 8k",
    "dark_academia": "Dark academia aesthetic, vintage library, moody atmosphere, warm candlelight, books and knowledge, classical, 8k",
    "synthwave": "Synthwave aesthetic, neon sunset, retro futuristic, grid patterns, purple and pink gradient, 80s vibes, 8k"
}

# Nature Themes
NATURE_PROMPTS = {
    "forest": "Mystical forest scene, sunbeams through trees, lush greenery, peaceful woodland path, magical atmosphere, 8k, photorealistic",
    "ocean": "Serene ocean view, crystal clear waters, tropical beach, gentle waves, paradise setting, stunning colors, 8k, photorealistic",
    "mountains": "Majestic mountain landscape, dramatic peaks, alpine scenery, pristine wilderness, breathtaking vista, 8k, photorealistic",
    "desert": "Beautiful desert landscape, sand dunes, warm golden light, vast open space, dramatic sky, 8k, photorealistic",
    "aurora": "Northern lights display, dancing aurora borealis, starry night sky, magical atmosphere, vivid colors, 8k, photorealistic"
}

# Space & Cosmos
SPACE_PROMPTS = {
    "nebula": "Colorful space nebula, cosmic clouds, stars and galaxies, vibrant colors, deep space photography, 8k",
    "planets": "Alien planet landscape, multiple moons in sky, sci-fi scenery, otherworldly atmosphere, cinematic, 8k",
    "galaxy": "Spiral galaxy, millions of stars, cosmic beauty, deep space view, astronomical wonder, 8k",
    "blackhole": "Black hole visualization, event horizon, gravitational lensing, cosmic phenomenon, scientific beauty, 8k",
    "stars": "Starfield panorama, milky way galaxy, countless stars, cosmic perspective, night sky magnificence, 8k"
}

# Abstract Art
ABSTRACT_PROMPTS = {
    "fluid": "Fluid art, flowing colors, marble texture, organic patterns, liquid dynamics, vibrant swirls, ultra detailed, sharp focus, 8k uhd, digital art masterpiece",
    "geometric": "Geometric abstract art, sharp angles, bold shapes, modern design, colorful composition, ultra detailed, sharp focus, 8k uhd, digital art, award winning",
    "fractal": "Fractal patterns, mathematical beauty, infinite detail, psychedelic colors, mesmerizing design, ultra detailed, sharp focus, 8k uhd, digital art masterpiece",
    "watercolor": "Abstract watercolor art, soft blending, dreamy colors, artistic expression, flowing paint, ultra detailed, sharp focus, 8k uhd, digital art, professional",
    "glitch": "Glitch art aesthetic, digital corruption, vibrant color distortion, cybernetic patterns, modern digital art, ultra detailed, sharp focus, 8k uhd, masterpiece"
}

# Cyberpunk
CYBERPUNK_PROMPTS = {
    "city": "Cyberpunk city night, neon lights, rain-soaked streets, futuristic buildings, blade runner atmosphere, 8k, cinematic",
    "tech": "Cyberpunk technology, holographic interfaces, neon circuitry, futuristic tech, sci-fi aesthetic, 8k, digital art",
    "dark": "Dark cyberpunk alley, moody atmosphere, neon signs, urban dystopia, gritty futuristic, 8k, cinematic"
}

# Fantasy
FANTASY_PROMPTS = {
    "castle": "Fantasy castle, magical kingdom, dramatic clouds, enchanted atmosphere, epic fantasy landscape, 8k, digital art",
    "dragon": "Majestic dragon flying, epic fantasy scene, magical atmosphere, dramatic lighting, mythical creature, 8k, digital art",
    "enchanted": "Enchanted forest, magical glowing plants, fairy lights, mystical atmosphere, fantasy wonderland, 8k, digital art",
    "portal": "Magical portal, swirling energy, fantasy gateway, mystical doorway, otherworldly magic, 8k, digital art"
}

# Create directories
APP_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
