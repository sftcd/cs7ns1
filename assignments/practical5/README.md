
# Team Practical assignment 5 - not Dante's, but CS7NS1's, Inferno...

The deadline for this is Monday November 19th.

Submissions will be open from Monday October 29th. You'll get mails before then
with team assignments and (later) your InfernoBall. The process for assigning
students to teams and the teams themselves are desribed 
[here](TeamSelection.md).

[Intro-slides](./inferno.pdf)

**DRAFT**
**Until the submission open date (Oct 29th) consider this a work-in-progress and liable to change**
**DRAFT**

**Late submissions are ickky.**

**Don't forget to stop your instances when you're done!**

<img align="right" src="Manetti_Everything_Reduced_to_One_Plan_1506_Cornell_CUL_PJM_1004_01.jpg" width="50%" />

(Image credit: [wikipedia](https://upload.wikimedia.org/wikipedia/commons/1/10/Manetti_Everything_Reduced_to_One_Plan_1506_Cornell_CUL_PJM_1004_01.jpg))

This practical is intended as a digital analog to the rings of Dante's 
Inferno - you have to pass through each of the outer rings to get to the
centre, after which, you, like Dante, will be free to ascend to a higher plane
than this module:-)

This is a team assignment. As previously explained initial teams of 4
will be randomly selected from the set of students who have submitted
some file to submitty, that scored >0. (Submitting an empty file is
not sufficicent, if a badly formatted file was submitted that scored
zero but that contains broken passwords, that'll be allowed.)
Students who are not assigned to one of the initial teams will need
to contact me (Stephen Farrell) to explain why they've not submitted
anything and to be assigned a team.

For this practical, you will be emailed a file containing an "InfernoBall"
which is a nested data structure, in this case with 10 layers, that you need to
solve. (So not a tarball, but a bit like one.) Each layer contains:

- a set of password hashes
- a set of Shamir-like shares
- an encrypted version of the layer(s) below.

By solving the hashes you can get enough passwords to recover the secret key to
decrypt the next layer down.  And then you do that again 'till you reach the
lowest layer.

To get marks you need to submit a file with the recovered secrets succesfully
used for decryption. You'll get marks for each correct secret found. There are
some bonus marks for the first team to solve each layer.
(**Details of bonuses are still being figured out.**)

As always, you can choose whatever technology you want to solve the problem. At
this point we assume each team will be able to figure out what's best to try.

A bit of background on secret-sharing may be needed before we explain this
more...

## Shamir-Sharing 

The general idea of k-of-n secret sharing is that we have n people who each get
a "share" in a secret, so that whenever k (or more) people combine their
shares, they can recover the secret, regardless of which subset of k people
combine shares.

The most common way to do that is called [Shamir secret
sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) and is based
on the simple idea that if we have a polynomial ``f()`` of degree k-1, k points
are all that is needed to reconstruct the formula for the polynomial.  Yet,
with k-1 points (or fewer), we cannot recover the formula for the polynomial.
To generate n shares, we simply take n (n>=k) points on the polynominal,
typically ``f(1),f(2),...,f(n)``, and distribute those. Once k people with
shares come together, they can re-construct the formula for the polynomial,
which is the secret.  We normally, (and equivalently), nominate ``f(0)``, as
the shared secret.  

To make this sufficiently secure, we don't use polynomials over the Real
numbers, but rather over a finite field, which results in less apparent
structure even if one only has k-1 shares.

There are many implementations of Shamir sharing, for the purposes of this
exercise we're using [this](https://github.com/blockstack/secret-sharing)
Python2.7 version as our reference implementation. That can be installed via:
 
			$ sudo -H pip install secretsharing  

There are many other implementations of Shamir sharing available, but, for this
practical, you MUST ensure that whatever implementation you use interoperates
with that python version, or you won't be able to solve the practical. I'd
advise just using the python version, unless you have a good reason to prefer
something else. Note that the python package in particular does not interop
with the Debian ``ssss`` package. (Feel free to fix that if you like:-)

However, vanilla Shamir secret sharing doesn't quite do what we need for this
practical.  In using Shamir-sharing, one starts with a secret and then
generates shares to distribute, whereas in our case, we are starting from a set
of (recovered) human-memorable passwords and want to generate a secret from k
of those. A little thought will convince you that the standard Shamir-scheme
cannot work that way, and be secure, so we need to tweak the Shamir scheme for
our purposes...

## Our Shamir-like variant

Our variant is relatively simple, for each set of n passwords, we want
knowledge of k passwords to allow reconstruction of the secret. To do that we
randomly generate a secret of the required length, then create n standard
Shamir-shares for that secret, then XOR each share with a hash of one of the
passwords and store that value as the share, along with the ciphertext that is
protected with the recoverable secret.

That way, knowledge of k passwords, allows one to hash each password and XOR
that value with the stored/"published" modified share values and recover the
secret.

This explains why each level of our InfernoBall has a ciphertext for the layer
below, a set of hashes that allow for password recovery and an equally-sized
set of modified shares to allow recovery of the secret once one has k passwords
recovered.

## InfernoBall k-of-n: what k and n?

In our InfernoBalls, the values of k and n are randomly selected at each level. You
can see n by inspection as you see the n hashes and n modified shares, but you
need to find the value of k as part of the practical.

## Submission Format

As you find secrets you can upload your results to submitty, in 
the [inferno](https://cs7ns1.scss.tcd.ie/index.php?semester=f18&course=cs7ns1&component=student&gradeable_id=as5)
gradable. (**Not yet live.**)

Remember that the submitty marks you get don't directly
map to your coursework mark for this assignment, so don't panic if
you can't solve all 10 levels.

As before, you must upload your entire set of secrets each time, as your
marks will reflect only your most recent submission.  (That is, the system does
not remember earlier submissions, it calculates your marks afresh each time.)
After 20 uploads, points will be deducted for having sent too many
submissions.  Once you have found some secrets, do upload those, as that'll
help us understand how students are getting on with the assignment.

The submission format is the secrets file, which has one ascii-hex secret
per line. The sample InfernoBall generation code outputs such a file.
The filename submitted must have a file extension of ".secrets", e.g. 
it might be called "team100.secrets"

For team assignments, any team member may submit and the last submitted
version will be used for marking.

## Team work

It's up to you to meet as a team and to divide up the work between
you as best suits individual team member skills. You will be required
to describe how you worked as a team in your final report for the
module, including stating which team members did what. 

Solving this practical is likely to involve these different tasks,
which may help you in structuring your team work:

1. Orchestrating hash cracking on CPUs/GPUs and dealing with AWS budget
1. Programming to solve the InfernoBall
1. Working with other teams to understand wordlists and recovered passwords
1. (Possibly: consider a crypto-break of the InfernoBall scheme)

Note that the last task above may or may not be worth spending time
on. If your team have some interest and knowledge in the area, you
might consider if there's a faster way to solve the problem than
starting from breaking hashes. (I don't know of one, but this scheme
has not been published/analysed, and such things are notoriously
likely to be broken.) If you did find such a break, that's great
and you'll have validly solved the practical, but please don't
tell other students if the break is computationally easy. (Do tell
me, though, I'll be interersted!) Overall, I'd recommend *not*
getting bogged down trying to break the crypto scheme or the
implementations used, but maybe take a quick look, just in case
I've missed something.

## Co-operation...

We'd encourage teams to collaborate to a limited extent for this practial.

We'll trust you to follow this guidance and won't try enforce it, but
we will give some bonus marks to each team that are first to solve
a level, to try motivate the co-operation we're after:-) Note that we'll
determine the bonus marks post-facto, after the submission deadline.
(**Details of bonuses are still being figured out.**)

We'd encourage teams to co-operate to crack hashes by sharing data about
passwords you've each recovered and the wordlists etc. you've tried, but we'd
prefer teams **not** co-operate on writing code, debugging or on orchestrating
cracking programs.

## Reporting

At the end of the module, you will be required to submit a description of your
work on hash cracking. Keep notes of what you've done for this assignment to
make that easier and so you don't forget what you did.

Keep the code and scripts you write for this practical, e.g., make a
git repo for them. 

A good description of how you orchestrated solving this challenge will attract
marks for your final report.  IOW, do consider orchestration, and do describe
how you dealt with, or why you discarded, orchestration in your final report on
the module.

## InfernoBall format and generation code

InfernoBalls are JSON objects, such as [this](./sample.as5) one. The
corresponding set of secrets are [here](./sample.secrets).  

Each layer of an InfernoBall has the following fields:

- ciphertext: contains the AES-CBC encrypted version of the next layer down
- hashes: contains a set of hashed passwords, with passwords from various
  sources and using various hashing algorithms
- shares: our modified Shamir-shares as described above

You can find Python code to create a test InfernoBall in [as5-makeinferno.py](./as5-makeinferno.py).
That code is the normative specification for the format.

The sample above was generated using:

			$ ./as5-makeinferno.py -u sample -p /usr/share/dict/words -s 1000
			Skips: 1000
			Doing level 0 with 18 passwords
			Doing level 1 with 18 passwords
			Doing level 2 with 15 passwords
			Doing level 3 with 14 passwords
			Doing level 4 with 17 passwords
			Doing level 5 with 13 passwords
			Doing level 6 with 16 passwords
			Doing level 7 with 16 passwords
			Doing level 8 with 13 passwords
			Doing level 9 with 14 passwords

That took about 30 seconds on my laptop. (The actual code to generate the
real InfernoBalls used is not the same but, modulo bugs, produces the same
format output.)


## Hints and non-hints

Depending on what submissions we see to submitty and when, we may
add to this list, but to get you going...

1. On Linux, and perhaps elsewhere, the python secretsharing module tries
hard to use cryptographically good random numbers from ``/dev/random``.
That causes the system to block when it runs out of what it considers
good randomness. To avoid this, I just did s/random/urandom/ in the
relevant python file which you can easily find with a bit of work.

1. As before, there are some passwords that are re-used over the entire
set of passwords used. There shouldn't be any hash value re-used though.

## Summary

So in summary:

- You'll get an email with your InfernoBall
- You need to solve as many layers as you can
- The format for the file to upload is described above
- Limited co-operation with other teams is encouraged

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

