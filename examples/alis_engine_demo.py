import json
import re
import os
import sys

class ALISEngine:
    def __init__(self):
        # The Brain: Variable Memory
        self.variables = {
            "__VERSION__": "2.0.0",
            "__AUTHOR__": "ALIS Protocol Team",
            "TRUE": True,
            "FALSE": False
        }
        self.registry = {}
        self.functions = {}
        self.system_messages = {}
        self.current_lang = ""

    def log(self, tag, message):
        """Standardized logging for the engine."""
        print(f"[{tag}] {message}")

    def load_language(self, lang_json):
        """Initializes the linguistic and system environment."""
        try:
            with open(lang_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.registry = data.get('registry', {})
                self.system_messages = data.get('system_messages', {})
                self.current_lang = data.get('language', 'Unknown')
                
                msg = self.system_messages.get("engine_loaded", "[*] Environment: {} loaded.").format(self.current_lang)
                self.log("SYS", msg)
        except Exception as e:
            self.log("CRITICAL", f"Language initialization failed: {e}")

    def evaluate_expression(self, expr):
        """Advanced Logic Evaluator with Type Awareness."""
        expr = expr.strip()
        if not expr: return None
        
        # String Literal Check
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Boolean/Numeric/Variable Resolution
        try:
            # Safe evaluation within the variable context
            return eval(expr, {"__builtins__": None}, self.variables)
        except:
            # Fallback for raw strings or undefined variables
            return self.variables.get(expr, expr)

    def parse_instruction(self, line):
        """Deconstructs the ALIS syntax (.ID Params)."""
        line = line.strip()
        if not line or line.startswith("//"): return None, None
        
        # Protocol standard: . followed by 2+ digits
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def run_command(self, cmd_id, params, line_num):
        """The Execution Heart: Mapping Logic IDs to Machine Actions."""
        
        # 1. Variable Assignment (Logic: Storage)
        if not cmd_id and "=" in params:
            parts = params.split("=", 1)
            var_name = parts[0].strip()
            self.variables[var_name] = self.evaluate_expression(parts[1])
            return

        # 2. Logic Mappings (.ID -> Action)
        if cmd_id == "06": # PRINT (Standard Output)
            result = self.evaluate_expression(params)
            print(f"> {result}")
            
        elif cmd_id == "13": # INPUT (Standard Input)
            prompt = self.system_messages.get("input_prompt", "Input {}: ").format(params)
            user_input = input(prompt)
            # Store with auto-type conversion
            self.variables[params.strip()] = self.evaluate_expression(f"'{user_input}'")

        elif cmd_id == "01": # IF (Flow Control)
            condition = self.evaluate_expression(params)
            if not condition:
                msg = self.system_messages.get("condition_not_met", "Line {} skipped.").format(line_num)
                self.log("LOG", msg)
                return "SKIP"

        elif cmd_id == "08": # DEFINE (Block Storage)
            # Managed in execute_file for block capturing
            pass

    def execute_file(self, file_path):
        """Processes the .alis logic script."""
        if not os.path.exists(file_path):
            error_msg = self.system_messages.get("file_not_found", "File {} not found.").format(file_path)
            self.log("ERROR", error_msg)
            return

        start_msg = self.system_messages.get("exec_start", "Executing: {}").format(file_path)
        self.log("ALIS", start_msg)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
                
        idx = 0
        while idx < len(lines):
            cmd_id, params = self.parse_instruction(lines[idx])
            
            # Block Capture Logic (Functions)
            if cmd_id == "08":
                func_name = params.strip()
                self.functions[func_name] = []
                idx += 1
                while idx < len(lines) and not lines[idx].strip().startswith(".11"):
                    self.functions[func_name].append(lines[idx])
                    idx += 1
                self.log("SYS", f"Function '{func_name}' registered.")
                idx += 1
                continue

            # Execution
            status = self.run_command(cmd_id, params, idx + 1)
            
            # Simple IF Skip (Next line skip)
            if status == "SKIP": idx += 1
            
            idx += 1
        
        finish_msg = self.system_messages.get("exec_finish", "Execution finished.")
        self.log("ALIS", finish_msg)

if __name__ == "__main__":
    alis = ALISEngine()
    # Path configuration for professional GitHub structure
    base = os.path.dirname(__file__)
    lang_p = os.path.join(base, "languages/en.json")
    code_p = os.path.join(base, "hello_world.alis")
    
    if os.path.exists(lang_p):
        alis.load_language(lang_p)
        if os.path.exists(code_p):
            alis.execute_file(code_p)
