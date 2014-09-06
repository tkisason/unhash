UNHash toolset  
Tools for better password analysis  

Tonimir Kisasondi (c) 2012 -  

Unhash toolset contains the following tools:
default\_passwords
------------------
A simple tool to help with fetching common lists from various online repositories and merging them ordered by occurance and weight of each pair. Contains a user-passwords list user\_pass\_services\_122013.txt (separated with space) that contains almost all common default preset passwords for network devices and services. Useful for checking if there are no factory passwords present on most services and devices.

botpass
---------
Botpass scrapes sshpot.com which collects data from ssh honeypots. This creates lists of user/pass pairs and ips that were used by attackes. The lists use a single space as a separator, so they can be used in Metasploit out-of-the box.

gwordlist
---------
Use google searches to create custom wordlists based on keywords you enter. Very useful for creating password lists based by scraping top n pages returned by google for each keyword and enhancing your chances of successful guessing.

unhash
------
A rule based password cracker that plays nice with john and hashcat. Check examples file for detailed examples and capabilities of this tool.

unhash-sieve
------------
A classifer and machine learning algorithm for creation of rules to be used with unhash and identify how passwords are created (to be disclosed).
