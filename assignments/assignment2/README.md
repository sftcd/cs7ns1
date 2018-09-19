
# CS7NS1/CS4400 Assignment 2

The deadline for this assignment is: 2018-09-26 23:59:59

For this first practical assignment, you are to:

- register with rosettahub to get your AWS budget
- create a linux instance
- compile JohnTheRipper
- run a benchmarking script
- upload the output from the benchmarking script to submitty
- stop your image

Each step is described further below. 

Usually with so many students doing an assignments, some tweaks
to these instructions will be needed, so check back here often
to see if there have been any updates.

**Don't forget to stop your instance when you're done!**

## Register with rosettahub

You will receive an email from rosettahub.com with the instructions
as to how to create and authorise your account. Follow the instructions
in the various emails.

According to rosettahub.com the workflow is:

1. Student receives a message with a link from us, clicks on the link to verify
   his/her email and accept the RosettaHUB terms and the AWS terms.

1. The student gets automatically processed and receives almost immediately a
   new AWS+RosettaHUB account and we pre-submit an AWS Educate application on
his/her behalf. The account is blocked.

1. Student receives an email from the AWS Educate team with the following
   subject: 'Email Verification - AWS Educate Application'.  Student clicks on
the link in the email to accept the AWS Educate terms.

1.  After approving the terms, Student receives an email with the following
	subject: 'AWS Educate Application Approved' with an AWS Promotional credit
code. Student logs in to RosettaHUB, clicks on the 'Go To AWS Console' button, 
searches for and clicks on the service named 'Billing', clicks on the 'Credits' 
option, enters the credit code, the security check and clicks on the button 
'Redeem' to get a budget of $100. 

1. You may only have an initial budget of five dollars. In that case, you
will want to request more budget. You won't need that for this assignment
so we'll return to that next time.

RosettaHub *do not* offer support to students, so do not mail them, except
as part of the registration flow.

## Create a linux instance

When logged into rosettahub:

- Click on an ubuntu 18.04 image, from the "images" set in the rosettahub console (you 
  may need to scroll down to find this)
- That'll ask for a new spot instance, take the defaults but give it a name you'll remember
- When the spot image is created, it'll appear at the top of the dashboard page
- Right-click the image and download the SSH private keys. Rename that file to something
  memorable and ``chmod 600 <private-key-file>``
- Right-click the image and choose to see the connection-settings
- SSH into your image and continue...

**Don't forget to stop your instance when you're done!**

- Before you shutdown/terminate your instance, you may want to save an
   image of that so you  don't have to re-install john etc every time.

## Compile JohnTheRipper

[JohnTheRipper](https://openwall.info/wiki/john) is 
a well-known hash cracker. It can be installed via
``apt`` but for this assignment you will need to download
and compile the community "Jumbo" version from the
[github repo](https://github.com/magnumripper/JohnTheRipper).

I recommend doing that on your local machine first to
avoid consuming AWS credits - you will need to figure out
what dependencies are needed for a successful build.
(There's not many, figuring that out is part of the 
assignment.)

I recommend cloning the john repo into a ``code``
subdirectory of your home directory, that is, the code
should end up in ``$HOME/code/JohnTheRipper`` - if you
put the code somewhere else, then you'll need to modify
the ``as2-bench.sh`` script described below.

## Run a benchmarking script

The benchmarking script is called ``as2-bench.sh`` - read it to 
see what it does. If it says all is well you can submit it's
output (the file ``as2-output.bench``) to submitty. If not, then
you may get some hints as to what was wrong by running the
``as2-validator.sh`` script with ``as2-output.bench`` as input.
(Which ``as2-bench.sh`` does internally.) 

A good looking ``as2-output.bench`` will look like:

			AWS Meta-data:
			
			m4.large
			i-007def62250c55c52
			ami-078b2e4efb41c1a1c
			ip-172-30-1-203.eu-west-1.compute.internal

			John bench mark:
			
			Benchmarking: argon2 [Blake2 AVX]... (2xOMP) DONE
			Speed for cost 1 (t) of 3, cost 2 (m) of 4096, cost 3 (p) of 1, cost 4 (type [0:Argon2d 1:Argon2i]) of 0 and 1
			Warning: "Many salts" test limited: 6/256
			Many salts:	168 c/s real, 84.2 c/s virtual
			Only one salt:	172 c/s real, 87.2 c/s virtual

## Upload results to submitty

You will shortly receive a mail with your initial submitty password. Follow
the instructions from that mail to login to [submitty](https://cs7ns1.scss.tcd.ie/) 
and change your initial password.

Once logged in, upload the file created from running the benchmarch 
script (``as2-output.bench``) to submitty as assignment2 and start accumulating marks!

Note that the ``as2-validator.sh`` script commands are not used at the back end
of submitty to check your submission. We use different code and may add
additional checks to the submitty copy of that, that we can run any time during
the course, so don't try fake an output that'll fool your local copy of
``as2-validator.sh``.  

## Stop your image

**Don't forget to stop your instance when you're done!**

If you do forget to stop the image, your AWS EC2 credits will all be used
up and you'll be sad.

## Support

RosettaHub *do not* offer support to students, so do not mail them, except
as part of the registration flow.

For questions about this assignment, mail Christian.

