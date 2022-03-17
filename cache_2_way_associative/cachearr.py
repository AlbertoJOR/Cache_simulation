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
            repla_list=[]  # lista que sirve para elegir el dato a remplazar
            set_line=[]    # contiene cada set, dos líneas de caché y la lista de remplazo
            set_line.append(CL.cacheline(i))
            set_line.append(CL.cacheline(i))
            set_line.append(repla_list)
            self.cachebank.append(set_line)

    def print_cache(self):
        """Imprime los contenidos de la caché en forma de tabla
        """
        print("CACHE BLOCK 1:")
        print ("{:<7} {:<7} {:<7} {:<34} {:<10}".format('index','valid','dirty','tag','data'))
        #print("index", "  ","valid", "   ", "dirty", "   ", "tag", "     ", "data" )
        for i in range(0,2**self.numsets):
            self.cachebank[i][0].print_cache_line()

        print()
        print("CACHE BLOCK 2:")
        print ("{:<7} {:<7} {:<7} {:<34} {:<10}".format('index','valid','dirty','tag','data'))
        #print("index", "  ","valid", "   ", "dirty", "   ", "tag", "     ", "data" )
        for i in range(0,2**self.numsets):
            self.cachebank[i][1].print_cache_line()
        for i in range(0, 2**self.numsets):
            print("Lista de remplazo", i, ":", self.cachebank[i][2])

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

        # Se extraen las dos líneas pertenecientes al set
        ch_line = self.cachebank[ch_set_dec][0]
        ch_line2 = self.cachebank[ch_set_dec][1]


        if((ch_line.valid==0 or(ch_line.tag != tag)) and (ch_line2.valid==0 or(ch_line2.tag != tag))):
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
            n_ind = self.replace(ch_set_dec, tag)
            self.cachebank[ch_set_dec][n_ind].set_atributes(ch_set_dec, 1, tag, data,0)

        else:
            print("LOAD: Cache hit")
            if ch_line.tag == tag:
                print("addr: ", addr, "  data:", ch_line.data)
                i = 0
            else : 
                i = 1
                print("addr: ", addr, "  data:", ch_line2.data)
            if(self.rep_pol == 2 ):
                # Si se unsa LRU se actualiza el dato al más utilizado
                self.read_LRU(ch_set_dec,i)
        print()

    def writeback(self,data, Tag, set_dec, addr_bin):
        """Aplica la escritura con la política de Write Back.

        Args:
            data (str hex): 
            Tag (str bin): 
            set_dec (int):
            addr_bin (str bin):
            i_index (int): indicé de la vía de la caché
        """

        ch_line = self.cachebank[set_dec][0]
        ch_line2= self.cachebank[set_dec][1]

        if(ch_line.tag != Tag and ch_line2.tag != Tag):
            print("Write: Cache miss")
            # Escribir en memoria
            i_index = self.replace(set_dec, Tag)
            if self.cachebank[set_dec][i_index].dirtybit :

                print("Replaced data written  in memory")
                self.main_mem[addr_bin] = self.cachebank[set_dec][i_index].data

            # Cambiar la cache
            self.cachebank[set_dec][i_index].set_atributes(set_dec, 1, Tag, data,0)
            if self.cachebank[set_dec][i_index].dirtybit == 0:
                print("New data written  in memory")
                self.main_mem[addr_bin] = self.cachebank[set_dec][i_index].data
                

        else:
            print("Write: Cache hit")
            if ch_line.tag == Tag:
                #print("TAG 1")
                self.cachebank[set_dec][0].write_data(data)
                if(self.rep_pol == 2):
                    # Actualiza el dato más
                    self.read_LRU(set_dec, 0)
            elif(ch_line2.tag==Tag):
                #print("TAG 2")
                self.cachebank[set_dec][1].write_data(data)
                if(self.rep_pol == 2) :
                    #actualiza el dato más usado 
                    self.read_LRU(set_dec, 1)




    def writethrough(self, data, Tag, set_dec, addr_bin):
        """Aplica la política write through

        Args:
            data (str hex): 
            Tag (str bin): 
            set_dec (int):
            addr_bin (str bin):
            i_index (int): indicé de la vía de la caché
        """
        ind_block = self.replace(set_dec, Tag)
        self.cachebank[set_dec][ind_block].set_atributes(set_dec, 1, Tag, data, 0)

        # Escribir en memoria 
        self.main_mem[addr_bin] = data

    def write( self, addr, data):
        """Método que simula la instrucción de escritura en la caché
        Aplica la poplítica correspondiente.

        Args:
            addr (hex str):
            data (hex str):
        """
        addr_dec = hexToDec(addr)
        addr_bin = decimalToBinary(addr_dec, 32)

        # Escribir en la caché
        Tag = addr_bin[:-(2+ self.numsets)]
        ch_set= addr_bin[-(2+self.numsets):-2]
        set_dec = binaryToDec(ch_set)

        
        if self.wb:
            self.writeback( data, Tag, set_dec, addr_bin)
        else: 
            self.writethrough( data, Tag, set_dec, addr_bin)

        print("Write add:  ", addr, "data:  ", data )

    def replace_FIFO(self, n_set, Tag):
        """Determina la pol FIFO. Va cambiando la lista
        de remplazo. 


        Args:
            n_set (int): indice del set

        Returns:
            int: indice que se tiene que remplazar del bloque
        """
        if self.cachebank[n_set][2] == []:
            # Si la lista está vacia por defecto toma la primer poscición 
            self.cachebank[n_set][2].append(0)
            return 0
        elif(len(self.cachebank[n_set][2])==1):
            # si contiene un solo valor, por defecto se escribe el segundo en
            # segunco bloque. self.cachebank[set_dec][0]
            if (Tag == self.cachebank[n_set][0].tag):
                return 0
            else :
                self.cachebank[n_set][2].append(1)
                return 1

        else:
            # Remplazar el primero y meterlo a la cola
            # Sirve para LRU 
            n_block = self.cachebank[n_set][2].pop(0)
            self.cachebank[n_set][2].append(n_block)
            return n_block
        
    def replace_Rand(self, n_set, Tag):
        """Remplaza aleatoriamente.

        Args:
            n_set (int): indice del dato en el que se encuentra.

        Returns:
            int : indice del dato a remplazar
        """
        if self.cachebank[n_set][2] == []:
            # Si la lista está vacia por defecto toma la primer poscición 
            self.cachebank[n_set][2].append(0)
            return 0
        elif(len(self.cachebank[n_set][2])==1):
            if (Tag == self.cachebank[n_set][0].tag):
                return 0
            else :
                self.cachebank[n_set][2].append(1)
                return 1

        else:
            rn= random.randint(0,1)
            n = self.cachebank[n_set][2].index(rn)
            n_block = self.cachebank[n_set][2].pop(n)
            self.cachebank[n_set][2].append(n_block)
            return n_block

    def read_LRU(self, n_set, i_block):
        
        # El menos usado recientemente estará al principio de la lista
        index = self.cachebank[n_set][2].index(i_block) # Busca el indice donde se encuentra
        # el dato utilizado

        # El dato utilizado se pone al final de la cola, por lo tanto el 
        # valor menos usado se encuentra en el inicio de la lista.
        self.cachebank[n_set][2].append(self.cachebank[n_set][2].pop(index))

    def replace(self, n_set, Tag):
        """Determina que política se va a utilizar.

        Args:
            n_set (int): conjunto al que pertence el dato a 
            modificar

        Returns:
            int: devuelve al indice del dato a remplazar.
        """
        if(self.rep_pol == 1):
            # FIFO Pol
            n = self.replace_FIFO(n_set, Tag)
        elif(self.rep_pol == 2):
            # LRU Pol
            n = self.replace_FIFO(n_set, Tag)
        else:
            n = self.replace_Rand(n_set, Tag)
        
        return n 





