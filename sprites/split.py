from PIL import Image
import numpy
gambar = numpy.array(Image.open("sprites/belt605x60.png"))
for i in range(0, 60*4, 60):
    Image.fromarray(gambar[i:i+59, :]).resize((1210, 120)
                                              ).save("sprites/conv"+str(180-i)+".png")
