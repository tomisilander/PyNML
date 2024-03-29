def get_ctb(ctblines):
    
    try:
        ctb = [list(map(int, l.split())) for l in ctblines if l.strip()]
    except:
        raise Exception("Could not interpret all entries as integers!")

    if len(ctb) < 2:
        raise Exception("At least two rows required!")
    else:
        clen = len(ctb[0])
        if clen < 2:
            raise Exception("At least two columns required!")
        for col in ctb:
            if len(col) != clen:
                msg = "All the colums should have equal amount of entries!"
                raise Exception(msg)

    return ctb
