"""Pollinations API Client"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional
import time
import random
from pathlib import Path
import config

class PollinationsClient:
    """Client for interacting with Pollinations API"""
    
    def __init__(self):
        self.api_key = config.POLLINATIONS_API_KEY
        self.base_url = config.POLLINATIONS_BASE_URL
        self.model = config.DEFAULT_MODEL
        self.session = requests.Session()
        
        # Optimize session for performance and reliability
        retry_strategy = Retry(
            total=2,  # Fewer retries for speed
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
            max_retries=retry_strategy
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.update_headers()
    
    def update_config(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Update API client configuration"""
        if api_key is not None:
            self.api_key = api_key if api_key else config.POLLINATIONS_API_KEY
            self.update_headers()
        if model is not None:
            self.model = model
        print(f"[API] Config updated: model={self.model}, has_custom_key={bool(api_key)}")

    def update_headers(self):
        """Update session headers with current API key"""
        if self.api_key and self.api_key.strip():
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key.strip()}"
            })
        else:
            if "Authorization" in self.session.headers:
                del self.session.headers["Authorization"]
    
    @staticmethod
    def add_prompt_variation(prompt: str) -> str:
        """
        Add subtle variations to prompt to ensure unique generations
        
        Args:
            prompt: Base prompt
            
        Returns:
            Prompt with variation
        """
        # Add variety descriptors
        variations = [
            "stunning", "breathtaking", "magnificent", "spectacular", "gorgeous",
            "beautiful", "amazing", "incredible", "mesmerizing", "captivating",
            "detailed", "ultra-detailed", "highly detailed", "intricate",
            "vivid", "vibrant", "rich", "dynamic", "atmospheric"
        ]
        
        # Add lighting variations
        lighting = [
            "perfect lighting", "dramatic lighting", "cinematic lighting",
            "natural lighting", "soft lighting", "volumetric lighting",
            "studio lighting", "golden hour", "blue hour"
        ]
        
        # Randomly add 1-2 descriptors
        selected = random.sample(variations, random.randint(1, 2))
        light = random.choice(lighting)
        
        # Insert variations naturally
        enhanced = f"{', '.join(selected)}, {prompt}, {light}"
        
        print(f"[API] Original prompt: {prompt[:60]}...")
        print(f"[API] Enhanced prompt: {enhanced[:60]}...")
        
        return enhanced
    
    def generate_image(
        self, 
        prompt: str, 
        width: int = 1920, 
        height: int = 1080,
        enhance: bool = True,
        seed: Optional[int] = None,
        add_variation: bool = True
    ) -> Optional[bytes]:
        """
        Generate an image using Pollinations API
        
        Args:
            prompt: Text description of the image
            width: Image width in pixels
            height: Image height in pixels
            enhance: Whether to enhance the prompt
            seed: Random seed for reproducibility (None = random)
            add_variation: Add random variations to prompt for uniqueness
            
        Returns:
            Image data as bytes, or None if failed
        """
        try:
            # Generate random seed if not provided (ensures unique images)
            if seed is None:
                seed = random.randint(1, 1000000000)
            
            print(f"[API] Generating: {width}x{height}, seed: {seed}")
            
            # Add variations to prompt for uniqueness (optional)
            if add_variation:
                prompt = self.add_prompt_variation(prompt)
            
            # Build the URL with parameters
            url = f"{self.base_url}/{requests.utils.quote(prompt)}"
            
            params = {
                "model": self.model,
                "width": width,
                "height": height,
                "seed": seed,  # Always include seed for unique images
                "enhance": "true",  # Always enhance for High Quality as requested
                "nologo": "true",   # Remove watermark for cleaner wallpapers
                "private": "true",  # Private generation for higher quality/priority
                "quality": "high",  # High quality as requested
                "nofeed": "true"    # Don't add to public feed
            }
            print(f"[API] URL: {url}")
            print(f"[API] Params: {params}")
            
            # Add cache-busting headers
            headers = {
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
            
            # Make the request with timeout
            print(f"[API] Sending request...")
            response = self.session.get(url, params=params, headers=headers, timeout=60)
            
            print(f"[API] Response status: {response.status_code}")
            print(f"[API] Content-Type: {response.headers.get('content-type')}")
            print(f"[API] Content size: {len(response.content)} bytes")
            
            response.raise_for_status()
            
            # Check if we got an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type:
                print(f"[API] ERROR: Not an image! Content-Type: {content_type}")
                print(f"[API] Response text: {response.text[:500]}")
                return None
            
            return response.content
            
        except requests.exceptions.Timeout:
            print(f"[API] ERROR: Request timed out after 60 seconds")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[API] ERROR: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print(f"[API] Response status: {e.response.status_code}")
                    print(f"[API] Response text: {e.response.text[:500]}")
                except:
                    pass
            return None
        except Exception as e:
            print(f"[API] UNEXPECTED ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_image(self, image_data: bytes, filename: str) -> Optional[Path]:
        """
        Save image data to a file
        
        Args:
            image_data: Raw image bytes
            filename: Name for the saved file
            
        Returns:
            Path to saved file, or None if failed
        """
        try:
            filepath = config.CACHE_DIR / filename
            filepath.write_bytes(image_data)
            return filepath
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def generate_and_save(
        self,
        prompt: str,
        filename: str = None,
        **kwargs
    ) -> Optional[Path]:
        """
        Generate an image and save it in one step
        
        Args:
            prompt: Text description
            filename: Output filename (auto-generated if None)
            **kwargs: Additional arguments for generate_image
            
        Returns:
            Path to saved image, or None if failed
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"wallpaper_{timestamp}.png"
        
        image_data = self.generate_image(prompt, **kwargs)
        if image_data:
            return self.save_image(image_data, filename)
        return None
    
    def test_connection(self) -> bool:
        """Test if API connection is working"""
        try:
            # Try a simple generation with a small image (no variations for testing)
            result = self.generate_image(
                "test image", 
                width=1024, 
                height=1024,
                add_variation=False
            )
            return result is not None
        except Exception:
            return False
