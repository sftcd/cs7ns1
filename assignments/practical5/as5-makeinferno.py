#!/usr/bin/python
# 
# Copyright (C) 2018, stephen.farrell@cs.tcd.ie
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Generate the student and marking file for one student for cs7ns1/as5

import os,sys,argparse,tempfile,shutil

# notes on secretsharing module below:
# - sudo -H pip install secret-sharing is needed first
# - secretsharing uses /dev/random by default, which is slow as it
#   gathers entropy from OS events - that's not only slow, but can
#   also frequently block, to get around this edit the source and
#   change it to use /dev/urandom which won't block
#   source to edit for me was:
#   /usr/local/lib/python2.7/dist-packages/secretsharing/entropy.py  
import secretsharing as sss

# for JSON output
import jsonpickle # install via  "$ sudo pip install -U jsonpickle"

# for hashing passwords
from hashlib import sha256

# needed for these: sudo -H pip install passlib argon2_cffi
from passlib.hash import pbkdf2_sha256,argon2,sha512_crypt,sha1_crypt

# for non-security sensitive random numbers
from random import randrange

# for encrypting you need: sudo -H pip install pycrypto
import base64
from Crypto.Cipher import AES
from Crypto import Random

# our cs7ns1-specific functions for shamir-like sharing

def pxor(pwd,share):
    '''
      XOR a hashed password into a Shamir-share

      1st few chars of share are index, then "-" then hexdigits
      we'll return the same index, then "-" then xor(hexdigits,sha256(pwd))
      we truncate the sha256(pwd) to if the hexdigits are shorter
      we left pad the sha256(pwd) with zeros if the hexdigits are longer
      we left pad the output with zeros to the full length we xor'd
    '''
    words=share.split("-")
    hexshare=words[1]
    slen=len(hexshare)
    hashpwd=sha256(pwd).hexdigest()
    hlen=len(hashpwd)
    outlen=0
    if slen<hlen:
        outlen=slen
        hashpwd=hashpwd[0:outlen]
    elif slen>hlen:
        outlen=slen
        hashpwd=hashpwd.zfill(outlen)
    else:
        outlen=hlen
    xorvalue=int(hexshare, 16) ^ int(hashpwd, 16) # convert to integers and xor 
    paddedresult='{:x}'.format(xorvalue)          # convert back to hex
    paddedresult=paddedresult.zfill(outlen)       # pad left
    result=words[0]+"-"+paddedresult              # put index back
    return result

def newsecret(numbytes):
    '''
        let's get a number of pseudo-random bytes, as a hex string
    '''
    binsecret=open("/dev/urandom", "rb").read(numbytes)
    secret=binsecret.encode('hex')
    return secret

def pwds_to_shares(pwds,k,numbytes):
    '''
        Give a set of n passwords, and a threshold (k) generate a set
        of Shamir-like 'public' shares for those.

        We do this by picking a random secret, generating a set of
        Shamir-shares for that, then XORing a hashed password with 
        each share.  Given the set of 'public' shares and k of the
        passwords, one can re-construct the secret.

        Note:  **There are no security guarantees for this**
        This is just done for a student programming exercise, and
        is not for real use. With guessable passwords, the secret 
        can be re-constructed!

    '''
    n=len(pwds) # we're in k-of-n mode...
    secret=newsecret(numbytes) # generate random secret
    shares=sss.SecretSharer.split_secret(secret,k,n) # split secret
    diffs=[] # diff the passwords and shares
    for i in range(0,n):
        diffs.append(pxor(pwds[i],shares[i]))
    return diffs

def pwds_shares_to_secret(kpwds,kinds,diffs):
    '''
        take k passwords, indices of those, and the "public" shares and 
        recover shamir secret
    '''
    shares=[]
    for i in range(0,len(kpwds)):
        shares.append(pxor(kpwds[i],diffs[kinds[i]]))
    secret=sss.SecretSharer.recover_secret(shares)
    return secret

# password hashing primitives

def newhash(p):
    '''
        Randomly pick a hash function and apply it
    '''
    # hashes supported
    hashalgs=[pbkdf2_sha256,argon2,sha512_crypt,sha1_crypt]
    halg=randrange(0,len(hashalgs))
    hash=hashalgs[halg].hash(p)
    return hash

# encrypt wrapper

# modified from https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def encrypt(raw, key):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

# main code...

# magic JSON incantation (I forget why, might not even be needed here:-)
jsonpickle.set_encoder_options('json', sort_keys=True, indent=2)
jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=2)

# defaults for some command line arguments (CLAs)
depth=10 # level of nesting
minppl=10 # ppl = passwords per level - we'll randomly select in this range, unless CLA overrides
maxppl=20
skips=0 # how many passwords from file to skip

# usage
def usage():
    print >>sys.stderr, "Usage: " + sys.argv[0] + " -u <username> -p <pwdfile> [-D <destdir>] [-s <skips>] [-m min] [-M max] [-l levels]" 
    sys.exit(1)

# getopt handling
argparser=argparse.ArgumentParser(description='Make as5 files for one studenrt')
argparser.add_argument('-u','--user',     
                    dest='username',
                    help='submitty username for student')
argparser.add_argument('-p','--passwords',     
                    dest='pwdfile',
                    help='file containing passwords, one per line')
argparser.add_argument('-D','--destdir',     
                    dest='destdir',
                    help='directory for output file')
argparser.add_argument('-s','--skip',     
                    dest='skips',
                    help='how many passwords from start of file to skip over')
argparser.add_argument('-m','--minppl',     
                    dest='minppl',
                    help='minimum passwords per level')
argparser.add_argument('-M','--maxppl',     
                    dest='maxppl',
                    help='maximum passwords per level')
argparser.add_argument('-l','--levels',     
                    dest='levels',
                    help='levels to generate')
args=argparser.parse_args()

# post opt checks
if args.username is None:
    usage()

if args.skips is not None:
    skips=int(args.skips)

if args.levels is not None:
    depth=int(args.levels)

if args.minppl is not None:
    minppl=int(args.minppl)

if args.maxppl is not None:
    maxppl=int(args.maxppl)

if minppl > maxppl:
    print "Can't have minppl > maxppl - exiting"
    sys.exit(5)

# derived parameters - mix/max passwords per level needed
mintpl=(minppl/10) # tpl = threshold per level - we'll randomly select in this range
if mintpl < 2: # can't have <2 shares:-)
    mintpl=2
maxtpl=(maxppl/2)

if args.pwdfile is None:
    usage()

if not os.path.isfile(args.pwdfile) or not os.access(args.pwdfile,os.R_OK):
    print "Can't read " + args.pwdfile + " - exiting"
    sys.exit(2)

# load passwords from file from offset, just a few thousand needed
# so ok memory-wise (I hope!)
passwords=[]
print "Skips: " + str(skips)
with open(args.pwdfile,"r") as pwdf:
    lno=0
    for line in pwdf:
        if lno >= skips:
            passwords.append(line.strip())
        lno += 1
npasswords=len(passwords)

destdir="."
if args.destdir is not None:
    destdir=args.destdir

if not os.access(destdir,os.W_OK):
    # not checking we can write to destdir but feck it, good enough:-)
    print "Can't read " + destdir + " - exiting"
    sys.exit(3)

# create a tmpdir and go there
tmpdir=tempfile.mkdtemp()

# Ensure the file is read/write by the creator only
saved_umask = os.umask(0077)

# next password to start from is at this index
bottom=0

try:
    # make layers 'till done
    centrelayercontent="Here be dragons!"
    prevlayercontent=centrelayercontent
    secrets=[]
    for level in range(0,depth):
        # select N passwords for this level
        npwds=randrange(minppl,maxppl) # number we'll use
        print "Doing level " + str(level) + " with " + str(npwds) + " passwords"
        lpwds=passwords[bottom:bottom+npwds]
        bottom+=npwds
        if bottom >= npasswords:
            print >>sys.stderr, "Bummer we're out of passwords (used " + str(npasswords) + ")"
            sys.exit(4)
        # pick threshold for this layer
        lthresh=randrange(mintpl,maxtpl)
        # generate shares/secret for those pwds
        shares=pwds_to_shares(lpwds,lthresh,BLOCK_SIZE)
        kinds = [i for i in xrange(lthresh)]
        levelsecret=pwds_shares_to_secret(lpwds[0:lthresh],kinds,shares)
        secrets.append(levelsecret)
        # hash the passwords
        hashes=[]
        for p in lpwds:
            # note newhash could throw exception for weird values of p
            # that's ok though, if it happens just try again from command line
            # with different passwords
            hashes.append(newhash(p)) 
        # encrypt prev layer 
        ciphertext=encrypt(jsonpickle.encode(prevlayercontent),levelsecret.zfill(32).decode('hex'))
        # make up this layer
        layercontent={}
        layercontent['hashes']=hashes
        layercontent['shares']=shares
        layercontent['ciphertext']=ciphertext
        # nesty nesting
        prevlayercontent=layercontent
    # write files
    cfname=args.username+".as5"
    path=os.path.join(tmpdir,cfname)
    with open(path,"w") as tmpf:
        tmpf.write(jsonpickle.encode(prevlayercontent))
    tmpf.close()
    shutil.move(path,destdir+"/"+cfname)
    csname=args.username+".secrets"
    path=os.path.join(tmpdir,csname)
    with open(path,"w") as tmpf:
        for sec in secrets:
            tmpf.write(sec+"\n")
    tmpf.close()
    shutil.move(path,destdir+"/"+csname)
except Exception as e:
    print >>sys.stderr, "Exception doing: " + args.username + " " + str(e)
    sys.exit(5)
finally:
    # clean up
    os.umask(saved_umask)
    shutil.rmtree(tmpdir,ignore_errors=True)

# success return, we're all done!
sys.exit(0)

