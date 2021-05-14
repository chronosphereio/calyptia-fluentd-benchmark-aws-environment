#!/bin/sh

while getopts s:r: option
do
case "${option}"
in
s) STEP=${OPTARG};;
r) RATE=${OPTARG};;
esac
done

usage() {
    echo "available options are:"
    echo "-s STEP (for set up total step(s))"
    echo "-r RATE (for set up generating line rate/sec)"
    exit 1
}

if [ -z $STEP ]; then
    echo "specify step with value -s VALUE."
    usage
fi

if [ -z $RATE ]; then
    echo "specify rate value with -r VALUE."
    usage
fi

sudo calyptia-fluentd -o calyptia-fluentd.log &

sleep 3

if [ $RATE -gt 0 ]; then
    loggen --size 300 --rate ${RATE} --interval $(( 2*STEP )) 127.0.0.1 514 2> /dev/null &
fi

sudo python3.8 -u /usr/local/bin/monitor $STEP | tee usage-$RATE.tsv

sudo killall -TERM calyptia-fluentd

exit 0
