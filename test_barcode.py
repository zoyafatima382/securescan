import barcode
from barcode.writer import ImageWriter

data = "123456789"
code128 = barcode.get('code128', data, writer=ImageWriter())
saved_file = code128.save('test_barcode')
print(f"Barcode saved to: {saved_file}")