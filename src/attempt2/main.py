import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import webbrowser
import os
from datetime import datetime
from enum import Enum

class DrillLevel(Enum):
    """Tux's motivation intensity levels"""
    ENCOURAGEMENT = "Let's get motivated!"
    INTENSITY = "Time to push harder!"
    FULL_DRILL_SERGEANT = "DROP AND GIVE ME CODE!"
    TOUGH_LOVE = "You think this is easy?"

class StudentProgress:
    """Track individual student progress and struggle patterns"""
    def __init__(self, name):
        self.name = name
        self.joined_date = datetime.now()
        self.languages_started = []
        self.languages_completed = []
        self.completion_attempts = {}  # Track how many times they tried
        self.decision_struggle_count = 0
        self.last_session = None
        self.motivation_level = 50  # 0-100 scale
        self.streak_days = 0
        
    def update_motivation(self, change):
        """Update motivation level based on actions"""
        self.motivation_level = max(0, min(100, self.motivation_level + change))
    
    def get_tux_phrase(self):
        """Get motivational phrase based on progress and struggle"""
        if self.motivation_level < 20:
            return random.choice([
                "Listen up recruit! I've seen QUITTERS before, but you're testing my patience!",
                "Your motivation is in the GUTTER! Time to get your head back in the GAME!",
                "I didn't leave the Marines to train COWARDS! STEP UP!",
            ])
        elif self.motivation_level < 50:
            return random.choice([
                "You're getting there, soldier! But we need MORE FIRE!",
                "That's a START, but I expect EXCELLENCE!",
                "Stop dragging your feet! Let's pick up the PACE!",
            ])
        elif self.motivation_level < 80:
            return random.choice([
                "NOW WE'RE TALKING! That's the attitude I want to see!",
                "I like your style, recruit! Keep that energy UP!",
                "You're starting to understand what it takes!",
            ])
        else:
            return random.choice([
                "THAT'S WHAT I'M TALKING ABOUT! You're a MACHINE!",
                "You've got the FIRE, recruit! Keep BURNING!",
                "Outstanding! You're showing TRUE DEDICATION!",
            ])

class TuxDrillSergeant:
    """Tux - The Marine Corp Drill Sergeant Instructor"""
    def __init__(self):
        self.drill_level = DrillLevel.ENCOURAGEMENT
        self.favorite_expressions = [
            "DROP AND GIVE ME CODE!",
            "I WANT TO SEE THOSE FINGERS ON THE KEYBOARD!",
            "YOU THINK THIS IS A JOKE?!",
            "MOVE IT! MOVE IT! MOVE IT!",
            "ATTENTION TO DETAIL, RECRUIT!",
            "I'VE TRAINED A LOT OF SOLDIERS, BUT YOU...",
            "GET YOUR HEAD IN THE GAME!",
            "NO PARTICIPATION TROPHIES HERE!",
            "PAIN IS WEAKNESS LEAVING THE BODY!",
            "YOU'RE STRONGER THAN YOU THINK!",
        ]
        
    def get_motivational_speech(self, context):
        """Generate context-aware motivational speeches"""
        speeches = {
            "starting_language": [
                "Listen up! You're about to embark on a MISSION to learn {language}!",
                "I didn't survive three tours to train QUITTERS! Now let's learn {language}!",
                "Alright recruit, {language} isn't EASY, but YOU'RE TOUGHER!",
            ],
            "struggle": [
                "I KNOW it's hard! But you know what's harder? GIVING UP!",
                "Every line of code you write makes you STRONGER!",
                "You think debugging is tough? Wait until you master it!",
                "INDECISION is your REAL ENEMY, not the CODE!",
            ],
            "checkpoint": [
                "CHECKPOINT REACHED! But this is just the BEGINNING!",
                "You're doing PUSH-UPS of code! Keep going!",
                "HALFWAY THERE, RECRUIT! NO BACKING DOWN NOW!",
            ],
            "completion": [
                "YOU DID IT! Now THAT'S what I call DETERMINATION!",
                "I KNEW you had it in you! OUTSTANDING PERFORMANCE!",
                "You just proved to yourself that you're UNSTOPPABLE!",
            ],
        }
        
        phrases = speeches.get(context, self.favorite_expressions)
        return random.choice(phrases)

class TuxLanguageLearner:
    def __init__(self, root):
        self.root = root
        self.root.title("TUX CODE BOOT CAMP - Where Weak Coders Come to GET STRONG!")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Student tracking
        self.current_student = None
        self.tux_sergeant = TuxDrillSergeant()
        
        # Language Database with difficulty progression
        self.languages = {
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
            },
            "Go": {
                "description": "Concurrent programming language developed by Google. BUILT FOR THE FUTURE!",
                "difficulty": "Intermediate",
                "drill_sergeant_take": "Go is LEAN, MEAN, and gets the JOB DONE! Learn this and you're UNSTOPPABLE!",
                "use_cases": ["Cloud Computing", "Network Programming", "Microservices"],
                "sample_code": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, Tux!\")\n}",
                "learning_resources":[
                    "https://go.dev/",
                    "https://www.freecodecamp.org/news/learn-golang-handbook/"
                ]
            },
            "Rust": {
                "description": "Systems programming language focused on memory safety and concurrency.",
                "difficulty": "Advanced",
                "drill_sergeant_take": "RUST is for SOLDIERS! The COMPILER will YELL at you just like I do!",
                "use_cases": ["Systems Programming", "WebAssembly", "Network Services"],
                "sample_code": "fn main() {\n    println!(\"Hello, Tux!\");\n    let greeting = String::from(\"Rust is awesome\");\n}",
                "learning_resources": [
                    "https://doc.rust-lang.org/book/",
                    "https://rustlings.cool/"
                ]
            },
            "C": {
                "description": "Low-level systems programming language with direct hardware access.",
                "difficulty": "Advanced",
                "drill_sergeant_take": "C is the FOUNDATION! Learn this and you'll understand EVERYTHING!",
                "use_cases": ["Operating Systems", "Embedded Systems", "Performance-critical Applications"],
                "sample_code": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, Tux!\\n\");\n    return 0;\n}",
                "learning_resources": [
                    "https://www.learn-c.org/",
                    "https://cplusplus.com/doc/tutorial/"
                ]
            },
            "C++": {
                "description": "Object-oriented systems programming language with high performance.",
                "difficulty": "Advanced",
                "drill_sergeant_take": "C++ is the ADVANCED TRAINING! You ready for this?!",
                "use_cases": ["Game Development", "High-Performance Applications", "System Software"],
                "sample_code": "#include <iostream>\nint main() {\n    std::cout << \"Hello, Tux!\" << std::endl;\n    return 0;\n}",
                "learning_resources": [
                    "https://www.learncpp.com/",
                    "https://www.cplusplus.com/doc/tutorial/"
                ]
            },
        }
        
        self.challenge_templates = {
            "Python": [
                ("BEGINNER DRILL", "Create a function that calculates Fibonacci sequence", "Easy"),
                ("INTERMEDIATE MISSION", "Build a todo list application with file persistence", "Medium"),
                ("ADVANCED OPERATION", "Implement a web scraper with error handling", "Hard"),
            ],
            "JavaScript": [
                ("BEGINNER DRILL", "Create an interactive form validator", "Easy"),
                ("INTERMEDIATE MISSION", "Build a real-time todo app with localStorage", "Medium"),
                ("ADVANCED OPERATION", "Create a web-based chat application with WebSockets", "Hard"),
            ],
            "Go": [
                ("BEGINNER DRILL", "Create a basic HTTP server", "Easy"),
                ("INTERMEDIATE MISSION", "Build a concurrent task processor", "Medium"),
                ("ADVANCED OPERATION", "Implement a microservice with error handling", "Hard"),
            ],
            "Rust": [
                ("BEGINNER DRILL", "Create a memory-safe calculator", "Easy"),
                ("INTERMEDIATE MISSION", "Build a concurrent web crawler", "Medium"),
                ("ADVANCED OPERATION", "Implement a thread-safe data structure", "Hard"),
            ],
            "C": [
                ("BEGINNER DRILL", "Create a simple calculator with pointers", "Easy"),
                ("INTERMEDIATE MISSION", "Implement dynamic array operations", "Medium"),
                ("ADVANCED OPERATION", "Build a file encryption utility", "Hard"),
            ],
            "C++": [
                ("BEGINNER DRILL", "Create an object-oriented game class", "Easy"),
                ("INTERMEDIATE MISSION", "Build a template-based data structure", "Medium"),
                ("ADVANCED OPERATION", "Implement a graphics rendering engine", "Hard"),
            ],
        }

    def create_login_screen(self):
        """Initial login/enrollment screen"""
        login_frame = tk.Frame(self.root, bg='#1a1a1a')
        login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tux's welcome banner
        banner_label = tk.Label(
            login_frame,
            text="TUX CODE BOOT CAMP",
            font=("Arial", 32, "bold"),
            fg="#ff6b6b",
            bg="#1a1a1a"
        )
        banner_label.pack(pady=20)
        
        subtitle = tk.Label(
            login_frame,
            text="Where Indecision DIES and Code is FORGED!",
            font=("Arial", 16, "italic"),
            fg="#ffd93d",
            bg="#1a1a1a"
        )
        subtitle.pack(pady=10)
        
        # Tux introduction
        intro_text = scrolledtext.ScrolledText(
            login_frame,
            height=8,
            width=80,
            font=("Courier", 11),
            bg="#2b2b2b",
            fg="#00ff00",
            wrap=tk.WORD
        )
        intro_text.pack(pady=20)
        
        intro_message = """
LISTEN UP, RECRUIT!

I'm TUX - former Marine Corps Drill Sergeant turned Code Master!

I've seen a LOT of people come through here. Talented folks. Smart folks. 
But you know what stopped them? INDECISION! They couldn't COMMIT! They couldn't PUSH!

But NOT YOU! You're here because you want to learn programming and you're ready to 
STOP SECOND-GUESSING YOURSELF! You're ready to BUILD something!

I'm here to help you find YOUR LANGUAGE, BUILD YOUR SKILLS, and prove to yourself 
that you've got the DISCIPLINE and DETERMINATION to become a PROGRAMMER!

Now... what's your NAME, recruit?
        """
        
        intro_text.insert(tk.END, intro_message)
        intro_text.config(state=tk.DISABLED)
        
        # Name entry
        name_frame = tk.Frame(login_frame, bg="#1a1a1a")
        name_frame.pack(pady=20)
        
        name_label = tk.Label(
            name_frame,
            text="Your Name (Recruit Identifier):",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        name_label.pack()
        
        self.name_entry = tk.Entry(
            name_frame,
            font=("Arial", 14),
            width=30,
            bg="#3b3b3b",
            fg="#ffffff",
            insertbackground="white"
        )
        self.name_entry.pack(pady=10)
        self.name_entry.bind('<Return>', lambda e: self.enroll_student())
        
        # Enroll button
        enroll_button = tk.Button(
            login_frame,
            text="ENROLL IN BOOT CAMP!",
            font=("Arial", 14, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            command=self.enroll_student,
            padx=20,
            pady=10
        )
        enroll_button.pack(pady=20)

    def enroll_student(self):
        """Enroll a new student and show their first challenge"""
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showwarning("HOLD IT!", "I need a NAME, recruit! SPEAK UP!")
            return
        
        self.current_student = StudentProgress(name)
        
        # Clear current frame
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show enrollment confirmation
        self.show_enrollment_speech(name)

    def show_enrollment_speech(self, name):
        """Dramatic enrollment speech from Tux"""
        speech_window = tk.Toplevel(self.root)
        speech_window.title("Boot Camp Enrollment")
        speech_window.geometry("700x500")
        speech_window.configure(bg='#1a1a1a')
        
        speech_frame = tk.Frame(speech_window, bg='#1a1a1a')
        speech_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tux_label = tk.Label(
            speech_frame,
            text="TUX DRILL SERGEANT",
            font=("Arial", 18, "bold"),
            fg="#ff6b6b",
            bg="#1a1a1a"
        )
        tux_label.pack(pady=10)
        
        speech_text = scrolledtext.ScrolledText(
            speech_frame,
            height=15,
            width=80,
            font=("Courier", 11),
            bg="#2b2b2b",
            fg="#00ff00",
            wrap=tk.WORD
        )
        speech_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        speech_content = f"""
WELCOME TO THE PROGRAM, {name.upper()}!

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

✓ COMMITMENT - Show up. Do the work. Don't make excuses.
✓ HONESTY - Tell me when you're struggling. I've BEEN THERE.
✓ EFFORT - Give me 100%. That's all I ask.
✓ DETERMINATION - When it gets hard, remember: IT'S SUPPOSED TO BE HARD!

The pain you feel right now? That's not weakness leaving your body - 
that's INDECISION DYING and DETERMINATION being BORN!

Ready to choose your first language, {name}?

LET'S MOVE OUT!
        """
        
        speech_text.insert(tk.END, speech_content)
        speech_text.config(state=tk.DISABLED)
        
        def continue_to_selection():
            speech_window.destroy()
            self.create_main_interface()
        
        continue_button = tk.Button(
            speech_frame,
            text="YES, SERGEANT TUX! LET'S GO!",
            font=("Arial", 12, "bold"),
            bg="#00ff00",
            fg="#000000",
            command=continue_to_selection,
            padx=20,
            pady=10
        )
        continue_button.pack(pady=10)

    def create_main_interface(self):
        """Main learning interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("1400x900")
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top banner with student info
        banner_frame = tk.Frame(main_frame, bg='#ff6b6b')
        banner_frame.pack(fill=tk.X, padx=0, pady=0)
        
        banner_text = tk.Label(
            banner_frame,
            text=f"BOOT CAMP IN SESSION - Recruit {self.current_student.name.upper()}",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            padx=20,
            pady=10
        )
        banner_text.pack(side=tk.LEFT)
        
        motivation_label = tk.Label(
            banner_frame,
            text=f"Motivation Level: {int(self.current_student.motivation_level)}/100",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            padx=20,
            pady=10
        )
        motivation_label.pack(side=tk.RIGHT)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar - Language selection
        left_frame = tk.Frame(content_frame, bg='#2b2b2b')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        languages_label = tk.Label(
            left_frame,
            text="CHOOSE YOUR WEAPON",
            font=("Arial", 14, "bold"),
            fg="#ffd93d",
            bg="#2b2b2b"
        )
        languages_label.pack(pady=10)
        
        # Language listbox
        self.language_listbox = tk.Listbox(
            left_frame,
            width=20,
            height=12,
            font=("Arial", 11, "bold"),
            bg="#3b3b3b",
            fg="#00ff00",
            selectmode=tk.SINGLE
        )
        self.language_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.language_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.language_listbox.yview)
        
        for language in sorted(self.languages.keys()):
            self.language_listbox.insert(tk.END, f"> {language}")
        
        self.language_listbox.bind('<<ListboxSelect>>', self.show_language_details)
        
        # Right frame - Language details
        right_frame = tk.Frame(content_frame, bg='#2b2b2b')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Language name
        self.language_name_label = tk.Label(
            right_frame,
            text="SELECT A LANGUAGE TO BEGIN",
            font=("Arial", 18, "bold"),
            fg="#ff6b6b",
            bg="#2b2b2b"
        )
        self.language_name_label.pack(pady=10)
        
        # Tux's take on the language
        self.tux_commentary_text = tk.Text(
            right_frame,
            height=3,
            width=70,
            font=("Courier", 10),
            bg="#3b3b3b",
            fg="#ffd93d",
            wrap=tk.WORD
        )
        self.tux_commentary_text.pack(pady=10)
        
        # Description
        self.description_text = tk.Text(
            right_frame,
            height=5,
            width=70,
            font=("Arial", 10),
            bg="#3b3b3b",
            fg="#ffffff",
            wrap=tk.WORD
        )
        self.description_text.pack(pady=10)
        
        # Sample code
        code_label = tk.Label(
            right_frame,
            text="SAMPLE CODE:",
            font=("Arial", 11, "bold"),
            fg="#00ff00",
            bg="#2b2b2b"
        )
        code_label.pack()
        
        self.code_sample_text = tk.Text(
            right_frame,
            height=8,
            width=70,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#00ff00",
            wrap=tk.WORD
        )
        self.code_sample_text.pack(pady=10)
        
        # Action buttons
        button_frame = tk.Frame(right_frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, pady=10)
        
        resources_button = tk.Button(
            button_frame,
            text="LEARNING RESOURCES",
            font=("Arial", 11, "bold"),
            bg="#00aa00",
            fg="#ffffff",
            command=self.open_learning_resources,
            padx=15,
            pady=8
        )
        resources_button.pack(side=tk.LEFT, padx=5)
        
        challenge_button = tk.Button(
            button_frame,
            text="TAKE THE CHALLENGE",
            font=("Arial", 11, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            command=self.generate_challenge,
            padx=15,
            pady=8
        )
        challenge_button.pack(side=tk.LEFT, padx=5)
        
        commit_button = tk.Button(
            button_frame,
            text="✓ I COMMIT TO THIS LANGUAGE",
            font=("Arial", 11, "bold"),
            bg="#ffd93d",
            fg="#000000",
            command=self.commit_to_language,
            padx=15,
            pady=8
        )
        commit_button.pack(side=tk.LEFT, padx=5)

    def show_language_details(self, event):
        """Display language details when selected"""
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index).replace("> ", "")
            
            self.language_name_label.config(text=f"FIGHT {selected_language.upper()}")
            
            self.tux_commentary_text.config(state=tk.NORMAL)
            self.tux_commentary_text.delete(1.0, tk.END)
            self.tux_commentary_text.insert(tk.END, self.languages[selected_language]['drill_sergeant_take'])
            self.tux_commentary_text.config(state=tk.DISABLED)
            
            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            language_info = self.languages[selected_language]
            
            desc = f"Difficulty: {language_info['difficulty']}\n\n"
            desc += f"Use Cases:\n"
            for use_case in language_info['use_cases']:
                desc += f"• {use_case}\n"
            
            self.description_text.insert(tk.END, desc)
            self.description_text.config(state=tk.DISABLED)
            
            self.code_sample_text.config(state=tk.NORMAL)
            self.code_sample_text.delete(1.0, tk.END)
            self.code_sample_text.insert(tk.END, language_info['sample_code'])
            self.code_sample_text.config(state=tk.DISABLED)
            
        except IndexError:
            messagebox.showwarning("HOLD IT!", "SELECT A LANGUAGE, RECRUIT!")

    def open_learning_resources(self):
        """Open learning resources in browser"""
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index).replace("> ", "")
            resources = self.languages[selected_language]['learning_resources']
            
            resource_window = tk.Toplevel(self.root)
            resource_window.title(f"{selected_language} Resources - GET LEARNING!")
            resource_window.geometry("600x300")
            resource_window.configure(bg='#1a1a1a')
            
            frame = tk.Frame(resource_window, bg='#1a1a1a')
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            label = tk.Label(
                frame,
                text=f"OPEN THESE RESOURCES TO BECOME A {selected_language.upper()} MASTER!",
                font=("Arial", 12, "bold"),
                fg="#00ff00",
                bg="#1a1a1a",
                wraplength=550
            )
            label.pack(pady=10)
            
            for i, resource in enumerate(resources, 1):
                def open_resource(url=resource):
                    webbrowser.open(url)
                
                resource_button = tk.Button(
                    frame,
                    text=f"Resource {i}: {resource[:50]}...",
                    font=("Arial", 10),
                    bg="#2b2b2b",
                    fg="#00ff00",
                    command=open_resource,
                    anchor=tk.W,
                    padx=10,
                    pady=10
                )
                resource_button.pack(fill=tk.X, pady=5)
            
            motivation_text = tk.Label(
                frame,
                text="\nGO LEARN! I'll be here when you're ready for a CHALLENGE!",
                font=("Arial", 11, "italic"),
                fg="#ffd93d",
                bg="#1a1a1a"
            )
            motivation_text.pack(pady=10)
            
        except IndexError:
            messagebox.showwarning("TUX SAYS:", "PICK A LANGUAGE FIRST!")

    def commit_to_language(self):
        """Student commits to learning a language"""
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index).replace("> ", "")
            
            if selected_language not in self.current_student.languages_started:
                self.current_student.languages_started.append(selected_language)
                self.current_student.update_motivation(10)
                
                messagebox.showinfo(
                    "COMMITMENT ACCEPTED!",
                    f"THAT'S WHAT I LIKE TO SEE!\n\n"
                    f"You've committed to learning {selected_language}!\n\n"
                    f"Now get to work and prove you're SERIOUS!\n\n"
                    f"Motivation: {int(self.current_student.motivation_level)}/100"
                )
            else:
                messagebox.showinfo(
                    "ALREADY COMMITTED",
                    f"You're ALREADY working on {selected_language}!\n"
                    f"Now FINISH what you STARTED!"
                )
                
        except IndexError:
            messagebox.showwarning("TUX SAYS:", "SELECT A LANGUAGE!")

    def generate_challenge(self):
        """Generate a coding challenge"""
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index).replace("> ", "")
            
            if selected_language not in self.challenge_templates:
                messagebox.showwarning("TUX SAYS:", f"I'm still building challenges for {selected_language}!")
                return
            
            challenges = self.challenge_templates[selected_language]
            challenge_name, challenge_desc, difficulty = random.choice(challenges)
            
            challenge_window = tk.Toplevel(self.root)
            challenge_window.title(f"{challenge_name} - {selected_language}")
            challenge_window.geometry("700x500")
            challenge_window.configure(bg='#1a1a1a')
            
            frame = tk.Frame(challenge_window, bg='#1a1a1a')
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Challenge header
            header_label = tk.Label(
                frame,
                text=f"{challenge_name} - {selected_language.upper()} ",
                font=("Arial", 16, "bold"),
                fg="#ff6b6b",
                bg="#1a1a1a"
            )
            header_label.pack(pady=10)
            
            # Difficulty indicator
            difficulty_colors = {"Easy": "#00ff00", "Medium": "#ffd93d", "Hard": "#ff6b6b"}
            difficulty_label = tk.Label(
                frame,
                text=f"Difficulty: {difficulty}",
                font=("Arial", 12, "bold"),
                fg=difficulty_colors.get(difficulty, "#ffffff"),
                bg="#1a1a1a"
            )
            difficulty_label.pack(pady=5)
            
            # Challenge description
            challenge_text = scrolledtext.ScrolledText(
                frame,
                height=12,
                width=80,
                font=("Courier", 11),
                bg="#2b2b2b",
                fg="#ffffff",
                wrap=tk.WORD
            )
            challenge_text.pack(fill=tk.BOTH, expand=True, pady=10)
            
            challenge_text.insert(tk.END, challenge_desc)
            challenge_text.config(state=tk.DISABLED)
            
            # Tux's motivation
            motivation_label = tk.Label(
                frame,
                text=self.tux_sergeant.get_motivational_speech("challenge"),
                font=("Arial", 11, "italic"),
                fg="#00ff00",
                bg="#1a1a1a",
                wraplength=650
            )
            motivation_label.pack(pady=10)
            
            # Action buttons
            button_frame = tk.Frame(frame, bg='#1a1a1a')
            button_frame.pack(fill=tk.X, pady=10)
            
            def accept_challenge():
                self.current_student.update_motivation(15)
                messagebox.showinfo(
                    "CHALLENGE ACCEPTED!",
                    f"NOW GET TO WORK!\n\n"
                    f"Complete this challenge and report back!\n"
                    f"NO EXCUSES!\n\n"
                    f"Motivation: {int(self.current_student.motivation_level)}/100"
                )
                challenge_window.destroy()
            
            accept_button = tk.Button(
                button_frame,
                text="ACCEPT CHALLENGE!",
                font=("Arial", 12, "bold"),
                bg="#ff6b6b",
                fg="#ffffff",
                command=accept_challenge,
                padx=20,
                pady=10
            )
            accept_button.pack(side=tk.LEFT, padx=5)
            
            skip_button = tk.Button(
                button_frame,
                text="Maybe Later",
                font=("Arial", 10),
                bg="#3b3b3b",
                fg="#ffffff",
                command=challenge_window.destroy,
                padx=15,
                pady=8
            )
            skip_button.pack(side=tk.LEFT, padx=5)
            
        except IndexError:
            messagebox.showwarning("TUX SAYS:", "PICK A LANGUAGE FIRST!")


def main():
    root = tk.Tk()
    app = TuxLanguageLearner(root)
    app.create_login_screen()
    root.mainloop()


if __name__ == "__main__":
    main()
