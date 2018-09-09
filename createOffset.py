from __future__ import print_function

outf = open('titleoff.txt','w')

offset = 0

with open('title.txt','r') as f:
    for line in f:
        fileNumber = line.split()[0]
        s = fileNumber + ' ' + str(offset)
        offset += len(line)
        # outf.write(s)
        print(s,file=outf)

outf.close()
