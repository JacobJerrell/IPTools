## IPy Notify

Published: 2017-10-26 15:20
Author: Jacob Jerrell

Credits:
Most recent update published on 2002-11-19 17:28:45
By Author: Charles Nichols

Use: To notify whomever that your IP address has changed if you have a non-static IP address and run a web server, game server, etc. Utilizes nested functions.

Currently supports Windoze, Linux, and OS X
Functions with a no-auth mailserver running on localhost.
Planning on expanding functionality to external mailservers but it doesn't fit my use case at this time
Additionally, the script (and it appears the original script had this flaw as well) only gets the private IP
So... doesn't really do much good for what it appears it was coded for to begin with.

If you need the functionality that the original description implies, you need to use a DDNS service

Note: I wrote this mostly as an experiment. While I do have a use case in mind, I also have control over my router and have static IPs set. My thoughts were to have this running on my media-server (PC), and when it gets a new IP, it sends the email, and my Raspberry Pi would be listening to that address. When the raspi gets a notification of a new IP for the media server, I would have a sister (child?) script that updates all of the paths. Again, this is all unnecessary and was just a fun experiment to see if I could convert the script to Python 3, support multiple platforms, and make a few other changes (Like using email.message).

If you like it, please feel free to test, comment, improve, etc.
