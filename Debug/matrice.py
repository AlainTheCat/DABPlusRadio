import sys

file = open('DAB_Shield.jpg', "rb")
matrice = list(file.read())
print(matrice)
file.close()

length = len(matrice)
print(length)

nbrow = length / 16

print(nbrow)

nbrow2 = int(nbrow)

modulo = length - nbrow2 * 16

print(nbrow2)

file2 = open("dab6.csv", "w")
for row in range(0, nbrow2):
    for col in range(0, 15):
        file2.write('{:02X}'.format(matrice[row * 16 + col]) + ", ")
    file2.write('{:02X}'.format(matrice[row * 16 + 15]))
    file2.write(";\n")
row = nbrow2
for col in range(0, modulo - 2):
    file2.write('{:02X}'.format(matrice[row * 16 + col]) + ", ")
file2.write('{:02X}'.format(matrice[row * 16 + modulo - 1]))
file2.write(";\n")

file2.close()


