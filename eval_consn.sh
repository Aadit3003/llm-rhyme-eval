#!/bin/bash
#SBATCH --job-name=consonance
#SBATCH --output=logs/olmo/consonance.out
#SBATCH --error=logs/olmo/consonance.err
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




python eval.py "olmo" "consonance" "title"
python eval.py "olmo" "consonance" "description"
echo "CONSONANCE DONE!!"






echo "ALL DONE!!"
