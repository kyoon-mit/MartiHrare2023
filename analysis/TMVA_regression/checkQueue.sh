#!/bin/bash

indexCommands=0

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    #echo -e "[$(date +'%T')] Queue: ${queueLength}"
    if true; then
    if [ "$queueLength" -lt 4000 ]; then
        python slurm.py -i commands.txt --minIndex $indexCommands --maxIndex $((indexCommands + 50))
        ((indexCommands += 50))
    fi
    if [ "$indexCommands" -gt 3003 ]; then
        break
    fi
    fi
    sleep 15
done

echo "All jobs queued. Exiting the loop."
