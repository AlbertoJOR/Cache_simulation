import cachearr as charr

if __name__ == "__main__":
    # El objetivo de este código es visualizar los misses y 
    # hit al usar la política de Write back, con especial énfasis
    # en la dirección "00000018"
    cache = charr.cachearr(3,True)
    cache.load('00000018')
    cache.print_cache()
    cache.load('00000028')
    cache.load('00000004')
    cache.print_cache()
    cache.load('00000018')
    cache.write('00000018',charr.generate32drnd())
    cache.print_cache()

    cache.load('00000018')
    rn2 = charr.generate32drnd()
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

    cache.write('00a00004',charr.generate32drnd())
    cache.write('00a00028',charr.generate32drnd())
    cache.print_cache()