import sys

filetxt = open("DAB_Picture1.txt", "r")

bufferLine = filetxt.readlines()

length = len(bufferLine)

print(length)

for line in range(0, length):
    print(bufferLine[line])

codestr = bufferLine[0]
print("Line 0: ", codestr)


bufferCol = []
bufferCol.clear()
for col in range(0, 40):
    print("codestr ", col, ": ", codestr[col*3: col*3 + 2])
    code = "0x" + codestr[col*3: col*3 + 2]
    print(code)
    bufferCol.append(int(code, 16))

print("bufferCol ", bufferCol)
