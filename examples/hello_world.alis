import json
import re
import os

class ALISEngine:
    def __init__(self):
        self.variables = {"PI": 3.14159, "VERSION": 1.5} # Pre-defined constants
        self.registry = {}
        self.functions = {}
        self.msgs = {}
        self.current_lang = ""

    def get_msg(self, key, default):
        return self.msgs.get(key, default)

    def load_language(self, lang_json):
        """Loads language and system UI messages from JSON."""
        try:
            with open(lang_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.registry = data['registry']
                self.msgs = data.get('system_messages', {})
                self.current_lang = data['language']
                print(self.get_msg("engine_loaded", "[*] Loaded: {}").format(self.current_lang))
        except Exception as e:
            print(f"CRITICAL SYSTEM ERROR: {e}")

    def evaluate_params(self, params):
        """Advanced Evaluator: Strings, Math, and Variable Logic."""
        params = params.strip()
        if not params: return ""
        
        # String detection
        if (params.startswith('"') and params.endswith('"')) or (params.startswith("'") and params.endswith("'")):
            return params[1:-1]
        
        # Advanced Math & Logic Evaluator
        try:
            # We allow basic math and comparisons within the variable context
            return eval(params, {"__builtins__": None}, self.variables)
        except:
            # If not a math expression, return as numeric or raw string
            try:
                if "." in params: return float(params)
                return int(params)
            except ValueError:
                return self.variables.get(params, params)

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("//"): return None, None
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def execute_file(self, alis_file_path):
        """The heart of the ALIS Protocol: Block and Logic Execution."""
        if not os.path.exists(alis_file_path):
            print(self.get_msg("file_not_found", "File {} not found").format(alis_file_path))
            return

        print(f"\n" + self.get_msg("exec_start", "Start: {}").format(alis_file_path))
        with open(alis_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
                
        line_idx = 0
        while line_idx < len(lines):
            line = lines[line_idx].strip()
            cmd_id, params = self.parse_line(line)
            
            # --- BLOCK DEFINITION (.08) ---
            if cmd_id == "08":
                func_name = params.strip()
                self.functions[func_name] = []
                line_idx += 1
                while line_idx < len(lines) and not lines[line_idx].strip().startswith(".11"):
                    self.functions[func_name].append(lines[line_idx])
                    line_idx += 1
                continue

            # --- RUN COMMAND ---
            self.run_command(cmd_id, params, line_idx + 1)
            line_idx += 1
            
        print(self.get_msg("exec_finish", "Finished"))

    def run_command(self, cmd_id, params, line_num):
        """Executes universal Logic IDs."""
        # VARIABLE ASSIGNMENT (x = y + 5)
        if not cmd_id and "=" in params:
            var_name, var_expr = params.split("=", 1)
            self.variables[var_name.strip()] = self.evaluate_params(var_expr)
            return

        if cmd_id == "06": # PRINT
            print(f"[OUTPUT]: {self.evaluate_params(params)}")
            
        elif cmd_id == "13": # INPUT
            prompt = self.get_msg("input_prompt", "Input {}: ").format(params)
            user_val = input(prompt)
            # Auto-detect if input is a number
            self.variables[params.strip()] = self.evaluate_params(f"'{user_val}'")
            
        elif cmd_id == "01": # IF (Logical Condition)
            if not self.evaluate_params(params):
                return "SKIP_NEXT" # For future block-skipping logic

        elif cmd_id == "10": # CALL FUNCTION
            func_name = params.strip()
            if func_name in self.functions:
                for f_line in self.functions[func_name]:
                    f_cmd, f_params = self.parse_line(f_line)
                    self.run_command(f_cmd, f_params, "inline")

if __name__ == "__main__":
    engine = ALISEngine()
    # Dynamic Path Setup
    base = os.path.dirname(__file__)
    lang = os.path.join(base, "languages/en.json")
    code = os.path.join(base, "hello_world.alis")
    
    if os.path.exists(lang) and os.path.exists(code):
        engine.load_language(lang)
        engine.execute_file(code)
