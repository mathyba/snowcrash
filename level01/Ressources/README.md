# LEVEL 01

## Vulnerability & exploit

Weak hashed password stored in world-readable file -> Crack password with brute-force

## External resources and commands

john the ripper

## Initial Context

Once again, our home directory is empty.
Given the lack of information, we can check /etc/passwd, as it can provide useful information on groups and users.

## Solving the challenge

In this case, we see that it contains a hashed password for flag01.

```
level01@SnowCrash:~$ grep 'flag01' /etc/passwd flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

According to [this discussion](https://security.stackexchange.com/questions/92766/what-can-hackers-do-with-ability-to-read-etc-passwd), most systems did this in the past, before using the more secure /etc/shadow.

Back then, it took some work to crack hashed passwords. Nowadays, there are tools to try millions of combinations, so let's try with the john software.
First, download the /etc/passwd on your local machine:

```
$:/snowcrash# scp -P 4242 scp://level01@<VM_IP_ADDR>/../../../etc/passwd level01/Ressources/passwd
```

Then, run john on that file:

```
$:/snowcrash# john level01/Ressources/passwd
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 128/128 SSE2-16])
Press 'q' or Ctrl-C to abort, almost any other key for status
abcdefg          (flag01)
1g 0:00:00:00 100% 2/3 33.33g/s 46433p/s 46433c/s 46433C/s raquel..bigman
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

So we can log in as flag01 with password "abcdefg" and run getflag to get the token for level01.
