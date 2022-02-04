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
    echo "-n AGENT_NAME (for specifying agent name: fluent-bit)"
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

export PATH=/opt/td-agent-bit/bin:$PATH

rm -rf /data/tail.0/
rm -f /data/test.log
touch /data/test.log

killall -KILL ${AGENT_NAME} || true # If agent is still running, it should be terminate.

${AGENT_NAME} -c ${HOME}/${AGENT_NAME}.conf &

sleep 3

if [ ${RATE} -gt 0 ]; then
    python3 /usr/local/bin/run_log_generator.py --log-size-in-bytes 1000 --log-rate ${RATE} --log-agent-input-type tail --processes 3 --tail-file-path /data/test.log --count ${STEP} &
fi

python3 -u `which monitor` $STEP ${AGENT_NAME} | tee usage-$AGENT_NAME-$RATE.tsv

killall -TERM python3
killall -KILL ${AGENT_NAME}

exit 0
