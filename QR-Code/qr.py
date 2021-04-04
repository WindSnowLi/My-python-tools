import zxing
import sys
reader = zxing.BarCodeReader()
barcode = reader.decode(sys.argv[1])
print(barcode.parsed)
