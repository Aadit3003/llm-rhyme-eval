#!/bin/bash
#SBATCH --job-name=small
#SBATCH --output=logs/llama3/small.out
#SBATCH --error=logs/llama3/small.err
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

python eval_small.py "llama3" "singlePerfect" "title"
python eval_small.py "llama3" "singlePerfect" "description"
echo "SINGLE PERFECT DONE!!"






echo "ALL DONE!!"
