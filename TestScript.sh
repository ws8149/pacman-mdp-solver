#!/bin/sh

rewardsArray=(-1 -0.7 -0.5 -0.2 0 0.2 0.5 0.7 1)
discountsArray=(0 0.2 0.5 0.7 1)

for d in "${discountsArray[@]}"
do
    for r in "${rewardsArray[@]}"
    do
        # echo $r ',' $d
        python pacman.py -q -n 50 -p MDPAgent -l mediumClassic --reward $r --discount $d        
        
        
    done
done


