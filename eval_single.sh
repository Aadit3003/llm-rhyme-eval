#!/bin/bash
#SBATCH --job-name=ol_single
#SBATCH --output=logs/olmo/single.out
#SBATCH --error=logs/olmo/single.err
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


python eval.py "olmo" "singlePerfect" "title"
python eval.py "olmo" "singlePerfect" "description"
echo "SINGLE PERFECT DONE!!"






echo "ALL DONE!!"
