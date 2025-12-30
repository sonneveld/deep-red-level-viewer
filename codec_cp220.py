import codecs
import encodings

def load():

    codecs.lookup("cp437")
    cp437 = encodings.cp437

    # Page A-19: https://www.minuszerodegrees.net/manuals/Olivetti/Olivetti%20-%20MS-DOS%203.30%20-%20Software%20Installation%20Guide.pdf
    # https://en.wikibooks.org/wiki/Character_Encodings/Code_Tables/MS-DOS/Code_page_220

    decoding_table = list(cp437.decoding_table)

    decoding_table[0x86] = 'À'
    decoding_table[0x8F] = 'È'

    decoding_table[0x91] = 'Í'
    decoding_table[0x92] = 'Ó'
    decoding_table[0x98] = 'Á'
    decoding_table[0x9B] = 'Ò'
    decoding_table[0x9D] = 'Ú'
    decoding_table[0x9F] = 'Ï'

    decoding_table[0xA9] = 'ŀ'
    decoding_table[0xAA] = 'Ŀ'

    decoding_table=''.join(decoding_table)


    class Codec(codecs.Codec):
        def encode(self, input_, errors='strict'):
            return codecs.charmap_encode(input_, errors, encoding_table)

        def decode(self, input_, errors='strict'):
            return codecs.charmap_decode(input_, errors, decoding_table)

    def lookup(name):
        if name != 'cp220':
            return None
        return codecs.CodecInfo(
            name='test',
            encode=Codec().encode,
            decode=Codec().decode,
        )


    encoding_table=codecs.charmap_build(decoding_table)
    codecs.register(lookup)
