import json

class ALISMemory:
    def __init__(self):
        self.variables = {
            "__VERSION__": "2.5.0",
            "PI": 3.14159,
            "TRUE": True,
            "FALSE": False
        }
        self.functions = {}  
        self.registry = {}   
        self.msgs = {}       

    def evaluate(self, expr):
        """Advanced Evaluator with Type Guard and Safety Logic."""
        if not expr: return None
        expr = str(expr).strip()
        
        # 1. String Literal Check
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # 2. Logic & Math Evaluation with TYPE GUARD
        try:
            # Safe evaluation context
            result = eval(expr, {"__builtins__": None}, self.variables)
            return result
        except TypeError as te:
            # Localized: Type mismatch error (DeepSeek will provide the message)
            err_template = self.msgs.get("type_error", "[TYPE GUARD]: Logic mismatch! {}")
            print(err_template.format(te))
            return None
        except NameError as e:
            # Localized: Variable not found
            var_name = str(e).split("'")[1] if "'" in str(e) else "unknown"
            err_template = self.msgs.get("var_undefined", "[PROTECTION]: Variable '{}' not found.")
            print(err_template.format(var_name))
            return None
        except Exception:
            # Fallback to direct variable fetch
            return self.variables.get(expr, expr)

    def set_var(self, name, value):
        """Stores variables only if they pass the Type Guard check."""
        evaluated_val = self.evaluate(value)
        if evaluated_val is not None:
            self.variables[name.strip()] = evaluated_val

    def get_var(self, name):
        """Safe retrieval of variables."""
        val = self.variables.get(name.strip())
        if val is None:
            err_template = self.msgs.get("var_undefined", "[PROTECTION]: '{}' not found.")
            print(err_template.format(name))
            return None
        return val
