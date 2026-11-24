# Creación de app

En esta última recta del trimestre hemos procedido a hacer un reto en el que se nos pedía crear una app de reservas de material de informática para el cole.
Y nos daban como herramienta; a parte de los horarios, un excel con todo el material y un código básico de referencia; la posibilidad de utilizar la IA.
Entonces nos pusimos manos a la obra.

Para empezar creé una carpeta en "src" donde escribiría mi código y utilizaría para guardar cualquier archivo involucrado.
Después empecé a comprender como funcionaba el lanzador streamlit a base de intentos de hacer operar el código base proporcionado y a partir de ello cogí toda la información y se la pasé a "NotebookLM" el cual me entrego un código bastante primitivo con el cual trabajé.

Al lanzar el código me di cuenta de que necesitaba mucho más que la función de cancelar reservas, que yo mismo le pedí a esta IA.

Entonces volví con NotebookLM y le presente una lista de ideas, que decidió ignorar, en ese momento cambié de IA a Gemini, con la cual cambié mi código hasta el punto de conseguir una aplicación totalmente funcional con: pantalla de registro, pantalla de elección de ciclo entre Infantil, Primaria y Secundaria, una pantalla completamente funcional de registro de daños en material con comentarios y conexión a la cantidad de unidades posibles a reservar, una pantalla por cada ciclo que contenía un sistema de reserva funcional independiente a los otros ciclos con registro público de todas las reservas y otro privado para el usuario para que pueda cancelar la reserva, y por último botones que den acceso a las pantallas anteriores.

Lo único que me faltaba era darle un diseño fresco que conseguí cambiando la translucidad de la tarjeta, añadiendo fondos por cada ciclo y uno general para registro de usuario, menú y registro de daños. Con estas mejoras conseguí llegar a la versión última de mi aplicación, la cual actualicé en github y extraí el código URL que ahora os proporciono.


[Pulsa aquí para entrar](https://plantillaportfolio---santi-hzcaspxqv3hcztobjztlzq.streamlit.app/)