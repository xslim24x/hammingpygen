from optparse import OptionParser
import math

parser = OptionParser()
parser.add_option("-l", "--length", dest="codelen", default="6 ",
                  help="custom length of code")
parser.add_option("-o", "--output", dest="outputfile", metavar="FILE",
                  help="Output codes to file")

#TODO: Add parity bit function

parser.add_option("-p", "--parity", dest="parity" ,
                  action="store_true", default=False,
                  help="checkbits include general parity check")

parser.add_option("-e", "--e", dest="encoded" ,
                  action="store_true", default=True,
                  help="display values in encoded form rather than standard form")

(options, args) = parser.parse_args()

# code len
n = int(options.codelen)

if options.parity:
    n -= 1

# check bits m
m = int(math.floor(math.log(n,2)))+1

# data bits
k = n - m
dmax = (2**m)-m-1
# parity


print "Hamming Code [%d,%d]" % (n+1 if options.parity else n,k)
print "\t total length [n] = %d" % n,
print "+1" if options.parity else ""
print "\t data bits [k] = %d" % k
print "\t check bits [m] = %d" % m,
print "+1" if options.parity else ""
print "\t total codes = %d" % 2**k

s1 = []
s2 = []
encodedform = []
temp = []
if options.encoded:
    print "\nEncoded form:"
for p in xrange(0,m):
    row = ""
    zeros = 2**(p)-1
    for pad in range(0,zeros):
        row += "0"
    for i in range(1,n+1-zeros):
        if ((i-1)/2**(p))%2==0:
            row += "1"
        else:
            row += "0"
    encodedform.append(row)
    temp.append(list(row))
    if options.encoded:
        print row


standardform = []
if not options.encoded:
    print "\nStandard form"
    print "D".center(k-1,' '),
    print "|",
    print "P".center(m-1,' ')

for r in range(0,m):
    tempdata = ""
    temppar = ""
    for c in range(0,n):
        if (math.log(c+1,2)%1!=0):
            tempdata += encodedform[r][c]
        else:
            temppar += encodedform[r][c]
    if not options.encoded:
        print tempdata + " " + temppar
    standardform.append(tempdata+temppar)

g = []
temp = 0
ident = "1"
ident += "0" * (k-1)

print "\nG matrix:"
for r in range(0,n):
    if ((math.log(r+1,2)%1!=0) and options.encoded) or (not options.encoded) and r < k:
        g.append(ident)
        print ident
        ident = str(bin(int(ident,base=2)>>1))[2:].zfill(k)
    else:
        print standardform[temp][0:k]
        g.append(standardform[temp][0:k])
        temp += 1

print "\nCode Words:"

for c in range(0,2**k):
    codeword = ""
    for b in g:
        weight = str.count(str(bin(int(b,base=2) & c)[2:]),"1")
        codeword += str(weight%2)
    if not options.encoded:
        codeword = codeword[:k] + " " + codeword[k:]
    print codeword + "\t",
    print str.count(codeword,"1")
