import string
import random
angka = list(range(1000, 9999))
random.shuffle(angka)
angka = angka[:100]
daerah = 'ABCD'
for i in angka:
    with open("data/plat1.csv", "a") as f:
        f.write("BG {0:04d} {1}{2}\n".format(i, random.choice(
            daerah), random.choice(string.ascii_uppercase)))
