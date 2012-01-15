from construct import Buffered

# http://construct.wikispaces.com/bitfields
# used for IVs since they span two bytes
def Swapped(subcon):
    """swaps the bytes of the stream, prior to parsing"""
    return Buffered(subcon,
        encoder = lambda buf: buf[::-1],
        decoder = lambda buf: buf[::-1],
        resizer = lambda length: length
    )