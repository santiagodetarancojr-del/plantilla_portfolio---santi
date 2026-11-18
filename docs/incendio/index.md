# Proyecto de incendio

Aquí documentaré la pregunta, los datos, el método, los resultados y las limitaciones del proyecto.

# Incendio Saler

En las últimas sesiones hemos trabajado con un código parecido, por no decir casi igual, al de la primera sesión de imágenes.
Entonces con las dos imágenes que nos proporcionaron empezamos a trabajar.

![Imagen de la combinación de tres colores del antes del Saler](antes_normal.png)
![Imagen de la combinación de tres colores del despues del Saler](despues_normal.png)

Después definimos las zonas verdes con el ndvi y yo también por mi propia cuenta hice la máscara de estas mismas.

![Imagen del ndvi del antes del Saler](antes_ndvi.png)
![Imagen del ndvi del despues del Saler](despues_ndvi.png)
![Imagen del ndvi máscara antes](antes_mascara.png)
![Imagen del ndvi máscara despues](despues_mascara.png)

Ahora empieza la dificultad de este reto, nos piden que distingamos la parte que ha sido incendiada, y despues sacar otra imagen con la diferencia.
Entonces para sacar la diferencia en la línea de código creo la variable "ndvi_dif", y creo la imagen con tonos rojos, y para la imagen de la zona quemada la variable "quemado".

![Imagen del ndvi_dif del Saler](diferencia_rojo.png)
![Imagen de la parte incendiada del Saler](parte_incendiada.png)

Por último para sacar la imagen de la diferencia de la vegetación creo la variable nbr, que es la división del antes y después, y ahí doy por finalizado el reto.

![Imagen del nbr del Saler](diferencia_nbr.png)

O al menos eso creía porque faltaba hacer más cosas como primero arreglar mi nbr y crear otras imágenes, como la severidad, una representación del área afectada. Entonces creo otras imágenes  de diferencia de vegetación en grises y otra imágen que define la diferencia de nbr y ndvi en rojo.

![Imagen del Saler correción en grises](dif_grises.png)
![Imagen de dif entre nbr y ndvi en rojo](nbr_y_ndvi_en_rojo.png)

Después para la severidad en un principio la calculo y con ello aparece una imagen que tiene defectos (unos píxeles sueltos que no forman parte del incendio y su área afectada).

![Imagen de severidad sin corregir](severidad_con_imperf.png)

Con esto intento solucionar el problema, creo una copia del código y con ella hago pruebas que concluyen en una imagen de la severidad más clara sin imperfecciones.

![Imagen de severidad corregida](severidad_perfecta.png)

Y por último hago que calcule desde la terminal cuánta área ha sido afectada en hectáreas teniendo en cuenta esa diferencia que extraigo del área quemada y también de esta misma área sin aquellas imperfecciones, o islas, borradas:

El área calculada con NDVI es 20.60 ha

El área calculada con NBR es 32.32 ha

Área NBR sin islas: 29.28 ha