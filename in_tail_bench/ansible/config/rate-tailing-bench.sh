#!/bin/sh

while getopts s:r:n: option
do
case "${option}"
in
s) STEP=${OPTARG};;
r) RATE=${OPTARG};;
n) AGENT_NAME=${OPTARG};;
esac
done

usage() {
    echo "available options are:"
    echo "-s STEP (for set up total step(s))"
    echo "-r RATE (for set up generating line rate/sec)"
    echo "-n AGENT_NAME (for specifying agent name: td-agent/calyptia-fluentd)"
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

if [ -z $AGENT_NAME ]; then
    echo "specify agent name with -n AGENT_NAME."
    usage
fi

${AGENT_NAME} -c ${HOME}/${AGENT_NAME}.conf -o ${AGENT_NAME}.log &

sleep 3

if [ $RATE -gt 0 ]; then
    dummer -c ${HOME}/dummer/dummer.conf -r $RATE &
fi

python3 -u `which monitor` $STEP ${AGENT_NAME} | tee usage-$AGENT_NAME-$RATE.tsv

killall -TERM dummer
killall -TERM ruby
killall -TERM ${AGENT_NAME}

exit 0
