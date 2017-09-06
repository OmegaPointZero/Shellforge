# Shellforge

Shellforge is a simple python script for shellcoders that generates shellcode via a fully editable .asm file, with access to the .o and raw executable as well. It's a perfect tool to quickly generate a quick and dirty execve shellcode as a starting point for your payload. Requires nasm and ld to be installed on the host machine. Written and tested on Ubuntu, Mint and Kali Linux.

# How to use it

I started writing shellforge when I was writing shellcode regularly. It's a script to quickly generate shellcode for a simple execve syscall.

Currently, it requires you to input the regular command-line option you want to encode (ie, "ls -la"), as well as the absolute path to the executable itself (/bin/ls).

The assembly code is written to an .asm file. Shellforge then calls nasm to compile this .asm file into a .o object file, then uses the linker ld to link it into an executable.

Shellforge has now written 3 files -- foo.asm, foo.o and foo. It then generates a bash script, foo.sh, and executes it. The bash script takes the executable file foo, dumps the contents of it with objdump -D, and some commandline-fu to extract the opcodes and write them to bytes with \x. The output of this bash script outputs all of the bytes, the raw shellcode, into foo.bin, the final file.

# What came in the most recent changes?

Shellforge added options to add all the arguments you want, of whatever length you need. Currently, due to the limited number of registers, it doesn't support more than four arguments in addition to the command itself. It also puts everything in a folder named "shellforge_NAME", where you specify the NAME.

# What's coming next?

>New Options to specify custom compilers and linkers. 
>A way to implement an way to add any number of arguments onto the stack. I'll need to write more assembly here to figure out exactly how to implement this.
