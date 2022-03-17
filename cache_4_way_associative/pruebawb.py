import cachearr as charr

if __name__ == "__main__":
    cache = charr.cachearr(3,True,0)
    # El objetivo de este código es visualizar los misses y hits
    # usando distintas politicas de escritura y de remplazo
    # Primer parámetro indica el núimero de sets en potencia de 2
    # 
    # Segundo paramatro al inicializar el objecto cachecarr:
    #   - False     write Through
    #   - True      write back
    # Tercer parámetro pólitica de remplazo:
    #   - 0         aleatorio
    #   - 1         FIFO
    #   - 2         LRU
    
    cache.load('00000018')
    cache.print_cache()
    cache.load('00000028')
    cache.load('00000004')
    cache.print_cache()
    cache.load('00000018')
    cache.write('00000018',charr.generate32drnd())
    cache.print_cache()

    cache.load('00000018')
    cache.write('00101018', charr.generate32drnd())

    cache.load('00101018')

    cache.print_cache()

    cache.load('00000018')
    cache.print_cache()

    cache.write('00000004',charr.generate32drnd())
    cache.write('00000028',charr.generate32drnd())
    cache.print_cache()

    cache.write('00000004',charr.generate32drnd())
    cache.write('00000028',charr.generate32drnd())
    cache.print_cache()

    # Prueba de LOAD, Tiene como objetivo mostrar el funcionamiento
    # de los remplazos en la dirección "00000004" correspondiente a
    # el primer set.
    print("Prueba Load:")

    cache.write('00a00004',charr.generate32drnd())
    cache.load('00a00004')
    cache.print_cache()

    cache.load('00a00004')
    cache.print_cache()
    cache.write('00a00104',charr.generate32drnd())
    cache.print_cache()

    cache.load('00a00004')
    cache.print_cache()
    cache.write('00a10004',charr.generate32drnd())
    cache.print_cache()

    cache.load('00a00004')
    cache.print_cache()
    cache.write('10a11004',charr.generate32drnd())
    cache.print_cache()

    cache.load('00a00004')
    cache.print_cache()
    cache.write('01a00004',charr.generate32drnd())
    cache.print_cache()

    cache.load('00a00004')
    cache.print_cache()
    cache.write('10a10004',charr.generate32drnd())
    cache.print_cache()

    # Prueba de Escritura, Tiene como objetivo mostrar el funcionamiento
    # de los remplazos en la dirección "00000004", correspondiente al 
    # primer set.
    print("Prueba Write:")

    cache.load('10a10004')
    cache.print_cache()
    cache.write('00a00004',charr.generate32drnd())
    cache.print_cache()

    cache.load('01a00004')
    cache.print_cache()
    cache.write('00a00004',charr.generate32drnd())
    cache.print_cache()

    cache.load('10a11004')
    cache.print_cache()
    cache.write('00a00004',charr.generate32drnd())
    cache.print_cache()

    cache.load('00a10004')
    cache.print_cache()
    cache.write('00a00004',charr.generate32drnd())
    cache.print_cache()

    cache.load('00a00104')
    cache.print_cache()
    cache.write('00a00004',charr.generate32drnd())
    cache.print_cache()

