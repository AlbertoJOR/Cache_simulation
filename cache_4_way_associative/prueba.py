import cachearr as charr

if __name__ == "__main__":
    cache = charr.cachearr(3)
    cache.load('00000018')
    cache.print_cache()
    cache.load('00000028')
    cache.load('00000004')
    cache.print_cache()
    cache.load('00000018')
    rn = charr.generate32drnd()
    cache.write('00000018',rn)
    cache.print_cache()

    cache.load('00000018')
    rn2 = charr.generate32drnd()
    cache.write('00101018', rn2)

    cache.load('00101018')

    cache.print_cache()

    cache.load('00000018')
    cache.print_cache()
