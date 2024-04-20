#!/bin/bash
#SBATCH --job-name=single
#SBATCH --output=logs/crystal/single.out
#SBATCH --error=logs/crystal/single.err
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --gres=gpu:A6000:1
#SBATCH --time 08:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here




python eval.py "crystal" "singlePerfect" "title"
python eval.py "crystal" "singlePerfect" "description"
echo "SINGLE PERFECT DONE!!"






echo "ALL DONE!!"
