#!/bin/bash
# run_overnight.sh

echo "Starting hardened defense sweep: $(date)"
python3 hardened_test.py
echo "Finished hardened defense sweep: $(date)"

echo "Starting duplication full grid: $(date)"
python3 run_tests.py
echo "Finished duplication full grid: $(date)"

echo "Starting confidence rerun on winner: $(date)"
python3 final_winner_test.py
echo "Finished confidence rerun: $(date)"

echo "ALL JOBS COMPLETE: $(date)"
