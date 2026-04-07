"""
Check Python syntax without importing TensorFlow
"""

import py_compile
import sys
from pathlib import Path


def check_file(filepath):
    """Check if a Python file has valid syntax"""
    try:
        py_compile.compile(filepath, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)


def main():
    """Check all Python files for syntax errors"""
    
    files_to_check = [
        'training/model.py',
        'training/data_pipeline.py',
        'training/train_model.py',
        'training/inference.py',
        'training/config.py',
        'training/test_model.py',
        'training/test_enhanced_model.py',
        'api/app.py',
        'data/merge_datasets.py',
        'example_usage.py',
        'verify_structure.py'
    ]
    
    print("="*60)
    print("SYNTAX CHECK")
    print("="*60 + "\n")
    
    all_valid = True
    
    for filepath in files_to_check:
        path = Path(filepath)
        if path.exists():
            valid, error = check_file(filepath)
            if valid:
                print(f"✓ {filepath}")
            else:
                print(f"✗ {filepath}")
                print(f"  Error: {error}")
                all_valid = False
        else:
            print(f"⚠ {filepath} (not found)")
    
    print("\n" + "="*60)
    if all_valid:
        print("✅ ALL FILES HAVE VALID SYNTAX")
    else:
        print("✗ SOME FILES HAVE SYNTAX ERRORS")
    print("="*60 + "\n")
    
    return 0 if all_valid else 1


if __name__ == '__main__':
    sys.exit(main())
