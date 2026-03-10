python
import json
import re

class ALISEngine:
    def __init__(self):
        self.variables = {}  # Kullanıcı değişkenlerini burada tutuyoruz
        self.registry = {}   # Seçilen dilin komut tablosu
        self.current_lang = ""

    def load_language(self, lang_json):
        """Dil paketini yükler."""
        with open(lang_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.registry = data['registry']
            self.current_lang = data['language']
            print(f"[*] ALIS Engine: {self.current_lang} environment loaded.")

    def parse_line(self, line):
        """Satırı komut (ID), parametre ve içerik olarak ayırır."""
        # Regex ile komutu (.ID) ve sonrasını ayırıyoruz
        match = re.match(r"^\.(\d+)\s*(.*)", line.strip())
        if not match:
            # Eğer başında nokta yoksa, bu bir değişken ataması veya veri olabilir
            return None, line.strip()
        
        command_id = match.group(1)
        params = match.group(2)
        return command_id, params

    def execute(self, alis_file):
        """ALIS dosyasını satır satır okur ve işler."""
        print(f"--- STARTING EXECUTION: {alis_file} ---")
        with open(alis_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip() or line.startswith("//"): continue # Boşluk ve yorumları atla
                
                cmd_id, params = self.parse_line(line)
                self.run_command(cmd_id, params, line_num)
        print("--- EXECUTION FINISHED ---")

    def run_command(self, cmd_id, params, line_num):
        """Komutları mantığa döker."""
        # (Bu kısım Bölüm 2'de genişletilecek)
        if cmd_id == "06": # PRINT
            # Tırnak içindeki metni veya değişkeni bul
            output = self.evaluate_params(params)
            print(output)
            def evaluate_params(self, params):
        """Parametreleri analiz eder: Sayı mı, metin mi, yoksa değişken mi?"""
        params = params.strip()
        # Eğer tırnak içindeyse metindir
        if (params.startswith('"') and params.endswith('"')) or (params.startswith("'") and params.endswith("'")):
            return params[1:-1]
        # Eğer sayıysa sayıya çevir
        try:
            if "." in params: return float(params)
            return int(params)
        except ValueError:
            # Sözlükte (hafızada) ara
            return self.variables.get(params, f"ERR: {params} is undefined")

    def run_command(self, cmd_id, params, line_num):
        """ALIS ID'lerini Python mantığına dönüştürür."""
        
        # 1. DEĞİŞKEN ATAMA MANTIĞI (Örn: sayi = 10)
        if not cmd_id and "=" in params:
            var_name, var_val = params.split("=", 1)
            self.variables[var_name.strip()] = self.evaluate_params(var_val)
            return

        # 2. .06: PRINT (Çıktı)
        if cmd_id == "06":
            output = self.evaluate_params(params)
            print(f"[OUTPUT]: {output}")

        # 3. .01: IF (Koşul - Basit Karşılaştırma)
        elif cmd_id == "01":
            # Örn: .01 x > 5
            # Basit bir mantık kontrolü (Geliştirilecek)
            condition_met = eval(params, {}, self.variables)
            if not condition_met:
                print(f"[INFO]: Line {line_num} condition not met. Skipping...")
                # (Döngü atlama mantığı Bölüm 3'te eklenecek)

        # 4. .11: BREAK (Döngü Kırma)
        elif cmd_id == "11":
            print(f"[SYSTEM]: Break called at line {line_num}")
            return "BREAK"

# --- TEST PROGRAMI (KODUN SONUNA EKLE) ---
if __name__ == "__main__":
    engine = ALISEngine()
    # Dil dosyasını yükle (Yolun doğru olduğundan emin ol)
    try:
        engine.load_language("languages/tr.json")
        # Önce bir değişken atayalım, sonra yazdıralım
        print("\n--- RUNNING INTERNAL TEST ---")
        engine.run_command(None, "sayi = 42", 1)
        engine.run_command("06", "sayi", 2)
        print("--- TEST FINISHED ---\n")
    except Exception as e:
        print(f"Test Error: {e}")
        import json
import re

class ALISEngine:
    def __init__(self):
        self.variables = {}  # Hafıza (Memory)
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
        
        # .ID Formatını yakala (Örn: .06)
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def execute_file(self, alis_file_path):
        """.alis dosyasını satır satır işler."""
        print(f"\n--- ALIS EXECUTION START: {alis_file_path} ---")
        try:
            with open(alis_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            line_idx = 0
            while line_idx < len(lines):
                line = lines[line_idx].strip()
                cmd_id, params = self.parse_line(line)
                
                if cmd_id:
                    # Komutu çalıştır
                    result = self.run_command(cmd_id, params, line_idx + 1)
                    # Eğer BREAK (.11) gelirse döngüden çık (Gelecekteki looplar için)
                    if result == "BREAK": break
                elif params and "=" in params:
                    # Değişken ataması (Örn: x = 5)
                    self.run_command(None, params, line_idx + 1)
                
                line_idx += 1
            print("--- ALIS EXECUTION FINISHED ---")
        except FileNotFoundError:
            print(f"[ERROR]: File {alis_file_path} not found.")

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
            # Basit bir eval mantığı (Geliştirilebilir güvenli bir parser ile)
            try:
                condition = eval(params, {}, self.variables)
                if not condition:
                    print(f"[LOG]: Line {line_num} condition ({params}) not met.")
                    # Gelecek versiyonda: Bloğu atla mantığı eklenecek
            except Exception as e:
                print(f"[SYNTAX ERROR]: Line {line_num} -> {e}")

        # .11: BREAK
        elif cmd_id == "11":
            return "BREAK"

# --- ALIS BOOTSTRAP ---
if __name__ == "__main__":
    demo_engine = ALISEngine()
    
    # 1. Dili Yükle
    demo_engine.load_language("languages/tr.json")
    
    # 2. Örnek dosyayı çalıştır (Önce hello_world.alis'i .06 ile güncellemiş olmalısın)
    # Eğer dosya yoksa hata vermemesi için kontrol:
    demo_engine.execute_file("hello_world.alis")
