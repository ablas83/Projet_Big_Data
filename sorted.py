import sys

malist = []

for line in sys.stdin:
    malist.append(line.strip())

malist.sort()

for line in malist:
    print(line)
