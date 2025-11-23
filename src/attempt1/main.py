import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import webbrowser

class TuxLanguageLearner:
    def __init__(self, root):
        self.root = root
        self.root.title("Tux Programming Boot Camp")
        self.root.geometry("1000x700")

        # Language Database
        self.languages = {
            "Python": {
                "description": "High-level, interpreted language known for readability and versatility.",
                "difficulty": "Beginner",
                "use_cases": ["Web Development", "Data Science", "AI/ML"],
                "sample_code": "print('Hello, Tux!')\ndef greet(name):\n    return f'Welcome, {name}!'",
                "learning_resources": [
                    "https://docs.python.org/3/tutorial/",
                    "https://www.codecademy.com/learn/learn-python-3"
                ]
            },
            "Rust": {
                "description": "Systems programming language focused on memory safety and concurrency.",
                "difficulty": "Advanced",
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
                "use_cases": ["Game Development", "High-Performance Applications", "System Software"],
                "sample_code": "#include <iostream>\nint main() {\n    std::cout << \"Hello, Tux!\" << std::endl;\n    return 0;\n}",
                "learning_resources": [
                    "https://www.learncpp.com/",
                    "https://www.cplusplus.com/doc/tutorial/"
                ]
            },
            "Assembly": {
                "description": "Low-level language that directly corresponds to machine instructions.",
                "difficulty": "Expert",
                "use_cases": ["Compiler Design", "Embedded Systems", "Reverse Engineering"],
                "sample_code": "; x86 Assembly Hello World\nsection .data\n    msg db 'Hello, Tux!', 0\n\nsection .text\n    global _start\n_start:\n    ; Output message\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, msg\n    mov edx, 12\n    int 0x80",
                "learning_resources": [
                    "https://www.cs.virginia.edu/~evans/cs216/guides/x86.html",
                    "https://www.assemblylanguagetuts.com/"
                ]
            },
            "Go": {
                "description": "Concurrent programming language developed by Google.",
                "difficulty": "Intermediate",
                "use_cases": ["Cloud Computing", "Network Programming", "Microservices"],
                "sample_code": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, Tux!\")\n}",
                "learning_resources":[
                      "https://go.dev/",
    '                  "https://www.freecodecamp.org/news/learn-golang-handbook/"
                ]
            "C#": {
                "description": "Microsoft's object-oriented language for .NET ecosystem.",
                "difficulty": "Intermediate",
                "use_cases": ["Windows Applications", "Game Development", "Enterprise Software"],
                "sample_code": "using System;\n\nclass TuxProgram {\n    static void Main() {\n        Console.WriteLine(\"Hello, Tux!\");\n    }\n}",
                "learning_resources": [
                    "https://docs.microsoft.com/en-us/dotnet/csharp/",
                    "https://www.codecademy.com/learn/learn-c-sharp"
                ]
            },
            "LOLCODE": {
                "description": "Esoteric programming language based on LOLcat internet meme.",
                "difficulty": "Novelty",
                "use_cases": ["Humor", "Esoteric Programming"],
                "sample_code": "HAI 1.2\n    CAN HAS STDIO?\n    VISIBLE \"HELLO TUX!\"\n    KTHXBYE",
                "learning_resources": [
                    "https://en.wikipedia.org/wiki/LOLCODE",
                    "https://github.com/justinmeza/lolcode-spec"
                ]
            },
            "Holy C": {
                "description": "Programming language created by Terry A. Davis for TempleOS.",
                "difficulty": "Unique",
                "use_cases": ["TempleOS Operating System", "Experimental Computing"],
                "sample_code": "void main() {\n    Print(\"Hello, Tux!\");\n}",
                "learning_resources": [
                    "https://www.templeos.org",
                    "https://en.wikipedia.org/wiki/TempleOS"
                ]
            },
            "INTERCAL": {
                "description": "Intentionally Complicated programming language designed to be absurd.",
                "difficulty": "Deliberately Difficult",
                "use_cases": ["Humor", "Esoteric Programming Challenge"],
                "sample_code": "DO ,1 <- #1\nPLEASE DO ,1 SUB #1 <- #1\nPLEASE DO ,1 SUB #2 <- #0\nDO COME FROM ,1\nPLEASE GIVE UP",
                "learning_resources": [
                    "https://www.muppetlabs.com/~breadbox/intercal/",
                    "https://en.wikipedia.org/wiki/INTERCAL"
                ]
            },
            "Shakespeare": {
                "description": "Esoteric programming language that looks like a Shakespearean play.",
                "difficulty": "Artistic Challenge",
                "use_cases": ["Artistic Programming", "Coding Creativity"],
                "sample_code": "The Awesome Program by Tux\n\nRomeo, a young programmer\nJuliet, a beautiful variable\n\nAct I: The Declaration\nRomeo: Thou art the square of my heart!\nJuliet: Speak thy mind, fair Romeo.\n\nRomeo: Open thy heart and be 5!\nJuliet: [Receives 5]",
                "learning_resources": [
                    "https://shakespearelang.sourceforge.net/",
                    "https://en.wikipedia.org/wiki/Shakespeare_Programming_Language"
                ]
            },
            "Rockstar": {
                "description": "Programming language designed to look like song lyrics.",
                "difficulty": "Creative",
                "use_cases": ["Artistic Coding", "Programmer Humor"],
                "sample_code": "Tux's Rockin' Program\n\nRock on, my heart!\nShout it out loud!\nRock on is as loud as the fire\nFire is 100\nYell Fire!\n\nKnock Fire down\nTake it to the top",
                "learning_resources": [
                    "https://github.com/RockstarLang/rockstar",
                    "https://esolangs.org/wiki/Rockstar"
                ]
            }
        }

    def create_main_interface(self):
        # Main window layout
        self.root.title("Tux Language Academy")
        
        # Language Selection Frame
        language_frame = tk.Frame(self.root)
        language_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Language Listbox
        self.language_listbox = tk.Listbox(language_frame, width=20, height=15)
        self.language_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Populate Listbox
        for language in self.languages.keys():
            self.language_listbox.insert(tk.END, language)
        
        # Bind selection event
        self.language_listbox.bind('<<ListboxSelect>>', self.show_language_details)
        
        # Details Frame
        details_frame = tk.Frame(self.root)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Language Name Label
        self.language_name_label = tk.Label(details_frame, text="Select a Language", font=("Arial", 18, "bold"))
        self.language_name_label.pack(pady=10)
        
        # Description Text
        self.description_text = tk.Text(details_frame, height=5, width=60, wrap=tk.WORD)
        self.description_text.pack(pady=10)
        
        # Code Sample Frame
        code_frame = tk.Frame(details_frame)
        code_frame.pack(pady=10)
        
        # Code Sample Label
        code_label = tk.Label(code_frame, text="Sample Code:", font=("Arial", 12, "bold"))
        code_label.pack()
        
        # Code Sample Text
        self.code_sample_text = tk.Text(code_frame, height=10, width=60, font=("Courier", 10))
        self.code_sample_text.pack()
        
        # Learning Resources Button
        resources_button = tk.Button(details_frame, text="Learning Resources", command=self.open_learning_resources)
        resources_button.pack(pady=10)
        
        # Challenge Generator Button
        challenge_button = tk.Button(details_frame, text="Generate Coding Challenge", command=self.generate_challenge)
        challenge_button.pack(pady=10)

    def show_language_details(self, event):
        # Get selected language
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index)
            
            # Update language name
            self.language_name_label.config(text=selected_language)
            
            # Clear previous text
            self.description_text.delete(1.0, tk.END)
            self.code_sample_text.delete(1.0, tk.END)
            
            # Get language details
            language_info = self.languages[selected_language]
            
            # Insert description
            self.description_text.insert(tk.END, f"Difficulty: {language_info['difficulty']}\n\n")
            self.description_text.insert(tk.END, language_info['description'])
            
            # Insert code
            for resource in resources:
                webbrowser.open(resource)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a language first.")

    def generate_challenge(self):
        # Get currently selected language
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index)
            
            # Challenges based on language difficulty
            challenges = {
                "Python": [
                    "Create a function that calculates Fibonacci sequence",
                    "Build a simple todo list application",
                    "Implement a basic calculator"
                ],
                "Rust": [
                    "Write a memory-safe data structure",
                    "Create a concurrent web scraper",
                    "Implement a basic networking tool"
                ],
                "C": [
                    "Create a dynamic memory allocation program",
                    "Implement a simple file encryption tool",
                    "Build a basic system monitoring utility"
                ],
                "C++": [
                    "Design an object-oriented game class",
                    "Create a template-based data structure",
                    "Implement a basic graphics rendering engine"
                ],
                "Assembly": [
                    "Write a simple mathematical operation in pure assembly",
                    "Create a basic input/output routine",
                    "Implement a low-level encryption algorithm"
                ],
                "Go": [
                    "Create a concurrent web server",
                    "Implement a basic microservice",
                    "Build a distributed key-value store"
                ],
                "C#": [
                    "Create a Windows desktop application",
                    "Implement a basic game using Unity",
                    "Build a CRUD application with .NET"
                ],
                "LOLCODE": [
                    "Write a program that can HAZ CHEEZBURGER",
                    "Create a meme generator in LOLCODE",
                    "Implement a silly calculator"
                ],
                "Holy C": [
                    "Create a simple graphics demo",
                    "Implement a basic system interrupt handler",
                    "Write a minimalist operating system routine"
                ],
                "INTERCAL": [
                    "Write a program that deliberately makes no sense",
                    "Create the most convoluted 'Hello World'",
                    "Implement a challenge that breaks all coding conventions"
                ],
                "Shakespeare": [
                    "Write a play that calculates fibonacci",
                    "Create a dramatic mathematical operation",
                    "Implement a character-driven algorithm"
                ],
                "Rockstar": [
                    "Compose a song that calculates prime numbers",
                    "Create a lyrical sorting algorithm",
                    "Write a rock ballad that solves a math problem"
                ]
            }
            
            # Select a random challenge
            challenge = random.choice(challenges.get(selected_language, 
                ["No challenges available for this language"]))
            
            # Create challenge window
            challenge_window = tk.Toplevel(self.root)
            challenge_window.title(f"{selected_language} Coding Challenge")
            challenge_window.geometry("500x300")
            
            # Challenge Details
            challenge_label = tk.Label(challenge_window, 
                text=f"Challenge for {selected_language}:", 
                font=("Arial", 14, "bold")
            )
            challenge_label.pack(pady=10)
            
            challenge_text = tk.Text(challenge_window, wrap=tk.WORD, height=10)
            challenge_text.insert(tk.END, challenge)
            challenge_text.config(state=tk.DISABLED)
            challenge_text.pack(padx=20, pady=10)
            
            # Accept Challenge Button
            def accept_challenge():
                # Open a code playground for the specific language
                self.open_language_specific_playground(selected_language)
                challenge_window.destroy()
            
            accept_button = tk.Button(challenge_window, 
                text="Accept Challenge", 
                command=accept_challenge
            )
            accept_button.pack(pady=10)
        
        except IndexError:
            messagebox.showwarning("Warning", "Please select a language first.")

    def open_language_specific_playground(self, language):
        # Create a specialized coding environment for each language
        playground_window = tk.Toplevel(self.root)
        playground_window.title(f"{language} Playground")
        playground_window.geometry("800x600")

        # Code input area
        code_frame = tk.Frame(playground_window)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        code_label = tk.Label(code_frame, text=f"Write Your {language} Code:")
        code_label.pack()

        code_text = tk.Text(code_frame, height=15, width=80, font=("Courier", 10))
        code_text.pack(padx=10, pady=10)

        # Output area
        output_frame = tk.Frame(playground_window)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        output_label = tk.Label(output_frame, text="Output:")
        output_label.pack()

        output_text = tk.Text(output_frame, height=5, width=80, state='disabled')
        output_text.pack(padx=10, pady=10)

        # Language-specific execution methods
        def run_code():
            output_text.config(state='normal')
            output_text.delete(1.0, tk.END)

            # Placeholder for language-specific execution
            # In a real-world scenario, you'd need more sophisticated 
            # execution environments for each language
            try:
                if language == "Python":
                    # Python execution
                    import sys
                    from io import StringIO
                    old_stdout = sys.stdout
                    redirected_output = sys.stdout = StringIO()

                    exec(code_text.get("1.0", tk.END))
        # Add menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Playground", command=self.create_main_interface)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Tutorial", command=self.launch_tutorial)
        help_menu.add_command(label="About", command=self.show_about)

        # Splash screen or welcome message
        self.show_welcome_screen()

    def show_about(self):
        # Create an about dialog
        about_window = tk.Toplevel(self.root)
        about_window.title("About Tux Language Academy")
        about_window.geometry("500x300")

        about_text = tk.Text(about_window, wrap=tk.WORD)
        about_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        about_content = """
        Tux Language Academy v1.0

        A Comprehensive Programming Language Learning Environment

        Created to explore and learn:
        - Python
        - Rust
        - C
        - C++
        - Assembly
        - Go
        - C#
        - LOLCODE
        - Holy C
        - INTERCAL
        - Shakespeare
        - Rockstar

        Features:
        - Interactive Language Explorer
        - Sample Code Demonstrations
        - Learning Resources
        - Coding Challenges
        - Language-Specific Playgrounds

        Developed with passion for programming education
        and linguistic diversity in coding.

        Inspired by the spirit of open-source learning
        and the creativity of programming languages.
        """

        about_text.insert(tk.END, about_content)
        about_text.config(state=tk.DISABLED)

    def show_welcome_screen(self):
        # Create a welcome screen
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Tux Language Academy")
        welcome_window.geometry("600x400")

        # Welcome message
        welcome_label = tk.Label(
            welcome_window, 
            text="Tux Language Academy", 
            font=("Arial", 24, "bold")
        )
        welcome_label.pack(pady=20)

        # Description
        desc_label = tk.Label(
            welcome_window, 
            text="Explore the Fascinating World of Programming Languages",
            font=("Arial", 14)
        )
        desc_label.pack(pady=10)

        # Welcome image (placeholder)
        try:g platforms from one code-base. It is free and open-source software, released under an MIT License. The compiler is written in OCaml. It can be 
            from PIL import Image, ImageTk
            # You would need to have a Tux or programming-related image
            image = Image.open("tux_logo.png")  # Replace with actual path
            photo = ImageTk.PhotoImage(image.resize((200, 200)))
            image_label = tk.Label(welcome_window, image=photo)
            image_label.image = photo  # Keep a reference
            image_label.pack(pady=20)
        except ImportError:
            # Fallback if PIL is not available
            tk.Label(welcome_window, text="🐧 Tux Welcomes You!", font=("Arial", 16)).pack(pady=20)

        # Start Exploring Button
        def start_exploring():
            welcome_window.destroy()

        start_button = tk.Button(
            welcome_window, 
            text="Start Exploring Languages", 
            command=start_exploring,
            width=20,
            height=2
        )
        start_button.pack(pady=20)

def main():
    root = tk

                    sys.stdout = old_stdout
                    output = redirected_output.getvalue()
                    output_text.insert(tk.END, output)
                else:
                    output_text.insert(tk.END, 
                        f"Live {language} execution not supported in this demo.\n"
                        "This would require language-specific compilers/interpreters."
                    )
            except Exception as e:
                output_text.insert(tk.END, f"Error: {str(e)}")

            output_text.config(state='disabled')

        # Run Code Button
        run_button = tk.Button(playground_window, text="Run Code", command=run_code)
        run_button.pack(pady=10)

    def launch_tutorial(self):
        # Create a tutorial window
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("Tux Language Academy Tutorial")
        tutorial_window.geometry("600x400")

        tutorial_text = tk.Text(tutorial_window, wrap=tk.WORD)
        tutorial_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tutorial_content = """
        Welcome to Tux Language Academy!

        How to Use the Application:
        1. Select a programming language from the left sidebar
        2. View language details in the main window
        3. Explore sample code and learning resources
        4. Generate coding challenges
        5. Practice in the language-specific playground

        Each language has unique characteristics:
        - Some are practical (Python, C++)
        - Some are experimental (Shakespeare, LOLCODE)
        - Some are system-level (Rust, C)

        Explore, learn, and have fun programming!
        """

        tutorial_text.insert(tk.END, tutorial_content)
        tutorial_text.config(state=tk.DISABLED)

    def run(self):
        # Create the main interface
        self.create_main_interface()

        # Add menu bar
        menubar = tk.Menu(self.
        # Add menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Playground", command=self.create_main_interface)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Tutorial", command=self.launch_tutorial)
        help_menu.add_command(label="About", command=self.show_about)

        # Splash screen or welcome message
        self.show_welcome_screen()

    def show_about(self):
        # Create an about dialog
        about_window = tk.Toplevel(self.root)
        about_window.title("About Tux Language Academy")
        about_window.geometry("500x300")

        about_text = tk.Text(about_window, wrap=tk.WORD)
        about_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        about_content = """
        Tux Language Academy v1.0

        A Comprehensive Programming Language Learning Environment

        Created to explore and learn:
        - Python
        - Rust
        - C
        - C++
        - Assembly
        - Go
        - C#
        - LOLCODE
        - Holy C
        - INTERCAL
        - Shakespeare
        - Rockstar

        Features:
        - Interactive Language Explorer
        - Sample Code Demonstrations
        - Learning Resources
        - Coding Challenges
        - Language-Specific Playgrounds

        Developed with passion for programming education
        and linguistic diversity in coding.

        Inspired by the spirit of open-source learning
        and the creativity of programming languages.
        """

        about_text.insert(tk.END, about_content)
        about_text.config(state=tk.DISABLED)

    def show_welcome_screen(self):
        # Create a welcome screen
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Tux Language Academy")
        welcome_window.geometry("600x400")

        # Welcome message
        welcome_label = tk.Label(
            welcome_window, 
            text="Tux Language Academy", 
            font=("Arial", 24, "bold")
        )
        welcome_label.pack(pady=20)

        # Description
        desc_label = tk.Label(
            welcome_window, 
            text="Explore the Fascinating World of Programming Languages",
            font=("Arial", 14)
        )
        desc_label.pack(pady=10)

        # Welcome image (placeholder)
        try:
            from PIL import Image, ImageTk
            # You would need to have a Tux or programming-related image
            image = Image.open("tux_logo.png")  # Replace with actual path
            photo = ImageTk.PhotoImage(image.resize((200, 200)))
            image_label = tk.Label(welcome_window, image=photo)
            image_label.image = photo  # Keep a reference
            image_label.pack(pady=20)
        except ImportError:
            # Fallback if PIL is not available
            tk.Label(welcome_window, text="🐧 Tux Welcomes You!", font=("Arial", 16)).pack(pady=20)

        # Start Exploring Button
        def start_exploring():
            welcome_window.destroy()

        start_button = tk.Button(
            welcome_window, 
            text="Start Exploring Languages", 
            command=start_exploring,
            width=20,
            height=2
        )
        start_button.pack(pady=20)

def main():
    root = tk.Tk()
    root.title("Tux Language Academy")
    root.geometry("1200x800")

    # Set up application icon (if possible)
    try:
        root.iconbitmap('tux_icon.ico')  # Windows
    except:
        try:
            img = tk.PhotoImage(file='tux_icon.png')  # Cross-platform fallback
            root.tk.call('wm', 'iconphoto', root._w, img)
        except:
            pass  # Icon setting is optional

    # Create application instance
    app = TuxLanguageLearner(root)
    
    # Run the application
    app.run()
    
    # Start the Tkinter event loop
    root.mainloop()

# Dependency Check and Installation Helper
def check_dependencies():
    dependencies = [
        'tkinter',
        'PIL',  # Pillow for image handling
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print("Missing dependencies detected:")
        for dep in missing_deps:
            print(f"- {dep}")
        
        print("\nAttempting to install dependencies...")
        
        try:
            import sys
            import subprocess
            
            # Attempt to install missing dependencies
            for dep in missing_deps:
                if dep == 'PIL':
                    dep = 'pillow'
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            
            print("Dependencies successfully installed!")
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            print("Please install manually using pip:")
            for dep in missing_deps:
                print(f"pip install {dep}")
            sys.exit(1)

# Logging and Error Handling
import logging
import traceback

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='tux_language_academy.log'
    )

def global_exception_handler(exctype, value, tb):
    """
    Global exception handler to log unexpected errors
    """
    logging.error("Uncaught exception", exc_info=(exctype, value, tb))
    
    # Print to console for immediate visibility
    print("An unexpected error occurred:")
    traceback.print_exception(exctype, value, tb)
    
    # Optional: Show user-friendly error dialog
    tk.messagebox.showerror(
        "Unexpected Error", 
        "An unexpected error occurred. Please check the log file."
    )

# Main execution
if __name__ == "__main__":
    # Set up logging
    setup_logging()
    
    # Check and install dependencies
    check_dependencies()
    
    # Set global exception handler
    import sys
    sys.excepthook = global_exception_handler
    
    try:
        # Run the main application
        main()
    except Exception as e:
        logging.error(f"Critical error in main application: {e}")
        print(f"Critical error: {e}")
        traceback.print_exc()

