"""
    Elaborado por:
    Alberto Josué Ortiz Rosales
    11-03-22

    Clase cacheline la cual contiene el dato, etiqueta, conjunto al que pertence.
    si ha sido modificado el dato 
"""
class cacheline():
    def __init__(self, index, valid = 0, tag = 0, data = 0, dirtybit = 0  ) -> None:
        """ Inicializa los valores de la clase

        Args:
            index (int): Indica el conjunto (set) al que pertence la línea.
            valid (int, optional): Indica si el dato existe en la caché.  Defaults to 0.
            tag (binary string, optional): Parte de la dirección. Defaults to 0.
            data (hex string, optional): Dato a almacenar en hexadecimal. Defaults to 0.
            dirtybit (int, optional): . Defaults to 0.
        """
        self.index = index
        self.valid = valid
        self.tag = tag
        self.data = data
        self.dirtybit = dirtybit
    def set_atributes(self, index, valid, tag, data, dirtybit):
        """Función que modifica los atributos.

        Args:
            index (int):
            valid (int):
            tag (binary str):
            data (hex str): 
            dirtybit (int): 
        """
        self.index = index
        self.valid = valid
        self.tag = tag
        self.data = data
        self.dirtybit = dirtybit
    def reste_atributes(self):
        """Restablece a 0 todos los atributos.
        """
        self.valid = 0
        self.tag = 0
        self. data = 0
        self. dirtybit = 0
    def flip_true_valid(self):
        """Cambia el valor del bit valido.
        """
        self.valid = 1

    def flip_true_dirty(self):
        """ Cambia el valor del dirty bit."""
        self.dirtybit = 1
    
    def write_data(self, data):
        """Establece el nuevo valor del dato a almacenar.

        Args:
            data (hex str):
        """
        self.data = data
        self.flip_true_dirty()

    
    def print_cache_line(self):
        """Imprime con formato la línea de la caché 
        """
        print ("{:<7} {:<7} {:<7} {:<34} {:<10}".format(self.index, self.valid, self.dirtybit, self.tag, self.data))
        #print(self.index , "  ",self.valid, "   ", self.dirtybit, "   ", self.tag, "     ", self.data )

