# Shellforge

Shellforge is a simple python script for shellcoders that generates shellcode via a fully editable .asm file, with access to the .o and raw executable as well. It's a perfect tool to quickly generate a quick and dirty execve shellcode as a starting point for your payload. Requires nasm and ld to be installed on the host machine.

# How it works

I wrote shellforge when I was writing shellcode regularly. It's a script to quickly generate shellcode for a simple execve syscall.

You input the absolute path to the executable-- ie, /bin/sh or /usr/bin/screenfetch or something. Output filenames are optional. If not specified, the output filename is the name of the executable in the path.

The string representing the path to the executable is then measured-- if this string doesn't have a number of characters evenly divisible by 4, it pads the begining of the path with "/" to avoid null terminators when pushing the values of this onto the stack.

When the string is the proper length, it is reversed, then encoded in hexadecimal. It's then broken into 4 byte words, and written into the assembly code.

The assembly code is written to an .asm file. Shellforge then calls nasm to compile this .asm file into a .o object file, then uses the linker ld to link it into an executable.

Shellforge has now written 3 files -- foo.asm, foo.o and foo. It then generates a bash script, foo.sh, and executes it. The bash script takes the executable file foo, dumps the contents of it with objdump -D, and some commandline-fu to extract the opcodes and write them to bytes with \x. The output of this bash script outputs all of the bytes, the raw shellcode, into foo.bin, the final file.

# What's coming next?

More options. Options for cleanup, to delete these files when they're done, or to write them all to a diretory so as to not clutter your working dircetory. There will also be new options to customize the assembler and linkers (so if you don't want to use nasm or ld, you can specify other options). 
