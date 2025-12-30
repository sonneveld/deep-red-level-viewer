from glob import glob
import struct
for fname in glob("game/mapas/*.pc1"):

    print()
    print(fname)
    with open(fname, 'rb') as f:
        header = f.read(0xa)

        # width, height, height, number of remaining bytes
        header = struct.unpack("<HHHI", header)
        
        print('header:', header)

        entries = []

        while True:
            offset = f.tell()
            entry = f.read(8)
            if not entry:
                break

            entry = struct.unpack("<II", entry)
            # print(f"{offset:8x}: {entry[0]:8x} {entry[1]:8x}")

            entries.append(entry)

    # dumping the columns
    for idx in range(header[0]):
        sub_ent = entries[idx*header[2]:(idx+1)*header[2] ]
        if not sub_ent:
            break
        print( f'{idx:02x}: ', ' '.join( [f"{x[0]:03x}" for x in sub_ent]))

