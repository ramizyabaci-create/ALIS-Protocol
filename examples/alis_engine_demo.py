import json
import os
from alis_memory import ALISMemory
from alis_parser import ALISParser

class ALISEngine:
    def __init__(self):
        self.mem = ALISMemory()
        self.parser = ALISParser()

    def log(self, tag, msg_key, param=""):
        """Sistem mesajlarını dilden bağımsız olarak yönetir."""
        message = self.mem.msgs.get(msg_key, f"[{tag}] {msg_key} {{}}").format(param)
        print(f"[{tag}] {message}")

    def load_language(self, lang_path):
        """Hafızaya dil sözlüğünü yükler."""
        if not os.path.exists(lang_path):
            print(f"[CRITICAL]: Language file not found at {lang_path}")
            return
        with open(lang_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.mem.registry = data.get('registry', {})
            self.mem.msgs = data.get('system_messages', {})
            # Yerelleştirilmiş yükleme mesajı
            self.log("SYS", "engine_loaded", data.get('language'))

    def run_command(self, cmd_id, params, line_num):
        """Hafıza ve Parser'ı kullanarak komutları yürütür."""
        # 1. Değişken Atama (.ID yoksa ve = varsa)
        if not cmd_id and "=" in params:
            var_name, var_expr = params.split("=", 1)
            self.mem.set_var(var_name, var_expr)
            return

        # 2. Mantıksal İşlemler (.ID varsa)
        if cmd_id == "06": # PRINT
            print(f"> {self.mem.evaluate(params)}")
            
        elif cmd_id == "13": # INPUT
            prompt = self.mem.msgs.get("input_prompt", "Input {}: ").format(params)
            user_val = input(prompt)
            self.mem.set_var(params, f"'{user_val}'")

        elif cmd_id == "10": # IMPORT
            self.execute_file(params.strip(), is_import=True)

        elif cmd_id == "01": # IF
            if not self.mem.evaluate(params):
                return "SKIP"

    def execute_file(self, file_path, is_import=False):
        """Programı satır satır yürütme mantığı."""
        if not os.path.exists(file_path):
            self.log("ERROR", "file_not_found", file_path)
            return

        if not is_import: self.log("ALIS", "exec_start", file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        idx = 0
        while idx < len(lines):
            cmd_id, params = self.parser.parse_line(lines[idx])
            
            # Fonksiyon Kaydı (.08)
            if cmd_id == "08":
                func_name = params.strip()
                self.mem.functions[func_name] = []
                idx += 1
                while idx < len(lines) and not lines[idx].strip().startswith(".11"):
                    self.mem.functions[func_name].append(lines[idx])
                    idx += 1
                idx += 1
                continue

            # Komutu Çalıştır
            status = self.run_command(cmd_id, params, idx + 1)
            if status == "SKIP": idx += 1
            
            idx += 1
        
        if not is_import: self.log("ALIS", "exec_finish")

if __name__ == "__main__":
    engine = ALISEngine()
    base = os.path.dirname(__file__)
    # Örnek başlangıç yolları
    engine.load_language(os.path.join(base, "languages/tr.json"))
    engine.execute_file(os.path.join(base, "hello_world.alis"))
