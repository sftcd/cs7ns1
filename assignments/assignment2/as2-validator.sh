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

# This is the script to to validate an output from as2-bench.sh for assignment1 of CS7NS1/CS4400
# The same script will be run after you submit to submitty

# timestamps are handy
function whenisitagain()
{
    date -u +%Y%m%d-%H%M%S
}
NOW=$(whenisitagain)

INPUT="$1"

if [ ! -f $INPUT ]
then
	echo "$0: you need to provide input"
	exit 99
fi

# the input here should look something like this:
#
#		AWS Meta-data:
#		
#		m4.large
#		i-007def62250c55c52
#		ami-078b2e4efb41c1a1c
#		ip-172-30-1-203.eu-west-1.compute.internal
#		
#		John bench mark:
#		
#		Benchmarking: argon2 [Blake2 AVX]... (2xOMP) DONE
#		Speed for cost 1 (t) of 3, cost 2 (m) of 4096, cost 3 (p) of 1, cost 4 (type [0:Argon2d 1:Argon2i]) of 0 and 1
#		Warning: "Many salts" test limited: 6/256
#		Many salts:	169 c/s real, 85.3 c/s virtual
#		Only one salt:	171 c/s real, 85.7 c/s virtual

res=0

donecheck=$(grep -c "DONE" $INPUT)
if [[ "$donecheck" != "1" ]]
then
	echo "$0: oops - expected 1 DONE in output, got $donecheck"
	res="$res 98"
fi

argon2check=$(grep -c "argon2" $INPUT)
if [[ "$argon2check" != "1" ]]
then
	echo "$0: oops - expected 1 argon2 in output, got $argon2check"
	res="$res 97"
fi

metacheck=$(grep -ci "no route" $INPUT)
if [[ "$metacheck" != "0" ]]
then
	echo "$0: oops - looks like no route to AWS meta-data (169.254.169.254)"
	res="$res 96"
fi

amicheck=$(grep -c "ami" $INPUT)
if [[ "$amicheck" != "1" ]]
then
	echo "$0: oops - expected 1 ami in output, got $amicheck"
	res="$res 95"
fi

# return result
if [[ "$res" == "0" ]]
then
	echo "ok"
	exit 0
else
	# note: res will accumulate problem numbers
	echo "400 NOT OK $res"
	echo 99
fi



