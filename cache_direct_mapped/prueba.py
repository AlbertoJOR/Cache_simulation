import cachearr as charr

if __name__ == "__main__":
    # Prueba que demuestra el funcionamiento de una caché
    # de mapeo directo con la política de write through
    cache = charr.cachearr(3)
    cache.load('00000018')
    cache.print_cache()
    cache.load('00000028')
    cache.load('00000004')
    cache.print_cache()
    cache.load('00000018')

    # La intención de este código es visualizar los hit y misses en 
    # el set perteneciente a la dirección "00000018"    
    cache.write('00000018',charr.generate32drnd())
    cache.print_cache()

    cache.load('00000018')
    cache.write('00101018', charr.generate32drnd())

    cache.load('00101018')

    cache.print_cache()

    cache.load('00000018')
    cache.print_cache()
