intensidad = float(input("Introduce el valor de la intensidad del bit "))

if intensidad < 0 or intensidad >255:
    print("Intensidad inválida")
elif intensidad < 99:
    print("Intensidad baja")
elif intensidad < 199:
    print("Intensidad media")
else:
    print("Intensidad alta")
