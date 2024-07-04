#!/bin/bash
#SBATCH --job-name=l3_single
#SBATCH --output=logs/llama3/single.out
#SBATCH --error=logs/llama3/single.err
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=aaditd@andrew.cmu.edu
#SBATCH -N 1
#SBATCH -p general
#SBATCH --gres=gpu:A6000:1
#SBATCH --mem=32G
#SBATCH --time=0-08:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here

python ../evaluate_rhyme.py "english" "llama3" "assonance" "title"
python ../evaluate_rhyme.py "english" "llama3" "assonance" "description"

python ../evaluate_rhyme.py "dutch" "llama3" "singlePerfect" "title"
python ../evaluate_rhyme.py "dutch" "llama3" "singlePerfect" "description"
echo "SINGLE PERFECT DONE!!"






echo "ALL DONE!!"
