import os

def apply_fixes():
    print("🔧 Iniciando parches críticos en l-er-simbio...\n")

    # --- FIX B: Cambiar MD5 por SHA256 en entity_runner.py ---
    path = 'core/entity_runner.py'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        if 'hashlib.md5' in code:
            code = code.replace('hashlib.md5', 'hashlib.sha256')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(code)
            print("✅ [FIX B] SHA256 aplicado en entity_runner.py")
        else:
            print("ℹ️  [FIX B] Ya estaba aplicado o no se encontró md5.")
    else:
        print("❌ [FIX B] No se encontró core/entity_runner.py")

    # --- FIX C: Subir umbral del Sistema Inmune en sistema_inmune.py ---
    path = 'core/sistema_inmune.py'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        if 'if total_campos > 50:' in code:
            code = code.replace('if total_campos > 50:', 'if total_campos > 200:')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(code)
            print("✅ [FIX C] Umbral de 50 a 200 aplicado en sistema_inmune.py")
        else:
            print("ℹ️  [FIX C] Ya estaba aplicado o no se encontró el umbral.")
    else:
        print("❌ [FIX C] No se encontró core/sistema_inmune.py")

    # --- FIX A1 y A2: Tokenizador en glifo_engine.py ---
    path = 'core/glifo_engine.py'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        old_extract = """    def extract_patterns(self, text: str) -> List[str]:
        \"\"\"Simple pattern extraction from a string of glyphs.\"\"\"
        return [glyph for glyph in text if glyph in self.glyphs]"""
        
        new_extract = """    def extract_patterns(self, text: str) -> List[str]:
        import re
        import unicodedata
        text = unicodedata.normalize("NFC", text)
        all_symbols = sorted(list(self.glyphs.keys()) + list(self.operators.keys()), key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(g) for g in all_symbols))
        return pattern.findall(text)"""
        
        if old_extract in code:
            code = code.replace(old_extract, new_extract)
            print("✅ [FIX A1] Tokenizador (extract_patterns) aplicado en glifo_engine.py")

        old_validate = """    def validate_expression(self, expression: str):
        parts = expression.split()
        errors = [f"Position {i+1}: '{s}' is not valid" for i, s in enumerate(parts) if not self.is_valid_glyph(s)]
        return len(errors) == 0, errors"""
        
        new_validate = """    def validate_expression(self, expression: str):
        tokens = self.extract_patterns(expression)
        errors = [f"Token '{t}' no reconocido" for t in tokens if not self.is_valid_glyph(t)]
        return len(errors) == 0, errors"""
        
        if old_validate in code:
            code = code.replace(old_validate, new_validate)
            print("✅ [FIX A2] Tokenizador (validate_expression) aplicado en glifo_engine.py")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
    else:
        print("❌ [FIX A] No se encontró core/glifo_engine.py")

    # --- FIX A3: Tokenizador en ler_parser.py ---
    path = 'core/ler_parser.py'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        old_extract_parser = """    def extract_patterns(self, text: str) -> List[str]:
        \"\"\"Simple pattern extraction from a string of glyphs.\"\"\"
        return [glyph for glyph in text if glyph in self.glyphs]"""
        
        new_extract_parser = """    def extract_patterns(self, text: str) -> List[str]:
        import re
        import unicodedata
        text = unicodedata.normalize("NFC", text)
        all_symbols = sorted(list(self.glyphs.keys()), key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(g) for g in all_symbols))
        return pattern.findall(text)"""
        
        if old_extract_parser in code:
            code = code.replace(old_extract_parser, new_extract_parser)
            print("✅ [FIX A3] Tokenizador (extract_patterns) aplicado en ler_parser.py")
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
    else:
        print("❌ [FIX A] No se encontró core/ler_parser.py")

    print("\n🚀 Parches finalizados.")

if __name__ == '__main__':
    apply_fixes()
