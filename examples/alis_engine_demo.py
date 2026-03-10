python
import json
import re
import os

class ALISEngine:
    def __init__(self):
        self.variables = {}  # In-memory storage for user variables
        self.registry = {}   # Command mapping for the selected language
        self.current_lang = ""

    def load_language(self, lang_json):
        """Loads the language pack and prepares the engine environment."""
        try:
            with open(lang_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.registry = data['registry']
                self.current_lang = data['language']
                print(f"[*] ALIS Engine: {self.current_lang} environment loaded successfully.")
        except Exception as e:
            print(f"[ERROR]: Could not load language file: {e}")

    def evaluate_params(self, params):
        """Analyzes data type: String, Numeric, or Variable reference."""
        params = params.strip()
        if not params: return ""
        
        # String detection (Quotes)
        if (params.startswith('"') and params.endswith('"')) or (params.startswith("'") and params.endswith("'")):
            return params[1:-1]
        
        # Basic Mathematical Operation detection (e.g., x + 5)
        if any(op in params for op in ['+', '-', '*', '/']):
            try:
                # Using a safe eval-like approach for basic math with memory variables
                return eval(params, {"__builtins__": None}, self.variables)
            except:
                pass

        # Numeric detection
        try:
            if "." in params: return float(params)
            return int(params)
        except ValueError:
            # Variable detection (Fetch from memory)
            return self.variables.get(params, params)

    def parse_line(self, line):
        """Extracts Command ID and Parameters from a line of code."""
        line = line.strip()
        if not line or line.startswith("//"): return None, None
        
        # Match .ID format (e.g., .01, .06)
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def execute_file(self, alis_file_path):
        """Executes an .alis file line by line."""
        if not os.path.exists(alis_file_path):
            print(f"[ERROR]: File {alis_file_path} not found.")
            return

        print(f"\n--- ALIS EXECUTION START: {alis_file_path} ---")
        with open(alis_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
                
        line_idx = 0
        while line_idx < len(lines):
            line = lines[line_idx].strip()
            cmd_id, params = self.parse_line(line)
            
            if cmd_id:
                result = self.run_command(cmd_id, params, line_idx + 1)
                if result == "BREAK": break
            elif params and "=" in params:
                self.run_command(None, params, line_idx + 1)
            
            line_idx += 1
        print("--- ALIS EXECUTION FINISHED ---")

    def run_command(self, cmd_id, params, line_num):
        """Core logic handler for ALIS IDs."""
        
        # VARIABLE ASSIGNMENT (No ID, contains '=')
        if not cmd_id and "=" in params:
            parts = params.split("=", 1)
            var_name = parts[0].strip()
            var_val = self.evaluate_params(parts[1])
            self.variables[var_name] = var_val
            return

        # .06: PRINT (Standard Output)
        if cmd_id == "06":
            val = self.evaluate_params(params)
            print(f"[OUTPUT]: {val}")

        # .13: INPUT (Standard Input) - NEW!
        elif cmd_id == "13":
            var_name = params.strip()
            user_val = input(f"[INPUT required for {var_name}]: ")
            self.variables[var_name] = self.evaluate_params(f"'{user_val}'")

        # .01: IF (Conditional Logic)
        elif cmd_id == "01":
            try:
                condition = eval(params, {"__builtins__": None}, self.variables)
                if not condition:
                    print(f"[LOG]: Line {line_num} condition ({params}) not met.")
            except Exception as e:
                print(f"[SYNTAX ERROR]: Line {line_num} -> {e}")

        # .11: BREAK
        elif cmd_id == "11":
            return "BREAK"

# --- ALIS BOOTSTRAP ---
if __name__ == "__main__":
    demo_engine = ALISEngine()
    
    # Set paths relative to script location
    lang_path = "languages/en.json"
    code_path = "hello_world.alis"
    
    # Check if files exist before running to avoid crash
    if os.path.exists(lang_path) and os.path.exists(code_path):
        demo_engine.load_language(lang_path)
        demo_engine.execute_file(code_path)
    else:
        print("[SYSTEM]: Please ensure hello_world.alis and languages/en.json are in the same folder.")
