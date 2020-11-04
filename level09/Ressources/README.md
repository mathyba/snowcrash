# LEVEL 09

## Vulnerability

Breakable encryption algorithm => reverse engineering

## Initial context

In our home directory, we see an executable with suid/guid and a token file that we can read but which content seems encrypted:

```
level09@SnowCrash:~$ ls -l
total 12
-rwsr-sr-x 1 flag09 level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09 level09   26 Mar  5  2016 token
level09@SnowCrash:~$ cat token
f4kmm6p|=�p�n��DB�Du{��
```

## Solving the challenge

We know the file expects an argument:

```
level09@SnowCrash:~$ ./level09
You need to provide only one arg.
```

But we won't be able to use ltrace to find out more, since the executable is protected.

```
level09@SnowCrash:~$ ./level09 token
tpmhr
level09@SnowCrash:~$ ltrace ./level09
__libc_start_main(0x80487ce, 1, 0xbffff7f4, 0x8048aa0, 0x8048b10 <unfinished ...>
ptrace(0, 0, 1, 0, 0xb7e2fe38)                                  = -1
puts("You should not reverse this"You should not reverse this
)                             = 28
+++ exited (status 1) ++
```

Let's figure out what the executable does.

```
level09@SnowCrash:~$ ./level09 token
tpmhr
level09@SnowCrash:~$ ./level09 hello
hfnos
level09@SnowCrash:~$ ./level09 aaaaaaa
abcdefg
```

By trying different things, we deduce that the executable expects a string as an argument, and encodes it by rotating each character by an incrementing index.
If this file was used to encrypt the password in the token file, perhaps we can provide our own program to reverse it.
This requires to overcome the fact that some of the encrypted token's bytes are non-decodable, as seen [here](https://vstinner.github.io/pep-383.html)

```
[snowcrash@docker] ~/level09/Ressources # cat decrypt.py
import sys

arg = sys.argv[1].encode(errors="surrogateescape")

print(''.join([chr(l - i) for i, l in enumerate(arg)]))

[snowcrash@docker] ~/level09/Ressources # scp -P 4242 scp://level09@192.168.0.169/token ./vmtoken
token                                                                                                                                                                           100%   26    60.0KB/s   00:00
```

And if we attempt to decrypt the token found on the virtual machine:

```
[snowcrash@docker] ~/level09/Ressources # python3 decrypt.py `cat vmtoken`
XXXXXXXXXXXXXXXXXXXXXXX
```
