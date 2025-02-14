#!/bin/bash
#SBATCH --job-name=l3_alliterative
#SBATCH --output=logs/llama3/alliterative.out
#SBATCH --error=logs/llama3/alliterative.err
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=aaditd@andrew.cmu.edu
#SBATCH -N 1
#SBATCH -p general
#SBATCH --gres=gpu:A6000:2
#SBATCH --mem=32G
#SBATCH --time=0-08:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here




python ../evaluate_rhyme.py "english" "llama3" "alliterative" "title"
python ../evaluate_rhyme.py "english" "llama3" "alliterative" "description"

python ../evaluate_rhyme.py "dutch" "llama3" "alliterative" "title"
python ../evaluate_rhyme.py "dutch" "llama3" "alliterative" "description"

echo "ALLITERATIVE DONE!!"






echo "ALL DONE!!"
