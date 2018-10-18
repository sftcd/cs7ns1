
# Practical assignment 4 - Break moar hashes...

The deadline for this is Friday October 19th.

**bug:** There's a bug in my submitty verification code. Descrypt passwords are
truncated to eight characters. When a descrypt password in my verifier database
should be 8 characters, it actually only has 7 characters. (My fault - it's due
to a scripting bug.) Passwords that are 7 characters or less aren't affected as
far as I know. The work-around is to drop the rightmost character for all the
descrypt passwords you upload to submitty, e.g. if the password for some
descrypt hash is "abcd1234" you should send "abcd123" instead. I sent mail to
the class about this on 20181004.

**Late submissions are not allowed.**

**Don't forget to stop your instance when you're done!**

For this practical, you will be emailed a list of 2000 password hashes and are
to solve those, finding the passwords for as many as you can.  Passwords are of
three different kinds this time, (i.e. selected in three different ways) and
six different hash functions are used. 

As you solve passwords you can upload your results to submitty, in the  [crack
moar
hashes](https://cs7ns1.scss.tcd.ie/index.php?semester=f18&course=cs7ns1&component=student&gradeable_id=as4)
gradable.
Remember that the submitty marks you get (from 2000) don't directly
map to your coursework mark for this assignment, so don't panic if
you can't solve all 2000.

As before, you must upload your entire set of solved hashes each time, as your
marks will reflect only your most recent submission.  (That is, the system does
not remember earlier submissions, it calculates your marks afresh each time.)
After 100 uploads, points will be deducted for having sent too many
submissions.  Once you have found some passwords, do upload those, as that'll
help staff understand how students are getting on with the assignment.

You can choose whatever technology you want to solve the problem, but this
assignment is scaled so that:

- you are likely to want to use a [GPU instance](#aws-gpu-instances) 
- you may want to write code or [scripts](#scripting-motivations-for) to orchestrate solving the problem

Where possible, I would recommend not using EC2 instances for development, but
rather try to break a subset of the hashes locally and when that seems to be
making some progress you can run your job on an EC2 instance. 

Co-operating with other students to work on this pratical is encouraged. Please
do that, but don't actually crack someone else's hashes though - you all should
want other potential team-members for the next practical to understand as much
of this as possible!

## Reporting

At the end of the module, you will be required to submit a description of your
work on hash cracking. Keep notes of what you've done for this assignment to
make that easier and so you don't forget what you did.

If you write any code or scripts for this practical, keep those, e.g., make a
git repo for them. 

A good description of how you orchestrated solving this challenge will attract
marks for your final report.  IOW, do consider orchestration, and do describe
how you dealt with, or why you discarded, orechestration in your final report on
the module.

## Broken hashes format

This is the same as for practical number 3.

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

## AWS GPU instances

**These can be expensive - pay attention  to the costs/budget**

**Do not leave your instances running**

AWS describe their GPU instances
[here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html).
There's guidance
[here](http://www.rockfishsec.com/2015/05/gpu-password-cracking-with-amazon-ec2.html)
on getting started with a g2.Nxlarge instance, but that assumes an "ordinary" AWS
account and not using rosetthahub.com (RH). 
There's guidance [here](https://medium.com/@iraklis/running-hashcat-v4-0-0-in-amazons-aws-new-p3-16xlarge-instance-e8fab4541e9b)
on getting started with a very large instance. Neither of those is exactly what
you want, but read both before you 
start so you understand the steps described below.
Go to labs to ask if/when you have questions.

The steps I (SF) followed to get a working GPU instance were:

1. Picking an instance type

	Spot image prices are described [here](https://aws.amazon.com/ec2/spot/pricing/) - as you'll
see GPU instances vary from $0.21/hr up to $11.87/hr.
	The cheapest is a g2.2xlarge but rosettabhub.com has a bug in requesting spot
instances for those (the max bid is too low) that they've not yet fixed. 
A g2.8xlarge seems like the next cheapest.

1. Download GPU driver

	You get an NVIDIA GPU driver [here](https://www.nvidia.com/Download/Find.aspx) - make sure 
you pick the right one.  For a g2.8xlarge you want to pick
GRID/GRID Series/GRID K520 and your OS etc.  That got me a file called
``NVIDIA-Linux-x86_64-367.128.run``. You should download such a file to your local
machine and hang on to it.

1. Start an instance via RH

	From RH, I chose an Ubuntu 18.04 image with a spot instance type of g2.8xlarge. 
	I launched that, downloaded private keys and SSH'd in as usual. 

1.  ``scp`` your driver file from your local machine to the VM.

			local$ scp -i private-keys-file.pem NVIDIA-Linux-x86_64-367.128.run ubuntu@vm-XX-XXX-XX-XX.rosettavm.com:

	If using Putty, you'll need to figure out how to transfer the file.


1. Do an update/upgrade cycle, and prepare various dependencies...

			vm$ sudo apt update
			vm$ sudo apt upgrade
			vm$ sudo apt-get install build-essential
			vm$ sudo apt-get install linux-image-extra-virtual

1. Run the driver install... Thas has various prompts - pick the sensible options:-)

			vm$ sudo /bin/bash NVIDIA-Linux-x86_64-367.128.run

	That'll give some warnings - you don't need graphics so X windows stuff doesn't matter.

1. Install hashcat 

			vm$ sudo apt install hashcat

	[Hashcat](https://hashcat.net/hashcat/) is another tool, like john, for
cracking hashes. Hashcat seems to win real password cracking competitions these
days more than john, and is pretty much designed with GPUs in mind.

1. Ensure hashcat sees the GPUs

			vm$ hashcat -I

	You can see what that ought look like [here](./hashcat-I-output.md).

1. Go back to RH and make an image of that VM. 

	That'll log you out of the VM but not stop it! (So you'll wanna go back and
	stop it later.) Creating an image may take a few minutes.
	You should be able to log back in a minute or two later. The saved image
	should be visible in RH after a few more minutes.

	I've noticed that sometimes attempting to re-launch a saved image 
	seems to not result in getting the same instance type, which is
	a problem for a GPU instance as you'll need the right drivers.
	For example, when trying to re-launch the image I saved for a g2.8xlarge
	instance, my chosen instance type was forgotten, another was
	provided as default and though one can chose a non-default, the
	only g-class instanaces offered were g2.2xlarage (that suffers
	from the RH underbidding bug), or g3.4xlarge, which doesn't
	use the same NVIDIA driver (apparently).

	I'd suggest scripting up the above process, so you can quickly go from
	a new image to a working GPU-enabled VM.

1. Run hashcat on an example

			vm$ echo '$1$wVm8cBcv$o7UmFE.v2Shi9vFt6qyU5/' >foo
			vm$ hashcat -a 3 -m 500 foo -1 '?d' '?1?1?1?1?1?1' -O
			... a short while later...
			vm$ cat $HOME/.hashcat/hastcat.potfile
			$1$wVm8cBcv$o7UmFE.v2Shi9vFt6qyU5/:123456
			vm$

## Scripting: motivations for...

There are 3 password kinds and 6 hashing algs in this practical.  You likely
have a local machine where you can do development and you have access to AWS
VMs via RH. There's a large variety of VM instance kinds, some with GPUs, some
without, some with more or less powerful CPUs, and each with it's own cost.
Even just with the john tool, the GPU and CPU implementations of the same
hashing algorithm differ and will perform differently. That's a lot of options
to investigate to find your best approach.

In addition, you cannot distinguish the password types until you solve the hashes. The tools
(john, hashcat, etc.) generally work better when you have some idea of the
password type, and have command line arguments that are specific to the kind of
password and attack you're currently mounting.
(In case you want to make some test hashes where you know the password to test
performance, for the ``argon2`` and ``pbkdf2-sha256`` hashes, I used the python
``passlib`` module, with ``argon2_cffi``. For the others the ``mkpasswd``
command sufficed.)

All the above suggests that you want to break the problem down first by
hash algorithm, then attack the easiest of those to crack. Which you consider
easiest will depend on your evaluation of the different algorithms, VM options
and your guesses as to password types.  As you learn more about the password
types, you can attack the harder/slower hash functions. And you'll likely not
want to be typing so much on the command line of the VM in AWS, but more likely
running things remotely from your local machine via scripts run remorely over SSH.

OTOH, you could just about keep track of all that manually, but you'll likely be
better off to write some scripts as you'll probably be cycling back and forth
with different attacks and different input files and maybe different tools.

## Hints and non-hints

Depending on what submissions we see to submitty and when, we may
add to this list, but to get you going...

1. Most passwords are only used to produce one hash. About 10% are the input for
more than one hash. Hashes with common passwords are likely but not certain
to have been allocated to different students.
1. None of the passwords here are super-strong - don't try solve this assignment
with guesses for super-strong passwords.

## Summary

So in summary:

- You'll get an email with your password hashes
- You need to solve as many of those as you can
- The format for the file to upload is described above
- This time, co-operating with other students is encouraged

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

