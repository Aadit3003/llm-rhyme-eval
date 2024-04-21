#!/bin/bash
#SBATCH --job-name=consonance
#SBATCH --output=logs/llama3/consonance.out
#SBATCH --error=logs/llama3/consonance.err
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




python eval.py "llama3" "consonance" "title"
python eval.py "llama3" "consonance" "description"
echo "CONSONANCE DONE!!"






echo "ALL DONE!!"
