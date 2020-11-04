# LEVEL 13

## Vulnerability

gdb available on the attacked server -> Privilege escalation by register manipulation

## External resources

gdb

## Initial context

In our home directory, we see an executable with suid/guid bit

```
level13@SnowCrash:~$ ls -l
total 8
-rwsr-sr-x 1 flag13 level13 7303 Aug 30  2015 level13
```

So we can run it as effective user flag13

```
level13@SnowCrash:~$ ./level13
UID 2013 started us but we we expect 4242
```

We see that the program is protected unless our user id is 4242.

Let's run gdb to look at the disassembly code:

```
level13@SnowCrash:~$ gdb -q ./level13
Reading symbols from /home/user/level13/level13...(no debugging symbols found)...done.
(gdb) disas main
Dump of assembler code for function main:
   0x0804858c <+0>:	push   %ebp
   0x0804858d <+1>:	mov    %esp,%ebp
   0x0804858f <+3>:	and    $0xfffffff0,%esp
   0x08048592 <+6>:	sub    $0x10,%esp
   0x08048595 <+9>:	call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   (...)
```

We see that right after the uid is retrieved, a check is done. Let's put a breakpoint there and run the program:

```
(gdb) break *main+14
Breakpoint 1 at 0x804859a
(gdb) r
Starting program: /home/user/level13/level13

Breakpoint 1, 0x0804859a in main ()
```

If we display the value in the EAX register, we see that its level12's uid

```
(gdb) print $eax
$1 = 2013

level13@SnowCrash:~$ cat /etc/passwd | grep level13
level13:x:2013:2013::/home/user/level13:/bin/bash
```

We can change the value in the register to 4242 and resume the program:

```
(gdb) set $eax=4242
(gdb) print $eax
$3 = 4242
(gdb) cont
Continuing.
your token is 2A31L79asukciNyi8uppkEuSx
[Inferior 1 (process 22851) exited with code 050]
```
