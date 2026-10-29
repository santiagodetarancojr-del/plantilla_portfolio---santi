import matplotlib.pyplot as plt
from pathlib import Path
import rasterio
import numpy as np

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

rgb_a = np.dstack((rojo_a,verde_a,azul_a))
rgb_d = np.dstack((rojo_d,verde_d,azul_d))

plt.figure(1)
plt.imshow(rgb_a)

plt.figure(2)
plt.imshow(rgb_d)

ndvi_a = (ir_a - rojo_a) / (ir_a + rojo_a)

plt.figure(3)
plt.imshow(ndvi_a, cmap="RdYlGn" , vmin= -1, vmax= 1)
plt.colorbar()

ndvi_d = (ir_d - rojo_d) / (ir_d + rojo_d)

plt.figure(4)
plt.imshow(ndvi_d, cmap="RdYlGn" , vmin= -1, vmax= 1)
plt.colorbar()

vegetacion_a = (ndvi_a > 0.4).astype(int)
vegetacion_d = (ndvi_d > 0.4).astype(int)

plt.figure(5)
plt.imshow(vegetacion_a, cmap="gray")

plt.figure(6)
plt.imshow(vegetacion_d, cmap="gray")

ndvi_dif = ndvi_a - ndvi_d

plt.figure(7)
plt.imshow(ndvi_dif, cmap ="Reds" , vmin= 0 , vmax= 1)

quemado = vegetacion_a - vegetacion_d

plt.figure(8)
plt.imshow(quemado > 0)

nbr_a = (ir_a - swir_a) / (ir_a + swir_a)
nbr_d = (ir_d - swir_d) / (ir_d + swir_d)
nbr_dif = nbr_a - nbr_d
quem_nbr = (nbr_dif >0.2) & (ndvi_a > 0.4)
plt.figure(9)
plt.imshow(quem_nbr, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="NBR")

#Cálculo de áreas
area_ndvi = np.count_nonzero(quemado) * 20 * 20 /10000
area_nbr = np.count_nonzero(quem_nbr) * 20 * 20 / 10000
print(f"El área quemada calculada con NDVI es {area_ndvi}ha")
print(f"El área quemada calculada con  el NBR es {area_nbr} ha")

plt.show()