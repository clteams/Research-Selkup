#!/usr/bin/python3

dict1 = open('Dictionary1Output.txt', encoding='utf-8').read().splitlines()

with open('Dictionary1Format.txt', 'a', encoding='utf-8') as d1f:
    for line in dict1:
        if len(line) == 1:
            d1f.write(line.upper() + ', ' + line + '\n')
        else:
            d1f.write(line + '\n')
    d1f.close()
