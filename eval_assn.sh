#!/bin/bash
#SBATCH --job-name=ol_assonance
#SBATCH --output=logs/olmo/assonance.out
#SBATCH --error=logs/olmo/assonance.err
#SBATCH -N 1
#SBATCH -p shire-general
#SBATCH --gres=gpu:A100_80GB:2
#SBATCH --mem=32G
#SBATCH --time=0-08:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here




python eval.py "olmo" "assonance" "title"
python eval.py "olmo" "assonance" "description"
echo "ASSONANCE DONE!!"






echo "ALL DONE!!"
