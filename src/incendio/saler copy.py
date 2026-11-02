import matplotlib.pyplot as plt
from pathlib import Path
import rasterio
import numpy as np

# CAMBIO 1: Importamos label para identificar grupos
# de píxeles conectados.
from scipy.ndimage import label


carpeta = Path(__file__).parent

with rasterio.open(carpeta / "Incendio_saler/B04_antes_20m.tif") as src:
    rojo_a = src.read(1)
with rasterio.open(carpeta / "Incendio_saler/B03_antes_20m.tif") as src:
    verde_a = src.read(1)
with rasterio.open(carpeta / "Incendio_saler/B02_antes_20m.tif") as src:
    azul_a = src.read(1)
with rasterio.open(carpeta / "Incendio_saler/B08_antes_20m.tif") as src:
    ir_a = src.read(1)
with rasterio.open(carpeta / "Incendio_saler/B12_antes_20m.tif") as src:
    swir_a = src.read(1)

with rasterio.open(carpeta / "Incendio_Saler29/B04_despues_20m.tif") as src:
    rojo_d = src.read(1)
with rasterio.open(carpeta / "Incendio_Saler29/B03_despues_20m.tif") as src:
    verde_d = src.read(1)
with rasterio.open(carpeta / "Incendio_Saler29/B02_despues_20m.tif") as src:
    azul_d = src.read(1)
with rasterio.open(carpeta / "Incendio_Saler29/B08_despues_20m.tif") as src:
    ir_d = src.read(1)
with rasterio.open(carpeta / "Incendio_Saler29/B12_despues_20m.tif") as src:
    swir_d = src.read(1)


rgb_a = np.dstack((rojo_a, verde_a, azul_a))
rgb_d = np.dstack((rojo_d, verde_d, azul_d))


# CAMBIO 2: Convertimos las bandas utilizadas para los índices
# a números decimales. Así evitamos errores en las restas
# cuando las imágenes originales contienen enteros sin signo.
# Lo hacemos después de crear las imágenes RGB para no
# modificar su representación original.
rojo_a = rojo_a.astype(float)
rojo_d = rojo_d.astype(float)
ir_a = ir_a.astype(float)
ir_d = ir_d.astype(float)
swir_a = swir_a.astype(float)
swir_d = swir_d.astype(float)


ndvi_a = (ir_a - rojo_a) / (ir_a + rojo_a)
ndvi_d = (ir_d - rojo_d) / (ir_d + rojo_d)
ndvi_dif = ndvi_a - ndvi_d

nbr_a = (ir_a - swir_a) / (ir_a + swir_a)
nbr_d = (ir_d - swir_d) / (ir_d + swir_d)
nbr_dif = nbr_a - nbr_d


# CLASIFICACIÓN DE SEVERIDAD

severidad = np.zeros(nbr_dif.shape, dtype=int)
vegetacion = ndvi_a > 0.4

severidad[(nbr_dif >= 0.1) & (nbr_dif < 0.27) & vegetacion] = 1
severidad[(nbr_dif >= 0.27) & (nbr_dif < 0.66) & vegetacion] = 2
severidad[(nbr_dif >= 0.66) & vegetacion] = 3


# CAMBIO 3: ELIMINACIÓN DE ISLAS AISLADAS

# Identificamos los píxeles afectados.
afectado = severidad > 0

# Asignamos un número diferente a cada grupo de píxeles
# conectados. Consideramos también las diagonales.
etiquetas, numero_grupos = label(
    afectado, structure=np.ones((3, 3))
)

# Contamos cuántos píxeles tiene cada grupo.
tamanos = np.bincount(etiquetas.ravel())

# La etiqueta 0 corresponde al fondo.
# La excluimos para que no sea seleccionada.
tamanos[0] = 0

# Identificamos el grupo más grande.
grupo_principal = np.argmax(tamanos)

# Creamos una máscara que contiene únicamente ese grupo.
mascara_principal = etiquetas == grupo_principal

# Eliminamos los demás grupos, pero conservamos los valores
# originales de severidad (1, 2 y 3) del incendio principal.
severidad_limpia = np.where(mascara_principal, severidad, 0)


# REPRESENTACIÓN DE IMÁGENES

plt.figure(1)
plt.imshow(rgb_a)

plt.figure(2)
plt.imshow(rgb_d)

plt.figure(3)
plt.imshow(ndvi_a, cmap="RdYlGn", vmin=-1, vmax=1)

plt.figure(4)
plt.imshow(ndvi_d, cmap="RdYlGn", vmin=-1, vmax=1)

plt.figure(5)
plt.imshow(ndvi_dif, cmap="Reds", vmin=0, vmax=1)


vegetacion_a = (ndvi_a > 0.4).astype(int)
vegetacion_d = (ndvi_d > 0.4).astype(int)

quemado_ndvi = (ndvi_a > 0.4) & (ndvi_d < 0.2)


plt.figure(6)
plt.imshow(quemado_ndvi)


plt.figure(7)
plt.imshow(nbr_dif, cmap="gray", vmin=-1, vmax=1)
plt.colorbar()


quem_nbr = (nbr_dif > 0.2) & (ndvi_a > 0.4)


plt.figure(8)
plt.imshow(quem_nbr.astype(int), cmap="Reds")
plt.colorbar()


# Imagen de severidad original
plt.figure(9)
plt.imshow(rgb_a)
plt.imshow(
    np.where(severidad == 0, np.nan, severidad),
    cmap="autumn_r", vmin=1, vmax=3, alpha=0.85
)
plt.colorbar(ticks=[1, 2, 3]).set_ticklabels(
    ["Baja", "Media", "Alta"]
)
plt.title("Severidad estimada del incendio")


# CAMBIO 4: Añadimos una figura con la máscara limpia.
# Mantenemos también la original para poder compararlas.
plt.figure(10)
plt.imshow(rgb_a)
plt.imshow(
    np.where(severidad_limpia == 0, np.nan, severidad_limpia),
    cmap="autumn_r", vmin=1, vmax=3, alpha=0.85
)
plt.colorbar(ticks=[1, 2, 3]).set_ticklabels(
    ["Baja", "Media", "Alta"]
)
plt.title("Severidad estimada - incendio principal")


# CÁLCULO DE ÁREAS

area_ndvi = np.count_nonzero(quemado_ndvi) * 20 * 20 / 10000
area_nbr = np.count_nonzero(quem_nbr) * 20 * 20 / 10000

print(f"El área calculada con NDVI es {area_ndvi:.2f} ha")
print(f"El área calculada con NBR es {area_nbr:.2f} ha")


# CAMBIO 5: Calculamos la superficie usando solamente
# los píxeles del incendio principal.
# Conservamos el umbral original dNBR > 0.2.
quem_nbr_limpio = quem_nbr & mascara_principal

area_nbr_limpia = (
    np.count_nonzero(quem_nbr_limpio) * 20 * 20 / 10000
)

print(f"Área NBR sin islas: {area_nbr_limpia:.2f} ha")


# CAMBIO 6: Mostramos cuántos grupos se han detectado
# y cuántos píxeles hemos eliminado de la clasificación.
eliminados = (
    np.count_nonzero(severidad)
    - np.count_nonzero(severidad_limpia)
)

print(f"Grupos detectados: {numero_grupos}")
print(f"Píxeles eliminados: {eliminados}")


plt.show()