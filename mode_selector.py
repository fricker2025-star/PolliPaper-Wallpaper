"""Revolutionary Mode Selector - Card-Based Visual Selection"""
import customtkinter as ctk
import config
from assets import IconManager

class VisualModeSelector(ctk.CTkFrame):
    """Never-before-seen card-based mode selector with categories"""
    
    # Mode categories with visual indicators
    MODE_CATEGORIES = {
        "CREATIVE": {
            "aesthetic": {"icon": "aesthetic", "color": "#ec4899", "desc": "Aesthetic Vibes"},
            "abstract": {"icon": "abstract", "color": "#8b5cf6", "desc": "Abstract Art"},
            "fantasy": {"icon": "fantasy", "color": "#a855f7", "desc": "Fantasy Worlds"}
        },
        "NATURAL": {
            "time_based": {"icon": "time_based", "color": "#f59e0b", "desc": "Time of Day"},
            "weather_based": {"icon": "weather_based", "color": "#3b82f6", "desc": "Weather Reactive"},
            "nature": {"icon": "nature", "color": "#10b981", "desc": "Nature Focus"}
        },
        "FUTURISTIC": {
            "space": {"icon": "space", "color": "#6366f1", "desc": "Space & Cosmos"},
            "cyberpunk": {"icon": "cyberpunk", "color": "#ec4899", "desc": "Cyberpunk"},
        },
        "DYNAMIC": {
            "music_based": {"icon": "music_based", "color": "#f472b6", "desc": "Music Reactive"},
            "manual": {"icon": "manual", "color": "#94a3b8", "desc": "Manual Mode"}
        }
    }
    
    def __init__(self, parent, current_mode="time_based", callback=None):
        super().__init__(parent, fg_color="transparent")
        self.current_mode = current_mode
        self.callback = callback
        self.popup = None
        
        # Create trigger button
        self.create_trigger()
    
    def create_trigger(self):
        """Create the clickable trigger button"""
        # Get current mode info
        mode_info = self.get_mode_info(self.current_mode)
        
        # Create professional trigger button with mode icon
        icon_img = IconManager.get_icon(mode_info['icon'], size=20, color="white")
        self.trigger = ctk.CTkButton(
            self,
            text=f"  {mode_info['desc'].upper()}",
            image=icon_img,
            compound="left",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=45,
            fg_color=config.COLORS["bg_light"],
            hover_color=config.COLORS["primary_dark"],
            border_width=1,
            border_color=config.COLORS["border_light"],
            corner_radius=8,
            anchor="center",
            command=self.toggle_popup
        )
        self.trigger.pack(fill="x")
        
        # Add a small chevron on the right if needed, but compound="left" already uses the image slot.
        # The dropdown indicator is handled by the SVG icon in the trigger button.
    
    def get_mode_info(self, mode_key):
        """Get visual info for a mode"""
        for category, modes in self.MODE_CATEGORIES.items():
            if mode_key in modes:
                return modes[mode_key]
        return {"icon": "palette", "color": "#8b5cf6", "desc": "Unknown"}
    
    def toggle_popup(self):
        """Show/hide the visual mode selector popup"""
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            self.popup = None
        else:
            self.show_popup()
    
    def show_popup(self):
        """Display the revolutionary card-based selector"""
        # Get position
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 5
        
        # Create popup window
        self.popup = ctk.CTkToplevel(self)
        self.popup.withdraw()
        self.popup.overrideredirect(True)
        self.popup.configure(fg_color=config.COLORS["bg_dark"])
        
        # Main container with border
        container = ctk.CTkFrame(
            self.popup,
            fg_color=config.COLORS["bg_card"],
            border_width=2,
            border_color=config.COLORS["border"],
            corner_radius=12
        )
        container.pack(padx=0, pady=0, fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(container, fg_color=config.COLORS["bg_dark"], corner_radius=0, height=50)
        header.pack(fill="x", padx=2, pady=(2, 10))
        header.pack_propagate(False)
        
        lightning_icon = IconManager.get_icon("lightning", size=18, color=config.COLORS["primary"])
        header_title = ctk.CTkLabel(
            header,
            text=" SELECT GENERATION MODE",
            image=lightning_icon,
            compound="left",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        )
        header_title.pack(pady=15)
        
        # Scrollable content
        scroll = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent",
            width=420,
            height=400,
            corner_radius=0
        )
        scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Create category sections
        for category, modes in self.MODE_CATEGORIES.items():
            self.create_category_section(scroll, category, modes)
        
        # Position and show
        self.popup.geometry(f"450x500+{x}+{y}")
        self.popup.deiconify()
        self.popup.lift()
        self.popup.focus_force()
        
        # Click outside to close
        self.popup.bind("<FocusOut>", lambda e: self.close_popup())
    
    def create_category_section(self, parent, category_name, modes):
        """Create a category section with mode cards"""
        # Category header
        cat_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cat_frame.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(
            cat_frame,
            text=category_name,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=config.COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w", padx=5)
        
        # Divider
        ctk.CTkFrame(
            cat_frame,
            fg_color=config.COLORS["divider"],
            height=1
        ).pack(fill="x", pady=5)
        
        # Mode cards
        for mode_key, mode_info in modes.items():
            self.create_mode_card(parent, mode_key, mode_info)
    
    def create_mode_card(self, parent, mode_key, mode_info):
        """Create a clickable mode card"""
        is_active = (mode_key == self.current_mode)
        
        # Card container
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["primary"] if is_active else config.COLORS["bg_medium"],
            border_width=2 if is_active else 1,
            border_color=config.COLORS["accent_gold"] if is_active else config.COLORS["border_light"],
            corner_radius=8,
            cursor="hand2"
        )
        card.pack(fill="x", pady=3)
        
        # Card content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=10)
        
        # Icon + Name
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        
        mode_icon = IconManager.get_icon(mode_info['icon'], size=20, color=config.COLORS["primary"] if is_active else "white")
        ctk.CTkLabel(
            left,
            text=f"  {mode_info['desc']}",
            image=mode_icon,
            compound="left",
            font=ctk.CTkFont(size=13, weight="bold" if is_active else "normal"),
            text_color=config.COLORS["text_primary"],
            anchor="w"
        ).pack(side="left")
        
        # Active indicator
        if is_active:
            check_icon = IconManager.get_icon("check", size=16, color=config.COLORS["accent_gold"])
            ctk.CTkLabel(
                content,
                text="",
                image=check_icon
            ).pack(side="right")
        
        # Hover effect
        def on_enter(e):
            if not is_active:
                card.configure(
                    fg_color=config.COLORS["hover_overlay"],
                    border_color=config.COLORS["border"]
                )
        
        def on_leave(e):
            if not is_active:
                card.configure(
                    fg_color=config.COLORS["bg_medium"],
                    border_color=config.COLORS["border_light"]
                )
        
        def on_click(e):
            self.select_mode(mode_key, mode_info)
        
        # Bind events
        for widget in [card, content, left]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
    
    def select_mode(self, mode_key, mode_info):
        """Handle mode selection"""
        self.current_mode = mode_key
        
        # Update trigger button with new icon and text
        mode_icon = IconManager.get_icon(mode_info['icon'], size=20, color="white")
        self.trigger.configure(
            text=f"  {mode_info['desc'].upper()}",
            image=mode_icon
        )
        
        # Callback
        if self.callback:
            self.callback(mode_key)
        
        # Close popup
        self.close_popup()
    
    def close_popup(self):
        """Close the popup"""
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            self.popup = None
    
    def get_mode(self):
        """Get current mode key"""
        return self.current_mode
    
    def set_mode(self, mode_key):
        """Set mode programmatically"""
        mode_info = self.get_mode_info(mode_key)
        self.current_mode = mode_key
        mode_icon = IconManager.get_icon(mode_info['icon'], size=20, color="white")
        self.trigger.configure(
            text=f"  {mode_info['desc'].upper()}",
            image=mode_icon
        )
