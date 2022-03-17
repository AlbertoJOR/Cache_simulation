"""
    Elaborado por:
    Alberto Josué Ortiz Rosales
    11-03-22

    Clase cachearr: Forma un arreglo de la clase cacheline para 
    conformar una memoria caché. Contiene un diccionario para 
    simular una RAM como memoria principal.

    Puede simular las políticas de remplazo: FIFO, Aleatoría, LRU.
    Esta caché es de 2 vías.
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
    def __init__(self, numsets, wb=False, replace = 0) -> None:
        """Inicializa los valores de la caché

        Args:
            numsets (int): indica la cantidad de conjuntos a formar (2^n), 
            wb (bool, optional): Indica si se realiza la política write back. Defaults to False.
            replace (int, optional): Establece la política de remplazo a seguir
            0 = Aleatorio, 1 = FIFO, 2 = LRU. Defaults to 0.
        """
        self.numsets = numsets
        self.wb= wb  
        self.rep_pol = replace
        for i in range(0,2**self.numsets):
            # Genera la caché vacia
            self.cachebank.append(CL.cacheline(i))
        repla_list=[] 
        self.cachebank.append(repla_list)

    def print_cache(self):
        """Imprime los contenidos de la caché en forma de tabla
        """
        print("CACHE BLOCK 1:")
        print ("{:<7} {:<7} {:<7} {:<34} {:<10}".format('index','valid','dirty','tag','data'))
        #print("index", "  ","valid", "   ", "dirty", "   ", "tag", "     ", "data" )
        for i in range(0,2**self.numsets):
            self.cachebank[i].print_cache_line()

        print()
    
        print("Lista  de remplazo", ":", self.cachebank[2**self.numsets])

        print()
    def load(self, addr):
        """Simula la intrucción de carga

        Args:
            addr (hex str):
        """
        # Se obtienen el Tag 
        addint = hexToDec(addr)
        binaddr= decimalToBinary(addint,32)
        tag = binaddr[:-2]

        for i in range(0, 2** self.numsets):
            if(self.cachebank[i].tag == tag or self.cachebank[i].valid):
                print("LOAD  hit")
                print("addr: ", addr, "  data:", self.cachebank[i].data)
                if(self.rep_pol == 2 ):
                # Si se unsa LRU se actualiza el dato al más utilizado
                    self.read_LRU(i)
                print()
                return 

        print("LOAD: Cache miss")

        # buscar el dato en la memoria
        data = None
        if binaddr in self.main_mem:
            # Existe el dato en memoria.
            data = self.main_mem[binaddr]
            print("In addr: ", addr, "  data:", data)
        else:
            # Simular que hay un dato en memoria
            # Si no se encuentra genera uno aleatorio
            n = randompower2(32)
            data = decimalToHex(n,8)
            self.main_mem[binaddr] = data
                
            print("addr: ", addr, "  data:", data )
        # Ver que dato remplazar con la política
        n_ind = self.replace(tag)
        self.cachebank[n_ind].set_atributes(n_ind, 1, tag, data,0)
        print()

        return


    def writeback(self,data, Tag, addr_bin):
        """Aplica la escritura con la política de Write Back.

        Args:
            data (str hex): 
            Tag (str bin): 
            set_dec (int):
            addr_bin (str bin):
            i_index (int): indicé de la vía de la caché
        """

        for i in range(0, 2** self.numsets):
            if(self.cachebank[i].tag ==Tag):
                print("Write hit  hit")
                self.cachebank[i].write_data(data)
                print("set: ", self.cachebank[i].index, "  data:", self.cachebank[i].data)
                if(self.rep_pol == 2 ):
                # Si se unsa LRU se actualiza el dato al más utilizado
                    self.read_LRU(i)
                print()
                return 

        print("Write: Cache miss")
        # Escribir en memoria
        i_index = self.replace( Tag)
        if self.cachebank[i_index].dirtybit :
            print("Replaced data written  in memory")
            self.main_mem[addr_bin] = self.cachebank[i_index].data
        # Cambiar la cache
        self.cachebank[i_index].set_atributes(i_index, 1, Tag, data,0)
        if self.cachebank[i_index].dirtybit == 0:
            print("New data written  in memory")
            self.main_mem[addr_bin] = self.cachebank[i_index].data
        return
                

        



    def writethrough(self, data, Tag, addr_bin):
        """Aplica la política write through

        Args:
            data (str hex): 
            Tag (str bin): 
            set_dec (int):
            addr_bin (str bin):
            i_index (int): indicé de la vía de la caché
        """
        ind_block= self.replace( Tag)
        self.cachebank[ind_block].set_atributes(ind_block,1, Tag, data, 0)

        # Escribir en memoria 
        self.main_mem[addr_bin] = data

    def write( self, addr, data):
        """Método que simula la instrucción de escritura en la caché
        Aplica la poplítica correspondiente

        Args:
            addr (hex str):
            data (hex str):
        """
        addr_dec = hexToDec(addr)
        addr_bin = decimalToBinary(addr_dec, 32)

        # Escribir en la caché
        Tag = addr_bin[:-2]
        
        
        if self.wb:
            self.writeback( data, Tag, addr_bin )
        else: 
            self.writethrough( data, Tag, addr_bin)

        print("Write add:  ", addr, "data:  ", data )

    def replace_FIFO(self, Tag):
        """Determina la pol FIFO. Va cambiando la lista
        de remplazo. 


        Args:
            n_set (int): indice del set

        Returns:
            int: indice que se tiene que remplazar del bloque

        """
        len_fifo = len(self.cachebank[2**self.numsets])
        for i in range (0 , 2**self.numsets):
            if len_fifo == i:
                for j in range(0, i):
                    if (Tag == self.cachebank[j].tag):
                        return j
                self.cachebank[2**self.numsets].append(i)
                return i
        
        # Remplazar el primero y meterlo a la cola
        # Sirve para LRU 
        n_block = self.cachebank[2**self.numsets].pop(0)
        self.cachebank[2**self.numsets].append(n_block)
        return n_block
        
    def replace_Rand(self, Tag):
        """Remplaza aleatoriamente.

        Args:
            n_set (int): indice del dato en el que se encuentra.

        Returns:
            int : indice del dato a remplazar
        """
        len_fifo = len(self.cachebank[2**self.numsets])
        for i in range (0 , 2**self.numsets):
            if len_fifo == i:
                for j in range(0, i):
                    if (Tag == self.cachebank[j].tag):
                        return j
                self.cachebank[2**self.numsets].append(i)
                return i
        
        # Remplazar el primero y meterlo a la cola
        # Sirve para LRU 
        rn = random.randint(0, 2**self.numsets-1)
        n = self.cachebank[2**self.numsets].index(rn)
        n_block = self.cachebank[2**self.numsets].pop(n)
        self.cachebank[2**self.numsets].append(n_block)
        return n_block

    def read_LRU(self, i_block):
        
        # El menos usado recientemente estará al principio de la lista
        index = self.cachebank[2**self.numsets].index(i_block) # Busca el indice donde se encuentra
        # el dato utilizado

        # El dato utilizado se pone al final de la cola, por lo tanto el 
        # valor menos usado se encuentra en el inicio de la lista.
        self.cachebank[2**self.numsets].append(self.cachebank[2**self.numsets].pop(index))

    def replace(self,  Tag):
        """Determina que política se va a utilizar.

        Args:
            n_set (int): conjunto al que pertence el dato a 
            modificar

        Returns:
            int: devuelve al indice del dato a remplazar.
        """
        if(self.rep_pol == 1):
            # FIFO Pol
            n = self.replace_FIFO( Tag)
        elif(self.rep_pol == 2):
            # LRU Pol
            n = self.replace_FIFO( Tag)
        else:
            n = self.replace_Rand( Tag)
        
        return n 





