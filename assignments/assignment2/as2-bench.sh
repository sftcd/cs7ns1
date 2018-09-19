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

# set -x

# This is the benchmark script to run for assignment1 of CS7NS1/CS4400

JOHNBIN=~/code/JohnTheRipper/run/john
CURL=`which curl`
CURLPARMS="-s"
OUTPUT="as2-output.bench"
VALIDATOR="as2-validator.sh"
FORMAT="argon2"
LOCAL="no"

# timestamps are handy
function whenisitagain()
{
    date -u +%Y%m%d-%H%M%S
}
NOW=$(whenisitagain)

if [ ! -f $JOHNBIN ]
then
	echo "Compile john first."
	exit 99
fi

if [[ "$CURL" == "" ]]
then
	echo "Install curl first."
	exit 98
fi	

if [ ! -f $VALIDATOR ]
then
	echo "Can't find validator $VALIDATOR - better fix that"
	exit 97
fi


# usage
function usage()
{
	echo "usage: $0 [-f format] [-l]" 
	exit 99
}

# options may be followed by one colon to indicate they have a required argument
if ! options=$(getopt -s bash -o f:lh -l format:,local,help -- "$@")
then
	# something went wrong, getopt will put out an error message for us
	exit 1
fi
eval set -- "$options"
while [ $# -gt 0 ]
do
	case "$1" in
		-h|--help) usage;;
		-f|--format) FORMAT=$2; shift;;
		-l|--local) LOCAL="yes";;
		(--) shift; break;;
		(-*) echo "$0: error - unrecognized option $1" 1>&2; exit 1;;
		(*)  break;;
	esac
	shift
done

tmpf=`mktemp /tmp/as2-XXXX`

# use aws metadata to get info about instance/AMI
if [[ "$LOCAL" != "yes" ]]
then
	echo "AWS Meta-data:" >>$tmpf
	$CURL $CURLPARMS http://169.254.169.254/latest/meta-data >>$tmpf 2>&1 
	echo "" >>$tmpf
	$CURL $CURLPARMS http://169.254.169.254/latest/meta-data/instance-type >>$tmpf 2>&1
	echo "" >>$tmpf
	$CURL $CURLPARMS http://169.254.169.254/latest/meta-data/instance-id >>$tmpf 2>&1
	echo "" >>$tmpf
	$CURL $CURLPARMS http://169.254.169.254/latest/meta-data/ami-id >>$tmpf 2>&1
	echo "" >>$tmpf
	$CURL $CURLPARMS http://169.254.169.254/latest/meta-data/hostname >>$tmpf 2>&1
	echo "" >>$tmpf
	echo "" >>$tmpf
fi

# run john 
echo "John bench mark:" >>$tmpf
echo "" >>$tmpf
$JOHNBIN --test --format:$FORMAT >>$tmpf

# keep a backup version of previous output
if [ -f $OUTPUT ]
then
	echo "backing up $OUTPUT to $OUTPUT.$NOW just in case you want that later."
	mv $OUTPUT $OUTPUT.$NOW
fi

mv $tmpf $OUTPUT

# validate output
result=`./$VALIDATOR $OUTPUT`
if [[ "$result" == "ok" ]]
then
	echo "$OUTPUT looks good to submit"
else
	echo "$OUTPUT looks doddy - check what $VALIDATOR didn't like"
fi

echo "Your output is in $OUTPUT"




