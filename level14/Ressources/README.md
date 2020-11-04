# LEVEL 14

## Vulnerability & exploit

Weak anti-debugging technique and available gdb => privilege escalation by manipulating registers

## External resources

gdb

## Initial context

There is nothing in our home directory.
Initial search (detailed in previous exercices) yields nothing of interest.

## Solving the challenge

Since we now know how to trick an executable into mistaking the user with a debugger, let's see if we can do the same with `getflag`.

```
level14@SnowCrash:~$ ltrace getflag
__libc_start_main(0x8048946, 1, 0xbffff7f4, 0x8048ed0, 0x8048f40 <unfinished ...>
ptrace(0, 0, 1, 0, 0)                                           = -1
puts("You should not reverse this"You should not reverse this
)                             = 28
+++ exited (status 1) +++
```

We see that the executable is protected by a call to ptrace.

Browsing man and [documentation](http://www.stonedcoder.org/~kd/lib/14-61-1-PB.pdf), we learn that gdb uses ptrace to handle the executable. and that ptrace can only be attached to a process once.  
If a debugger that uses ptrace (e.g. gdb or ltrace) is used on a process that makes a call to ptrace, it will result in an error and ptrace will return -1.

To trick the debugger, we can try to create our own ptrace function and have the linker load it by setting the env variable LD_PRELOAD:

```
[snowcrash@docker] ~/level14/Ressources # cat ptrace.c
#include <stdio.h>

long ptrace(int i, int j, void *addr, void *data)
{
    printf("CUSTOM PTRACE");
}
```

Upload this file to the virtual machine:

```
[snowcrash@docker] ~/level14/Ressources # scp -P 4242 ptrace.c scp://level14@192.168.0.169/../../../tmp/ptrace.c
```

and compile it:

```
level14@SnowCrash:/tmp$ gcc -shared ptrace.c -o ptrace.so
```

level14@SnowCrash:/tmp$ gcc -shared ptrace.c -o ptrace.so
level14@SnowCrash:/tmp$ ls -l ptrace.so
-rwxrwxr-x 1 level14 level14 6754 Nov 3 11:36 ptrace.so

```
level14@SnowCrash:/tmp$ gdb -q
(gdb) set environment LD_PRELOAD=./ptrace.so
(gdb) file /bin/getflag
Reading symbols from /bin/getflag...(no debugging symbols found)...done.
(gdb) break *main
Breakpoint 2 at 0x8048946
(gdb) r
Starting program: /bin/getflag
Injection Linked lib detected exit..
CUSTOM PTRACECUSTOM PTRACEDuring startup program exited with code 1.
```

`getflag` seems to be protected against linked lib injection, so let's examine the registers' content:

```
level14@SnowCrash:/tmp$ gdb -q
(gdb) file /bin/getflag
Reading symbols from /bin/getflag...(no debugging symbols found)...done.
(gdb) disas main
Dump of assembler code for function main:
   0x08048946 <+0>:	push   %ebp
   0x08048947 <+1>:	mov    %esp,%ebp
   0x08048949 <+3>:	push   %ebx
   0x0804894a <+4>:	and    $0xfffffff0,%esp
   0x0804894d <+7>:	sub    $0x120,%esp
   0x08048953 <+13>:	mov    %gs:0x14,%eax
   0x08048959 <+19>:	mov    %eax,0x11c(%esp)
   0x08048960 <+26>:	xor    %eax,%eax
   0x08048962 <+28>:	movl   $0x0,0x10(%esp)
   0x0804896a <+36>:	movl   $0x0,0xc(%esp)
   0x08048972 <+44>:	movl   $0x1,0x8(%esp)
   0x0804897a <+52>:	movl   $0x0,0x4(%esp)
   0x08048982 <+60>:	movl   $0x0,(%esp)
   0x08048989 <+67>:	call   0x8048540 <ptrace@plt>
   0x0804898e <+72>:	test   %eax,%eax
   (...)
```

We see that immediately after the ptrace call, the value in register eax is tested.
We can set a breakpoint on that test, and display the registers content: we see that the value in eax is -1

```
(gdb) break *main+72
(gdb) Breakpoint 1 at 0x804898e
(gdb) r
Starting program: /bin/getflag

Breakpoint 1, 0x0804898e in main ()
(gdb) print $eax
$1 = -1
```

We can therefore change the value in the register to 0, to bypass the error when calling ptrace:

```
(gdb) set $eax=0
(gdb) print $eax
$2 = 0
(gdb) cont
Continuing.
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)
```

We successfully bypassed the call to ptrace!
However, we are still identified as level14 instead of flag14. If we look again at the disassembly code, we see that a check is made during a call to getuid:

```
(gdb) disas main
   (...)
   0x08048acf <+393>:   je     0x8048e46 <main+1280>
   0x08048ad5 <+399>:   mov    0x804b060,%eax
   0x08048ada <+404>:   mov    %eax,%edx
   0x08048adc <+406>:   mov    $0x804906c,%eax
   0x08048ae1 <+411>:   mov    %edx,0xc(%esp)
   0x08048ae5 <+415>:   movl   $0x20,0x8(%esp)
   0x08048aed <+423>:   movl   $0x1,0x4(%esp)
   0x08048af5 <+431>:   mov    %eax,(%esp)
   0x08048af8 <+434>:   call   0x80484c0 <fwrite@plt>
   0x08048afd <+439>:   call   0x80484b0 <getuid@plt>
   0x08048b02 <+444>:   mov    %eax,0x18(%esp)
   0x08048b06 <+448>:   mov    0x18(%esp),%eax
   0x08048b0a <+452>:   cmp    $0xbbe,%eax
   (...)

(gdb) break *main+452
Breakpoint 2 at 0x8048b0a
```

Now we can run the executable again, repeat the first steps to bypass ptrace, and continue:

```
(gdb) cont
Continuing.

Breakpoint 2, 0x08048b0a in main ()
(gdb) print $eax
$4 = 2014
```

The value in the register is consistent with our previous result:

```
level14@SnowCrash:~$ cat /etc/passwd | grep level14
level14:x:2014:2014::/home/user/level14:/bin/bash
```

If we want to pretend to be running the executable as flag14, we should change the value in the register from 2014 to 3014:

```
level14@SnowCrash:~$ cat /etc/passwd | grep flag14
flag14:x:3014:3014::/home/flag/flag14:/bin/bash
```

```
(gdb) set $eax=3014
(gdb) print $eax
$5 = 3014
(gdb) cont
Continuing.
Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

This is in fact a flag token, so we can su to flag14 and run getflag to get the final token.
