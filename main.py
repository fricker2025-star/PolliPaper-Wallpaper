"""Revolutionary Professional UI - Visual Command Center"""
import customtkinter as ctk
import threading
import time
from pathlib import Path
import sys

import config
from api_client import PollinationsClient
from system_utils import WallpaperManager, TimeDetector, WeatherDetector, MusicAnalyzer, LocationDetector, SettingsManager
from startup_manager import StartupManager
from tray_manager import TrayManager

class RevolutionaryPolliPaperApp(ctk.CTk):
    """Revolutionary Visual Command Center for Wallpaper Generation"""
    
    # Mode configurations with professional styling
    MODES = {
        "time_based": {
            "name": "Time of Day",
            "icon": "🌅",
            "gradient": ["#f59e0b", "#fb923c"],
            "desc": "Matches current time"
        },
        "weather_based": {
            "name": "Weather Live",
            "icon": "⛅",
            "gradient": ["#3b82f6", "#60a5fa"],
            "desc": "Reacts to weather"
        },
        "music_based": {
            "name": "Music Sync",
            "icon": "🎵",
            "gradient": ["#ec4899", "#f472b6"],
            "desc": "Audio visualization"
        },
        "aesthetic": {
            "name": "Aesthetic",
            "icon": "🌈",
            "gradient": ["#a855f7", "#c084fc"],
            "desc": "Trendy aesthetics"
        },
        "nature": {
            "name": "Nature",
            "icon": "🌲",
            "gradient": ["#10b981", "#34d399"],
            "desc": "Natural landscapes"
        },
        "space": {
            "name": "Space",
            "icon": "🌌",
            "gradient": ["#6366f1", "#818cf8"],
            "desc": "Cosmic scenes"
        },
        "abstract": {
            "name": "Abstract",
            "icon": "🎨",
            "gradient": ["#8b5cf6", "#a78bfa"],
            "desc": "Digital art"
        },
        "cyberpunk": {
            "name": "Cyberpunk",
            "icon": "⚡",
            "gradient": ["#ec4899", "#8b5cf6"],
            "desc": "Neon future"
        },
        "fantasy": {
            "name": "Fantasy",
            "icon": "🐉",
            "gradient": ["#a855f7", "#ec4899"],
            "desc": "Magical worlds"
        },
        "manual": {
            "name": "Custom",
            "icon": "✏️",
            "gradient": ["#64748b", "#94a3b8"],
            "desc": "Your prompt"
        }
    }
    
    def __init__(self):
        super().__init__()
        
        # Initialize systems
        self.settings = SettingsManager.load_settings()
        self.api_client = PollinationsClient()
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
        
        # Header
        self.create_header(main)
        
        # Mode Grid (Revolutionary part)
        self.create_mode_grid(main)
        
        # Side Panel
        self.create_side_panel(main)
        
        # Footer Status
        self.create_footer(main)
    
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
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=config.COLORS["primary"]
        ).pack(anchor="w")
        
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
        ctk.CTkButton(
            menu_frame,
            text="❓ Help",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=80,
            height=35,
            fg_color=config.COLORS["bg_light"],
            hover_color=config.COLORS["hover_overlay"],
            corner_radius=8,
            command=self.show_help
        ).pack(side="left", padx=3)
        
        # Settings button
        ctk.CTkButton(
            menu_frame,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=90,
            height=35,
            fg_color=config.COLORS["bg_light"],
            hover_color=config.COLORS["hover_overlay"],
            corner_radius=8,
            command=self.show_settings
        ).pack(side="left", padx=3)
        
        # Support button
        ctk.CTkButton(
            menu_frame,
            text="💜 Support",
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
        
        self.status_indicator = ctk.CTkLabel(
            right,
            text="● READY",
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
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=config.COLORS["text_muted"],
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
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
        
        # Icon
        icon = ctk.CTkLabel(
            content,
            text=mode_info["icon"],
            font=ctk.CTkFont(size=48)
        )
        icon.pack(pady=(10, 5))
        
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
        
        # Hover effects - check stored active state
        def on_enter(e):
            if not self.mode_cards[mode_key]['is_active']:
                card.configure(
                    fg_color=config.COLORS["hover_overlay"],
                    border_color=config.COLORS["primary"]
                )
        
        def on_leave(e):
            if not self.mode_cards[mode_key]['is_active']:
                card.configure(
                    fg_color=config.COLORS["bg_card"],
                    border_color=config.COLORS["border_light"]
                )
        
        def on_click(e):
            # Visual feedback - quick flash
            card.configure(fg_color=config.COLORS["primary"])
            card.after(100, lambda: card.configure(
                fg_color=config.COLORS["bg_card"] if mode_key != self.current_mode else config.COLORS["bg_card"]
            ))
            self.select_mode(mode_key)
        
        def on_double_click(e):
            # Double click to select and generate immediately
            self.select_mode(mode_key)
            self.generate_wallpaper()
        
        # Bind events to all widgets
        for widget in [card, content, icon, name, desc]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            widget.bind("<Double-Button-1>", on_double_click)
    
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
        ctk.CTkLabel(
            panel,
            text="⚡ QUICK ACTIONS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=25, pady=(25, 20), anchor="w")
        
        # Generate Button (HUGE)
        self.generate_btn = ctk.CTkButton(
            panel,
            text="✨ GENERATE NOW",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=80,
            fg_color=config.COLORS["primary"],
            hover_color=config.COLORS["primary_hover"],
            corner_radius=12,
            border_width=2,
            border_color=config.COLORS["accent_gold"],
            command=self.generate_wallpaper
        )
        self.generate_btn.pack(padx=25, pady=(0, 15), fill="x")
        
        # Auto-change
        ctk.CTkLabel(
            panel,
            text="AUTO-CHANGE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=config.COLORS["text_muted"]
        ).pack(padx=25, pady=(15, 8), anchor="w")
        
        self.auto_btn = ctk.CTkButton(
            panel,
            text="▶ START AUTO-CHANGE",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=55,
            fg_color=config.COLORS["secondary"],
            hover_color=config.COLORS["secondary_hover"],
            corner_radius=10,
            command=self.toggle_auto_change
        )
        self.auto_btn.pack(padx=25, pady=(0, 10), fill="x")
        
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
        self.footer_mode = ctk.CTkLabel(
            info_frame,
            text=f"{self.MODES[self.current_mode]['icon']} {self.MODES[self.current_mode]['name']}",
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
    
    def select_mode(self, mode_key):
        """Handle mode selection - OPTIMIZED"""
        print(f"[MODE] Selected: {mode_key}")
        
        # Don't do anything if already selected
        if mode_key == self.current_mode:
            return
        
        old_mode = self.current_mode
        self.current_mode = mode_key
        
        # Update footer and status
        mode_info = self.MODES[mode_key]
        self.footer_mode.configure(text=f"{mode_info['icon']} {mode_info['name']}")
        self.status_text.configure(text=f"Mode: {mode_info['name']} - {mode_info['desc']}")
        
        # Update old card (deactivate)
        if old_mode in self.mode_cards:
            old_card_data = self.mode_cards[old_mode]
            old_card_data['card'].configure(
                border_width=1,
                border_color=config.COLORS["border_light"]
            )
            old_card_data['indicator'].place_forget()
            old_card_data['is_active'] = False
        
        # Update new card (activate)
        if mode_key in self.mode_cards:
            new_card_data = self.mode_cards[mode_key]
            new_card_data['card'].configure(
                border_width=2,
                border_color=config.COLORS["accent_gold"]
            )
            new_card_data['indicator'].place(relx=0, rely=1, relwidth=1, anchor="sw")
            new_card_data['is_active'] = True
    
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
        
        ctk.CTkLabel(
            header,
            text="❓ HELP & SHORTCUTS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            header,
            text="✕",
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
            text="✨ Welcome to PolliPaper",
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
            text="🎨 Generation Modes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            section_frame,
            text="• Time of Day — Dynamic wallpapers matching current time\n• Weather Live — Reacts to your local weather conditions\n• Music Sync — Visualizes your currently playing music\n• Aesthetic — Trendy vaporwave and modern art styles\n• Nature — Serene landscapes and natural beauty\n• Space — Cosmic scenes and celestial wonders\n• Abstract — Digital art patterns and shapes\n• Cyberpunk — Neon-lit futuristic cityscapes\n• Fantasy — Magical worlds and mythical scenes\n• Custom — Your own creative prompts",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_primary"],
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Keyboard shortcuts section
        section_frame2 = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        section_frame2.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame2,
            text="⌨️ Keyboard Shortcuts",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            section_frame2,
            text="• Enter / Space → Generate wallpaper with selected mode\n• Escape → Minimize to system tray\n• Ctrl + Q → Quit application\n• Double-click any mode → Quick generate",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_primary"],
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Quick tips section
        section_frame3 = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12)
        section_frame3.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame3,
            text="💡 Quick Tips",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            section_frame3,
            text="• Use AUTO-CHANGE to refresh wallpapers automatically\n• Set intervals from 1 to 240 minutes for auto-generation\n• All wallpapers are saved to your Pictures folder\n• Settings are saved automatically\n• Minimize to tray to keep it running in background",
            font=ctk.CTkFont(size=13),
            text_color=config.COLORS["text_primary"],
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Footer
        ctk.CTkLabel(
            content,
            text="Made with 💜 by the PolliPaper Team",
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
        
        ctk.CTkLabel(
            header,
            text="⚙️ SETTINGS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            header,
            text="✕",
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
        ctk.CTkLabel(
            container,
            text="⚙️ APPLICATION SETTINGS",
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
        
        # Save button
        def save_settings():
            self.settings["resolution"] = resolution_var.get()
            self.settings["auto_start"] = auto_start_var.get()
            self.settings["enhance_prompts"] = enhance_var.get()
            
            # Update auto-start
            if auto_start_var.get():
                StartupManager.toggle(True)
            else:
                StartupManager.toggle(False)
            
            SettingsManager.save_settings(self.settings)
            self.status_text.configure(text="Settings saved successfully!")
            self.close_panel()
        
        ctk.CTkButton(
            container,
            text="💾 SAVE SETTINGS",
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
        
        ctk.CTkLabel(
            header,
            text="💜 SUPPORT & CONTRIBUTE",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            header,
            text="✕",
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
        
        ctk.CTkLabel(
            info_card,
            text="🎨 POLLIPAPER v2.0",
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
        
        ctk.CTkLabel(
            github_card,
            text="🌟 GitHub Repository",
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
        
        ctk.CTkLabel(
            contrib_card,
            text="💻 How to Contribute",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 15), anchor="w")
        
        steps = [
            "1️⃣  Fork the repository",
            "2️⃣  Create a feature branch",
            "3️⃣  Make your changes",
            "4️⃣  Submit a pull request"
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
        
        ctk.CTkLabel(
            help_card,
            text="🤝 Ways to Help",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 15), anchor="w")
        
        ways = [
            "⭐ Star the repository",
            "🐛 Report bugs and issues",
            "💡 Suggest new features",
            "📝 Improve documentation",
            "🎨 Share your wallpapers",
            "🔧 Fix bugs and add features"
        ]
        
        for way in ways:
            ctk.CTkLabel(
                help_card,
                text=way,
                font=ctk.CTkFont(size=13),
                text_color=config.COLORS["text_secondary"],
                anchor="w"
            ).pack(padx=20, pady=3, anchor="w")
        
        ctk.CTkLabel(help_card, text="").pack(pady=10)
        
        # Links card
        links_card = ctk.CTkFrame(content, fg_color=config.COLORS["bg_dark"], corner_radius=12, border_width=1, border_color=config.COLORS["border"])
        links_card.pack(fill="x", padx=25, pady=15)
        
        ctk.CTkLabel(
            links_card,
            text="🔗 Quick Links",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=config.COLORS["text_primary"]
        ).pack(padx=20, pady=(20, 15), anchor="w")
        
        ctk.CTkButton(
            links_card,
            text="📋 Report an Issue",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=config.COLORS["warning"],
            hover_color="#d97706",
            corner_radius=8,
            height=40,
            command=lambda: self.open_url("https://github.com/fricker2025-star/PolliPaper-Wallpaper/issues")
        ).pack(padx=20, pady=5, fill="x")
        
        ctk.CTkButton(
            links_card,
            text="📖 View Documentation",
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
        
        ctk.CTkLabel(
            footer_card,
            text="Built with ❤️ using Python & CustomTkinter",
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
    
    def generate_wallpaper(self):
        """Generate wallpaper"""
        if self.is_generating:
            return
        
        # Show progress
        self.is_generating = True
        self.progress.place(relx=0, rely=0, relwidth=1)
        self.progress.start()
        self.status_indicator.configure(text="● GENERATING", text_color=config.COLORS["warning"])
        self.status_text.configure(text="Creating your wallpaper...")
        self.generate_btn.configure(state="disabled", text="⏳ GENERATING...")
        
        # Generate in thread
        def gen_thread():
            from system_utils import TimeDetector, WeatherDetector
            import time
            
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
            
            if mode == "time_based":
                prompt = TimeDetector.get_time_prompt()
            elif mode == "weather_based":
                prompt = WeatherDetector.get_weather_prompt()
            elif mode == "music_based":
                prompt = self.music_analyzer.get_music_prompt()
            else:
                # Get random prompt from mode category
                import random
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
            
            print(f"[GENERATION] Mode: {mode}, Prompt: {prompt[:60]}...")
            
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
                    enhance=True
                )
                
                if image_path:
                    print(f"[GENERATION] Image saved to {image_path}")
                    self.after(0, lambda: self.status_text.configure(text="Setting wallpaper..."))
                    
                    if self.wallpaper_manager.set_wallpaper(image_path):
                        self.after(0, lambda: self.on_generation_success())
                    else:
                        print(f"[ERROR] Failed to set wallpaper")
                        self.after(0, lambda: self.on_generation_error("Failed to set wallpaper"))
                else:
                    print(f"[ERROR] Failed to generate image")
                    self.after(0, lambda: self.on_generation_error("Failed to generate image"))
            except Exception as e:
                print(f"[ERROR] Exception: {e}")
                import traceback
                traceback.print_exc()
                self.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=gen_thread, daemon=True).start()
    
    def on_generation_success(self):
        """Handle successful generation"""
        self.is_generating = False
        self.progress.stop()
        self.progress.place_forget()
        self.status_indicator.configure(text="● SUCCESS", text_color=config.COLORS["success"])
        self.status_text.configure(text="Wallpaper applied!")
        self.generate_btn.configure(state="normal", text="✨ GENERATE NOW")
    
    def on_generation_error(self, error_msg="Generation failed"):
        """Handle generation error"""
        self.is_generating = False
        self.progress.stop()
        self.progress.place_forget()
        self.status_indicator.configure(text="● ERROR", text_color=config.COLORS["danger"])
        self.status_text.configure(text=f"Error: {error_msg}")
        self.generate_btn.configure(state="normal", text="✨ GENERATE NOW")
    
    def toggle_auto_change(self):
        """Toggle auto-change - OPTIMIZED"""
        if self.auto_change_active:
            self.auto_change_active = False
            self.auto_btn.configure(
                text="▶ START AUTO-CHANGE",
                fg_color=config.COLORS["secondary"],
                hover_color=config.COLORS["secondary_hover"]
            )
            self.status_text.configure(text="Auto-change stopped")
        else:
            self.auto_change_active = True
            self.auto_btn.configure(
                text="⏸ STOP AUTO-CHANGE",
                fg_color=config.COLORS["danger"],
                hover_color="#dc2626"
            )
            interval = self.interval_var.get()
            self.status_text.configure(text=f"Auto-change active ({interval} min)")
            
            # Generate first wallpaper immediately
            self.generate_wallpaper()
            
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
                self.generate_wallpaper()
    
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
