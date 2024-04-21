#!/bin/bash
#SBATCH --job-name=alliterative
#SBATCH --output=logs/olmo/alliterative.out
#SBATCH --error=logs/olmo/alliterative.err
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




python eval.py "olmo" "alliterative" "title"
python eval.py "olmo" "alliterative" "description"
echo "ALLITERATIVE DONE!!"






echo "ALL DONE!!"