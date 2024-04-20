#!/bin/bash
#SBATCH --job-name=double
#SBATCH --output=logs/crystal/double.out
#SBATCH --error=logs/crystal/double.err
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




python eval.py "crystal" "doublePerfect" "title"
python eval.py "crystal" "doublePerfect" "description"
echo "DOUBLE PERFECT DONE!!"






echo "ALL DONE!!"
