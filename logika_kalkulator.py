# logika_kalkulator.py

import math

def evaluate_expression(expression):
    try:
        # Menangani fungsi matematika seperti log dan sqrt yang mungkin dimasukkan di basic calculator
        expression = expression.replace('sqrt(', 'math.sqrt(').replace('log(', 'math.log10(')
        # Ganti ^ dengan ** untuk perpangkatan
        expression = expression.replace('^', '**')
        
        result = eval(expression)
        return result
    except Exception:
        return "Error"

def calculate_function(func_name, value):
    try:
        value = float(value)
        if func_name == "sin":
            return round(math.sin(math.radians(value)), 4)
        elif func_name == "cos":
            return round(math.cos(math.radians(value)), 4)
        elif func_name == "tan":
            return round(math.tan(math.radians(value)), 4)
        elif func_name == "log":
            return round(math.log10(value), 4)
        elif func_name == "sqrt":
            return round(math.sqrt(value), 4)
        else:
            return "Error"
    except Exception:
        return "Error"

def convert_units(value, from_unit, to_unit, factor):
    try:
        return value * factor
    except Exception:
        return "Error"