
# CS7NS1/CS4400 Practical 3

The deadline for this assignment is: 20181001. 
Submissions will be allowed from Sep 25th.

**Late submissions are not allowed.**

**Don't forget to stop your instance when you're done!**

For this practical, you will be emailed a list of 1000 password hashes
and are to solve those, finding the passwords for as many as you can.  Every
hash and password are unique - each of the (176,000!) passwords I generated
is given to just one student.

As you solve passwords you can upload your results to submitty, in the  [crack
some
hashes](https://cs7ns1.scss.tcd.ie/index.php?semester=f18&course=cs7ns1&component=student&gradeable_id=as3)
gradable.

You must upload your entire set of solved hashes each time, as your marks will
reflect only your most recent submission.  (That is, the system does not
remember earlier submissions, it calculates your marks afresh each time.) After
100 uploads, points will be deducted for having sent too many submissions. 

You can choose whatever technology you want to solve the problem, but this
assignment is scaled so that a naive solution solving a reasonable number of
hashes would consume a fairly small number of hours running an EC2
instance.  Note that a GPU is not required for this assignment, if you choose
to use one, then you will consume budget that you might want later (but it's up
to you!).

You are deliberately not being given much detail of the password hash format or
recommendations as to how to solve the problem. Figuring out how to solve a
problem like this is part of the practical. (But is not hard.)

Where possible, I would recommend not using EC2 instances for development, but
rather try to break a subset of the hashes locally and when that works you can
(if you choose) run your job on an EC2 instance. 

## Reporting

At the end of the module, you will be required to submit a description
of your work on hash cracking. Keep notes of what you've done for this
assignment to make that easier and so you don't forget what you did.

If you write any code or scripts for this practical, keep those,
e.g., make a git repo for them. 

## Broken hashes format

The following specifies the format of file you should upload:

- The file you upioad to submitty MUST use a ".broken" extension.
- The file contains one line per broken hash. 
- Each line contains the hash value, one space character, the
password and then the end of line character.
- There are no headers or footers.
- Passwords can contain spaces.
- The order of lines in the file is not significant, you can re-order them
as needed.

After upload you won't of course be shown the passwords you
didn't get, so if you have format isues with the file you
upload, that could be somewhat hard to debug.

Only hashes that were sent to you will count towards marks - you get nothing
for submitting someone else's solved hashes, ones you just make up, or
duplicates:-)

## Examples

- [as3-sample.hashes](as3-sample.hashes) contains 20 hashes
- [as3-sample.broken](as2-sample.broken) shows the correct upload file 
  if solving those hashes.

The content of the sample files mentioned above is:

The 20 hashes there are:

			$1$Ywp7jlLj$gYwRx59k2jmKymeN5449i.
			$1$fFttyOvL$.ps0Ums8.ZhyzvdP.Ijb51
			$1$ENjP8uqT$RrB.ZDkMZTMSte2wIvMpX1
			$1$k7Yty829$w2KKHlkdbzlj9TJfemwBv.
			$1$kEiBStaL$zLhcBZck9FYa1a/LtBuNw1
			$1$KHgx.ZYU$5TWEkLNo1tD.cvyShtlnV.
			$1$kNLnctJM$WpQvlbO27gNCaHy1bgD7T0
			$1$Vl84e/wU$YPbBlrdn4gM9gzrfiiUBa/
			$1$CaKUjwFW$lOi.XbAkXPI/9bTbGBw43.
			$1$.er44fIX$SRfC4R8gvLPtovNxD4Yfp/
			$1$dYmOWQFL$xmiaqTJobMYdb/K9QaIv11
			$1$kgn3NW1e$G9j6bFsunPXw1c4eP/gPH.
			$1$pUaVYwAu$UMUUqXORQfMOf4n6ag1wR.
			$1$KSksta19$UuNE0xkDvfMMJQwNJ4WEh.
			$1$zAe8c2g9$.WN9l27xuL58hc6l1P1aj0
			$1$SA/CkBcj$VR0Eguokk6L3GCfApf/4O.
			$1$/gqKLQBx$roSzbsDEGwqeOzQNXZS.Q/
			$1$ciWKeOez$Cs6xS13gvJQW1bE/W3w5A1
			$1$drQU5IUB$oCvHr1iDHzLIXtDNwU9D40
			$1$oPql4Hju$PXpP5g/he/XE4O0x8MLPB1

The corresponding ``.broken`` file is:

			$1$Ywp7jlLj$gYwRx59k2jmKymeN5449i. FahdActs
			$1$fFttyOvL$.ps0Ums8.ZhyzvdP.Ijb51 FedsActs
			$1$ENjP8uqT$RrB.ZDkMZTMSte2wIvMpX1 FidoActs
			$1$k7Yty829$w2KKHlkdbzlj9TJfemwBv. FiskActs
			$1$kEiBStaL$zLhcBZck9FYa1a/LtBuNw1 Fr'sActs
			$1$KHgx.ZYU$5TWEkLNo1tD.cvyShtlnV. FreyActs
			$1$kNLnctJM$WpQvlbO27gNCaHy1bgD7T0 GE'sActs
			$1$Vl84e/wU$YPbBlrdn4gM9gzrfiiUBa/ GageActs
			$1$CaKUjwFW$lOi.XbAkXPI/9bTbGBw43. GaleActs
			$1$.er44fIX$SRfC4R8gvLPtovNxD4Yfp/ GaulActs
			$1$dYmOWQFL$xmiaqTJobMYdb/K9QaIv11 Ge'sActs
			$1$kgn3NW1e$G9j6bFsunPXw1c4eP/gPH. GereActs
			$1$pUaVYwAu$UMUUqXORQfMOf4n6ag1wR. GillActs
			$1$KSksta19$UuNE0xkDvfMMJQwNJ4WEh. GishActs
			$1$zAe8c2g9$.WN9l27xuL58hc6l1P1aj0 GobiActs
			$1$SA/CkBcj$VR0Eguokk6L3GCfApf/4O. GoreActs
			$1$/gqKLQBx$roSzbsDEGwqeOzQNXZS.Q/ GrayActs
			$1$ciWKeOez$Cs6xS13gvJQW1bE/W3w5A1 GrisActs
			$1$drQU5IUB$oCvHr1iDHzLIXtDNwU9D40 GwenActs
			$1$oPql4Hju$PXpP5g/he/XE4O0x8MLPB1 HaasActs

## Hints and non-hints

- The password values in the sample above are *not* a hint
for this practical. 
- There is a shortcut way to solve this practical so that
you can recover all 1000 hashes in about one minute. If
you find that, please don't tell other students. (I'm
really not sure if students will or won't find this, but
marking will be adjusted depending on how many do and
it'll be obvious from the submissions:-)

## Scoring and Marking

You get 1 point for each correct hash/password pair in the uploaded 
file that matches the specific set of hashes you were given. (Duplicates 
are not counted).

As mentioned in class, points here are not directly mapped to
marks for the module. We'll see how everyone does before deciding
how to weight points.

## Summary

So in summary:

- You'll get an email with your password hashes
- You need to solve as many of those as you can
- The format for the file to upload is described above and
  here's an [example](as3-sample.broken).

Usually with so many students doing an assignments, some tweaks
to these instructions will be needed, so check back here often
to see if there have been any updates.


## Stop your image

**Don't forget to stop your instance when you're done!**

If you do forget to stop the image, your AWS EC2 credits will all be used
up and you'll be sad.

## Support

RosettaHub *do not* offer support to students, so do not mail them, except
as part of the registration flow.

For questions about this assignment, mail Christian.

