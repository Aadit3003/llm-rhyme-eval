#!/bin/bash
#SBATCH --job-name=rhy
#SBATCH --output=logs/rhy.out
#SBATCH --error=logs/rhy.err
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --gres=gpu:A6000:1
#SBATCH --time 04:00:00 

echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here




python eval.py "/home/aaditd/3_Rhyme/data/english/test/singlePerfect.txt" "/home/aaditd/3_Rhyme/output/english/llama2/singlePerfect.txt"
echo "SINGLE PERFECT DONE!!"

python eval.py "/home/aaditd/3_Rhyme/data/english/test/doublePerfect.txt" "/home/aaditd/3_Rhyme/output/english/llama2/doublePerfect.txt"
echo "DOUBLE PERFECT DONE!!"

python eval.py "/home/aaditd/3_Rhyme/data/english/test/assonance.txt" "/home/aaditd/3_Rhyme/output/english/llama2/assonance.txt"
echo "ASSONANCE DONE!!"

python eval.py "/home/aaditd/3_Rhyme/data/english/test/consonance.txt" "/home/aaditd/3_Rhyme/output/english/llama2/consonance.txt"
echo "CONSONANCE DONE!!"



echo "ALL DONE!!"
