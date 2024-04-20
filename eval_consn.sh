#!/bin/bash
#SBATCH --job-name=consonance
#SBATCH --output=logs/consonance.out
#SBATCH --error=logs/consonance.err
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




python eval.py "consonance" "title"
python eval.py "consonance" "description"
echo "CONSONANCE DONE!!"






echo "ALL DONE!!"
