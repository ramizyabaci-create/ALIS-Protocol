
        self.registry = {}
        self.functions = {}  # NEW: Storage for function blocks
        self.msgs = {}
        self.current_lang = ""

    def get_msg(self, key, default):
        return self.msgs.get(key, default)

    def load_language(self, lang_json):
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
        params = params.strip()
        if not params: return ""
        if (params.startswith('"') and params.endswith('"')) or (params.startswith("'") and params.endswith("'")):
            return params[1:-1]
        
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
        line = line.strip()
        if not line or line.startswith("//"): return None, None
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    # --- PART 2 WILL CONTINUE HERE (execute_file & run_command improvements) ---
 def execute_file(self, alis_file_path):
        """Executes .alis file with Function Block and Loop support."""
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
            
            # --- NEW: FUNCTION DEFINITION (.08) ---
            if cmd_id == "08":
                func_name = params.strip()
                self.functions[func_name] = []
                line_idx += 1
                # Capture block until next function or specific end
                while line_idx < len(lines) and not self.parse_line(lines[line_idx])[0] in ["08", "11"]:
                    self.functions[func_name].append(lines[line_idx])
                    line_idx += 1
                print(f"[*] Registered function: {func_name}")
                continue

            # --- NORMAL EXECUTION ---
            self.run_command(cmd_id, params, line_idx + 1)
            line_idx += 1
            
        print(self.get_msg("exec_finish", "Finished"))

    def run_command(self, cmd_id, params, line_num):
        """Executes core logic and calls defined functions."""
        # VARIABLE ASSIGNMENT
        if not cmd_id and "=" in params:
            parts = params.split("=", 1)
            self.variables[parts[0].strip()] = self.evaluate_params(parts[1])
            return

        # .06: PRINT
        if cmd_id == "06":
            print(f"[OUTPUT]: {self.evaluate_params(params)}")
            
        # .13: INPUT
        elif cmd_id == "13":
            prompt = self.get_msg("input_prompt", "Input {}: ").format(params)
            user_val = input(prompt)
            self.variables[params.strip()] = self.evaluate_params(f"'{user_val}'")

        # CALL FUNCTION (If command matches a stored function name)
        # For now, we use a simple pattern or dedicated ID like .10 (Call)
        elif cmd_id == "10": # CALL
            func_name = params.strip()
            if func_name in self.functions:
                print(f"[CALLING]: {func_name}")
                for f_line in self.functions[func_name]:
                    f_cmd, f_params = self.parse_line(f_line)
                    self.run_command(f_cmd, f_params, "inline")
            else:
                print(f"[ERR]: Function '{func_name}' not found.")

if __name__ == "__main__":
    engine = ALISEngine()
    lang_file = "languages/en.json" 
    code_file = "hello_world.alis"
    
    if os.path.exists(lang_file):
        engine.load_language(lang_file)
        engine.execute_file(code_file)
