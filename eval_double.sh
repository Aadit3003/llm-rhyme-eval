#!/bin/bash
#SBATCH --job-name=l_double
#SBATCH --output=logs/llama2/double.out
#SBATCH --error=logs/llama2/double.err
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=aaditd@andrew.cmu.edu
#SBATCH -N 1
#SBATCH -p shire-general
#SBATCH --gres=gpu:A6000
#SBATCH --mem=32G
#SBATCH --time=04:00:00

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here




# python eval.py "llama2" "doublePerfect" "title"
python eval.py "llama2" "doublePerfect" "description"
echo "DOUBLE PERFECT DONE!!"






echo "ALL DONE!!"
