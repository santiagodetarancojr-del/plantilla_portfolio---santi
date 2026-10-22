size = 1500
transferencia = 25
tiempo_total = (size / transferencia) +30
tiempo_minutos = tiempo_total / 60

print(f"Tamaño de disco {size}")
print(f"La velocidad de transferencia es: {transferencia}")
print(f"El tiempo total estimado es de: {tiempo_minutos} minutos")
