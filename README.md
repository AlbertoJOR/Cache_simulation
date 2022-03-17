# Cache_simulation
El proposito de este repositorio es mostrar el funcionamiento de los distintos tipos de caché usando python3. Los tipos de cachés a mostrar son:

- Mapeo directo.
- Asociativa 2 bloques.
- Asociativa 4 bloques.
- Totalmente Asociativa.

Se realiza mediante una clase llamada cachearr que consisten en un arreglo de subclases cacheline, las cuales contienen los datos de una líne de una caché (bit valido, etiqueta, bit sucio, set, dato), para simular la memoria principal se hace uso de un diccionario y para aplicar las políticas de remplazo se hace uso de una lista. La simulación es llevada a cabo por tres métodos básicos: 

- **Load** se encaga de simula la instrucción de cargar un dato desde la caché, si se produce un miss entonces lo buscará en la memoria principal y se aplica algún tipo de política de remplazo (_FIFO_, _LRU_, _ALEATORIO_) en las memorias asociativas.
- **write** escribe un dato en la memoria caché, si se produce un miss se aplica la técnica de remplazo correspondiente en las memorias asociativas (_FIFO_, _LRU_, _ALEATORIO_), también se selecciona el tipo de política que se quiere seguir al escribir( _write back_, _write through_).
- **print_cache** se encarga de desplegar los contenidos de la caché en la pantalla.
