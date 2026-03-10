Python
import json
import os

# ALIS Basit Çeviri Motoru (Demo Prototype)
def run_alis_demo(alis_file, lang_json):
    # Dil dosyasını (JSON) yükle
    try:
        with open(lang_json, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        registry = lang_data['registry']
        
        # .alis dosyasını oku (Örn: 101 "Hello World")
        with open(alis_file, 'r', encoding='utf-8') as f:
            code_line = f.readline().strip()

        # Parçalara ayır (ID ve İçerik)
        parts = code_line.split(" ", 1)
        token_id = parts[0]
        content = parts[1] if len(parts) > 1 else ""

        # ID Karşılığını bul (101 -> yazdir/print)
        command = registry.get(token_id, "UNDEFINED_ID")
        
        print(f"\n--- ALIS ENGINE RUNNING ---")
        print(f"Raw Input (Numerical ID): {code_line}")
        print(f"Loaded Language Pack: {lang_json}")
        print(f"Rendered Output: {command} {content}")
        print(f"---------------------------\n")

    except FileNotFoundError:
        print(f"Error: Could not find {alis_file} or {lang_json}")

# --- TEST ---
# Simulating the bridge: ID 101 from hello_world.alis to Turkish
run_alis_demo("examples/hello_world.alis", "examples/languages/tr.json")
