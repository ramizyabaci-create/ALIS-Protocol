python
import json
import re
import os

class ALISEngine:
    def __init__(self):
        self.variables = {}
        self.registry = {}
        self.msgs = {}  # System messages from JSON
        self.current_lang = ""

    def get_msg(self, key, default):
        """Fetches a localized message or returns default."""
        return self.msgs.get(key, default)

    def load_language(self, lang_json):
        """Loads logic mapping and UI messages from JSON."""
        try:
            with open(lang_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.registry = data['registry']
                self.msgs = data.get('system_messages', {})
                self.current_lang = data['language']
                # Localized: Loaded message
                print(self.get_msg("engine_loaded", "[*] Loaded: {}").format(self.current_lang))
        except Exception as e:
            print(f"CRITICAL SYSTEM ERROR: {e}")

    def evaluate_params(self, params):
        """Identifies types: Strings, Math, or Variable Memory."""
        params = params.strip()
        if not params: return ""
        if (params.startswith('"') and params.endswith('"')) or (params.startswith("'") and params.endswith("'")):
            return params[1:-1]
        
        # Safe Basic Math with Variables
        if any(op in params for op in ['+', '-', '*', '/']):
            try:
                return eval(params, {"__builtins__": None}, self.variables)
            except: pass

        try:
            if "." in params: return float(params)
            return int(params)
        except ValueError:
            return self.variables.get(params, params)

    def parse_line(self, line):
        """Splits syntax into Prefix, ID and Params."""
        line = line.strip()
        if not line or line.startswith("//"): return None, None
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def execute_file(self, alis_file_path):
        """Main execution engine using localized strings."""
        if not os.path.exists(alis_file_path):
            # Localized: File not found
            print(self.get_msg("file_not_found", "File {} not found").format(alis_file_path))
            return

        # Localized: Start Execution
        print(f"\n" + self.get_msg("exec_start", "Start: {}").format(alis_file_path))
        
        with open(alis_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
                
        line_idx = 0
        loop_start = -1
        loop_condition = ""

        while line_idx < len(lines):
            line = lines[line_idx].strip()
            cmd_id, params = self.parse_line(line)
            
            # --- LOOP LOGIC (WHILE .05) ---
            if cmd_id == "05":
                loop_start = line_idx
                loop_condition = params
                try:
                    if not eval(loop_condition, {"__builtins__": None}, self.variables):
                        while line_idx < len(lines) and ".11" not in lines[line_idx]:
                            line_idx += 1
                        line_idx += 1
                        continue
                except: pass

            # --- RUN COMMAND ---
            result = self.run_command(cmd_id, params, line_idx + 1)

            # --- END BLOCK (.11) ---
            if cmd_id == "11" and loop_start != -1:
                line_idx = loop_start
                continue
            
            line_idx += 1
            
        # Localized: Finish Execution
        print(self.get_msg("exec_finish", "Finished"))

    def run_command(self, cmd_id, params, line_num):
        """Logic execution with localized user feedback."""
        # VARIABLE ASSIGNMENT
        if not cmd_id and "=" in params:
            parts = params.split("=", 1)
            var_name = parts[0].strip()
            var_val = self.evaluate_params(parts[1])
            self.variables[var_name] = var_val
            return

        if cmd_id == "06": # PRINT
            print(f"[OUTPUT]: {self.evaluate_params(params)}")
            
        elif cmd_id == "13": # INPUT
            # Localized: Input prompt
            prompt = self.get_msg("input_prompt", "Input {}: ").format(params)
            user_val = input(prompt)
            self.variables[params.strip()] = self.evaluate_params(f"'{user_val}'")
            
        elif cmd_id == "01": # IF
            try:
                condition = eval(params, {"__builtins__": None}, self.variables)
                if not condition:
                    # Localized: Condition skipped
                    print(self.get_msg("condition_not_met", "Skip line {}").format(line_num, params))
            except Exception as e:
                # Localized: Syntax Error
                print(self.get_msg("syntax_error", "Error at {}: {}").format(line_num, e))

if __name__ == "__main__":
    engine = ALISEngine()
    # Testing for Global Versatility
    # Change to 'tr.json' and you'll see every error/system message in Turkish!
    lang_file = "languages/en.json" 
    code_file = "hello_world.alis"
    
    if os.path.exists(lang_file):
        engine.load_language(lang_file)
        engine.execute_file(code_file)
