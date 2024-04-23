#!/bin/bash
#SBATCH --job-name=small2
#SBATCH --output=logs/crystal/small.out
#SBATCH --error=logs/crystal/small.err
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100:1
#SBATCH --time 02:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here


# python ol.py

python eval_small.py "crystal" "singlePerfect" "title"
python eval_small.py "crystal" "singlePerfect" "description"
echo "SINGLE PERFECT DONE!!"






echo "ALL DONE!!"
