#!/bin/bash
#SBATCH --job-name=double
#SBATCH --output=logs/llama3/double.out
#SBATCH --error=logs/llama3/double.err
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




python eval.py "llama3" "doublePerfect" "title"
python eval.py "llama3" "doublePerfect" "description"
echo "DOUBLE PERFECT DONE!!"






echo "ALL DONE!!"
