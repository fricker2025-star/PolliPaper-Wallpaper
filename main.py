"""Revolutionary Professional UI - Visual Command Center"""
import customtkinter as ctk
import threading
import time
import random
import os
import traceback
from pathlib import Path
import sys
from PIL import Image
from assets import IconManager

import config
from api_client import PollinationsClient
from system_utils import (
    WallpaperManager, TimeDetector, WeatherDetector, 
    MusicAnalyzer, LocationDetector, SettingsManager, GameDetector
)
from startup_manager import StartupManager
from tray_manager import TrayManager

class RevolutionaryPolliPaperApp(ctk.CTk):
    """Revolutionary Visual Command Center for Wallpaper Generation"""
    
    # Mode configurations with professional styling
    MODES = config.MODE_THEMES
    
    def __init__(self):
        super().__init__()
        
        # Initialize systems
        self.settings = SettingsManager.load_settings()
        self.api_client = PollinationsClient()
        
        # Update API client with saved settings
        if self.settings.get("api_key") or self.settings.get("model"):
            self.api_client.update_config(
                api_key=self.settings.get("api_key"),
                model=self.settings.get("model", "flux")
            )
        
        self.wallpaper_manager = WallpaperManager()
        self.music_analyzer = MusicAnalyzer()
        
        # State
        self.current_mode = self.settings.get("mode", "time_based")
        self.is_generating = False
        self.auto_change_active = False
        self.is_closing = False
        self.current_wallpaper = None
        
        # Store mode cards for easy updates
        self.mode_cards = {}
        
        # Slide-in panel state
        self.current_panel = None
        
        # Setup window
        self.setup_window()
        
        # Create revolutionary UI
        self.create_revolutionary_ui()
        
        # Start system tray
        self.tray_manager = TrayManager(self)
        self.tray_manager.run()
        
        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Keyboard shortcuts
        self.bind("<Return>", lambda e: self.generate_wallpaper())  # Enter to generate
        self.bind("<space>", lambda e: self.generate_wallpaper())   # Space to generate
        self.bind("<Escape>", lambda e: self.minimize_to_tray())    # Esc to minimize
        self.bind("<Control-q>", lambda e: self.cleanup_and_exit()) # Ctrl+Q to quit
    
    def setup_window(self):
        """Setup professional window - CENTERED"""
        self.title("PolliPaper - AI Wallpaper Engine")
        
        # Set window icon
        try:
            import os
            icon_ico = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            icon_png = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            
            if os.path.exists(icon_ico):
                self.iconbitmap(icon_ico)
            elif os.path.exists(icon_png):
                from PIL import Image, ImageTk
                img = Image.open(icon_png)
                photo = ImageTk.PhotoImage(img)
                self.iconphoto(False, photo)
        except Exception as e:
            print(f"[WINDOW] Error setting icon: {e}")
        
        # Set size first
        window_width = 1400
        window_height = 900
        
        # Calculate center position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set geometry with position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(1200, 800)
        self.configure(fg_color=config.COLORS["bg_app"])
    
    def create_revolutionary_ui(self):
        """Create revolutionary visual command center"""
        # Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header (Top)
        self.create_header(main)
        
        # Footer (Bottom)
        self.create_footer(main)
        
        # Side Panel (Right) - Pack this before the expandable grid
        self.create_side_panel(main)
        
        # Mode Grid (Left/Center) - This will fill the remaining space
        self.create_mode_grid(main)
    
    def create_header(self, parent):
        """Create professional header"""
        header = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        header.pack(fill="x", pady=(0, 30))
        header.pack_propagate(False)
        
        # Left: Branding
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        
        ctk.CTkLabel(
            left,
            text="POLLIPAPER",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=config.COLORS["primary"]
        ).pack(anchor="w")
        
        # Gradient Underline for Header (New)
        underline = ctk.CTkFrame(
            left,
            height=4,
            fg_color="transparent"
        )
        underline.pack(fill="x", pady=(2, 0))
        
        grad_frame = ctk.CTkFrame(underline, height=4, fg_color=config.COLORS["secondary"], corner_radius=2)
        grad_frame.place(relx=0, rely=0, relwidth=0.4)
        
        grad_frame2 = ctk.CTkFrame(underline, height=4, fg_color=config.COLORS["primary"], corner_radius=2)
        grad_frame2.place(relx=0.42, rely=0, relwidth=0.2)
        
        ctk.CTkLabel(
            left,
            text="AI Wallpaper Generation Platform",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_muted"]
        ).pack(anchor="w")
        
        # Center: Menu buttons
        menu_frame = ctk.CTkFrame(header, fg_color="transparent")
        menu_frame.pack(side="right", padx=(0, 30))
        
        # Help button
        self.help_icon = IconManager.get_icon("help", size=16, color="white")
        ctk.CTkButton(
            menu_frame,
            text="  Help",
            image=self.help_icon,
            compound="left",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=80,
            height=35,
            fg_color=config.COLORS["bg_light"],
            hover_color=config.COLORS["hover_overlay"],
            corner_radius=8,
            command=self.show_help
        ).pack(side="left", padx=3)
        
        # Settings button
        self.settings_icon = IconManager.get_icon("settings", size=16, color="white")
        ctk.CTkButton(
            menu_frame,
            text="  Settings",
            image=self.settings_icon,
            compound="left",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=90,
            height=35,
            fg_color=config.COLORS["bg_light"],
            hover_color=config.COLORS["hover_overlay"],
            corner_radius=8,
            command=self.show_settings
        ).pack(side="left", padx=3)
        
        # Support button
        self.support_icon = IconManager.get_icon("support", size=16, color="white")
        ctk.CTkButton(
            menu_frame,
            text="  Support",
            image=self.support_icon,
            compound="left",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=90,
            height=35,
            fg_color=config.COLORS["secondary"],
            hover_color=config.COLORS["secondary_hover"],
            corner_radius=8,
            command=self.show_support
        ).pack(side="left", padx=3)
        
        # Right: Status
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")
        
        self.ready_icon = IconManager.get_icon("status", size=12, color=config.COLORS["success"])
        self.status_indicator = ctk.CTkLabel(
            right,
            text="  READY",
            image=self.ready_icon,
            compound="left",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=config.COLORS["success"]
        )
        self.status_indicator.pack(anchor="e")
        
        self.status_text = ctk.CTkLabel(
            right,
            text="Select a mode to begin",
            font=ctk.CTkFont(size=12),
            text_color=config.COLORS["text_secondary"]
        )
        self.status_text.pack(anchor="e")
    
    def create_mode_grid(self, parent):
        """Create revolutionary mode selection grid"""
        # Container
        grid_container = ctk.CTkFrame(parent, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, side="left")
        
        # Title
        ctk.CTkLabel(
            grid_container,
            text="SELECT GENERATION MODE",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=config.COLORS["primary"],
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Grid frame
        grid = ctk.CTkFrame(grid_container, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        
        # Configure grid (4 columns x 3 rows)
        for i in range(4):
            grid.columnconfigure(i, weight=1, uniform="col")
        for i in range(3):
            grid.rowconfigure(i, weight=1, uniform="row")
        
        # Create mode cards
        row = 0
        col = 0
        for mode_key, mode_info in self.MODES.items():
            self.create_mode_card(grid, mode_key, mode_info, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
    
    def create_mode_card(self, parent, mode_key, mode_info, row, col):
        """Create a professional mode card"""
        is_active = (mode_key == self.current_mode)
        
        # Card frame
        card = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_card"],
            corner_radius=16,
            border_width=2 if is_active else 1,
            border_color=config.COLORS["accent_gold"] if is_active else config.COLORS["border_light"],
            cursor="hand2"
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        # Store reference to card
        self.mode_cards[mode_key] = {
            'card': card,
            'is_active': is_active
        }
        
        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Icon with Gradient Background (New)
        icon_bg = ctk.CTkFrame(
            content,
            fg_color=mode_info["gradient"][0],
            width=80,
            height=80,
            corner_radius=40
        )
        icon_bg.pack(pady=(5, 10))
        icon_bg.pack_propagate(False)

        # SVG Icon
        mode_icon = IconManager.get_icon(mode_key, size=40, color="white")
        icon = ctk.CTkLabel(
            icon_bg,
            text="",
            image=mode_icon
        )
        icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Store icon reference
        self.mode_cards[mode_key]['icon_label'] = icon
        
        # Name
        name = ctk.CTkLabel(
            content,
            text=mode_info["name"].upper(),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=config.COLORS["text_primary"]
        )
        name.pack(pady=(0, 2))
        
        # Description
        desc = ctk.CTkLabel(
            content,
            text=mode_info["desc"],
            font=ctk.CTkFont(size=11),
            text_color=config.COLORS["text_muted"]
        )
        desc.pack()
        
        # Active indicator (always create, show/hide as needed)
        indicator = ctk.CTkFrame(
            card,
            fg_color=config.COLORS["accent_gold"],
            height=3,
            corner_radius=0
        )
        if is_active:
            indicator.place(relx=0, rely=1, relwidth=1, anchor="sw")
        
        # Store indicator reference
        self.mode_cards[mode_key]['indicator'] = indicator
        self.mode_cards[mode_key]['icon_bg'] = icon_bg
        
        # Hover effects - check stored active state
        def on_enter(e):
            if not self.mode_cards[mode_key]['is_active']:
                card.configure(
                    fg_color=config.COLORS["hover_overlay"],
                    border_color=config.COLORS["primary"]
                )
                icon_bg.configure(fg_color=mode_info["gradient"][1])
            
            # Update description label on hover
            if hasattr(self, 'mode_desc_label'):
                self.mode_desc_label.configure(
                    text=mode_info["desc"],
                    text_color=config.COLORS["text_primary"]
                )
        
        def on_leave(e):
            if not self.mode_cards[mode_key]['is_active']:
                card.configure(
                    fg_color=config.COLORS["bg_card"],
                    border_color=config.COLORS["border_light"]
                )
                icon_bg.configure(fg_color=mode_info["gradient"][0])
            
            # Reset description label to current mode's desc
            if hasattr(self, 'mode_desc_label'):
                current_info = self.MODES[self.current_mode]
                self.mode_desc_label.configure(
                    text=current_info["desc"],
                    text_color=config.COLORS["text_muted"]
                )
        
        def on_click(e):
            # Visual feedback - quick flash
            card.configure(fg_color=config.COLORS["primary"])
            card.after(100, lambda: card.configure(
                fg_color=config.COLORS["bg_card"]
            ))
            self.select_mode(mode_key)
        
        def on_double_click(e):
            # Double click to select and generate immediately
            self.select_mode(mode_key)
            self.generate_wallpaper()
        
        # Bind events to all widgets
        for widget in [card, content, icon, name, desc, icon_bg]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            widget.bind("<Double-Button-1>", on_double_click)
    
    def add_tooltip(self, widget, text):
        """Add hover tooltip to a widget using the mode description label"""
        def on_enter(e):
            if hasattr(self, 'mode_desc_label'):
                self.mode_desc_label.configure(
                    text=text,
                    text_color=config.COLORS["text_primary"]
                )
        
        def on_leave(e):
            if hasattr(self, 'mode_desc_label'):
                current_info = self.MODES[self.current_mode]
                self.mode_desc_label.configure(
                    text=current_info["desc"],
                    text_color=config.COLORS["text_muted"]
                )
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def create_side_panel(self, parent):
        """Create professional side control panel"""
        panel = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_dark"],
            width=350,
            corner_radius=20,
            border_width=1,
            border_color=config.COLORS["border"]
        )
        panel.pack(side="right", fill="y", padx=(20, 0))
        panel.pack_propagate(False)
        
        # Title
        lightning_icon = IconManager.get_icon("lightning", size=20, color=config.COLORS["primary"])
        self.quick_actions_header = ctk.CTkLabel(
            panel,
            text="  QUICK ACTIONS",
            image=lightning_icon,
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        )
        self.quick_actions_header.pack(padx=25, pady=(25, 20), anchor="w")

        # Preview Area (New)
        self.preview_frame = ctk.CTkFrame(
            panel,
            fg_color=config.COLORS["bg_app"],
            height=180,
            corner_radius=12,
            border_width=1,
            border_color=config.COLORS["border"]
        )
        self.preview_frame.pack(padx=25, pady=(0, 20), fill="x")
        self.preview_frame.pack_propagate(False)

        # Mode description label (New)
        self.mode_desc_label = ctk.CTkLabel(
            panel,
            text=self.MODES[self.current_mode]["desc"],
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=config.COLORS["text_muted"],
            wraplength=300,
            justify="left"
        )
        self.mode_desc_label.pack(padx=25, pady=(0, 20), anchor="w")

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="AI VISION READY\n\nWaiting for generation...",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=config.COLORS["text_muted"],
            justify="center"
        )
        self.preview_label.pack(expand=True, fill="both")
        
        # Add a subtle hint icon to preview
        hint_icon = IconManager.get_icon("sparkles", size=32, color=config.COLORS["bg_medium"])
        hint_label = ctk.CTkLabel(self.preview_frame, text="", image=hint_icon)
        hint_label.place(relx=0.5, rely=0.35, anchor="center")

        # Custom Prompt Input (Hidden by default)
        self.prompt_frame = ctk.CTkFrame(panel, fg_color="transparent")
        
        ctk.CTkLabel(
            self.prompt_frame,
            text="CUSTOM PROMPT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=config.COLORS["text_muted"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.prompt_entry = ctk.CTkTextbox(
            self.prompt_frame,
            height=100,
            corner_radius=12,
            border_width=1,
            border_color=config.COLORS["border"],
            fg_color=config.COLORS["bg_app"],
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_primary"]
        )
        self.prompt_entry.pack(fill="x")
        
        # Placeholder text
        placeholder = "Enter your creative prompt here..."
        self.prompt_entry.insert("1.0", placeholder)
        
        def on_focus_in(e):
            if self.prompt_entry.get("1.0", "end-1c") == placeholder:
                self.prompt_entry.delete("1.0", "end")
        
        def on_focus_out(e):
            if not self.prompt_entry.get("1.0", "end-1c").strip():
                self.prompt_entry.insert("1.0", placeholder)
                
        self.prompt_entry.bind("<FocusIn>", on_focus_in)
        self.prompt_entry.bind("<FocusOut>", on_focus_out)

        # Show prompt frame if manual mode is active
        if self.current_mode == "manual":
            self.prompt_frame.pack(padx=25, pady=(0, 20), fill="x")

        # Generate Button (HUGE)
        self.generate_icon = IconManager.get_icon("generate", size=24, color="white")
        self.generate_btn = ctk.CTkButton(
            panel,
            text="  GENERATE NOW",
            image=self.generate_icon,
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=80,
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            corner_radius=12,
            border_width=2,
            border_color=config.COLORS["accent_gold"],
            command=self.generate_wallpaper
        )
        self.generate_btn.pack(padx=25, pady=(0, 10), fill="x")
        self.add_tooltip(self.generate_btn, "Instantly generate and apply a new wallpaper based on your current mode and settings.")
        
        # History Button (New)
        history_icon = IconManager.get_icon("refresh", size=16, color=config.COLORS["text_secondary"])
        self.history_btn = ctk.CTkButton(
            panel,
            text="  View Generation History",
            image=history_icon,
            compound="left",
            font=ctk.CTkFont(size=12),
            height=35,
            fg_color="transparent",
            hover_color=config.COLORS["bg_medium"],
            text_color=config.COLORS["text_secondary"],
            command=self.show_history
        )
        self.history_btn.pack(padx=25, pady=(0, 15), anchor="w")
        self.add_tooltip(self.history_btn, "Review and re-apply wallpapers from your previous generations.")
        
        # Auto-change
        ctk.CTkLabel(
            panel,
            text="AUTO-CHANGE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=config.COLORS["text_muted"]
        ).pack(padx=25, pady=(15, 8), anchor="w")
        
        self.play_icon = IconManager.get_icon("play", size=20, color="white")
        self.stop_icon = IconManager.get_icon("stop", size=20, color="white")
        self.auto_btn = ctk.CTkButton(
            panel,
            text="  START AUTO-CHANGE",
            image=self.play_icon,
            compound="left",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=55,
            fg_color=config.COLORS["secondary"],
            hover_color=config.COLORS["secondary_hover"],
            corner_radius=10,
            command=self.toggle_auto_change
        )
        self.auto_btn.pack(padx=25, pady=(0, 10), fill="x")
        self.add_tooltip(self.auto_btn, "Automatically rotate your wallpaper at your chosen interval.")
        
        # Interval slider
        interval_frame = ctk.CTkFrame(panel, fg_color="transparent")
        interval_frame.pack(padx=25, pady=(10, 20), fill="x")
        
        self.interval_var = ctk.IntVar(value=self.settings.get("auto_change_interval", 3600) // 60)
        
        ctk.CTkLabel(
            interval_frame,
            text="Interval (minutes)",
            font=ctk.CTkFont(size=11),
            text_color=config.COLORS["text_secondary"]
        ).pack(anchor="w")
        
        self.interval_slider = ctk.CTkSlider(
            interval_frame,
            from_=1,
            to=240,
            variable=self.interval_var,
            button_color=config.COLORS["primary"],
            button_hover_color=config.COLORS["primary_hover"],
            progress_color=config.COLORS["primary"]
        )
        self.interval_slider.pack(fill="x", pady=8)
        self.add_tooltip(self.interval_slider, "Set how often (1-240 min) PolliPaper should automatically generate a new wallpaper.")
        
        self.interval_label = ctk.CTkLabel(
            interval_frame,
            text=f"{self.interval_var.get()} min",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        )
        self.interval_label.pack(anchor="w")
        self.interval_var.trace_add("write", lambda *args: self.interval_label.configure(text=f"{self.interval_var.get()} min"))
    
    def create_footer(self, parent):
        """Create status footer"""
        footer = ctk.CTkFrame(
            parent,
            fg_color=config.COLORS["bg_dark"],
            height=60,
            corner_radius=12
        )
        footer.pack(fill="x", side="bottom", pady=(20, 0))
        footer.pack_propagate(False)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(
            footer,
            mode="indeterminate",
            height=3,
            progress_color=config.COLORS["gradient_pink"]
        )
        self.progress.place(relx=0, rely=0, relwidth=1)
        self.progress.place_forget()
        
        # Status info
        info_frame = ctk.CTkFrame(footer, fg_color="transparent")
        info_frame.pack(expand=True)
        
        # Current mode display
        mode_info = self.MODES[self.current_mode]
        self.footer_icon = IconManager.get_icon(self.current_mode, size=20, color=config.COLORS["primary"])
        self.footer_mode = ctk.CTkLabel(
            info_frame,
            text=f"  {mode_info['name']}",
            image=self.footer_icon,
            compound="left",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=config.COLORS["text_primary"]
        )
        self.footer_mode.pack(side="left", padx=20)
        
        # Version
        ctk.CTkLabel(
            info_frame,
            text=f"v{config.APP_VERSION}",
            font=ctk.CTkFont(size=11),
            text_color=config.COLORS["text_muted"]
        ).pack(side="right", padx=20)
    
    def _animate_loading(self):
        """Animate the status indicator icon while generating"""
        if not self.is_generating:
            return
            
        # Update dots in status indicator
        current_text = self.status_indicator.cget("text")
        if "..." in current_text:
            new_text = "  GENERATING"
        elif ".." in current_text:
            new_text = "  GENERATING..."
        elif "." in current_text:
            new_text = "  GENERATING.."
        else:
            new_text = "  GENERATING."
            
        self.status_indicator.configure(text=new_text)
        
        # Schedule next frame
        if self.is_generating:
            self.after(500, self._animate_loading)

    def quick_generate(self, mode_key):
        """Quickly switch mode and generate from tray"""
        if mode_key in self.MODES:
            self.select_mode(mode_key)
            self.generate_wallpaper()

    def select_mode(self, mode_key):
        """Update selected mode with dynamic UI tinting"""
        print(f"[MODE] Selected: {mode_key}")
        
        # Don't do anything if already selected
        if mode_key == self.current_mode:
            return
            
        old_mode = self.current_mode
        self.current_mode = mode_key
        
        # Update settings
        self.settings["mode"] = mode_key
        SettingsManager.save_settings(self.settings)
        
        # Get theme info
        theme = self.MODES.get(mode_key, self.MODES["manual"])
        accent_color = theme.get("accent", config.COLORS["primary"])
        
        # Update old card (deactivate)
        if old_mode in self.mode_cards:
            old_card_data = self.mode_cards[old_mode]
            old_card_data['card'].configure(
                border_width=1,
                border_color=config.COLORS["border_light"]
            )
            old_card_data['indicator'].place_forget()
            old_card_data['icon_bg'].configure(fg_color=self.MODES[old_mode]["gradient"][0])
            old_card_data['is_active'] = False
        
        # Update new card (activate)
        if mode_key in self.mode_cards:
            new_card_data = self.mode_cards[mode_key]
            new_card_data['card'].configure(
                border_width=2,
                border_color=accent_color
            )
            new_card_data['indicator'].configure(fg_color=accent_color)
            new_card_data['indicator'].place(relx=0, rely=1, relwidth=1, anchor="sw")
            new_card_data['icon_bg'].configure(fg_color=self.MODES[mode_key]["gradient"][1])
            new_card_data['is_active'] = True

        # Update dynamic UI tinting
        self.update_ui_theme(mode_key)
        
        # Show/Hide prompt frame for manual mode
        if mode_key == "manual":
            self.prompt_frame.pack(padx=25, pady=(0, 20), fill="x", before=self.generate_btn)
            # Pick a random example for the placeholder if it's currently the default
            import random
            examples = [
                "A futuristic neon cyberpunk city in the rain",
                "A peaceful zen garden with cherry blossoms",
                "Epic space nebula with vibrant cosmic dust",
                "Minimalist mountain landscape at sunset",
                "Digital art of a magical forest with fireflies"
            ]
            current = self.prompt_entry.get("1.0", "end-1c").strip()
            if not current or current == "Enter your creative prompt here...":
                self.prompt_entry.delete("1.0", "end")
                self.prompt_entry.insert("1.0", random.choice(examples))
        else:
            if hasattr(self, 'prompt_frame'):
                self.prompt_frame.pack_forget()
            
        # Update status and footer
        self.footer_icon = IconManager.get_icon(mode_key, size=20, color=accent_color)
        self.footer_mode.configure(
            text=f"  {mode_key.replace('_', ' ').title()}",
            image=self.footer_icon
        )
        self.status_text.configure(text=f"Mode: {mode_key.replace('_', ' ').title()} - {theme.get('desc', '')}")
        
        # Update description label
        if hasattr(self, 'mode_desc_label'):
            self.mode_desc_label.configure(text=theme.get('desc', ''))
        
    def update_ui_theme(self, mode_key):
        """Update application colors based on mode"""
        theme = self.MODES.get(mode_key, self.MODES["manual"])
        accent = theme.get("accent", config.COLORS["primary"])
        
        # Update main generate button
        if hasattr(self, 'generate_btn'):
            self.generate_btn.configure(
                fg_color=accent,
                hover_color=theme["gradient"][1],
                border_color=accent
            )
            
        # Update status indicator if ready
        if not self.is_generating:
            self.status_indicator.configure(text_color=accent)
            # Update status icon color
            self.ready_icon = IconManager.get_icon("status", size=12, color=accent)
            self.status_indicator.configure(image=self.ready_icon)

        # Update preview border
        if hasattr(self, 'preview_frame'):
            self.preview_frame.configure(border_color=accent)
            
        # Update quick actions header
        if hasattr(self, 'quick_actions_header'):
            self.quick_actions_header.configure(text_color=accent)
            # Update lightning icon color too
            self.lightning_icon = IconManager.get_icon("lightning", size=20, color=accent)
            self.quick_actions_header.configure(image=self.lightning_icon)

        # Update progress bar color
        if hasattr(self, 'progress'):
            self.progress.configure(progress_color=accent)
    
    def show_history(self):
        """Show history of generated wallpapers"""
        # Check if same panel is already open (toggle off)
        if self.current_panel and hasattr(self.current_panel, 'panel_type') and self.current_panel.panel_type == 'history':
            self.close_panel()
            return
        
        # Close any other open panel
        if self.current_panel:
            self.close_panel()
        
        # Create history panel
        panel = ctk.CTkFrame(
            self,
            fg_color=config.COLORS["bg_dark"],
            corner_radius=20,
            border_width=0
        )
        panel.place(relx=0.42, rely=0.02, relwidth=0.56, relheight=0.96)
        panel.panel_type = 'history'
        self.current_panel = panel
        
        # Header
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        history_icon = IconManager.get_icon("refresh", size=24, color=config.COLORS["primary"])
        ctk.CTkLabel(
            header,
            text="  Generation History",
            image=history_icon,
            compound="left",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(side="left")
        
        # Close button
        ctk.CTkButton(
            header,
            text="✕",
            width=35,
            height=35,
            fg_color="transparent",
            hover_color=config.COLORS["bg_medium"],
            text_color=config.COLORS["text_muted"],
            font=ctk.CTkFont(size=20),
            command=self.close_panel
        ).pack(side="right")
        
        # Scrollable container for history items
        scroll_frame = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent",
            scrollbar_button_color=config.COLORS["bg_medium"],
            scrollbar_button_hover_color=config.COLORS["primary"]
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Load history from outputs folder
        import os
        from PIL import Image
        
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        if not os.path.exists(outputs_dir):
            ctk.CTkLabel(scroll_frame, text="No generations found yet.", text_color=config.COLORS["text_muted"]).pack(pady=50)
            return
            
        # Get all images, sorted by date (newest first)
        files = [f for f in os.listdir(outputs_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(outputs_dir, x)), reverse=True)
        
        if not files:
            ctk.CTkLabel(scroll_frame, text="No generations found yet.", text_color=config.COLORS["text_muted"]).pack(pady=50)
            return
            
        for i, filename in enumerate(files):
            file_path = os.path.join(outputs_dir, filename)
            
            # History card
            card = ctk.CTkFrame(
                scroll_frame,
                fg_color=config.COLORS["bg_medium"],
                corner_radius=12,
                height=100
            )
            card.pack(fill="x", padx=20, pady=10)
            card.pack_propagate(False)
            
            # Thumbnail (async-ish load)
            try:
                img = Image.open(file_path)
                img.thumbnail((120, 80))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 80))
                
                thumb_label = ctk.CTkLabel(card, image=ctk_img, text="", corner_radius=8)
                thumb_label.pack(side="left", padx=10, pady=10)
            except Exception as e:
                print(f"[HISTORY] Error loading thumbnail: {e}")
            
            # Info and actions
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Filename/Date
            date_str = filename.split('_')[1] if '_' in filename else filename
            ctk.CTkLabel(
                info_frame,
                text=f"Wallpaper {i+1}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=config.COLORS["text_primary"]
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=date_str,
                font=ctk.CTkFont(size=11),
                text_color=config.COLORS["text_muted"]
            ).pack(anchor="w")
            
            # Apply button
            apply_btn = ctk.CTkButton(
                card,
                text="Apply",
                width=80,
                height=30,
                fg_color=config.COLORS["primary"],
                hover_color=config.COLORS["primary_hover"],
                command=lambda p=file_path: self.apply_historic_wallpaper(p)
            )
            apply_btn.pack(side="right", padx=20)

    def apply_historic_wallpaper(self, file_path):
        """Re-apply a wallpaper from history"""
        try:
            from tray_manager import WallpaperManager
            WallpaperManager.set_wallpaper(file_path)
            self.on_generation_success(file_path)
            self.status_text.configure(text="History wallpaper applied!")
            self.close_panel()
        except Exception as e:
            print(f"[HISTORY] Error applying: {e}")

    def show_help(self):
        """Show help slide-in panel"""
        # Check if same panel is already open (toggle off)
        if self.current_panel and hasattr(self.current_panel, 'panel_type') and self.current_panel.panel_type == 'help':
            self.close_panel()
            return
        
        # Close any other open panel
        if self.current_panel:
            self.close_panel()
        
        # Create modern panel with margins and shadow effect
        panel = ctk.CTkFrame(
            self,
            fg_color=config.COLORS["bg_dark"],
            corner_radius=20,
            border_width=0
        )
        # Position: right side with margins (60% width, margins all around)
        panel.place(relx=0.42, rely=0.02, relwidth=0.56, relheight=0.96)
        panel.panel_type = 'help'
        panel.bind("<Button-1>", lambda e: None)
        self.current_panel = panel
        
        # Bring to front with shadow effect
        panel.lift()
        self.current_panel = panel
        
        # Header with close button
        header = ctk.CTkFrame(panel, fg_color=config.COLORS["info"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        help_header_icon = IconManager.get_icon("help", size=24, color="white")
        ctk.CTkLabel(
            header,
            text="  HELP & SHORTCUTS",
            image=help_header_icon,
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)
        
        close_icon = IconManager.get_icon("close", size=20, color="white")
        ctk.CTkButton(
            header,
            text="",
            image=close_icon,
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#FF4444",
            command=self.close_panel
        ).pack(side="right", padx=20)
        
        # Scrollable content area
        content = ctk.CTkScrollableFrame(panel, fg_color=config.COLORS["bg_card"])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome section
        ctk.CTkLabel(
            content,
            text="Welcome to PolliPaper",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            content,
            text="Your AI-powered wallpaper generation companion",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_muted"]
        ).pack(pady=(0, 30))
        
        # Generation Modes section
        section_frame = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame,
            text="Generation Modes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        modes_help = [
            ("time_based", "Time of Day: Dynamic wallpapers matching current time"),
            ("weather_based", "Weather Live: Reacts to your local weather conditions"),
            ("music_based", "Music Sync: Visualizes your currently playing music"),
            ("gaming", "Game Sense: Detects your running game and adapts"),
            ("aesthetic", "Aesthetic: Trendy vaporwave and modern art styles"),
            ("nature", "Nature: Serene landscapes and natural beauty"),
            ("space", "Space: Cosmic scenes and celestial wonders"),
            ("abstract", "Abstract: Digital art patterns and shapes"),
            ("cyberpunk", "Cyberpunk: Neon-lit futuristic cityscapes"),
            ("fantasy", "Fantasy: Magical worlds and mythical scenes"),
            ("manual", "Custom: Your own creative prompts")
        ]
        
        for icon_name, text in modes_help:
            row = ctk.CTkFrame(section_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=2)
            
            icon = IconManager.get_icon(icon_name, size=16, color=config.COLORS["text_primary"])
            ctk.CTkLabel(
                row,
                text=f"  {text}",
                image=icon,
                compound="left",
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_primary"],
                justify="left"
            ).pack(side="left")
            
        # Add bottom padding
        ctk.CTkLabel(section_frame, text="", height=10).pack()
        
        # Keyboard shortcuts section
        section_frame2 = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        section_frame2.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame2,
            text="Keyboard Shortcuts",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        shortcuts = [
            ("Enter / Space: Generate wallpaper with selected mode"),
            ("Escape: Minimize to system tray"),
            ("Ctrl + Q: Quit application"),
            ("Double-click any mode: Quick generate")
        ]
        
        for text in shortcuts:
            row = ctk.CTkFrame(section_frame2, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=2)
            
            dot_icon = IconManager.get_icon("dot", size=10, color=config.COLORS["primary"])
            ctk.CTkLabel(
                row,
                text=f"  {text}",
                image=dot_icon,
                compound="left",
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_primary"]
            ).pack(side="left")

        # Add bottom padding
        ctk.CTkLabel(section_frame2, text="", height=10).pack()
        
        # Quick tips section
        section_frame3 = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        section_frame3.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame3,
            text="Quick Tips",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        tips = [
            "Use AUTO-CHANGE to refresh wallpapers automatically",
            "Set intervals from 1 to 240 minutes for auto-generation",
            "All wallpapers are saved to your Pictures folder",
            "Settings are saved automatically",
            "Minimize to tray to keep it running in background"
        ]
        
        for text in tips:
            row = ctk.CTkFrame(section_frame3, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=2)
            
            dot_icon = IconManager.get_icon("dot", size=10, color=config.COLORS["success"])
            ctk.CTkLabel(
                row,
                text=f"  {text}",
                image=dot_icon,
                compound="left",
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_primary"]
            ).pack(side="left")

        # Add bottom padding
        ctk.CTkLabel(section_frame3, text="", height=10).pack()
        
        # Footer
        ctk.CTkLabel(
            content,
            text="Made with Passion by the PolliPaper Team",
            font=ctk.CTkFont(size=12),
            text_color=config.COLORS["text_muted"]
        ).pack(pady=(30, 10))
    
    def show_settings(self):
        """Show settings slide-in panel"""
        # Check if same panel is already open (toggle off)
        if self.current_panel and hasattr(self.current_panel, 'panel_type') and self.current_panel.panel_type == 'settings':
            self.close_panel()
            return
        
        # Close any other open panel
        if self.current_panel:
            self.close_panel()
        
        # Create modern panel with margins and shadow effect
        panel = ctk.CTkFrame(
            self,
            fg_color=config.COLORS["bg_dark"],
            corner_radius=20,
            border_width=0
        )
        # Position: right side with margins (55% width)
        panel.place(relx=0.47, rely=0.02, relwidth=0.51, relheight=0.96)
        panel.panel_type = 'settings'
        panel.bind("<Button-1>", lambda e: None)
        self.current_panel = panel
        
        # Bring to front
        panel.lift()
        
        # Header with close button
        header = ctk.CTkFrame(panel, fg_color=config.COLORS["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        settings_icon = IconManager.get_icon("settings", size=24, color="white")
        ctk.CTkLabel(
            header,
            text="  SETTINGS",
            image=settings_icon,
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)
        
        close_icon = IconManager.get_icon("close", size=20, color="white")
        ctk.CTkButton(
            header,
            text="",
            image=close_icon,
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#FF4444",
            command=self.close_panel
        ).pack(side="right", padx=20)
        
        # Simple scrollable content
        container = ctk.CTkScrollableFrame(panel, fg_color=config.COLORS["bg_card"])
        container.pack(fill="both", expand=True)
        
        # Title
        container_icon = IconManager.get_icon("settings", size=24, color=config.COLORS["primary"])
        ctk.CTkLabel(
            container,
            text="  APPLICATION SETTINGS",
            image=container_icon,
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(pady=(10, 20))
        
        # Resolution setting
        res_frame = ctk.CTkFrame(container, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        res_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            res_frame,
            text="Wallpaper Resolution",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=15, pady=(15, 5), anchor="w")
        
        resolution_var = ctk.StringVar(value=self.settings.get("resolution", "1920x1080"))
        res_menu = ctk.CTkOptionMenu(
            res_frame,
            variable=resolution_var,
            values=config.SUPPORTED_RESOLUTIONS,
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["bg_light"],
            button_color=config.COLORS["primary"],
            corner_radius=8
        )
        res_menu.pack(padx=15, pady=(0, 15), fill="x")
        
        # Auto-start setting
        auto_frame = ctk.CTkFrame(container, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        auto_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            auto_frame,
            text="Startup Options",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=15, pady=(15, 10), anchor="w")
        
        auto_start_var = ctk.BooleanVar(value=self.settings.get("auto_start", False))
        ctk.CTkCheckBox(
            auto_frame,
            text="Start with Windows",
            variable=auto_start_var,
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"]
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # Enhance prompts setting
        enhance_frame = ctk.CTkFrame(container, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        enhance_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            enhance_frame,
            text="Generation Options",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=15, pady=(15, 10), anchor="w")
        
        enhance_var = ctk.BooleanVar(value=self.settings.get("enhance_prompts", True))
        ctk.CTkCheckBox(
            enhance_frame,
            text="Enhance prompts with variations",
            variable=enhance_var,
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"]
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # API Key & Model selection
        api_frame = ctk.CTkFrame(container, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        api_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            api_frame,
            text="Pollinations API (Optional)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=15, pady=(15, 5), anchor="w")
        
        api_key_var = ctk.StringVar(value=self.settings.get("api_key", ""))
        api_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="Enter your API key to unlock more models...",
            textvariable=api_key_var,
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["bg_light"],
            border_color=config.COLORS["border_light"],
            height=35
        )
        api_entry.pack(padx=15, pady=(5, 10), fill="x")
        
        # Model selection frame (initially hidden if no API key)
        model_frame = ctk.CTkFrame(api_frame, fg_color="transparent")
        model_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            model_frame,
            text="Generation Model",
            font=ctk.CTkFont(size=12),
            text_color=config.COLORS["text_secondary"]
        ).pack(padx=15, pady=(5, 0), anchor="w")
        
        model_var = ctk.StringVar(value=self.settings.get("model", "flux"))
        model_menu = ctk.CTkOptionMenu(
            model_frame,
            variable=model_var,
            values=config.POLLINATIONS_MODELS,
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["bg_light"],
            button_color=config.COLORS["primary"],
            corner_radius=8,
            state="normal" if api_key_var.get() else "disabled"
        )
        model_menu.pack(padx=15, pady=(5, 15), fill="x")
        
        # Dynamic visibility/state logic
        def on_api_key_change(*args):
            if api_key_var.get().strip():
                model_menu.configure(state="normal")
            else:
                model_menu.configure(state="disabled")
                model_var.set("flux") # Reset to default if no key
        
        api_key_var.trace_add("write", on_api_key_change)
        
        # UX Options setting
        ux_frame = ctk.CTkFrame(container, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        ux_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            ux_frame,
            text="User Experience",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=15, pady=(15, 10), anchor="w")
        
        show_preview_var = ctk.BooleanVar(value=self.settings.get("show_preview", True))
        ctk.CTkCheckBox(
            ux_frame,
            text="Show Generation Preview",
            variable=show_preview_var,
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"]
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # Save button
        def save_settings():
            self.settings["resolution"] = resolution_var.get()
            self.settings["auto_start"] = auto_start_var.get()
            self.settings["enhance_prompts"] = enhance_var.get()
            self.settings["api_key"] = api_key_var.get().strip()
            self.settings["model"] = model_var.get()
            self.settings["show_preview"] = show_preview_var.get()
            
            # Update API client with new settings
            self.api_client.update_config(
                api_key=self.settings["api_key"] if self.settings["api_key"] else None,
                model=self.settings["model"]
            )
            
            # Update auto-start
            if auto_start_var.get():
                StartupManager.toggle(True)
            else:
                StartupManager.toggle(False)
                
            # Update preview visibility immediately
            if not self.settings["show_preview"]:
                self.preview_label.configure(image=None, text="PREVIEW DISABLED")
            else:
                if hasattr(self, 'current_wallpaper') and self.current_wallpaper:
                    # Update preview with current wallpaper if enabled
                    self.on_generation_success(self.current_wallpaper)
                else:
                    self.preview_label.configure(image=None, text="NO PREVIEW AVAILABLE")
            
            SettingsManager.save_settings(self.settings)
            self.status_text.configure(text="Settings saved successfully!")
            self.close_panel()
        
        ctk.CTkButton(
            container,
            text=" SAVE SETTINGS",
            image=settings_icon,
            compound="left",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            fg_color=config.COLORS["success"],
            hover_color="#059669",
            corner_radius=10,
            command=save_settings
        ).pack(pady=20, padx=10, fill="x")
    
    def show_support(self):
        """Show support slide-in panel with beautiful design"""
        # Check if same panel is already open (toggle off)
        if self.current_panel and hasattr(self.current_panel, 'panel_type') and self.current_panel.panel_type == 'support':
            self.close_panel()
            return
        
        # Close any other open panel
        if self.current_panel:
            self.close_panel()
        
        # Create modern panel with margins and shadow effect (wider for content)
        panel = ctk.CTkFrame(
            self,
            fg_color=config.COLORS["bg_dark"],
            corner_radius=20,
            border_width=0
        )
        # Position: right side with margins (62% width)
        panel.place(relx=0.4, rely=0.02, relwidth=0.58, relheight=0.96)
        panel.panel_type = 'support'
        panel.bind("<Button-1>", lambda e: None)
        
        # Bring to front
        panel.lift()
        
        # Header with close button
        header = ctk.CTkFrame(panel, fg_color=config.COLORS["secondary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        self.current_panel = panel
        
        support_icon = IconManager.get_icon("support", size=24, color="white")
        ctk.CTkLabel(
            header,
            text="  SUPPORT & CONTRIBUTE",
            image=support_icon,
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)
        
        close_icon = IconManager.get_icon("close", size=20, color="white")
        ctk.CTkButton(
            header,
            text="",
            image=close_icon,
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#FF4444",
            command=self.close_panel
        ).pack(side="right", padx=20)
        
        # Simple scrollable content
        content = ctk.CTkScrollableFrame(panel, fg_color=config.COLORS["bg_card"])
        content.pack(fill="both", expand=True)
        
        # App info card
        info_card = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12, border_width=1, border_color=config.COLORS["border"])
        info_card.pack(fill="x", padx=25, pady=(25, 15))
        
        palette_icon = IconManager.get_icon("palette", size=24, color=config.COLORS["secondary"])
        ctk.CTkLabel(
            info_card,
            text="  POLLIPAPER v2.0",
            image=palette_icon,
            compound="left",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=config.COLORS["secondary"]
        ).pack(padx=20, pady=(20, 5))
        
        ctk.CTkLabel(
            info_card,
            text="AI-Powered Wallpaper Generation Platform",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_secondary"]
        ).pack(padx=20, pady=(0, 20))
        
        # GitHub card
        github_card = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12, border_width=1, border_color=config.COLORS["border"])
        github_card.pack(fill="x", padx=25, pady=15)
        
        star_icon = IconManager.get_icon("star", size=20, color=config.COLORS["accent_gold"])
        ctk.CTkLabel(
            github_card,
            text="  GitHub Repository",
            image=star_icon,
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 10), anchor="w")
        
        github_link = ctk.CTkButton(
            github_card,
            text="https://github.com/fricker2025-star/PolliPaper-Wallpaper",
            font=ctk.CTkFont(size=12),
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            corner_radius=8,
            height=40,
            anchor="w",
            command=lambda: self.open_url("https://github.com/fricker2025-star/PolliPaper-Wallpaper")
        )
        github_link.pack(padx=20, pady=(0, 20), fill="x")
        
        # Contribute card
        contrib_card = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12, border_width=1, border_color=config.COLORS["border"])
        contrib_card.pack(fill="x", padx=25, pady=15)
        
        code_icon = IconManager.get_icon("code", size=20, color=config.COLORS["primary"])
        ctk.CTkLabel(
            contrib_card,
            text="  How to Contribute",
            image=code_icon,
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 15), anchor="w")
        
        steps = [
            "1. Fork the repository",
            "2. Create a feature branch",
            "3. Make your changes",
            "4. Submit a pull request"
        ]
        
        for step in steps:
            ctk.CTkLabel(
                contrib_card,
                text=step,
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_secondary"],
                anchor="w"
            ).pack(padx=20, pady=3, anchor="w")
        
        ctk.CTkLabel(contrib_card, text="").pack(pady=10)
        
        # Ways to help card
        help_card = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12, border_width=1, border_color=config.COLORS["border"])
        help_card.pack(fill="x", padx=25, pady=15)
        
        support_way_icon = IconManager.get_icon("support", size=20, color=config.COLORS["secondary"])
        ctk.CTkLabel(
            help_card,
            text="  Ways to Help",
            image=support_way_icon,
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 15), anchor="w")
        
        ways = [
            "Star the repository",
            "Report bugs and issues",
            "Suggest new features",
            "Improve documentation",
            "Share your wallpapers",
            "Fix bugs and add features"
        ]
        
        for way in ways:
            row = ctk.CTkFrame(help_card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=2)
            
            dot_icon = IconManager.get_icon("dot", size=10, color=config.COLORS["secondary"])
            ctk.CTkLabel(
                row,
                text=f"  {way}",
                image=dot_icon,
                compound="left",
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_secondary"],
                anchor="w"
            ).pack(side="left")
        
        ctk.CTkLabel(help_card, text="").pack(pady=10)
        
        # Links card
        links_card = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12, border_width=1, border_color=config.COLORS["border"])
        links_card.pack(fill="x", padx=25, pady=15)
        
        links_header_icon = IconManager.get_icon("support", size=20, color=config.COLORS["info"])
        ctk.CTkLabel(
            links_card,
            text="  Quick Links",
            image=links_header_icon,
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 15), anchor="w")
        
        alert_icon = IconManager.get_icon("alert", size=16, color="white")
        ctk.CTkButton(
            links_card,
            text="  Report an Issue",
            image=alert_icon,
            compound="left",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=config.COLORS["warning"],
            hover_color="#d97706",
            corner_radius=8,
            height=40,
            command=lambda: self.open_url("https://github.com/fricker2025-star/PolliPaper-Wallpaper/issues")
        ).pack(padx=20, pady=5, fill="x")
        
        info_icon = IconManager.get_icon("info", size=16, color="white")
        ctk.CTkButton(
            links_card,
            text="  View Documentation",
            image=info_icon,
            compound="left",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=config.COLORS["info"],
            hover_color="#2563eb",
            corner_radius=8,
            height=40,
            command=lambda: self.open_url("https://github.com/fricker2025-star/PolliPaper-Wallpaper/wiki")
        ).pack(padx=20, pady=5, fill="x")
        
        ctk.CTkLabel(links_card, text="").pack(pady=10)
        
        # Footer
        footer_card = ctk.CTkFrame(content, fg_color="transparent")
        footer_card.pack(fill="x", padx=25, pady=(15, 25))
        
        heart_icon = IconManager.get_icon("heart", size=14, color="#ef4444")
        ctk.CTkLabel(
            footer_card,
            text="  Built with Passion using Python & CustomTkinter",
            image=heart_icon,
            compound="left",
            font=ctk.CTkFont(size=11),
            text_color=config.COLORS["text_muted"]
        ).pack(pady=5)
        
        ctk.CTkLabel(
            footer_card,
            text="Powered by Pollinations AI",
            font=ctk.CTkFont(size=11),
            text_color=config.COLORS["text_muted"]
        ).pack(pady=5)
        
        self.current_panel = panel
    
    def open_url(self, url):
        """Open URL in browser"""
        import webbrowser
        webbrowser.open(url)
    
    def close_panel(self):
        """Close the current slide-in panel"""
        if self.current_panel:
            self.current_panel.destroy()
            self.current_panel = None
    
    def generate_wallpaper(self, is_auto=False):
        """Generate wallpaper"""
        if self.is_generating:
            return
        
        # Get custom prompt if in manual mode
        custom_prompt = None
        if self.current_mode == "manual":
            custom_prompt = self.prompt_entry.get("1.0", "end-1c").strip()
            placeholder = "Enter your creative prompt here..."
            if not custom_prompt or custom_prompt == placeholder:
                self.status_text.configure(text="Please enter a prompt first!")
                return
        
        # Show progress
        self.is_generating = True
        self.progress.place(relx=0, rely=0, relwidth=1)
        self.progress.start()
        
        # Start animation
        self._animate_loading()
        
        refresh_icon = IconManager.get_icon("refresh", size=20, color="white")
        self.status_indicator.configure(text="  GENERATING", image=refresh_icon, text_color=config.COLORS["warning"])
        self.status_text.configure(text="Creating your wallpaper...")
        self.generate_btn.configure(state="disabled", text="  GENERATING...", image=refresh_icon)
        
        # Generate in thread
        def gen_thread():
            # Update status with timer
            start_time = time.time()
            
            def update_timer():
                if self.is_generating:
                    elapsed = int(time.time() - start_time)
                    self.status_text.configure(text=f"Creating your wallpaper... ({elapsed}s)")
                    self.after(1000, update_timer)
            
            self.after(0, update_timer)
            
            # Get prompt based on mode
            mode = self.current_mode
            
            # Seed handling: None for random, or specific if needed
            seed = None
            
            if mode == "manual":
                prompt = custom_prompt
            elif mode == "time_based":
                prompt = TimeDetector.get_time_prompt()
            elif mode == "weather_based":
                prompt = WeatherDetector.get_weather_prompt()
            elif mode == "music_based":
                prompt = self.music_analyzer.get_music_prompt()
            elif mode == "gaming":
                prompt = GameDetector.get_game_prompt()
            else:
                # Get random prompt from mode category
                if mode == "aesthetic":
                    prompt = random.choice(list(config.AESTHETIC_PROMPTS.values()))
                elif mode == "nature":
                    prompt = random.choice(list(config.NATURE_PROMPTS.values()))
                elif mode == "space":
                    prompt = random.choice(list(config.SPACE_PROMPTS.values()))
                elif mode == "abstract":
                    prompt = random.choice(list(config.ABSTRACT_PROMPTS.values()))
                elif mode == "cyberpunk":
                    prompt = random.choice(list(config.CYBERPUNK_PROMPTS.values()))
                elif mode == "fantasy":
                    prompt = random.choice(list(config.FANTASY_PROMPTS.values()))
                else:
                    prompt = TimeDetector.get_time_prompt()
            
            print(f"[GENERATION] Mode: {mode}, Prompt: {prompt[:60]}..., Auto: {is_auto}, Seed: {seed}")
            
            # Get resolution
            res = self.settings.get("resolution", "1920x1080").split("x")
            width, height = int(res[0]), int(res[1])
            
            # Generate
            try:
                print(f"[GENERATION] Generating {width}x{height} image...")
                self.after(0, lambda: self.status_text.configure(text="Contacting AI server..."))
                
                image_path = self.api_client.generate_and_save(
                    prompt=prompt,
                    width=width,
                    height=height,
                    enhance=True,
                    seed=seed
                )
                
                if image_path:
                    print(f"[GENERATION] Image saved to {image_path}")
                    self.after(0, lambda: self.status_text.configure(text="Setting wallpaper..."))
                    
                    if self.wallpaper_manager.set_wallpaper(image_path):
                        self.after(0, lambda: self.on_generation_success(image_path))
                    else:
                        print(f"[ERROR] Failed to set wallpaper")
                        self.after(0, lambda: self.on_generation_error("Failed to set wallpaper"))
                else:
                    print(f"[ERROR] Failed to generate image")
                    self.after(0, lambda: self.on_generation_error("Failed to generate image"))
            except Exception as e:
                print(f"[ERROR] Exception: {e}")
                traceback.print_exc()
                self.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=gen_thread, daemon=True).start()
    
    def on_generation_success(self, image_path=None):
        """Handle successful generation"""
        self.is_generating = False
        self.progress.stop()
        self.progress.place_forget()
        
        # Update status with check icon
        check_icon = IconManager.get_icon("check", size=14, color=config.COLORS["success"])
        self.status_indicator.configure(text="  SUCCESS", image=check_icon, text_color=config.COLORS["success"])
        self.status_text.configure(text="Wallpaper applied!")
        
        # Reset generate button with generate icon
        self.generate_btn.configure(state="normal", text="  GENERATE NOW", image=self.generate_icon)
        
        if image_path:
            self.current_wallpaper = image_path
            
            # Skip preview if disabled in settings
            if not self.settings.get("show_preview", True):
                self.preview_label.configure(image=None, text="PREVIEW DISABLED")
                return
                
            try:
                # Load and resize for preview - OPTIMIZED
                with Image.open(image_path) as img:
                    # Aspect ratio maintaining resize
                    w, h = img.size
                    
                    # Panel width is ~300 (350 - margins)
                    target_w = 300
                    target_h = int((h / w) * target_w)
                    
                    # If still too tall, cap height
                    if target_h > 180:
                        target_h = 180
                        target_w = int((w / h) * target_h)
                    
                    # Use faster resizing for preview
                    img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(target_w, target_h))
                    self.preview_label.configure(image=img_ctk, text="")
            except Exception as e:
                print(f"[PREVIEW] Error updating: {e}")
    
    def on_generation_error(self, error_msg="Generation failed"):
        """Handle generation error"""
        self.is_generating = False
        self.progress.stop()
        self.progress.place_forget()
        
        # Update status with alert icon
        alert_icon = IconManager.get_icon("alert", size=14, color=config.COLORS["danger"])
        self.status_indicator.configure(text="  ERROR", image=alert_icon, text_color=config.COLORS["danger"])
        self.status_text.configure(text=f"Error: {error_msg}")
        
        # Reset generate button with generate icon
        self.generate_btn.configure(state="normal", text="  GENERATE NOW", image=self.generate_icon)
    
    def toggle_auto_change(self):
        """Toggle auto-change - OPTIMIZED"""
        if self.auto_change_active:
            self.auto_change_active = False
            self.auto_btn.configure(
                text="  START AUTO-CHANGE",
                image=self.play_icon,
                fg_color=config.COLORS["secondary"],
                hover_color=config.COLORS["secondary_hover"]
            )
            self.status_text.configure(text="Auto-change stopped")
        else:
            self.auto_change_active = True
            self.auto_btn.configure(
                text="  STOP AUTO-CHANGE",
                image=self.stop_icon,
                fg_color=config.COLORS["danger"],
                hover_color="#dc2626"
            )
            interval = self.interval_var.get()
            self.status_text.configure(text=f"Auto-change active ({interval} min)")
            
            # Generate first wallpaper immediately
            self.generate_wallpaper(is_auto=True)
            
            # Start loop for subsequent generations
            threading.Thread(target=self.auto_change_loop, daemon=True).start()
    
    def auto_change_loop(self):
        """Auto-change loop"""
        while self.auto_change_active:
            interval = self.interval_var.get() * 60
            elapsed = 0
            while elapsed < interval and self.auto_change_active:
                time.sleep(1)
                elapsed += 1
            
            if self.auto_change_active and not self.is_generating:
                self.generate_wallpaper(is_auto=True)
    
    def save_settings(self):
        """Save settings"""
        self.settings["mode"] = self.current_mode
        self.settings["auto_change_interval"] = self.interval_var.get() * 60
        SettingsManager.save_settings(self.settings)
        self.status_text.configure(text="Settings saved!")
    
    def on_closing(self):
        """Handle window close - minimize to tray instead of exit"""
        self.minimize_to_tray()
    
    def minimize_to_tray(self):
        """Minimize to tray"""
        self.withdraw()
    
    def cleanup_and_exit(self):
        """Clean up and exit"""
        import os
        if hasattr(self, 'is_closing') and self.is_closing:
            os._exit(0)
            return
        
        self.is_closing = True
        self.auto_change_active = False
        
        if hasattr(self, 'tray_manager'):
            try:
                self.tray_manager.stop()
            except:
                pass
        
        try:
            SettingsManager.save_settings(self.settings)
        except:
            pass
        
        try:
            self.quit()
            self.destroy()
        except:
            pass
        
        os._exit(0)

def main():
    """Main entry point"""
    app = RevolutionaryPolliPaperApp()
    if "--minimized" in sys.argv:
        app.withdraw()
    app.mainloop()

if __name__ == "__main__":
    main()
