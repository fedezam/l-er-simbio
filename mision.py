# mision.py
def sumar_pares(numeros):
    suma = 0
    for num in numeros:
        if num % 2 == 0:
            suma += num
    return suma * 2 # <--- BUG LÓGICO INTENCIONAL

# El test que falla:
assert sumar_pares([1, 2, 3, 4, 5]) == 6, "Fallo: El resultado es incorrecto."
print("¡Misión cumplida! Código correcto.")
