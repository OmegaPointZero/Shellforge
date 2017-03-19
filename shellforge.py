import sys
import os

def help():
	print """
	Welcome to shellforge.py -- Version 0.85 -- an execve shellcoder written
	in python without using C. Here's how to use it:

 	$ python shellforge.py /path/to/executable outputfilename

	The first argument is the absolute path that you want to pack into the 
	execve shellcode. The output filename is optional; if you ignore it 
	ShellForge will opt to use the name of the executable in the path.

	The output is a total of 5 files. $ shellforge /bin/foo bar will write
	a shellcode in assembly to pass /bin/foo to execve, and save it as 
	bar.asm. It then compiles it with nasm to make bar.o, which is then 
	linked with ld to make the executable bar. Shellforge then quickly writes
	the bash script bar.sh and runs it, which opens bar in objectdump,
	extracts the bytes for the shellcode, and writes them to bar.bin.

	Press CTRL^C to quit, or write the path to an executable to encode\n
	"""
	instring = raw_input("> ")
	filename = instring.split('/')[-1]
	assemble(instring, filename)

def read_input():
	filename = ""
	instring = "" 
	if len(sys.argv) == 3:
		instring = sys.argv[1]
		filename = sys.argv[2]
		assemble(instring, filename)
	elif len(sys.argv) == 2:
		instring = sys.argv[1]
		filename = str(sys.argv[1]).split('/')[-1]
		assemble(instring, filename)
	elif len(sys.argv) == 1:
		help()

def get_shellcode(filename):
	shellcode = open("%ssh" % filename, "w")
	shellcode.write("for i in `objdump -d %s | tr '\\t' ' ' | tr ' ' '\\n' | egrep '^[0-9a-f]{2}$' ` ; do echo -n \"\\x$i\" ; done" % filename)
	shellcode.close()
	os.system("mv %ssh %s.sh && chmod +x %s.sh" % (filename, filename, filename))
	os.system("./%s.sh > %s.bin" % (filename,filename) )

def write_file(filename, shellcode):
	file = open("%s.asm" % filename, "w")
	file.write(shellcode)
	file.close()
	open(filename, "w")
	os.system("nasm -f elf -o %s.o %s.asm" % ((filename,filename)))
	os.system("ld -m elf_i386 -o %s %s.o"% (filename, filename))
	get_shellcode(filename)	

def assemble(instring, filename):
	shellcode = ""
	shellcode = "".join((shellcode, "global _start\nsection .text\n\n_start:\n\txor\t\teax,eax\n\tpush\t\teax\n"))
	while (len(instring) % 4 != 0):
		instring = "/" + instring
	instring = instring[::-1].encode('hex')
	while instring:
		shellcode = "".join((shellcode, "\tpush\t\t0x%s ; %s\n" % (instring[:8], instring[:8].decode('hex') ) ))
		instring = instring[8:]
	shellcode = "".join((shellcode, "\tmov\t\tebx, esp\n\tpush\t\teax\n\tmov\t\tedx, esp\n\tpush\t\tebx\n\tmov\t\tecx, esp\n\tmov\t\tal, 0x0b; execve syscall number\n\tint\t\t0x80"))	
	write_file(filename, shellcode)

read_input()
