import os
from alis_memory import ALISMemory
from alis_parser import ALISParser

class ALISEngine:
    def __init__(self):
        self.mem = ALISMemory()
        self.parser = ALISParser()

    def log(self, tag, msg_key, param=""):
        message = self.mem.msgs.get(msg_key, f"[{tag}] {msg_key} {}").format(param)
        print(f"[{tag}] {message}")

    def load_language(self, lang_path):
        with open(lang_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.mem.registry = data.get('registry', {})
            self.mem.msgs = data.get('system_messages', {})
            self.log("SYS", "engine_loaded", data.get('language'))

    def run_command(self, cmd_id, params, line_num):
        if not cmd_id and "=" in params: # Atama
            var, val = params.split("=", 1)
            self.mem.variables[var.strip()] = self.mem.evaluate(val)
        elif cmd_id == "06": # PRINT
            print(f"> {self.mem.evaluate(params)}")
        elif cmd_id == "10": # IMPORT
            self.execute_file(params.strip(), is_import=True)
        # Diğer komutlar buraya eklenecek...

    def execute_file(self, file_path, is_import=False):
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        idx = 0
        while idx < len(lines):
            cmd_id, params = self.parser.parse_line(lines[idx])
            # Fonksiyon ve Döngü mantığı burada çalışacak...
            self.run_command(cmd_id, params, idx + 1)
            idx += 1

if __name__ == "__main__":
    engine = ALISEngine()
    # Başlatma kodları...
