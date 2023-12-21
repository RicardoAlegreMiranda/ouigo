from typing import Optional
from dataclasses import dataclass, field

def greet(name: str = field(default="Ana")):
    if name is not None:
        return f"Hello, {name}!"
    else:
        return "Hello, anonymous!"


# Ejemplos de uso
print(greet("Alice"))  # Salida: Hello, Alice!
print(greet())  # Salida: Hello, anonymous!
