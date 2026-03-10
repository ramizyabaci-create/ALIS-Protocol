import json

class ALISMemory:
    def __init__(self):
        # Global constants and versioning
        self.variables = {
            "__VERSION__": "2.4.0",
            "PI": 3.14159,
            "TRUE": True,
            "FALSE": False
        }
        self.functions = {}  
        self.registry = {}   
        self.msgs = {}       # Localized system messages

    def evaluate(self, expr):
        """Advanced Evaluator with Undefined Variable Protection."""
        if not expr: return None
        expr = str(expr).strip()
        
        # 1. String Literal Check
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # 2. Logic & Math Evaluation
        try:
            # We use a restricted environment for security
            return eval(expr, {"__builtins__": None}, self.variables)
        except NameError as e:
            # EXTRACT: Which variable caused the error?
            var_name = str(e).split("'")[1]
            # Use localized message or fallback to default
            err_template = self.msgs.get("var_undefined", "[PROTECTION]: Variable '{}' is not defined yet.")
            print(err_template.format(var_name))
            return None # Prevent crash, return None
        except Exception:
            # If it's not math/logic, it might be a raw string or a single variable
            return self.variables.get(expr, expr)

    def set_var(self, name, value):
        """Safely stores a variable after evaluating its value."""
        self.variables[name.strip()] = self.evaluate(value)

    def get_var(self, name):
        """Retrieves a variable or provides protection feedback."""
        val = self.variables.get(name.strip())
        if val is None:
            err_template = self.msgs.get("var_undefined", "[PROTECTION]: Variable '{}' not found.")
            print(err_template.format(name))
            return None
        return val
     
