import cachearr as charr

if __name__ == "__main__":
    cache = charr.cachearr(3,True,2)
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

    cache.write('00000004',charr.generate32drnd())
    cache.write('00000028',charr.generate32drnd())
    cache.print_cache()

    cache.write('00000004',charr.generate32drnd())
    cache.write('00000028',charr.generate32drnd())
    cache.print_cache()

    # Load
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

# WRITE

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

