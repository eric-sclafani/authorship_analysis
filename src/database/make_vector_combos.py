#!/usr/bin/env python3
"""
This script is for  generating all possible combinations of feature vectors and saving them. Done so I can avoid dim reduction
on the fly which takes a very long time to compute especially on large datasets
"""
import argparse
from pathlib import Path

from queries import select_features


def make_save_dir(dir_path=".saved_combos") -> None:
    path = Path(dir_path)
    if not path.exists():
        path.mkdir(parents=True)
        
def generate_all_feature_linear_combinations():
    
    HIGH_LEVEL_FEATURES = [
        "pos_unigrams", 
        "pos_bigrams", 
        "letters", 
        "emojis", 
        "morph_tags", 
        "dep_labels",
        "punctuation", 
        "func_words"
        ]
    
    




def main():
    
    make_save_dir()
    
    parser = argparse.ArgumentParser()
    
    
    
    

if __name__ == "__main__":
    main()