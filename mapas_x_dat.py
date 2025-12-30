import codecs
from glob import glob

import codec_cp220

codec_cp220.load()


'''
In English:

Maps
..
Shot=
Cannon=
Speed =
'''

for x in glob("game/mapas/*.dat"):
    print()
    print(x)
    with open(x, 'rb') as f:
        data = f.read()
    data = data.splitlines()
    for line in data:
        line = codecs.decode(line, encoding='cp220')
        print(line)
