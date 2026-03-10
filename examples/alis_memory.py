import json

class ALISMemory:
    def __init__(self):
        # Initial memory with system constants
        self.variables = {
            "__VERSION__": "2.2.0",
            "PI": 3.14159,
            "TRUE": True,
            "FALSE": False
        }
        self.functions = {}  # Store code blocks
        self.registry = {}   # ID mappings
        self.msgs = {}       # System UI messages

    def evaluate(self, expr):
        """Advanced Evaluator: Strings, Math, and Variable Resolution."""
        if not expr: return None
        expr = str(expr).strip()
        
        # String detection (Quotes)
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Mathematical and Logical Evaluator
        try:
            # Safe evaluation within the engine's memory context
            return eval(expr, {"__builtins__": None}, self.variables)
        except:
            # Fallback: Return stored variable or raw string
            return self.variables.get(expr, expr)

    def set_var(self, name, value):
        """Stores a variable in memory."""
        self.variables[name.strip()] = self.evaluate(value)

    def get_var(self, name):
        """Retrieves a variable from memory."""
        return self.variables.get(name.strip(), f"UNDEFINED: {name}")
