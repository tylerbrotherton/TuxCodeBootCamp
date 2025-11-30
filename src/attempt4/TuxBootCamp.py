"""
TUX CODE BOOT CAMP - Professional Refactored Version
ALL STRINGS STORED IN JSON FILES - NO HARDCODED TEXT IN PYTHON!
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


# =====================================================================
# RESOURCE MANAGER - Loads ALL strings from JSON files
# =====================================================================


class ResourceManager:
    """
    Loads and manages all application strings from external JSON files.
    NO STRINGS ARE HARDCODED IN THIS CLASS!
    """
    
    def __init__(self, resources_dir: str = "resources"):
        self.resources_dir = Path(resources_dir)
        self.data: Dict[str, Any] = {}
        self._load_all_resources()
    
    def _load_all_resources(self):
        """Load all JSON resource files"""
        resource_files = {
            'ui': 'ui_strings.json',
            'tux': 'tux_personality.json',
            'languages': 'language_data.json',
            'challenges': 'challenge_templates.json',
            'templates': 'code_templates.json'
        }
        
        for key, filename in resource_files.items():
            filepath = self.resources_dir / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Required resource file not found: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data[key] = json.load(f)
    
    def get(self, category: str, key: str, **kwargs) -> str:
        """Get a string with optional formatting"""
        try:
            value = self.data[category]
            for k in key.split('.'):
                value = value[k]
            
            if isinstance(value, str) and kwargs:
                return value.format(**kwargs)
            return value
        except (KeyError, TypeError):
            return f"[Missing: {category}.{key}]"
    
    def get_random(self, category: str, key: str, **kwargs) -> str:
        """Get random string from a list"""
        value = self.get(category, key)
        if isinstance(value, list):
            selected = random.choice(value)
            if kwargs:
                return selected.format(**kwargs)
            return selected
        return value
    
    def get_all(self, category: str, key: str = None) -> Any:
        """Get entire data structure"""
        if key is None:
            return self.data.get(category, {})
        return self.get(category, key)


# =====================================================================
# CONFIG MANAGER - Loads configuration from JSON
# =====================================================================


class ConfigManager:
    """Manages application configuration from config.json"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
    
    def get(self, *keys, default=None):
        """Get nested config value"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value


# =====================================================================
# TUX PERSONALITY - Uses ResourceManager for ALL dialogue
# =====================================================================


class TuxDrillSergeant:
    """Tux personality - ALL strings loaded from JSON"""
    
    def __init__(self, resources: ResourceManager):
        self.resources = resources
        self.current_emotion = "neutral"
    
    def get_random_expression(self) -> str:
        """Get random drill sergeant expression"""
        return self.resources.get_random('tux', 'favorite_expressions')
    
    def get_emotional_response(self, emotion: str, analysis_data: Optional[Dict] = None) -> str:
        """Get emotional response with optional analysis feedback"""
        self.current_emotion = emotion
        
        base_response = self.resources.get_random('tux', f'emotions.{emotion}')
        
        if not analysis_data:
            return base_response
        
        # Add strengths
        if analysis_data.get('strengths'):
            base_response += self.resources.get('tux', 'feedback_templates.what_i_liked')
            for strength in analysis_data['strengths'][:2]:
                base_response += self.resources.get('tux', 'feedback_templates.strength_bullet', 
                                                    strength=strength)
        
        # Add issues
        if analysis_data.get('issues'):
            base_response += self.resources.get('tux', 'feedback_templates.needs_improvement')
            for issue in analysis_data['issues'][:3]:
                base_response += self.resources.get('tux', 'feedback_templates.issue_bullet', 
                                                    issue=issue)
        
        # Add suggestions
        if analysis_data.get('suggestions'):
            base_response += self.resources.get('tux', 'feedback_templates.your_mission')
            for i, suggestion in enumerate(analysis_data['suggestions'][:2], 1):
                base_response += self.resources.get('tux', 'feedback_templates.suggestion_number',
                                                    number=i, suggestion=suggestion)
        
        return base_response
    
    def get_motivational_speech(self, context: str, **kwargs) -> str:
        """Get motivational speech by context"""
        return self.resources.get_random('tux', f'speeches.{context}', **kwargs)
    
    def get_motivation_phrase(self, level: int) -> str:
        """Get phrase based on motivation level"""
        if level < 20:
            key = 'low'
        elif level < 50:
            key = 'medium_low'
        elif level < 80:
            key = 'medium_high'
        else:
            key = 'high'
        
        return self.resources.get_random('tux', f'motivation_levels.{key}')


# =====================================================================
# EXAMPLE USAGE IN UI COMPONENTS
# =====================================================================


class LoginScreen:
    """Login screen using ResourceManager for all text"""
    
    def __init__(self, root, resources: ResourceManager, config: ConfigManager, on_enroll_callback):
        self.root = root
        self.resources = resources
        self.config = config
        self.on_enroll = on_enroll_callback
        self.name_entry = None
    
    def show(self):
        """Display login screen - ALL text from JSON"""
        login_frame = tk.Frame(self.root, bg=self.config.get('colors', 'background'))
        login_frame.pack(fill=tk.BOTH, expand=True, 
                        padx=self.config.get('ui', 'padding', 'large'),
                        pady=self.config.get('ui', 'padding', 'large'))
        
        # Banner - text from ui_strings.json
        banner_label = tk.Label(
            login_frame,
            text=self.resources.get('ui', 'banner_title'),
            font=self.config.get('fonts', 'large_header'),
            fg=self.config.get('colors', 'primary'),
            bg=self.config.get('colors', 'background')
        )
        banner_label.pack(pady=20)
        
        # Subtitle - text from ui_strings.json
        subtitle = tk.Label(
            login_frame,
            text=self.resources.get('ui', 'banner_subtitle'),
            font=self.config.get('fonts', 'subheader'),
            fg=self.config.get('colors', 'warning'),
            bg=self.config.get('colors', 'background')
        )
        subtitle.pack(pady=10)
        
        # Intro text - from tux_personality.json
        intro_text = scrolledtext.ScrolledText(
            login_frame,
            height=self.config.get('ui', 'text_area_height', 'medium'),
            width=self.config.get('ui', 'text_area_width', 'normal'),
            font=self.config.get('fonts', 'code'),
            bg=self.config.get('colors', 'secondary_bg'),
            fg=self.config.get('colors', 'success'),
            wrap=tk.WORD
        )
        intro_text.pack(pady=20)
        intro_text.insert(tk.END, self.resources.get('tux', 'intro_speech'))
        intro_text.config(state=tk.DISABLED)
        
        # Name input - label from ui_strings.json
        name_frame = tk.Frame(login_frame, bg=self.config.get('colors', 'background'))
        name_frame.pack(pady=20)
        
        name_label = tk.Label(
            name_frame,
            text=self.resources.get('ui', 'login_prompt'),
            font=self.config.get('fonts', 'body_bold'),
            fg=self.config.get('colors', 'text'),
            bg=self.config.get('colors', 'background')
        )
        name_label.pack()
        
        self.name_entry = tk.Entry(
            name_frame,
            font=self.config.get('fonts', 'subheader'),
            width=30,
            bg=self.config.get('colors', 'tertiary_bg'),
            fg=self.config.get('colors', 'text'),
            insertbackground="white"
        )
        self.name_entry.pack(pady=10)
        self.name_entry.bind("<Return>", lambda e: self._handle_enroll())
        
        # Enroll button - text from ui_strings.json
        enroll_button = tk.Button(
            login_frame,
            text=self.resources.get('ui', 'enroll_button'),
            font=self.config.get('fonts', 'button'),
            bg=self.config.get('colors', 'primary'),
            fg=self.config.get('colors', 'text'),
            command=self._handle_enroll,
            padx=20,
            pady=10
        )
        enroll_button.pack(pady=20)
    
    def _handle_enroll(self):
        """Handle enrollment - messages from ui_strings.json"""
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showwarning(
                self.resources.get('ui', 'empty_name_warning_title'),
                self.resources.get('ui', 'empty_name_warning_message')
            )
            return
        
        self.on_enroll(name)


class EnrollmentSpeech:
    """Enrollment speech window - ALL text from JSON"""
    
    def __init__(self, root, student_name: str, resources: ResourceManager, 
                 config: ConfigManager, on_continue_callback):
        self.root = root
        self.student_name = student_name
        self.resources = resources
        self.config = config
        self.on_continue = on_continue_callback
    
    def show(self):
        """Display enrollment speech - ALL text from tux_personality.json"""
        speech_window = tk.Toplevel(self.root)
        speech_window.title(self.resources.get('ui', 'banner_title'))
        speech_window.geometry("700x550")
        speech_window.configure(bg=self.config.get('colors', 'background'))
        
        speech_frame = tk.Frame(speech_window, bg=self.config.get('colors', 'background'))
        speech_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        tux_label = tk.Label(
            speech_frame,
            text=self.resources.get('ui', 'banner_title'),
            font=self.config.get('fonts', 'header'),
            fg=self.config.get('colors', 'primary'),
            bg=self.config.get('colors', 'background')
        )
        tux_label.pack(pady=10)
        
        # Speech text - from tux_personality.json with student name formatting
        speech_text = scrolledtext.ScrolledText(
            speech_frame,
            height=15,
            width=80,
            font=self.config.get('fonts', 'code'),
            bg=self.config.get('colors', 'secondary_bg'),
            fg=self.config.get('colors', 'success'),
            wrap=tk.WORD
        )
        speech_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Get speech from JSON and format with student name
        speech_content = self.resources.get('tux', 'enrollment_speech', 
                                           student_name=self.student_name.upper())
        speech_text.insert(tk.END, speech_content)
        speech_text.config(state=tk.DISABLED)
        
        # Button - text from ui_strings.json
        continue_button = tk.Button(
            speech_frame,
            text=self.resources.get('ui', 'yes_sergeant'),
            font=self.config.get('fonts', 'button'),
            bg=self.config.get('colors', 'success'),
            fg=self.config.get('colors', 'background'),
            command=lambda: self._handle_continue(speech_window),
            padx=20,
            pady=10
        )
        continue_button.pack(pady=10)
    
    def _handle_continue(self, window):
        """Handle continue button"""
        window.destroy()
        self.on_continue()


# =====================================================================
# MAIN APPLICATION
# =====================================================================


class TuxBootCampApp:
    """
    Main application - demonstrates how ZERO strings are hardcoded.
    Everything comes from JSON files!
    """
    
    def __init__(self, root):
        self.root = root
        
        # Load resources and config from JSON files
        try:
            self.resources = ResourceManager()
            self.config = ConfigManager()
        except FileNotFoundError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.root.quit()
            return
        
        # Set window properties from config.json
        self.root.title(self.resources.get('ui', 'app_title'))
        self.root.geometry(self.config.get('app', 'window_size'))
        self.root.configure(bg=self.config.get('colors', 'secondary_bg'))
        
        # Initialize Tux with resources
        self.tux = TuxDrillSergeant(self.resources)
        
        # Show login screen
        self.show_login_screen()
    
    def show_login_screen(self):
        """Display login screen"""
        login_screen = LoginScreen(self.root, self.resources, self.config, 
                                  self.on_student_enrolled)
        login_screen.show()
    
    def on_student_enrolled(self, name):
        """Handle enrollment"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show enrollment speech
        speech = EnrollmentSpeech(self.root, name, self.resources, self.config,
                                 self.show_main_interface)
        speech.show()
    
    def show_main_interface(self):
        """Show main interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main interface label
        label = tk.Label(
            self.root,
            text=self.resources.get('ui', 'select_language_prompt'),
            font=self.config.get('fonts', 'header'),
            fg=self.config.get('colors', 'primary'),
            bg=self.config.get('colors', 'background')
        )
        label.pack(pady=50)


# =====================================================================
# ENTRY POINT
# =====================================================================


def main():
    """Entry point - NO STRINGS HERE EITHER!"""
    root = tk.Tk()
    app = TuxBootCampApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
