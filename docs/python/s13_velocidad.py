entrada_1 = input("Dime una disancia para metros: ")
entrada_2 = input("Dime un tiempo para segundos: ")

print(type(entrada_1))

distancia_m = float(entrada_1)

tiempo_s = float(entrada_2)

velocidad_1 = distancia_m / tiempo_s

velocidad_2 = velocidad_1 * 3.6

print(f"La distancia es {distancia_m / 1000}")
print(f"La distancia es {tiempo_s/ 3600}")
print(f"La velocidad es {velocidad_2}")
