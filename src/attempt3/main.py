import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import webbrowser
import os
from datetime import datetime
from enum import Enum

"""
TUX CODE BOOT CAMP - With AI Code Analysis

REQUIREMENTS:
pip install aiohttp

This application uses the Ollama api to grade students

FEATURES:
- AI-powered code analysis using Claude Sonnet 4
- Emotional feedback from Sergeant Tux based on code quality
- Automatic file creation for challenges
- Real-time motivation tracking
- Multi-language support
"""

# =====================================================================
# ENUMS AND DATA CLASSES
# =====================================================================


class DrillLevel(Enum):
    """Tuxs motivation intensity levels"""

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
        self.completion_attempts = {}
        self.decision_struggle_count = 0
        self.last_session = None
        self.motivation_level = 50
        self.streak_days = 0

    def update_motivation(self, change):
        """Update motivation level based on actions"""
        self.motivation_level = max(0, min(100, self.motivation_level + change))

    def get_tux_phrase(self):
        """Get motivational phrase based on progress and struggle"""
        if self.motivation_level < 20:
            return random.choice(
                [
                    "Listen up recruit! I've seen QUITTERS before, but you're testing my patience!",
                    "Your motivation is in the GUTTER! Time to get your head back in the GAME!",
                    "I didn't leave the Marines to train COWARDS! STEP UP!",
                ]
            )
        elif self.motivation_level < 50:
            return random.choice(
                [
                    "You're getting there, soldier! But we need MORE FIRE!",
                    "That's a START, but I expect EXCELLENCE!",
                    "Stop dragging your feet! Let's pick up the PACE!",
                ]
            )
        elif self.motivation_level < 80:
            return random.choice(
                [
                    "NOW WE'RE TALKING! That's the attitude I want to see!",
                    "I like your style, recruit! Keep that energy UP!",
                    "You're starting to understand what it takes!",
                ]
            )
        else:
            return random.choice(
                [
                    "THAT'S WHAT I'M TALKING ABOUT! You're a MACHINE!",
                    "You've got the FIRE, recruit! Keep BURNING!",
                    "Outstanding! You're showing TRUE DEDICATION!",
                ]
            )


# =====================================================================
# AI CODE ANALYZER
# =====================================================================


class CodeAnalyzer:
    """Uses Claude API to analyze student code submissions"""

    def __init__(self):
        self.api_url = "https://api.anthropic.com/v1/messages"

    async def analyze_code(self, language, challenge_desc, student_code):
        """Analyze student code and provide feedback"""
        try:
            import aiohttp
            import asyncio

            prompt = self._build_analysis_prompt(language, challenge_desc, student_code)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1000,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                ) as response:
                    data = await response.json()

                    if response.status != 200:
                        return self._create_error_result(data)

                    return self._parse_ai_response(data)

        except Exception as e:
            return {
                "success": False,
                "correct": False,
                "feedback": f"Analysis error: {str(e)}",
                "tux_emotion": "confused",
            }

    def _build_analysis_prompt(self, language, challenge_desc, student_code):
        """Build the prompt for code analysis"""
        return f"""You are Sergeant Tux analyzing recruit code for a programming boot camp. 

CHALLENGE: {challenge_desc}
LANGUAGE: {language}

STUDENT CODE:
```{language.lower()}
{student_code}
```

Analyze this code and respond in this EXACT JSON format:
{{
    "correct": true/false,
    "completeness": 0-100,
    "quality_score": 0-100,
    "overachiever": true/false,
    "issues": ["issue1", "issue2"],
    "strengths": ["strength1", "strength2"],
    "suggestions": ["suggestion1", "suggestion2"],
    "summary": "brief summary"
}}

IMPORTANT ANALYSIS CRITERIA:
1. Does it meet or EXCEED the challenge requirements?
2. If the student went BEYOND requirements (added error handling, additional features, better practices), they are an OVERACHIEVER
3. Award high scores (90+) for code that exceeds expectations
4. Check syntax and functionality
5. Recognize professional practices (error handling, input validation, memory safety, good naming)

Be tough but FAIR. Recognize excellence when you see it. If a recruit went above and beyond, they deserve HIGH MARKS!

If the challenge is "beginner" level but the code shows "intermediate" or "advanced" practices, this is OUTSTANDING and should score 95+.
    """

    def _parse_ai_response(self, data):
        """Parse AI response into usable format"""
        try:
            content = data.get("content", [])
            text = ""

            for block in content:
                if block.get("type") == "text":
                    text += block.get("text", "")

            # Clean up potential markdown formatting
            text = text.strip()
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()

            import json

            analysis = json.loads(text)

            # Determine Tux's emotion based on results
            emotion = self._determine_tux_emotion(analysis)

            return {
                "success": True,
                "correct": analysis.get("correct", False),
                "completeness": analysis.get("completeness", 0),
                "quality_score": analysis.get("quality_score", 0),
                "issues": analysis.get("issues", []),
                "strengths": analysis.get("strengths", []),
                "suggestions": analysis.get("suggestions", []),
                "summary": analysis.get("summary", ""),
                "tux_emotion": emotion,
            }

        except Exception as e:
            return self._create_error_result({"error": str(e)})

    def _determine_tux_emotion(self, analysis):
        # Determine Tux's emotional response based on code quality"""
        correct = analysis.get("correct", False)
        completeness = analysis.get("completeness", 0)
        quality = analysis.get("quality_score", 0)
        overachiever = analysis.get("overachiever", False)

        # Special recognition for overachievers
        if overachiever or (correct and quality >= 95):
            return "exceptional"  # New top tier!
        elif correct and completeness >= 90 and quality >= 80:
            return "proud"
        elif correct and completeness >= 70:
            return "satisfied"
        elif completeness >= 50:
            return "encouraging"
        elif completeness >= 30:
            return "stern"
        else:
            return "disappointed"

    def _create_error_result(self, error_data):
        """Create error result"""
        return {
            "success": False,
            "correct": False,
            "feedback": f"Could not analyze code: {error_data}",
            "tux_emotion": "confused",
        }


# =====================================================================
# FILE MANAGEMENT
# =====================================================================


class ChallengeFileManager:
    """Handles creation and management of challenge files"""

    EXTENSIONS = {
        "Python": ".py",
        "JavaScript": ".js",
        "Go": ".go",
        "Rust": ".rs",
        "C": ".c",
        "C++": ".cpp",
        "Assembly": ".asm",
        "C#": ".cs",
        "LOLCODE": ".lol",
        "Holy C": ".hc",
        "INTERCAL": ".i",
        "Shakespeare": ".spl",
        "Rockstar": ".rock",
    }

    COMMENT_STYLES = {
        "Python": ("#", "#"),
        "JavaScript": ("//", "//"),
        "Go": ("//", "//"),
        "Rust": ("//", "//"),
        "C": ("//", "//"),
        "C++": ("//", "//"),
        "Assembly": (";", ";"),
        "C#": ("//", "//"),
        "LOLCODE": ("BTW", "BTW"),
        "Holy C": ("//", "//"),
        "INTERCAL": ("NOTE", "NOTE"),
        "Shakespeare": ("", ""),
        "Rockstar": ("(", ")"),
    }

    def __init__(self, base_directory="TuxBootCamp_Challenges"):
        self.base_directory = base_directory
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Create challenges directory if it doesn't exist"""
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)

    def create_challenge_file(
        self, language, challenge_name, challenge_desc, difficulty, student_name
    ):
        """Create a new file with function headers and comments"""
        filename = self._generate_filename(challenge_name, language)
        content = self._generate_content(
            language, challenge_name, challenge_desc, difficulty, student_name
        )

        filepath = os.path.join(self.base_directory, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def _generate_filename(self, challenge_name, language):
        """Generate a safe filename for the challenge"""
        safe_name = challenge_name.replace(" ", "_").replace(":", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = self.EXTENSIONS.get(language, ".txt")
        return f"{safe_name}_{timestamp}{extension}"

    def _generate_content(
        self, language, challenge_name, challenge_desc, difficulty, student_name
    ):
        """Generate file content based on language"""
        comment_start, _ = self.COMMENT_STYLES.get(language, ("#", "#"))

        header = self._generate_header(
            comment_start,
            student_name,
            challenge_name,
            language,
            difficulty,
            challenge_desc,
        )

        template = self._get_language_template(language, comment_start)

        return header + template

    def _generate_header(self, comment, student, challenge, language, difficulty, desc):
        """Generate file header with challenge information"""
        return f"""{comment}{'=' * 70}
{comment} TUX CODE BOOT CAMP - CHALLENGE FILE
{comment} {'=' * 70}
{comment} Recruit: {student}
{comment} Challenge: {challenge}
{comment} Language: {language}
{comment} Difficulty: {difficulty}
{comment} Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{comment} {'=' * 70}
{comment}
{comment} MISSION BRIEFING:
{comment} {desc}
{comment}
{comment} YOUR ORDERS:
{comment} 1. Read the mission briefing carefully
{comment} 2. Complete the function implementation below
{comment} 3. Test your code thoroughly
{comment} 4. Report back to Sergeant Tux when complete!
{comment}
{comment} REMEMBER: Comments are your BATTLE PLAN! Use them!
{comment} {'=' * 70}

"""

    def _get_language_template(self, language, comment):
        """Get language-specific code template"""
        templates = {
            "Python": self._python_template,
            "JavaScript": self._javascript_template,
            "Go": self._go_template,
            "Rust": self._rust_template,
            "C": self._c_template,
            "C++": self._cpp_template,
            "C#": self._csharp_template,
            "Assembly": self._assembly_template,
            "LOLCODE": self._lolcode_template,
        }

        template_func = templates.get(
            language, lambda c: self._generic_template(language, c)
        )
        return template_func(comment)

    def _python_template(self, comment):
        return """
def main():
    \"\"\"
    Main function - This is where your code execution begins!
    Purpose: Implement the challenge requirements here
    \"\"\"
    # TODO: Write your code here, recruit!
    pass


def helper_function():
    \"\"\"
    Helper function - Break down complex problems into smaller pieces!
    Purpose: Add any helper functions you need
    \"\"\"
    # TODO: Implement helper logic
    pass


if __name__ == "__main__":
    main()
    
# SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _javascript_template(self, comment):
        return """
// Main function - This is your entry point!
// Purpose: Implement the challenge requirements here
function main() {
    // TODO: Write your code here, recruit!
    
}

// Helper function - Break it down into manageable pieces!
// Purpose: Add any helper functions you need
function helperFunction() {
    // TODO: Implement helper logic
    
}

// Execute main function
main();

// SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _go_template(self, comment):
        return """
package main

import "fmt"

// main - This is your entry point!
// Purpose: Implement the challenge requirements here
func main() {
    // TODO: Write your code here, recruit!
    fmt.Println("Challenge started!")
    
}

// helperFunction - Break it down into manageable pieces!
// Purpose: Add any helper functions you need
func helperFunction() {
    // TODO: Implement helper logic
    
}

// SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _rust_template(self, comment):
        return """
// main - This is your entry point!
// Purpose: Implement the challenge requirements here
fn main() {
    // TODO: Write your code here, recruit!
    println!("Challenge started!");
    
}

// helper_function - Break it down into manageable pieces!
// Purpose: Add any helper functions you need
fn helper_function() {
    // TODO: Implement helper logic
    
}

// SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _c_template(self, comment):
        return """
#include <stdio.h>

// main - This is your entry point!
// Purpose: Implement the challenge requirements here
int main() {
    // TODO: Write your code here, recruit!
    printf("Challenge started!\\n");
    
    return 0;
}

// helperFunction - Break it down into manageable pieces!
// Purpose: Add any helper functions you need
void helperFunction() {
    // TODO: Implement helper logic
    
}

// SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _cpp_template(self, comment):
        return """
#include <iostream>
using namespace std;

// main - This is your entry point!
// Purpose: Implement the challenge requirements here
int main() {
    // TODO: Write your code here, recruit!
    cout << "Challenge started!" << endl;
    
    return 0;
}

// helperFunction - Break it down into manageable pieces!
// Purpose: Add any helper functions you need
void helperFunction() {
    // TODO: Implement helper logic
    
}

// SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _csharp_template(self, comment):
        return """
using System;

class TuxChallenge
{
    // Main - This is your entry point!
    // Purpose: Implement the challenge requirements here
    static void Main()
    {
        // TODO: Write your code here, recruit!
        Console.WriteLine("Challenge started!");
        
    }
    
    // HelperFunction - Break it down into manageable pieces!
    // Purpose: Add any helper functions you need
    static void HelperFunction()
    {
        // TODO: Implement helper logic
        
    }
}

// SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _assembly_template(self, comment):
        return """
section .data
    ; Data section - Define your variables here
    msg db 'Challenge started!', 0xA
    len equ $ - msg

section .bss
    ; BSS section - Uninitialized data

section .text
    global _start

; Main entry point
; Purpose: Implement the challenge requirements here
_start:
    ; TODO: Write your code here, recruit!
    
    ; Exit program
    mov eax, 1
    xor ebx, ebx
    int 0x80

; Helper function - Break it down into manageable pieces!
; Purpose: Add any helper functions you need
helper_function:
    ; TODO: Implement helper logic
    ret

; SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _lolcode_template(self, comment):
        return """
HAI 1.2
    CAN HAS STDIO?
    
    BTW Main function - This is your entry point!
    BTW Purpose: Implement the challenge requirements here
    
    VISIBLE "Challenge started!"
    
    BTW TODO: Write your code here, recruit!
    
    
    BTW Helper section - Break it down!
    BTW Purpose: Add any helper logic you need
    
    
KTHXBYE

BTW SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def _generic_template(self, language, comment):
        return f"""
{comment} Main function - This is your entry point!
{comment} Purpose: Implement the challenge requirements here

{comment} TODO: Write your code here, recruit!


{comment} Helper function - Break it down into manageable pieces!

{comment} TODO: Implement helper logic


{comment} SERGEANT TUX SAYS: "Show me what you've got, recruit!"
"""

    def open_file(self, filepath):
        """Open file in default editor"""
        try:
            if os.name == "nt":  # Windows
                os.startfile(filepath)
            elif os.name == "posix":  # macOS and Linux
                os.system(
                    f'open "{filepath}"'
                    if os.uname().sysname == "Darwin"
                    else f'xdg-open "{filepath}"'
                )
        except Exception as e:
            raise Exception(f"Could not open file: {str(e)}")


# =====================================================================
# LANGUAGE DATA REPOSITORY
# =====================================================================


class LanguageRepository:
    """Stores and manages programming language data"""

    def __init__(self):
        self.languages = {
            "Python": {
                "description": "High-level, interpreted language known for readability and versatility.",
                "difficulty": "Beginner",
                "drill_sergeant_take": "PERFECT for BEGINNERS! Easy to READ but don't let that make you LAZY!",
                "use_cases": ["Web Development", "Data Science", "AI/ML"],
                "sample_code": "print('Hello, Tux!')\ndef greet(name):\n    return f'Welcome, {name}!'",
                "learning_resources": [
                    "https://docs.python.org/3/tutorial/",
                    "https://www.codecademy.com/learn/learn-python-3",
                ],
            },
            "JavaScript": {
                "description": "The language of the WEB! If you want to make things MOVE, this is IT!",
                "difficulty": "Beginner-Intermediate",
                "drill_sergeant_take": "JavaScript is EVERYWHERE! Master this and you can CONQUER the web!",
                "use_cases": ["Web Development", "Frontend", "Full Stack"],
                "sample_code": "console.log('Hello, Tux!');\nfunction greet(name) {\n    return `Welcome, ${name}!`;\n}",
                "learning_resources": [
                    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                    "https://www.codecademy.com/learn/learn-javascript",
                ],
            },
            "Go": {
                "description": "Concurrent programming language developed by Google.",
                "difficulty": "Intermediate",
                "drill_sergeant_take": "Go is LEAN, MEAN, and gets the JOB DONE! Learn this and you're UNSTOPPABLE!",
                "use_cases": [
                    "Cloud Computing",
                    "Network Programming",
                    "Microservices",
                ],
                "sample_code": 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, Tux!")\n}',
                "learning_resources": [
                    "https://go.dev/",
                    "https://www.freecodecamp.org/news/learn-golang-handbook/",
                ],
            },
            "Rust": {
                "description": "Systems programming language focused on memory safety and concurrency.",
                "difficulty": "Advanced",
                "drill_sergeant_take": "RUST is for SOLDIERS! The COMPILER will YELL at you just like I do!",
                "use_cases": ["Systems Programming", "WebAssembly", "Network Services"],
                "sample_code": 'fn main() {\n    println!("Hello, Tux!");\n    let greeting = String::from("Rust is awesome");\n}',
                "learning_resources": [
                    "https://doc.rust-lang.org/book/",
                    "https://rustlings.cool/",
                ],
            },
            "C": {
                "description": "Low-level systems programming language with direct hardware access.",
                "difficulty": "Advanced",
                "drill_sergeant_take": "C is the FOUNDATION! Learn this and you'll understand EVERYTHING!",
                "use_cases": [
                    "Operating Systems",
                    "Embedded Systems",
                    "Performance-critical Applications",
                ],
                "sample_code": '#include <stdio.h>\n\nint main() {\n    printf("Hello, Tux!\\n");\n    return 0;\n}',
                "learning_resources": [
                    "https://www.learn-c.org/",
                    "https://cplusplus.com/doc/tutorial/",
                ],
            },
            "C++": {
                "description": "Object-oriented systems programming language with high performance.",
                "difficulty": "Advanced",
                "drill_sergeant_take": "C++ is the ADVANCED TRAINING! You ready for this?!",
                "use_cases": [
                    "Game Development",
                    "High-Performance Applications",
                    "System Software",
                ],
                "sample_code": '#include <iostream>\nint main() {\n    std::cout << "Hello, Tux!" << std::endl;\n    return 0;\n}',
                "learning_resources": [
                    "https://www.learncpp.com/",
                    "https://www.cplusplus.com/doc/tutorial/",
                ],
            },
            "Assembly": {
                "description": "Low-level language that directly corresponds to machine instructions.",
                "difficulty": "Expert",
                "drill_sergeant_take": "ASSEMBLY is for the ELITE SOLDIERS! This is where the REAL WORK gets done!",
                "use_cases": [
                    "Compiler Design",
                    "Embedded Systems",
                    "Reverse Engineering",
                ],
                "sample_code": "section .data\n    msg db 'Hello, Tux!', 0\nsection .text\n    global _start\n_start:\n    mov eax, 1\n    mov ebx, 0",
                "learning_resources": [
                    "https://www.cs.virginia.edu/~evans/cs216/guides/x86.html",
                    "https://www.assemblylanguagetuts.com/",
                ],
            },
            "C#": {
                "description": "Microsoft's object-oriented language for .NET ecosystem.",
                "difficulty": "Intermediate",
                "drill_sergeant_take": "C# is POWERFUL and MODERN! Microsoft BUILT this for PROFESSIONALS!",
                "use_cases": [
                    "Windows Applications",
                    "Game Development",
                    "Enterprise Software",
                ],
                "sample_code": 'using System;\n\nclass TuxProgram {\n    static void Main() {\n        Console.WriteLine("Hello, Tux!");\n    }\n}',
                "learning_resources": [
                    "https://docs.microsoft.com/en-us/dotnet/csharp/",
                    "https://www.codecademy.com/learn/learn-c-sharp",
                ],
            },
            "LOLCODE": {
                "description": "Esoteric programming language based on LOLcat internet meme.",
                "difficulty": "Novelty",
                "drill_sergeant_take": "LOLCODE is UNCONVENTIONAL! It teaches you to THINK DIFFERENT and HAVE FUN!",
                "use_cases": ["Humor", "Esoteric Programming", "Creative Coding"],
                "sample_code": 'HAI 1.2\n    CAN HAS STDIO?\n    VISIBLE "HELLO TUX!"\n    KTHXBYE',
                "learning_resources": [
                    "https://en.wikipedia.org/wiki/LOLCODE",
                    "https://github.com/justinmeza/lolcode-spec",
                ],
            },
            "Holy C": {
                "description": "Programming language created by Terry A. Davis for TempleOS.",
                "difficulty": "Unique",
                "drill_sergeant_take": "Holy C is EXPERIMENTAL! It's for the VISIONARIES willing to explore!",
                "use_cases": [
                    "TempleOS Operating System",
                    "Experimental Computing",
                    "System Design",
                ],
                "sample_code": 'void main() {\n    Print("Hello, Tux!");\n}',
                "learning_resources": [
                    "https://www.templeos.org",
                    "https://en.wikipedia.org/wiki/TempleOS",
                ],
            },
            "INTERCAL": {
                "description": "Intentionally Complicated programming language designed to be absurd.",
                "difficulty": "Deliberately Difficult",
                "drill_sergeant_take": "INTERCAL is a CHALLENGE like no other! MASTER this and you can MASTER anything!",
                "use_cases": [
                    "Humor",
                    "Esoteric Programming Challenge",
                    "Mental Exercise",
                ],
                "sample_code": "DO ,1 <- #1\nPLEASE DO ,1 SUB #1 <- #1\nPLEASE DO ,1 SUB #2 <- #0\nDO COME FROM ,1",
                "learning_resources": [
                    "https://www.muppetlabs.com/~breadbox/intercal/",
                    "https://en.wikipedia.org/wiki/INTERCAL",
                ],
            },
            "Shakespeare": {
                "description": "Esoteric programming language that looks like a Shakespearean play.",
                "difficulty": "Artistic Challenge",
                "drill_sergeant_take": "SHAKESPEARE is ART meets CODE! Show me your CREATIVITY, recruit!",
                "use_cases": [
                    "Artistic Programming",
                    "Coding Creativity",
                    "Theatrical Expression",
                ],
                "sample_code": "Romeo, a young programmer.\nJuliet, a beautiful variable.\n\nRomeo: Thou art the sum of a proud strong lord!",
                "learning_resources": [
                    "https://shakespearelang.sourceforge.net/",
                    "https://en.wikipedia.org/wiki/Shakespeare_Programming_Language",
                ],
            },
            "Rockstar": {
                "description": "Programming language designed to look like song lyrics.",
                "difficulty": "Creative",
                "drill_sergeant_take": "ROCKSTAR is MUSIC meets CODE! If you can COMPOSE, you can PROGRAM!",
                "use_cases": [
                    "Artistic Coding",
                    "Programmer Humor",
                    "Musical Expression",
                ],
                "sample_code": "Rock on, my heart!\nShout it out loud!\nRock on is as loud as the fire\nFire is 100",
                "learning_resources": [
                    "https://github.com/RockstarLang/rockstar",
                    "https://esolangs.org/wiki/Rockstar",
                ],
            },
        }

        self.challenge_templates = {
            "Python": [
                (
                    "BEGINNER DRILL",
                    "Implement a Fibonacci sequence generator with  memorization using decorators",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Build a CLI todo app with SQLite persistence and CRUD operations",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Create a multi-threaded web scraper with proxy rotation and rate limiting",
                    "Hard",
                ),
            ],
            "JavaScript": [
                (
                    "BEGINNER DRILL",
                    "Build form validation with regex patterns and real-time error feedback",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create PWA with Service Workers and IndexedDB for offline functionality",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Develop real-time collaborative editor using WebSockets and Operational Transformation",
                    "Hard",
                ),
            ],
            "Go": [
                (
                    "BEGINNER DRILL",
                    "Build HTTP server with Gorilla Mux and middleware for request logging",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create concurrent prime number generator with worker pools",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Implement REST API with JWT authentication and rate limiting",
                    "Hard",
                ),
            ],
            "Rust": [
                (
                    "BEGINNER DRILL",
                    "Create safe calculator with compile-time validation of arithmetic operations",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Build async web crawler with Tokio and Serde for JSON parsing",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Implement thread-safe LRU cache using crossbeam and parking_lot",
                    "Hard",
                ),
            ],
            "C": [
                (
                    "BEGINNER DRILL",
                    "Implement binary calculator with stack-based expression evaluation",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create memory-managed dynamic array with custom realloc implementation",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Build AES-128 ECB encryption utility with hex encoding/decoding",
                    "Hard",
                ),
            ],
            "C++": [
                (
                    "BEGINNER DRILL",
                    "Design polymorphic game entity system with virtual inheritance",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Implement template metaprogramming for compile-time factorial calculation",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Create OpenGL-based 2D renderer with texture atlases and shaders",
                    "Hard",
                ),
            ],
            "Assembly": [
                (
                    "BEGINNER DRILL",
                    "Implement stack-based arithmetic operations in 64-bit x86 assembly",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create system call-based file copier with buffer management",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Implement RSA encryption/decryption in pure assembly",
                    "Hard",
                ),
            ],
            "C#": [
                (
                    "BEGINNER DRILL",
                    "Build WPF calculator with MVVM pattern and data binding",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create file synchronization utility with ZIP compression",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Develop multiplayer networked game with SignalR and concurrency control",
                    "Hard",
                ),
            ],
            "LOLCODE": [
                (
                    "BEGINNER DRILL",
                    "Create program that outputs 'Hello, World!' with ASCII art",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Build meme generator that combines text and image operations",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Implement calculator with custom LOLCODE math syntax parser",
                    "Hard",
                ),
            ],
            "Holy C": [
                (
                    "BEGINNER DRILL",
                    "Create VGA mode 13h graphics demo with pixel plotting",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Implement interrupt-driven keyboard handler in real mode",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Write bootloader that loads and executes a simple OS kernel",
                    "Hard",
                ),
            ],
            "INTERCAL": [
                (
                    "BEGINNER DRILL",
                    "Write 'Hello, World!' using COME FROM and SUB instruction",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create program that uses . and ? for input/output in non-standard ways",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Implement obfuscated algorithm with maximum use of INTERCAL's esoteric features",
                    "Hard",
                ),
            ],
            "Shakespeare": [
                (
                    "BEGINNER DRILL",
                    "Write sonnet-style program that outputs ASCII art",
                    "Easy",
                ),
                (
                    "INTERMEDIATE MISSION",
                    "Create play that performs basic arithmetic operations",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Implement recursive algorithm using Shakespearean dialogue structure",
                    "Hard",
                ),
            ],
            "Rockstar": [
                ("BEGINNER DRILL", "Compose song that outputs a love letter", "Easy"),
                (
                    "INTERMEDIATE MISSION",
                    "Create lyrical implementation of bubble sort",
                    "Medium",
                ),
                (
                    "ADVANCED OPERATION",
                    "Write rock ballad that calculates Fibonacci sequence",
                    "Hard",
                ),
            ],
        }

    def get_language(self, name):
        """Get language data by name"""
        return self.languages.get(name)

    def get_all_languages(self):
        """Get all available languages"""
        return sorted(self.languages.keys())

    def get_challenges(self, language):
        """Get challenges for a specific language"""
        return self.challenge_templates.get(language, [])

    def has_challenges(self, language):
        """Check if language has challenges available"""
        return language in self.challenge_templates


# =====================================================================
# DRILL SERGEANT PERSONALITY
# =====================================================================


class TuxDrillSergeant:
    """Tux - The Marine Corp Drill Sergeant Instructor"""

    def __init__(self):
        self.drill_level = DrillLevel.ENCOURAGEMENT
        self.current_emotion = "neutral"
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

        # Emotion-based responses
        self.emotion_responses = {
            "exceptional": [
                "🎖️ RECRUIT! I need to SALUTE YOU! This is EXCEPTIONAL work!",
                "OUTSTANDING! You didn't just meet expectations - you CRUSHED them!",
                "THIS is what EXCELLENCE looks like! You're not just a recruit anymore!",
                "I've trained HUNDREDS of soldiers, and THIS... this is ELITE level!",
                "PROMOTED! You've shown MASTERY beyond your rank! EXCEPTIONAL!",
            ],
            "proud": [
                "OUTSTANDING WORK, RECRUIT! This is EXACTLY what I wanted to see!",
                "NOW THAT'S WHAT I'M TALKING ABOUT! You're a NATURAL!",
                "EXCEPTIONAL! You've got the HEART of a TRUE PROGRAMMER!",
                "I'm PROUD of you, soldier! This is SUPERIOR work!",
            ],
            "satisfied": [
                "GOOD JOB! You got it done and that's what matters!",
                "SOLID WORK! You're making REAL progress here!",
                "That's what I like to see! Keep this momentum going!",
                "WELL DONE! You're proving yourself, recruit!",
            ],
            "encouraging": [
                "You're ON THE RIGHT TRACK! Just needs some polish!",
                "I see POTENTIAL here! Let's tighten this up!",
                "GOOD EFFORT! You're getting there, keep pushing!",
                "Not bad! But I KNOW you can do BETTER!",
            ],
            "stern": [
                "This needs MORE WORK, recruit! I expect BETTER!",
                "You're CAPABLE of more than this! DIG DEEPER!",
                "UNACCEPTABLE! Get back in there and FIX THIS!",
                "Is THIS your best? Because I DON'T BELIEVE IT!",
            ],
            "disappointed": [
                "WHAT IS THIS?! Did you even TRY?!",
                "I've seen BEGINNERS do better! GET IT TOGETHER!",
                "This is LAZY WORK! You're BETTER than this!",
                "RECRUIT! Drop and give me TWENTY LINES of PROPER CODE!",
            ],
            "confused": [
                "What in the WORLD is going on here?!",
                "I can't even BEGIN to understand this mess!",
                "EXPLAIN YOURSELF, RECRUIT! What were you THINKING?!",
            ],
        }

    def get_motivational_speech(self, context, language=None):
        """Generate context-aware motivational speeches"""
        speeches = {
            "starting_language": [
                f"Listen up! You're about to embark on a MISSION to learn {language}!",
                f"I didn't survive three tours to train QUITTERS! Now let's learn {language}!",
                f"Alright recruit, {language} isn't EASY, but YOU'RE TOUGHER!",
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

    def get_emotional_response(self, emotion, analysis_data=None):
        """Get Tux's response based on emotion and analysis"""
        self.current_emotion = emotion

        base_response = random.choice(
            self.emotion_responses.get(emotion, self.favorite_expressions)
        )

        if analysis_data and emotion in ["proud", "satisfied", "encouraging"]:
            # Add positive reinforcement
            if analysis_data.get("strengths"):
                strengths = analysis_data["strengths"][:2]  # Top 2 strengths
                base_response += f"\n\nWhat I LIKED:\n"
                for strength in strengths:
                    base_response += f"✓ {strength}\n"

        if analysis_data and emotion in ["stern", "disappointed", "encouraging"]:
            # Add constructive criticism
            if analysis_data.get("issues"):
                issues = analysis_data["issues"][:3]  # Top 3 issues
                base_response += f"\n\nWhat needs IMPROVEMENT:\n"
                for issue in issues:
                    base_response += f"✗ {issue}\n"

        if analysis_data and analysis_data.get("suggestions"):
            base_response += f"\n\nYour MISSION:\n"
            for i, suggestion in enumerate(analysis_data["suggestions"][:2], 1):
                base_response += f"{i}. {suggestion}\n"

        return base_response

    def get_random_expression(self):
        """Get a random drill sergeant expression"""
        return random.choice(self.favorite_expressions)

    def get_emotion_color(self):
        """Get color code for current emotion"""
        colors = {
            "proud": "#00ff00",
            "satisfied": "#90EE90",
            "encouraging": "#ffd93d",
            "stern": "#ff8c00",
            "disappointed": "#ff0000",
            "confused": "#9370db",
            "neutral": "#ffffff",
        }
        return colors.get(self.current_emotion, "#ffffff")


# =====================================================================
# UI COMPONENTS
# =====================================================================


class LoginScreen:
    """Handles the login/enrollment screen"""

    def __init__(self, root, on_enroll_callback):
        self.root = root
        self.on_enroll = on_enroll_callback
        self.name_entry = None

    def show(self):
        """Display the login screen"""
        login_frame = tk.Frame(self.root, bg="#1a1a1a")
        login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_banner(login_frame)
        self._create_intro_text(login_frame)
        self._create_name_input(login_frame)
        self._create_enroll_button(login_frame)

    def _create_banner(self, parent):
        """Create banner and subtitle"""
        banner_label = tk.Label(
            parent,
            text="TUX CODE BOOT CAMP",
            font=("Arial", 32, "bold"),
            fg="#ff6b6b",
            bg="#1a1a1a",
        )
        banner_label.pack(pady=20)

        subtitle = tk.Label(
            parent,
            text="Where Indecision DIES and Code is FORGED!",
            font=("Arial", 16, "italic"),
            fg="#ffd93d",
            bg="#1a1a1a",
        )
        subtitle.pack(pady=10)

    def _create_intro_text(self, parent):
        """Create introductory text"""
        intro_text = scrolledtext.ScrolledText(
            parent,
            height=8,
            width=80,
            font=("Courier", 11),
            bg="#2b2b2b",
            fg="#00ff00",
            wrap=tk.WORD,
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

    def _create_name_input(self, parent):
        """Create name input field"""
        name_frame = tk.Frame(parent, bg="#1a1a1a")
        name_frame.pack(pady=20)

        name_label = tk.Label(
            name_frame,
            text="Your Name (Recruit Identifier):",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#1a1a1a",
        )
        name_label.pack()

        self.name_entry = tk.Entry(
            name_frame,
            font=("Arial", 14),
            width=30,
            bg="#3b3b3b",
            fg="#ffffff",
            insertbackground="white",
        )
        self.name_entry.pack(pady=10)
        self.name_entry.bind("<Return>", lambda e: self._handle_enroll())

    def _create_enroll_button(self, parent):
        """Create enrollment button"""
        enroll_button = tk.Button(
            parent,
            text="ENROLL IN BOOT CAMP!",
            font=("Arial", 14, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            command=self._handle_enroll,
            padx=20,
            pady=10,
        )
        enroll_button.pack(pady=20)

    def _handle_enroll(self):
        """Handle enrollment submission"""
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning("HOLD IT!", "I need a NAME, recruit! SPEAK UP!")
            return

        self.on_enroll(name)


class EnrollmentSpeech:
    """Handles the enrollment speech window"""

    def __init__(self, root, student_name, on_continue_callback):
        self.root = root
        self.student_name = student_name
        self.on_continue = on_continue_callback

    def show(self):
        """Display enrollment speech"""
        speech_window = tk.Toplevel(self.root)
        speech_window.title("Boot Camp Enrollment")
        speech_window.geometry("700x550")
        speech_window.configure(bg="#1a1a1a")

        speech_frame = tk.Frame(speech_window, bg="#1a1a1a")
        speech_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_header(speech_frame)
        self._create_speech_text(speech_frame)
        self._create_continue_button(speech_frame, speech_window)

    def _create_header(self, parent):
        """Create header label"""
        tux_label = tk.Label(
            parent,
            text="TUX DRILL SERGEANT",
            font=("Arial", 18, "bold"),
            fg="#ff6b6b",
            bg="#1a1a1a",
        )
        tux_label.pack(pady=10)

    def _create_speech_text(self, parent):
        """Create speech text area"""
        speech_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            width=80,
            font=("Courier", 11),
            bg="#2b2b2b",
            fg="#00ff00",
            wrap=tk.WORD,
        )
        speech_text.pack(fill=tk.BOTH, expand=True, pady=10)

        speech_content = f"""
WELCOME TO THE PROGRAM, {self.student_name.upper()}!

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

Ready to choose your first language, {self.student_name}?

LET'S MOVE OUT!
        """

        speech_text.insert(tk.END, speech_content)
        speech_text.config(state=tk.DISABLED)

    def _create_continue_button(self, parent, window):
        """Create continue button"""
        continue_button = tk.Button(
            parent,
            text="YES, SERGEANT TUX! LET'S GO!",
            font=("Arial", 12, "bold"),
            bg="#00ff00",
            fg="#000000",
            command=lambda: self._handle_continue(window),
            padx=20,
            pady=10,
        )
        continue_button.pack(pady=10)

    def _handle_continue(self, window):
        """Handle continue button click"""
        window.destroy()
        self.on_continue()


class MainInterface:
    """Main learning interface"""

    def __init__(self, root, student, language_repo, file_manager, tux_sergeant):
        self.root = root
        self.student = student
        self.language_repo = language_repo
        self.file_manager = file_manager
        self.tux = tux_sergeant

        self.language_listbox = None
        self.language_name_label = None
        self.tux_commentary_text = None
        self.description_text = None
        self.code_sample_text = None
        self.motivation_label = None

    def show(self):
        """Display main interface"""
        self.root.geometry("1400x900")

        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_banner(main_frame)

        content_frame = tk.Frame(main_frame, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_left_panel(content_frame)
        self._create_right_panel(content_frame)

    def _create_banner(self, parent):
        """Create top banner with student info"""
        banner_frame = tk.Frame(parent, bg="#ff6b6b")
        banner_frame.pack(fill=tk.X, padx=0, pady=0)

        banner_text = tk.Label(
            banner_frame,
            text=f"BOOT CAMP IN SESSION - Recruit {self.student.name.upper()}",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            padx=20,
            pady=10,
        )
        banner_text.pack(side=tk.LEFT)

        self.motivation_label = tk.Label(
            banner_frame,
            text=f"Motivation Level: {int(self.student.motivation_level)}/100",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            padx=20,
            pady=10,
        )
        self.motivation_label.pack(side=tk.RIGHT)

    def _create_left_panel(self, parent):
        """Create language selection panel"""
        left_frame = tk.Frame(parent, bg="#2b2b2b")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        languages_label = tk.Label(
            left_frame,
            text="CHOOSE YOUR WEAPON",
            font=("Arial", 14, "bold"),
            fg="#ffd93d",
            bg="#2b2b2b",
        )
        languages_label.pack(pady=10)

        self.language_listbox = tk.Listbox(
            left_frame,
            width=20,
            height=15,
            font=("Arial", 10, "bold"),
            bg="#3b3b3b",
            fg="#00ff00",
            selectmode=tk.SINGLE,
        )
        self.language_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.language_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.language_listbox.yview)

        for language in self.language_repo.get_all_languages():
            self.language_listbox.insert(tk.END, language)

        self.language_listbox.bind("<<ListboxSelect>>", self._on_language_select)

    def _create_right_panel(self, parent):
        """Create language details panel"""
        right_frame = tk.Frame(parent, bg="#2b2b2b")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.language_name_label = tk.Label(
            right_frame,
            text="SELECT A LANGUAGE TO BEGIN",
            font=("Arial", 18, "bold"),
            fg="#ff6b6b",
            bg="#2b2b2b",
        )
        self.language_name_label.pack(pady=10)

        self.tux_commentary_text = tk.Text(
            right_frame,
            height=3,
            width=70,
            font=("Courier", 10),
            bg="#3b3b3b",
            fg="#ffd93d",
            wrap=tk.WORD,
        )
        self.tux_commentary_text.pack(pady=10)

        self.description_text = tk.Text(
            right_frame,
            height=5,
            width=70,
            font=("Arial", 10),
            bg="#3b3b3b",
            fg="#ffffff",
            wrap=tk.WORD,
        )
        self.description_text.pack(pady=10)

        code_label = tk.Label(
            right_frame,
            text="SAMPLE CODE:",
            font=("Arial", 11, "bold"),
            fg="#00ff00",
            bg="#2b2b2b",
        )
        code_label.pack()

        self.code_sample_text = tk.Text(
            right_frame,
            height=6,
            width=70,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#00ff00",
            wrap=tk.WORD,
        )
        self.code_sample_text.pack(pady=10)

        self._create_action_buttons(right_frame)

    def _create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg="#2b2b2b")
        button_frame.pack(fill=tk.X, pady=10)

        resources_button = tk.Button(
            button_frame,
            text="LEARNING RESOURCES",
            font=("Arial", 10, "bold"),
            bg="#00aa00",
            fg="#ffffff",
            command=self._open_resources,
            padx=10,
            pady=6,
        )
        resources_button.pack(side=tk.LEFT, padx=3)

        challenge_button = tk.Button(
            button_frame,
            text="TAKE CHALLENGE",
            font=("Arial", 10, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            command=self._generate_challenge,
            padx=10,
            pady=6,
        )
        challenge_button.pack(side=tk.LEFT, padx=3)

        submit_button = tk.Button(
            button_frame,
            text="SUBMIT CODE",
            font=("Arial", 10, "bold"),
            bg="#9370db",
            fg="#ffffff",
            command=self._submit_code,
            padx=10,
            pady=6,
        )
        submit_button.pack(side=tk.LEFT, padx=3)

        commit_button = tk.Button(
            button_frame,
            text="COMMIT",
            font=("Arial", 10, "bold"),
            bg="#ffd93d",
            fg="#000000",
            command=self._commit_language,
            padx=10,
            pady=6,
        )
        commit_button.pack(side=tk.LEFT, padx=3)

    def _on_language_select(self, event):
        """Handle language selection"""
        try:
            selected_index = self.language_listbox.curselection()[0]
            selected_language = self.language_listbox.get(selected_index)

            language_data = self.language_repo.get_language(selected_language)
            if not language_data:
                return

            self.language_name_label.config(text=selected_language.upper())

            self.tux_commentary_text.config(state=tk.NORMAL)
            self.tux_commentary_text.delete(1.0, tk.END)
            self.tux_commentary_text.insert(
                tk.END, language_data["drill_sergeant_take"]
            )
            self.tux_commentary_text.config(state=tk.DISABLED)

            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            desc = f"Difficulty: {language_data['difficulty']}\n\n"
            desc += "Use Cases:\n"
            for use_case in language_data["use_cases"]:
                desc += f"- {use_case}\n"
            self.description_text.insert(tk.END, desc)
            self.description_text.config(state=tk.DISABLED)

            self.code_sample_text.config(state=tk.NORMAL)
            self.code_sample_text.delete(1.0, tk.END)
            self.code_sample_text.insert(tk.END, language_data["sample_code"])
            self.code_sample_text.config(state=tk.DISABLED)

        except IndexError:
            pass

    def _get_selected_language(self):
        """Get currently selected language"""
        try:
            selected_index = self.language_listbox.curselection()[0]
            return self.language_listbox.get(selected_index)
        except IndexError:
            return None

    def _open_resources(self):
        """Open learning resources"""
        selected_language = self._get_selected_language()
        if not selected_language:
            messagebox.showwarning("TUX SAYS:", "PICK A LANGUAGE FIRST!")
            return

        language_data = self.language_repo.get_language(selected_language)
        resources = language_data["learning_resources"]

        resource_window = tk.Toplevel(self.root)
        resource_window.title(f"{selected_language} Resources - GET LEARNING!")
        resource_window.geometry("600x250")
        resource_window.configure(bg="#1a1a1a")

        frame = tk.Frame(resource_window, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        label = tk.Label(
            frame,
            text=f"OPEN THESE RESOURCES FOR {selected_language.upper()}!",
            font=("Arial", 12, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
            wraplength=550,
        )
        label.pack(pady=10)

        for i, resource in enumerate(resources, 1):

            def open_resource(url=resource):
                webbrowser.open(url)

            resource_button = tk.Button(
                frame,
                text=f"Resource {i}: {resource[:45]}...",
                font=("Arial", 9),
                bg="#2b2b2b",
                fg="#00ff00",
                command=open_resource,
                anchor=tk.W,
                padx=10,
                pady=8,
            )
            resource_button.pack(fill=tk.X, pady=4)

        motivation_text = tk.Label(
            frame,
            text="\nGO LEARN! Report back when ready for a CHALLENGE!",
            font=("Arial", 10, "italic"),
            fg="#ffd93d",
            bg="#1a1a1a",
        )
        motivation_text.pack(pady=10)

    def _commit_language(self):
        """Commit to learning a language"""
        selected_language = self._get_selected_language()
        if not selected_language:
            messagebox.showwarning("TUX SAYS:", "SELECT A LANGUAGE!")
            return

        if selected_language not in self.student.languages_started:
            self.student.languages_started.append(selected_language)
            self.student.update_motivation(10)
            self._update_motivation_display()

            messagebox.showinfo(
                "COMMITMENT ACCEPTED!",
                f"THAT'S WHAT I LIKE TO SEE!\n\n"
                f"You've committed to {selected_language}!\n\n"
                f"Now get to work and prove you're SERIOUS!\n\n"
                f"Motivation: {int(self.student.motivation_level)}/100",
            )
        else:
            messagebox.showinfo(
                "ALREADY COMMITTED",
                f"You're ALREADY working on {selected_language}!\n"
                f"Now FINISH what you STARTED!",
            )

    def _generate_challenge(self):
        """Generate a coding challenge"""
        selected_language = self._get_selected_language()
        if not selected_language:
            messagebox.showwarning("TUX SAYS:", "PICK A LANGUAGE FIRST!")
            return

        if not self.language_repo.has_challenges(selected_language):
            messagebox.showwarning(
                "TUX SAYS:", f"Still building challenges for {selected_language}!"
            )
            return

        challenges = self.language_repo.get_challenges(selected_language)
        challenge_name, challenge_desc, difficulty = random.choice(challenges)

        challenge_window = ChallengeWindow(
            self.root,
            selected_language,
            challenge_name,
            challenge_desc,
            difficulty,
            self.student,
            self.file_manager,
            self.tux,
            self._update_motivation_display,
        )
        challenge_window.show()

    def _submit_code(self):
        """Submit code for AI analysis"""
        selected_language = self._get_selected_language()
        if not selected_language:
            messagebox.showwarning("TUX SAYS:", "SELECT A LANGUAGE FIRST!")
            return

        # Open file dialog to select code file
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            title="SELECT YOUR CODE FILE",
            initialdir="TuxBootCamp_Challenges",
            filetypes=[
                (
                    f"{selected_language} files",
                    f"*{ChallengeFileManager.EXTENSIONS.get(selected_language, '.txt')}",
                ),
                ("All files", "*.*"),
            ],
        )

        if not filename:
            return

        # Read the code
        try:
            with open(filename, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            messagebox.showerror("ERROR", f"Could not read file: {str(e)}")
            return

        # Show submission window
        submission_window = CodeSubmissionWindow(
            self.root,
            selected_language,
            code_content,
            self.student,
            self.tux,
            self._update_motivation_display,
        )
        submission_window.show()

    def _update_motivation_display(self):
        """Update motivation level display"""
        if self.motivation_label:
            self.motivation_label.config(
                text=f"Motivation Level: {int(self.student.motivation_level)}/100"
            )

    def update_motivation(self, change):
        """Update student motivation"""
        self.student.update_motivation(change)
        self._update_motivation_display()


class ChallengeWindow:
    """Challenge display and acceptance window"""

    def __init__(
        self,
        root,
        language,
        challenge_name,
        challenge_desc,
        difficulty,
        student,
        file_manager,
        tux_sergeant,
        on_motivation_update,
    ):
        self.root = root
        self.language = language
        self.challenge_name = challenge_name
        self.challenge_desc = challenge_desc
        self.difficulty = difficulty
        self.student = student
        self.file_manager = file_manager
        self.tux = tux_sergeant
        self.on_motivation_update = on_motivation_update

    def show(self):
        """Display challenge window"""
        challenge_window = tk.Toplevel(self.root)
        challenge_window.title(f"{self.challenge_name} - {self.language}")
        challenge_window.geometry("700x480")
        challenge_window.configure(bg="#1a1a1a")

        frame = tk.Frame(challenge_window, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_header(frame)
        self._create_challenge_text(frame)
        self._create_motivation(frame)
        self._create_buttons(frame, challenge_window)

    def _create_header(self, parent):
        """Create challenge header"""
        header_label = tk.Label(
            parent,
            text=f"{self.challenge_name} - {self.language.upper()}",
            font=("Arial", 15, "bold"),
            fg="#ff6b6b",
            bg="#1a1a1a",
        )
        header_label.pack(pady=8)

        difficulty_colors = {"Easy": "#00ff00", "Medium": "#ffd93d", "Hard": "#ff6b6b"}
        difficulty_label = tk.Label(
            parent,
            text=f"Difficulty: {self.difficulty}",
            font=("Arial", 11, "bold"),
            fg=difficulty_colors.get(self.difficulty, "#ffffff"),
            bg="#1a1a1a",
        )
        difficulty_label.pack(pady=4)

    def _create_challenge_text(self, parent):
        """Create challenge description"""
        challenge_text = scrolledtext.ScrolledText(
            parent,
            height=10,
            width=80,
            font=("Courier", 10),
            bg="#2b2b2b",
            fg="#ffffff",
            wrap=tk.WORD,
        )
        challenge_text.pack(fill=tk.BOTH, expand=True, pady=8)
        challenge_text.insert(tk.END, self.challenge_desc)
        challenge_text.config(state=tk.DISABLED)

    def _create_motivation(self, parent):
        """Create motivational message"""
        motivation_label = tk.Label(
            parent,
            text=self.tux.get_motivational_speech("completion"),
            font=("Arial", 10, "italic"),
            fg="#00ff00",
            bg="#1a1a1a",
            wraplength=650,
        )
        motivation_label.pack(pady=8)

    def _create_buttons(self, parent, window):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg="#1a1a1a")
        button_frame.pack(fill=tk.X, pady=8)

        accept_button = tk.Button(
            button_frame,
            text="ACCEPT CHALLENGE!",
            font=("Arial", 11, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            command=lambda: self._accept_challenge(window),
            padx=15,
            pady=8,
        )
        accept_button.pack(side=tk.LEFT, padx=4)

        skip_button = tk.Button(
            button_frame,
            text="Maybe Later",
            font=("Arial", 9),
            bg="#3b3b3b",
            fg="#ffffff",
            command=window.destroy,
            padx=12,
            pady=6,
        )
        skip_button.pack(side=tk.LEFT, padx=4)

    def _accept_challenge(self, window):
        """Handle challenge acceptance"""
        try:
            # Create the challenge file
            filename = self.file_manager.create_challenge_file(
                self.language,
                self.challenge_name,
                self.challenge_desc,
                self.difficulty,
                self.student.name,
            )

            # Update motivation
            self.student.update_motivation(15)
            self.on_motivation_update()

            # Show success message
            messagebox.showinfo(
                "CHALLENGE ACCEPTED!",
                f"NOW GET TO WORK!\n\n"
                f"Your challenge file has been created:\n{filename}\n\n"
                f"Complete this and report back!\n"
                f"NO EXCUSES!\n\n"
                f"Motivation: {int(self.student.motivation_level)}/100",
            )

            # Open the file
            self.file_manager.open_file(filename)

            window.destroy()

        except Exception as e:
            messagebox.showerror(
                "FILE CREATION ERROR", f"Couldn't create challenge file:\n{str(e)}"
            )


class CodeSubmissionWindow:
    """Window for submitting and analyzing code"""

    def __init__(
        self, root, language, code_content, student, tux_sergeant, on_motivation_update
    ):
        self.root = root
        self.language = language
        self.code_content = code_content
        self.student = student
        self.tux = tux_sergeant
        self.on_motivation_update = on_motivation_update
        self.analyzer = CodeAnalyzer()

        # Extract challenge description from code comments
        self.challenge_desc = self._extract_challenge_description()

    def _extract_challenge_description(self):
        """Extract challenge description from code file"""
        lines = self.code_content.split("\n")
        for line in lines:
            if "MISSION BRIEFING:" in line:
                # Find the next line after MISSION BRIEFING
                idx = lines.index(line)
                if idx + 1 < len(lines):
                    desc_line = lines[idx + 1]
                    # Remove comment markers
                    desc_line = (
                        desc_line.replace("#", "")
                        .replace("//", "")
                        .replace(";", "")
                        .strip()
                    )
                    return desc_line
        return "Complete the coding challenge"

    def show(self):
        """Display submission window"""
        self.window = tk.Toplevel(self.root)
        self.window.title(f"CODE SUBMISSION - {self.language}")
        self.window.geometry("900x700")
        self.window.configure(bg="#1a1a1a")

        frame = tk.Frame(self.window, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_header(frame)
        self._create_code_display(frame)
        self._create_analysis_section(frame)
        self._create_submit_button(frame)

    def _create_header(self, parent):
        """Create header"""
        header = tk.Label(
            parent,
            text=f"SUBMIT YOUR {self.language.upper()} CODE",
            font=("Arial", 16, "bold"),
            fg="#ff6b6b",
            bg="#1a1a1a",
        )
        header.pack(pady=10)

    def _create_code_display(self, parent):
        """Create code display area"""
        code_label = tk.Label(
            parent,
            text="YOUR CODE:",
            font=("Arial", 11, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
        )
        code_label.pack(anchor=tk.W, pady=(10, 5))

        self.code_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            width=100,
            font=("Courier", 9),
            bg="#2b2b2b",
            fg="#00ff00",
            wrap=tk.WORD,
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.code_text.insert(tk.END, self.code_content)
        self.code_text.config(state=tk.DISABLED)

    def _create_analysis_section(self, parent):
        """Create analysis results section"""
        analysis_label = tk.Label(
            parent,
            text="TUX'S ANALYSIS:",
            font=("Arial", 11, "bold"),
            fg="#ffd93d",
            bg="#1a1a1a",
        )
        analysis_label.pack(anchor=tk.W, pady=(10, 5))

        self.analysis_text = scrolledtext.ScrolledText(
            parent,
            height=10,
            width=100,
            font=("Courier", 10),
            bg="#2b2b2b",
            fg="#ffffff",
            wrap=tk.WORD,
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.analysis_text.insert(tk.END, "Waiting for submission...")
        self.analysis_text.config(state=tk.DISABLED)

    def _create_submit_button(self, parent):
        """Create submit button"""
        button_frame = tk.Frame(parent, bg="#1a1a1a")
        button_frame.pack(fill=tk.X, pady=10)

        self.submit_button = tk.Button(
            button_frame,
            text="SUBMIT FOR REVIEW!",
            font=("Arial", 12, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            command=self._submit_code,
            padx=20,
            pady=10,
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(
            button_frame,
            text="Close",
            font=("Arial", 10),
            bg="#3b3b3b",
            fg="#ffffff",
            command=self.window.destroy,
            padx=15,
            pady=8,
        )
        close_button.pack(side=tk.LEFT, padx=5)

    def _submit_code(self):
        """Submit code for AI analysis"""
        self.submit_button.config(state=tk.DISABLED, text="ANALYZING...")
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "Sergeant Tux is reviewing your code...\n\n")
        self.analysis_text.config(state=tk.DISABLED)

        # Run analysis in background
        import threading

        thread = threading.Thread(target=self._run_analysis)
        thread.daemon = True
        thread.start()

    def _run_analysis(self):
        """Run AI analysis in background thread"""
        import asyncio

        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(
                self.analyzer.analyze_code(
                    self.language, self.challenge_desc, self.code_content
                )
            )

            # Update UI in main thread
            self.root.after(0, lambda: self._display_results(result))

        except Exception as e:
            error_result = {
                "success": False,
                "tux_emotion": "confused",
                "summary": f"Analysis failed: {str(e)}",
            }
            self.root.after(0, lambda: self._display_results(error_result))
        finally:
            loop.close()

    def _display_results(self, result):
        """Display analysis results"""
        emotion = result.get("tux_emotion", "neutral")

        # Get Tux's emotional response
        tux_response = self.tux.get_emotional_response(emotion, result)

        # Update analysis text
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)

        # Add header with emotion color
        emotion_color = self.tux.get_emotion_color()
        self.analysis_text.tag_config(
            "header", foreground=emotion_color, font=("Courier", 11, "bold")
        )
        self.analysis_text.insert(tk.END, "=" * 80 + "\n", "header")
        self.analysis_text.insert(tk.END, f"SERGEANT TUX'S VERDICT\n", "header")
        self.analysis_text.insert(tk.END, "=" * 80 + "\n\n", "header")

        # Add Tux's response
        self.analysis_text.insert(tk.END, tux_response + "\n\n")

        # Add technical details
        if result.get("success"):
            self.analysis_text.insert(tk.END, "=" * 80 + "\n")
            self.analysis_text.insert(tk.END, "TECHNICAL ANALYSIS:\n")
            self.analysis_text.insert(tk.END, "=" * 80 + "\n\n")

            self.analysis_text.insert(
                tk.END,
                f"Correctness: {'✓ CORRECT' if result.get('correct') else '✗ INCORRECT'}\n",
            )
            self.analysis_text.insert(
                tk.END, f"Completeness: {result.get('completeness', 0)}%\n"
            )
            self.analysis_text.insert(
                tk.END, f"Quality Score: {result.get('quality_score', 0)}%\n\n"
            )

            if result.get("summary"):
                self.analysis_text.insert(tk.END, f"Summary: {result['summary']}\n")

        self.analysis_text.config(state=tk.DISABLED)

        # Update motivation based on result
        if result.get("correct"):
            motivation_change = 20
        elif result.get("completeness", 0) >= 50:
            motivation_change = 10
        else:
            motivation_change = -5

        self.student.update_motivation(motivation_change)
        self.on_motivation_update()

        # Re-enable submit button
        self.submit_button.config(state=tk.NORMAL, text="SUBMIT FOR REVIEW!")


# =====================================================================
# APPLICATION CONTROLLER
# =====================================================================


class TuxBootCampApp:
    """Main application controller"""

    def __init__(self, root):
        self.root = root
        self.root.title("TUX CODE BOOT CAMP - Where Weak Coders Come to GET STRONG!")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")

        # Initialize components
        self.student = None
        self.tux_sergeant = TuxDrillSergeant()
        self.language_repo = LanguageRepository()
        self.file_manager = ChallengeFileManager()

        # Start with login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Display login screen"""
        login_screen = LoginScreen(self.root, self.on_student_enrolled)
        login_screen.show()

    def on_student_enrolled(self, name):
        """Handle student enrollment"""
        self.student = StudentProgress(name)

        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Show enrollment speech
        self.show_enrollment_speech()

    def show_enrollment_speech(self):
        """Show enrollment speech"""
        speech = EnrollmentSpeech(
            self.root, self.student.name, self.show_main_interface
        )
        speech.show()

    def show_main_interface(self):
        """Show main learning interface"""
        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create and show main interface
        main_interface = MainInterface(
            self.root,
            self.student,
            self.language_repo,
            self.file_manager,
            self.tux_sergeant,
        )
        main_interface.show()


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================


def main():
    root = tk.Tk()
    app = TuxBootCampApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
