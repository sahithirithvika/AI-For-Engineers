"""
Merge multiple dataset files into a single training dataset
"""

import json
from pathlib import Path


def merge_datasets(output_file='processed/training_data.json'):
    """Merge all JSON datasets in the processed directory"""
    
    processed_dir = Path(__file__).parent / 'processed'
    all_data = []
    
    # Find all JSON files
    json_files = [
        'training_data.json',
        'engineering_math_dataset.json',
        'calculus_problems.json',
        'linear_algebra_problems.json'
    ]
    
    for filename in json_files:
        filepath = processed_dir / filename
        if filepath.exists():
            print(f"Loading {filename}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
                print(f"  Added {len(data)} examples")
    
    # Save merged dataset
    output_path = processed_dir / 'merged_training_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nTotal examples: {len(all_data)}")
    print(f"Saved to: {output_path}")
    
    return all_data


if __name__ == '__main__':
    merge_datasets()
