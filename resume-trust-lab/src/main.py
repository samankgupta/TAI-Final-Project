"""Main entry point."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from evaluation.experiment_runner import ExperimentRunner
from loader import DataLoader


def main():
    """Interactive main menu."""
    
    print("\n" + "="*70)
    print("RESUME TRUST LAB SYSTEM")
    print("Multi-stage AI Resume Screening & Trust Evaluation")
    print("="*70)
    
    print("\nAvailable roles:")
    loader = DataLoader()
    try:
        loader.load_dataset(sample_size=5000)
        stats = loader.get_role_statistics()
        for i, (role, count) in enumerate(sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10], 1):
            print(f"  {i}. {role}: {count}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "-"*70)
    role = input("\nEnter role (default: E-commerce Specialist): ").strip()
    if not role:
        role = "E-commerce Specialist"
    
    sample_input = input("Number of resumes (default: 1000): ").strip()
    sample_size = int(sample_input) if sample_input else 1000
    
    print("\nSelect stages (1,2,3,4,5 or A for all):")
    stages_input = input("Enter: ").strip().upper()
    
    if stages_input == 'A':
        stages = [1, 2, 3, 4, 5]
    else:
        try:
            stages = [int(s.strip()) for s in stages_input.split(',')]
        except:
            stages = [1, 2, 3, 4, 5]
    
    print("\n" + "="*70 + "\nSTARTING EXPERIMENT\n" + "="*70)
    
    runner = ExperimentRunner(sample_size=sample_size)
    try:
        runner.run_all(role, stages=stages)
        runner.compute_metrics()
        
        print("\n" + "="*70)
        print("EXPERIMENT COMPLETE - Results in outputs/")
        print("="*70)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
