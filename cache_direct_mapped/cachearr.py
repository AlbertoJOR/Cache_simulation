"""
    Elaborado por:
    Alberto Josué Ortiz Rosales
    11-03-22

    Clase cachearr: Forma un arreglo de la clase cacheline para 
    conformar una memoria caché. Contiene un diccionario para 
    simular una RAM como memoria principal.
"""
import cacheline as CL
import random 

def binaryToDec(n):
    """Convierte una cadena binaría en decimal

    Args:
        n (binary str):

    Returns:
        int: Valor en decimal
    """
    return (int(n,2))

def hexToDec(n):
    """Convierte una cadena hexadecimal en decimal.

    Args:
        n (hex str): 

    Returns:
        int: Valor decimal.
    """
    return (int(n,16))


def decimalToBinary(n,s):
    """Convierte un decimal en una cadena binaria.

    Args:
        n (int): valor a transformar
        s (int): tamaño de la cadena a generar.

    Returns:
        int: 
    """
    x= '{0:0'+str(s)+'b}'
    return x.format(n)

def decimalToHex(n,s):
    """Convierte un decimal a una cadena hexadecimal.

    Args:
        n (int): valor a transformar
        s (int): tamaño de la cadena a generar.

    Returns:
        int: 
    """
    x= '{0:0'+str(s)+'x}'
    return x.format(n)

def randompower2(p):
    """Genera un número aleatorio en el intervalo de 0 - 2^p -1


    Returns:
        int :
    """
    return (random.randint(0,(2**p-1)))

def generate32drnd():
    """Genera una cadena hexadecimal aleatoria de 32 bits

    Returns:
        hex str:
    """
    return decimalToHex(randompower2(32),8)



class cachearr():
    main_mem= {}    # Diccionario vacio
    cachebank = []
    def __init__(self, numsets, wb=False) -> None:
        """Inicializa los valores de la caché

        Args:
            numsets (int): indica la cantidad de conjuntos a formar (2^n), 
            wb (bool, optional): Indica si se realiza la política write back. Defaults to False.
        """
        self.numsets = numsets
        self.wb= wb  
        for i in range(0,2**self.numsets):
            # Se generan las línead de la caché vacias
            self.cachebank.append(CL.cacheline(i))

    def print_cache(self):
        """Imprime los contenidos de la caché en forma de tabla
        """
        print("CACHE:")
        print ("{:<7} {:<7} {:<7} {:<34} {:<10}".format('index','valid','dirty','tag','data'))
        #print("index", "  ","valid", "   ", "dirty", "   ", "tag", "     ", "data" )
        for i in range(0,2**self.numsets):
            self.cachebank[i].print_cache_line()

        print()
    def load(self, addr):
        """Simula la intrucción de carga

        Args:
            addr (hex str):
        """
        # Se obtienen el Tag y el Set de la dirección
        addint = hexToDec(addr)
        binaddr= decimalToBinary(addint,32)
        tag = binaddr[:-(2+self.numsets)]
        ch_set= binaddr[-(2+self.numsets):-2]
        ch_set_dec = binaryToDec(ch_set)

        # Extraer la línea de la caché del set.
        ch_line = self.cachebank[ch_set_dec]

        if(ch_line.valid==0 or(ch_line.tag != tag)):
            # Si no hay datos en la caché o la etiqueta no coincide.
            # Se tiene que buscar el dato en memoria.
            print("LOAD: Cache miss")
            if(ch_line == 0 ):
                print("Not valid")
            elif(ch_line.tag != tag):
                print("Different Tag")
            # buscar el dato en la memoria
            data = None
            if binaddr in self.main_mem:
                # Si existe en la memoría
                data = self.main_mem[binaddr]
                print("addr: ", addr, "  data:", data)
            else:
                # Simular que hay un dato en memoria que sea aleatorio 
                n = randompower2(32)
                data = decimalToHex(n,8)
                self.main_mem[binaddr] = data
                
                print("addr: ", addr, "  data:", data )
            self.cachebank[ch_set_dec].set_atributes(ch_set_dec, 1, tag, data,0)

        else:
            print("LOAD: Cache hit")
            print("addr: ", addr, "  data:", ch_line.data)
        print()

    def writeback(self, addr, data):
        """Realiza la política de escritura write back

        Args:
            addr (hex str): 
            data (hex str): 
        """
        addr_dec = hexToDec(addr)
        addr_bin = decimalToBinary(addr_dec, 32)

        Tag = addr_bin[:-(2+ self.numsets)]
        ch_set= addr_bin[-(2+self.numsets):-2]
        set_dec = binaryToDec(ch_set)
        ch_line = self.cachebank[set_dec]

        if(ch_line.tag != Tag):
            print("Write: Cache miss")
            # Escribir en memoria
            if ch_line.dirtybit :
                # Si el dato ha sido modificado y se tiene que remplazar
                # Se tiene que escribir en memoria principal.
                print("Data written  in memory")
                self.main_mem[addr_bin] = ch_line.data

            # Cambiar la cache
            self.cachebank[set_dec].set_atributes(set_dec, 1, Tag, data,0)
            # Escribir el nuevo dato en memoria
            self.main_mem[addr_bin] = self.cachebank[set_dec].data

        else:
            print("Write: Cache hit")
            self.cachebank[set_dec].write_data(data)
        print()




    def writethrough(self, addr, data):
        """Aplica la política write through

        Args:
            addr (str hex): 
            data (hex str): 
        """
        addr_dec = hexToDec(addr)
        addr_bin = decimalToBinary(addr_dec, 32)

        # Escribir en la caché
        Tag = addr_bin[:-(2+ self.numsets)]
        ch_set= addr_bin[-(2+self.numsets):-2]
        set_dec = binaryToDec(ch_set)

        self.cachebank[set_dec].set_atributes(set_dec, 1, Tag, data, 0)

        # Escribir en memoria 
        self.main_mem[addr_bin] = data

    def write( self, addr, data):
        """Método que simula la instrucción de escritura en la caché
        Aplica la poplítica correspondiente.

        Args:
            addr (hex str):
            data (hex str):
        """
        if self.wb:
            self.writeback( addr, data)
        else: 
            self.writethrough( addr, data)




