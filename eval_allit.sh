#!/bin/bash
#SBATCH --job-name=alliterative
#SBATCH --output=logs/llama3/alliterative.out
#SBATCH --error=logs/llama3/alliterative.err
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100:2
#SBATCH --time 08:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here




python eval.py "llama3" "alliterative" "title"
python eval.py "llama3" "alliterative" "description"
echo "ALLITERATIVE DONE!!"






echo "ALL DONE!!"
