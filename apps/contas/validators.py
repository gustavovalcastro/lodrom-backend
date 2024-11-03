import re

def invalid_phone_number(celular):
    # Pattern for (XX)XXXXX-XXXX
    modelo = r'\(\d{2}\)\d{5}-\d{4}'
    return not re.fullmatch(modelo, celular)
