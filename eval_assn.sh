#!/bin/bash
#SBATCH --job-name=assonance
#SBATCH --output=logs/llama3/assonance.out
#SBATCH --error=logs/llama3/assonance.err
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




python eval.py "llama3" "assonance" "title"
python eval.py "llama3" "assonance" "description"
echo "ASSONANCE DONE!!"






echo "ALL DONE!!"
