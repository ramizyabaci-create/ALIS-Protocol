
import re

class ALISParser:
    @staticmethod
    def parse_line(line):
        """Standard ALIS Lexer: Splits .ID and Parameters."""
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith("//"): 
            return None, None
        
        # Protocol standard: . followed by digits (e.g., .01, .06)
        match = re.match(r"^\.(\d+)\s*(.*)", line)
        if match:
            return match.group(1), match.group(2)
        
        # If no .ID, check for variable assignments (e.g., x = 5)
        if "=" in line:
            return None, line
            
        return "RAW", line
