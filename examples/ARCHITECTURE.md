⚙️ Technical Implementation: The ALIS Transpiler Logic
The core mission for Group 1 (Compiler Architects) is to develop the ALIS Engine, which follows this execution flow:
Lexical Analysis: The engine reads the .alis file (e.g., .06 "Hello World").
Logic Mapping: It identifies the Prefix (.) and the ID (06).
Target Selection: Based on the environment, the engine converts the ID into:
High-Level: Standard Python/C++ code.
Low-Level: Native Assembly opcodes (via the ALIS Compiler Plugin).
Localization: For display purposes, it fetches the string from the chosen .json language pack (e.g., yazdir, print, drucken).
🛠️ Join Group 1: The Architects
We are looking for developers to build the first ALIS-to-Python Transpiler.
Goal: Convert a full .alis sequence into a runnable .py script.
Focus: Mapping the 44 Core IDs to Python's internal AST (Abstract Syntax Tree).
