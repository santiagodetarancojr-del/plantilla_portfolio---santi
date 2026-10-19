
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ruta = Path(__file__).parent / "foto.jpg"
ruta = Path(__file__).parent / "foto2.jpg"
imagen = plt.imread(ruta)


rojo = imagen[:,:,0]
verde  = imagen[:,:,1]
azul = imagen[:,:,2]

plt.figure(1)
plt.imshow(rojo, cmap="Reds")

plt.figure(2)
plt.imshow(azul,cmap="Blues")

plt.figure(3)
plt.imshow(verde, cmap="Greens")

plt.figure(4)
plt.imshow(imagen)

plt.figure(5)
rgb = np.dstack((verde, azul, rojo))
plt.imshow(rgb)

plt.show()