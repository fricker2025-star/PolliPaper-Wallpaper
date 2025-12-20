"""First-run setup wizard for PolliPaper"""

import customtkinter as ctk
from tkinter import messagebox
import config
from system_utils import WallpaperManager
from api_client import PollinationsClient

class SetupWizard(ctk.CTkToplevel):
    """Setup wizard for first-time users"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.current_step = 0
        self.setup_complete = False
        
        # Configure window
        self.title("Welcome to PolliPaper!")
        self.geometry("700x500")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f'700x500+{x}+{y}')
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        
        # Create steps
        self.steps = [
            self.create_welcome_step,
            self.create_permissions_step,
            self.create_test_step,
            self.create_complete_step
        ]
        
        # Show first step
        self.show_step(0)
    
    def show_step(self, step_num):
        """Show a specific step"""
        # Clear container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.current_step = step_num
        
        # Create step
        self.steps[step_num]()
    
    def create_welcome_step(self):
        """Welcome screen"""
        # Title
        title = ctk.CTkLabel(
            self.container,
            text="✨ Welcome to PolliPaper!",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=config.COLORS["primary"]
        )
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Content frame
        content = ctk.CTkFrame(self.container, fg_color=config.COLORS["bg_medium"], corner_radius=20)
        content.grid(row=1, column=0, sticky="nsew", pady=20)
        content.grid_columnconfigure(0, weight=1)
        
        # Icon/Image placeholder
        icon = ctk.CTkLabel(
            content,
            text="🎨",
            font=ctk.CTkFont(size=80)
        )
        icon.pack(pady=(40, 20))
        
        # Description
        desc = ctk.CTkLabel(
            content,
            text="AI-Powered Dynamic Wallpaper Engine\n\nTransform your desktop with stunning AI-generated wallpapers\nthat adapt to time, weather, and your music!",
            font=ctk.CTkFont(size=14),
            text_color=config.COLORS["text_secondary"],
            justify="center"
        )
        desc.pack(pady=20)
        
        # Features
        features_frame = ctk.CTkFrame(content, fg_color="transparent")
        features_frame.pack(pady=20)
        
        features = [
            "🌅 Time-reactive wallpapers",
            "⛅ Weather-based generation",
            "🎵 Music visualizations",
            "🎨 Custom AI prompts"
        ]
        
        for i, feature in enumerate(features):
            row = i // 2
            col = i % 2
            label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_primary"]
            )
            label.grid(row=row, column=col, padx=20, pady=5, sticky="w")
        
        # Navigation
        self.create_navigation(next_text="Let's Get Started →")
    
    def create_permissions_step(self):
        """Permissions and setup step"""
        # Title
        title = ctk.CTkLabel(
            self.container,
            text="🔧 Quick Setup",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=config.COLORS["primary"]
        )
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Content
        content = ctk.CTkFrame(self.container, fg_color=config.COLORS["bg_medium"], corner_radius=20)
        content.grid(row=1, column=0, sticky="nsew", pady=20)
        
        # Info text
        info = ctk.CTkLabel(
            content,
            text="PolliPaper needs permission to change your wallpaper.\n\nThis is a one-time setup to ensure everything works smoothly.",
            font=ctk.CTkFont(size=14),
            text_color=config.COLORS["text_secondary"],
            justify="center"
        )
        info.pack(pady=(30, 20))
        
        # Permission items
        items_frame = ctk.CTkFrame(content, fg_color=config.COLORS["bg_light"], corner_radius=15)
        items_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        permissions = [
            ("✅ Wallpaper Control", "Required to change your desktop background"),
            ("✅ Internet Access", "Required to generate AI wallpapers"),
            ("✅ Settings Storage", "Save your preferences and settings")
        ]
        
        for i, (title_text, desc) in enumerate(permissions):
            item_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
            item_frame.pack(pady=10, padx=20, fill="x")
            
            item_title = ctk.CTkLabel(
                item_frame,
                text=title_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=config.COLORS["success"],
                anchor="w"
            )
            item_title.pack(anchor="w")
            
            item_desc = ctk.CTkLabel(
                item_frame,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color=config.COLORS["text_secondary"],
                anchor="w"
            )
            item_desc.pack(anchor="w")
        
        # Note
        note = ctk.CTkLabel(
            content,
            text="💡 Your privacy is protected. No data is collected or shared.",
            font=ctk.CTkFont(size=12),
            text_color=config.COLORS["warning"]
        )
        note.pack(pady=(0, 20))
        
        # Navigation
        self.create_navigation(show_back=True, next_text="Continue →")
    
    def create_test_step(self):
        """Test wallpaper functionality"""
        # Title
        title = ctk.CTkLabel(
            self.container,
            text="🎨 Let's Test!",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=config.COLORS["primary"]
        )
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Content
        content = ctk.CTkFrame(self.container, fg_color=config.COLORS["bg_medium"], corner_radius=20)
        content.grid(row=1, column=0, sticky="nsew", pady=20)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        
        # Info
        info = ctk.CTkLabel(
            content,
            text="Let's generate your first AI wallpaper!\n\nClick the button below to create a beautiful test wallpaper.",
            font=ctk.CTkFont(size=14),
            text_color=config.COLORS["text_secondary"],
            justify="center"
        )
        info.grid(row=0, column=0, pady=(30, 20))
        
        # Test button frame
        test_frame = ctk.CTkFrame(content, fg_color="transparent")
        test_frame.grid(row=1, column=0)
        
        # Test button
        self.test_btn = ctk.CTkButton(
            test_frame,
            text="🎨 Generate Test Wallpaper",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=60,
            width=300,
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            corner_radius=15,
            command=self.test_wallpaper
        )
        self.test_btn.pack(pady=20)
        
        # Status label
        self.test_status = ctk.CTkLabel(
            test_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_secondary"]
        )
        self.test_status.pack()
        
        # Progress
        self.test_progress = ctk.CTkProgressBar(test_frame, width=300)
        self.test_progress.pack(pady=10)
        self.test_progress.set(0)
        self.test_progress.pack_forget()
        
        # Navigation
        self.create_navigation(show_back=True, next_text="Finish Setup →", next_state="disabled")
    
    def test_wallpaper(self):
        """Test wallpaper generation"""
        self.test_btn.configure(state="disabled")
        self.test_status.configure(text="⟳ Generating wallpaper...", text_color=config.COLORS["primary"])
        self.test_progress.pack()
        self.test_progress.start()
        
        def generate():
            try:
                # Get screen resolution
                width, height = WallpaperManager.get_screen_resolution()
                
                # Generate test wallpaper
                client = PollinationsClient()
                image_path = client.generate_and_save(
                    prompt="Beautiful serene landscape at golden hour, mountains, lake reflection, peaceful atmosphere, 8k, photorealistic",
                    width=width,
                    height=height
                )
                
                if image_path:
                    # Set wallpaper
                    if WallpaperManager.set_wallpaper(image_path, show_error_dialog=True):
                        self.after(0, self.test_success)
                    else:
                        self.after(0, self.test_failed, "Failed to set wallpaper - check permissions")
                else:
                    self.after(0, self.test_failed, "Failed to generate image")
                    
            except Exception as e:
                self.after(0, self.test_failed, str(e))
        
        import threading
        threading.Thread(target=generate, daemon=True).start()
    
    def test_success(self):
        """Handle successful test"""
        self.test_progress.stop()
        self.test_progress.pack_forget()
        self.test_status.configure(
            text="✅ Success! Your wallpaper has been changed!",
            text_color=config.COLORS["success"]
        )
        self.test_btn.configure(text="✓ Test Complete", state="disabled")
        
        # Enable next button
        self.next_btn.configure(state="normal")
    
    def test_failed(self, error):
        """Handle failed test"""
        self.test_progress.stop()
        self.test_progress.pack_forget()
        self.test_status.configure(
            text=f"⚠ Error: {error}",
            text_color=config.COLORS["danger"]
        )
        self.test_btn.configure(text="🔄 Try Again", state="normal")
    
    def create_complete_step(self):
        """Setup complete"""
        # Title
        title = ctk.CTkLabel(
            self.container,
            text="🎉 All Set!",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=config.COLORS["success"]
        )
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Content
        content = ctk.CTkFrame(self.container, fg_color=config.COLORS["bg_medium"], corner_radius=20)
        content.grid(row=1, column=0, sticky="nsew", pady=20)
        
        # Success icon
        icon = ctk.CTkLabel(
            content,
            text="✨",
            font=ctk.CTkFont(size=80)
        )
        icon.pack(pady=(40, 20))
        
        # Message
        msg = ctk.CTkLabel(
            content,
            text="Setup Complete!\n\nYou're ready to transform your desktop with\nstunning AI-generated wallpapers.",
            font=ctk.CTkFont(size=16),
            text_color=config.COLORS["text_primary"],
            justify="center"
        )
        msg.pack(pady=20)
        
        # Tips
        tips_frame = ctk.CTkFrame(content, fg_color=config.COLORS["bg_light"], corner_radius=15)
        tips_frame.pack(pady=20, padx=40, fill="x")
        
        tips = [
            "💡 Try different generation modes in Settings",
            "⏰ Enable Auto-Change for automatic updates",
            "🎨 Create custom prompts for unique wallpapers"
        ]
        
        for tip in tips:
            tip_label = ctk.CTkLabel(
                tips_frame,
                text=tip,
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_secondary"],
                anchor="w"
            )
            tip_label.pack(pady=8, padx=20, anchor="w")
        
        # Navigation
        self.create_navigation(next_text="Start Using PolliPaper →", is_final=True)
    
    def create_navigation(self, show_back=False, next_text="Next", next_state="normal", is_final=False):
        """Create navigation buttons"""
        nav_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        nav_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        nav_frame.grid_columnconfigure(1, weight=1)
        
        if show_back:
            back_btn = ctk.CTkButton(
                nav_frame,
                text="← Back",
                font=ctk.CTkFont(size=14),
                width=120,
                height=40,
                fg_color=config.COLORS["bg_light"],
                hover_color=config.COLORS["border"],
                command=lambda: self.show_step(self.current_step - 1)
            )
            back_btn.grid(row=0, column=0, sticky="w")
        
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text=next_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,
            height=40,
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            state=next_state,
            command=self.complete if is_final else lambda: self.show_step(self.current_step + 1)
        )
        self.next_btn.grid(row=0, column=2, sticky="e")
    
    def complete(self):
        """Complete setup"""
        self.setup_complete = True
        self.destroy()
