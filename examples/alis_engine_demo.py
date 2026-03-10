python
import json
import re
import os

class ALISEngine:
    def __init__(self):
        self.variables = {}  # Bellek (Memory)
        self.registry = {}   # Dil Sözlüğü
        self.current_lang = ""

    def load_language(self, lang_json):
        """Sözlüğü yükler ve motoru o dile hazırlar."""
        try:
            with open(lang_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.registry = data['registry']
                self.current_lang = data['language']
                print(f"[*] ALIS Engine: {self.current_lang} environment loaded successfully.")
        except Exception as e:
            print(f"[ERROR]: Could not load language file: {e}")

    def evaluate_params(self, params):
        """Verinin türünü anlar: Metin mi, sayı mı, değişken mi?"""
        params = params.strip()
        if not params: return ""
        # Metin kontrolü (Tırnaklar)
        if (params.startswith('"') and params.endswith('"')) or (params.startswith("'") and params.endswith("'")):
            return params[1:-1]
        # Sayı kontrolü
        try:
            if "." in params: return float(params)
            return int(params)
        except ValueError:
            # Değişken kontrolü (Hafızadan getir)
            return self.variables.get(params, params)

    def parse_line(self, line):
        """ID ve parametreleri ayırır."""
        line = line.strip()
        if not line or line.startswith("//"): return None, None
        
        # .ID Formatını yakala (Örn: .01, .06)
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def execute_file(self, alis_file_path):
        """.alis dosyasını satır satır işler."""
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
        """ID'leri mantığa dönüştüren ana merkez."""
        
        # DEĞİŞKEN ATAMA (No ID, contains '=')
        if not cmd_id and "=" in params:
            parts = params.split("=", 1)
            var_name = parts[0].strip()
            var_val = self.evaluate_params(parts[1])
            self.variables[var_name] = var_val
            return

        # .06: PRINT (Ekrana Yazdır)
        if cmd_id == "06":
            val = self.evaluate_params(params)
            print(f"[OUTPUT]: {val}")

        # .01: IF (Basit Koşul)
        elif cmd_id == "01":
            try:
                condition = eval(params, {}, self.variables)
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
    
    # Dosya yollarını mevcut klasöre göre ayarla
    # Script examples içinde çalıştığı varsayılırsa:
    lang_path = "languages/tr.json"
    code_path = "hello_world.alis"
    
    demo_engine.load_language(lang_path)
    demo_engine.execute_file(code_path)
