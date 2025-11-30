"""
TUX CODE BOOT CAMP - Refactored Version
Strings externalized to JSON configuration files
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from pathlib import Path
from typing import Dict, List, Any


# =====================================================================
# STRING RESOURCE MANAGER
# =====================================================================


class StringResourceManager:
    """Manages all application strings from external JSON files"""
    
    def __init__(self, resources_dir: str = "resources"):
        self.resources_dir = Path(resources_dir)
        self.strings: Dict[str, Any] = {}
        self._load_all_resources()
    
    def _load_all_resources(self):
        """Load all string resources from JSON files"""
        resource_files = {
            'ui': 'ui_strings.json',
            'tux': 'tux_personality.json',
            'languages': 'language_data.json',
            'challenges': 'challenge_templates.json',
            'templates': 'code_templates.json'
        }
        
        for key, filename in resource_files.items():
            filepath = self.resources_dir / filename
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.strings[key] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Resource file {filename} not found. Creating default...")
                self._create_default_resource(key, filepath)
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.strings[key] = json.load(f)
    
    def _create_default_resource(self, resource_type: str, filepath: Path):
        """Create default resource file if missing"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        defaults = {
            'ui': self._default_ui_strings(),
            'tux': self._default_tux_strings(),
            'languages': self._default_language_data(),
            'challenges': self._default_challenges(),
            'templates': self._default_templates()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(defaults[resource_type], f, indent=2, ensure_ascii=False)
    
    def get(self, category: str, key: str, **kwargs) -> str:
        """Get a string resource with optional formatting"""
        try:
            value = self.strings[category][key]
            if isinstance(value, str) and kwargs:
                return value.format(**kwargs)
            return value
        except KeyError:
            return f"[Missing: {category}.{key}]"
    
    def get_random(self, category: str, key: str, **kwargs) -> str:
        """Get a random string from a list of strings"""
        try:
            values = self.strings[category][key]
            if isinstance(values, list):
                value = random.choice(values)
                if kwargs:
                    return value.format(**kwargs)
                return value
            return values
        except KeyError:
            return f"[Missing: {category}.{key}]"
    
    def get_all(self, category: str, key: str) -> Any:
        """Get entire data structure (for lists, dicts, etc.)"""
        try:
            return self.strings[category][key]
        except KeyError:
            return None
    
    # Default resource generators
    def _default_ui_strings(self) -> dict:
        return {
            "app_title": "TUX CODE BOOT CAMP - Where Weak Coders Come to GET STRONG!",
            "banner_title": "TUX CODE BOOT CAMP",
            "banner_subtitle": "Where Indecision DIES and Code is FORGED!",
            "login_prompt": "Your Name (Recruit Identifier):",
            "enroll_button": "ENROLL IN BOOT CAMP!",
            "empty_name_warning_title": "HOLD IT!",
            "empty_name_warning_message": "I need a NAME, recruit! SPEAK UP!",
            "select_language_prompt": "SELECT A LANGUAGE TO BEGIN",
            "choose_weapon_label": "CHOOSE YOUR WEAPON",
            "sample_code_label": "SAMPLE CODE:",
            "learning_resources_button": "LEARNING RESOURCES",
            "take_challenge_button": "TAKE CHALLENGE",
            "submit_code_button": "SUBMIT CODE",
            "commit_button": "COMMIT",
            "accept_challenge_button": "ACCEPT CHALLENGE!",
            "maybe_later_button": "Maybe Later",
            "close_button": "Close",
            "motivation_level_label": "Motivation Level: {level}/100",
            "boot_camp_session": "BOOT CAMP IN SESSION - Recruit {name}",
            "difficulty_label": "Difficulty: {difficulty}",
            "submit_for_review": "SUBMIT FOR REVIEW!",
            "analyzing": "ANALYZING...",
            "your_code_label": "YOUR CODE:",
            "tux_analysis_label": "TUX'S ANALYSIS:",
            "waiting_submission": "Waiting for submission...",
            "reviewing_code": "Sergeant Tux is reviewing your code...\n\n"
        }
    
    def _default_tux_strings(self) -> dict:
        return {
            "favorite_expressions": [
                "DROP AND GIVE ME CODE!",
                "I WANT TO SEE THOSE FINGERS ON THE KEYBOARD!",
                "YOU THINK THIS IS A JOKE?!",
                "MOVE IT! MOVE IT! MOVE IT!",
                "ATTENTION TO DETAIL, RECRUIT!",
                "I'VE TRAINED A LOT OF SOLDIERS, BUT YOU...",
                "GET YOUR HEAD IN THE GAME!",
                "NO PARTICIPATION TROPHIES HERE!",
                "PAIN IS WEAKNESS LEAVING THE BODY!",
                "YOU'RE STRONGER THAN YOU THINK!"
            ],
            "emotions": {
                "exceptional": [
                    "🎖️ RECRUIT! I need to SALUTE YOU! This is EXCEPTIONAL work!",
                    "OUTSTANDING! You didn't just meet expectations - you CRUSHED them!",
                    "THIS is what EXCELLENCE looks like! You're not just a recruit anymore!",
                    "I've trained HUNDREDS of soldiers, and THIS... this is ELITE level!",
                    "PROMOTED! You've shown MASTERY beyond your rank! EXCEPTIONAL!"
                ],
                "proud": [
                    "OUTSTANDING WORK, RECRUIT! This is EXACTLY what I wanted to see!",
                    "NOW THAT'S WHAT I'M TALKING ABOUT! You're a NATURAL!",
                    "EXCEPTIONAL! You've got the HEART of a TRUE PROGRAMMER!",
                    "I'm PROUD of you, soldier! This is SUPERIOR work!"
                ],
                "satisfied": [
                    "GOOD JOB! You got it done and that's what matters!",
                    "SOLID WORK! You're making REAL progress here!",
                    "That's what I like to see! Keep this momentum going!",
                    "WELL DONE! You're proving yourself, recruit!"
                ],
                "encouraging": [
                    "You're ON THE RIGHT TRACK! Just needs some polish!",
                    "I see POTENTIAL here! Let's tighten this up!",
                    "GOOD EFFORT! You're getting there, keep pushing!",
                    "Not bad! But I KNOW you can do BETTER!"
                ],
                "stern": [
                    "This needs MORE WORK, recruit! I expect BETTER!",
                    "You're CAPABLE of more than this! DIG DEEPER!",
                    "UNACCEPTABLE! Get back in there and FIX THIS!",
                    "Is THIS your best? Because I DON'T BELIEVE IT!"
                ],
                "disappointed": [
                    "WHAT IS THIS?! Did you even TRY?!",
                    "I've seen BEGINNERS do better! GET IT TOGETHER!",
                    "This is LAZY WORK! You're BETTER than this!",
                    "RECRUIT! Drop and give me TWENTY LINES of PROPER CODE!"
                ]
            },
            "motivation_levels": {
                "low": [
                    "Listen up recruit! I've seen QUITTERS before, but you're testing my patience!",
                    "Your motivation is in the GUTTER! Time to get your head back in the GAME!",
                    "I didn't leave the Marines to train COWARDS! STEP UP!"
                ],
                "medium_low": [
                    "You're getting there, soldier! But we need MORE FIRE!",
                    "That's a START, but I expect EXCELLENCE!",
                    "Stop dragging your feet! Let's pick up the PACE!"
                ],
                "medium_high": [
                    "NOW WE'RE TALKING! That's the attitude I want to see!",
                    "I like your style, recruit! Keep that energy UP!",
                    "You're starting to understand what it takes!"
                ],
                "high": [
                    "THAT'S WHAT I'M TALKING ABOUT! You're a MACHINE!",
                    "You've got the FIRE, recruit! Keep BURNING!",
                    "Outstanding! You're showing TRUE DEDICATION!"
                ]
            },
            "speeches": {
                "starting_language": [
                    "Listen up! You're about to embark on a MISSION to learn {language}!",
                    "I didn't survive three tours to train QUITTERS! Now let's learn {language}!",
                    "Alright recruit, {language} isn't EASY, but YOU'RE TOUGHER!"
                ],
                "struggle": [
                    "I KNOW it's hard! But you know what's harder? GIVING UP!",
                    "Every line of code you write makes you STRONGER!",
                    "You think debugging is tough? Wait until you master it!",
                    "INDECISION is your REAL ENEMY, not the CODE!"
                ],
                "completion": [
                    "YOU DID IT! Now THAT'S what I call DETERMINATION!",
                    "I KNEW you had it in you! OUTSTANDING PERFORMANCE!",
                    "You just proved to yourself that you're UNSTOPPABLE!"
                ]
            },
            "intro_speech": """
LISTEN UP, RECRUIT!

I'm TUX - former Marine Corps Drill Sergeant turned Code Master!

I've seen a LOT of people come through here. Talented folks. Smart folks. 
But you know what stopped them? INDECISION! They couldn't COMMIT! They couldn't PUSH!

But NOT YOU! You're here because you want to learn programming and you're ready to 
STOP SECOND-GUESSING YOURSELF! You're ready to BUILD something!

I'm here to help you find YOUR LANGUAGE, BUILD YOUR SKILLS, and prove to yourself 
that you've got the DISCIPLINE and DETERMINATION to become a PROGRAMMER!

Now... what's your NAME, recruit?
            """,
            "enrollment_speech": """
WELCOME TO THE PROGRAM, {student_name}!

From this moment forward, you are NOT just "someone interested in programming."
YOU are a CODE RECRUIT! You are IN this program!

Here's how this works:

1. YOU will choose a programming language
2. YOU will commit to learning it (no turning back!)
3. I will PUSH you with challenges and motivation
4. YOU will complete each challenge or tell me why you QUIT

No more fence-sitting! No more "maybe I'll try next week!"

You have DECIDED to be here. I see it. That TAKES GUTS!

Now, here's what I need from you:

COMMITMENT - Show up. Do the work. Don't make excuses.
HONESTY - Tell me when you're struggling. I've BEEN THERE.
EFFORT - Give me 100%. That's all I ask.
DETERMINATION - When it gets hard, remember: IT'S SUPPOSED TO BE HARD!

The pain you feel right now? That's not weakness leaving your body - 
that's INDECISION DYING and DETERMINATION being BORN!

Ready to choose your first language, {student_name}?

LET'S MOVE OUT!
            """
        }
    
    def _default_language_data(self) -> dict:
        return {
            "Python": {
                "description": "High-level, interpreted language known for readability and versatility.",
                "difficulty": "Beginner",
                "drill_sergeant_take": "PERFECT for BEGINNERS! Easy to READ but don't let that make you LAZY!",
                "use_cases": ["Web Development", "Data Science", "AI/ML"],
                "sample_code": "print('Hello, Tux!')\ndef greet(name):\n    return f'Welcome, {name}!'",
                "learning_resources": [
                    "https://docs.python.org/3/tutorial/",
                    "https://www.codecademy.com/learn/learn-python-3"
                ]
            },
            "JavaScript": {
                "description": "The language of the WEB! If you want to make things MOVE, this is IT!",
                "difficulty": "Beginner-Intermediate",
                "drill_sergeant_take": "JavaScript is EVERYWHERE! Master this and you can CONQUER the web!",
                "use_cases": ["Web Development", "Frontend", "Full Stack"],
                "sample_code": "console.log('Hello, Tux!');\nfunction greet(name) {\n    return `Welcome, ${name}!`;\n}",
                "learning_resources": [
                    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                    "https://www.codecademy.com/learn/learn-javascript"
                ]
            }
        }
    
    def _default_challenges(self) -> dict:
        return {
            "Python": [
                {
                    "name": "BEGINNER DRILL",
                    "description": "Implement a Fibonacci sequence generator with memorization using decorators",
                    "difficulty": "Easy"
                },
                {
                    "name": "INTERMEDIATE MISSION",
                    "description": "Build a CLI todo app with SQLite persistence and CRUD operations",
                    "difficulty": "Medium"
                }
            ]
        }
    
    def _default_templates(self) -> dict:
        return {
            "file_header": """{comment}{'=' * 70}
{comment} TUX CODE BOOT CAMP - CHALLENGE FILE
{comment} {'=' * 70}
{comment} Recruit: {student}
{comment} Challenge: {challenge}
{comment} Language: {language}
{comment} Difficulty: {difficulty}
{comment} Date: {date}
{comment} {'=' * 70}
{comment}
{comment} MISSION BRIEFING:
{comment} {description}
{comment}
{comment} YOUR ORDERS:
{comment} 1. Read the mission briefing carefully
{comment} 2. Complete the function implementation below
{comment} 3. Test your code thoroughly
{comment} 4. Report back to Sergeant Tux when complete!
{comment}
{comment} REMEMBER: Comments are your BATTLE PLAN! Use them!
{comment} {'=' * 70}

""",
            "Python": """
def main():
    \"\"\"
    Main function - This is where your code execution begins!
    Purpose: Implement the challenge requirements here
    \"\"\"
    # TODO: Write your code here, recruit!
    pass


if __name__ == "__main__":
    main()
    
# SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""
        }


# =====================================================================
# CONFIGURATION MANAGER
# =====================================================================


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> dict:
        """Get default configuration"""
        return {
            "app": {
                "title": "TUX CODE BOOT CAMP",
                "version": "2.0",
                "window_size": "1400x900"
            },
            "colors": {
                "background": "#1a1a1a",
                "secondary_bg": "#2b2b2b",
                "tertiary_bg": "#3b3b3b",
                "primary": "#ff6b6b",
                "success": "#00ff00",
                "warning": "#ffd93d",
                "text": "#ffffff",
                "code": "#00ff00"
            },
            "fonts": {
                "header": ("Arial", 18, "bold"),
                "subheader": ("Arial", 14, "bold"),
                "body": ("Arial", 11),
                "code": ("Courier", 10)
            },
            "paths": {
                "challenges_dir": "TuxBootCamp_Challenges",
                "resources_dir": "resources"
            }
        }
    
    def get(self, *keys, default=None):
        """Get nested config value"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)


# =====================================================================
# USAGE EXAMPLE
# =====================================================================


class RefactoredTuxApp:
    """Example of refactored application using external strings"""
    
    def __init__(self, root):
        self.root = root
        self.strings = StringResourceManager()
        self.config = ConfigManager()
        
        # Set window properties from config
        self.root.title(self.strings.get('ui', 'app_title'))
        self.root.geometry(self.config.get('app', 'window_size'))
        self.root.configure(bg=self.config.get('colors', 'background'))
    
    def create_login_screen(self):
        """Example: Create login screen using external strings"""
        frame = tk.Frame(
            self.root, 
            bg=self.config.get('colors', 'background')
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Banner
        banner = tk.Label(
            frame,
            text=self.strings.get('ui', 'banner_title'),
            font=self.config.get('fonts', 'header'),
            fg=self.config.get('colors', 'primary'),
            bg=self.config.get('colors', 'background')
        )
        banner.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            frame,
            text=self.strings.get('ui', 'banner_subtitle'),
            font=self.config.get('fonts', 'body'),
            fg=self.config.get('colors', 'warning'),
            bg=self.config.get('colors', 'background')
        )
        subtitle.pack(pady=10)
        
        # Intro text
        intro_text = scrolledtext.ScrolledText(
            frame,
            height=8,
            width=80,
            font=self.config.get('fonts', 'code'),
            bg=self.config.get('colors', 'secondary_bg'),
            fg=self.config.get('colors', 'success'),
            wrap=tk.WORD
        )
        intro_text.pack(pady=20)
        intro_text.insert(tk.END, self.strings.get('tux', 'intro_speech'))
        intro_text.config(state=tk.DISABLED)
    
    def get_tux_response(self, emotion: str) -> str:
        """Example: Get Tux's emotional response"""
        return self.strings.get_random('tux', f'emotions.{emotion}')
    
    def get_motivational_speech(self, context: str, **kwargs) -> str:
        """Example: Get motivational speech"""
        return self.strings.get_random('tux', f'speeches.{context}', **kwargs)


# Example usage
if __name__ == "__main__":
    # This demonstrates the refactored approach
    root = tk.Tk()
    app = RefactoredTuxApp(root)
    app.create_login_screen()
    root.mainloop()
