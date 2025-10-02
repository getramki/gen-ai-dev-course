#!/usr/bin/env python3
"""
Master Setup Script for Bedrock Security Exercises
This script runs all three exercises in sequence to set up complete security framework.
"""

import sys
import os
import subprocess
from pathlib import Path

def run_exercise(exercise_dir, script_name):
    """Run a specific exercise script"""
    script_path = Path(exercise_dir) / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        print(f"\n🚀 Running {script_name}...")
        result = subprocess.run([sys.executable, str(script_path)], 
                              cwd=exercise_dir, 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
            print(result.stdout)
            return True
        else:
            print(f"❌ {script_name} failed")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    """Run all security exercises in sequence"""
    print("🛡️ Bedrock Security Framework Setup")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    
    exercises = [
        {
            'name': 'Exercise 1: IAM Security Setup',
            'dir': base_dir / 'exercise-1-iam-security',
            'script': 'setup_iam.py'
        },
        {
            'name': 'Exercise 2: Guardrails Setup',
            'dir': base_dir / 'exercise-2-content-filtering',
            'script': 'setup_guardrails.py'
        },
        {
            'name': 'Exercise 3: CloudTrail Setup',
            'dir': base_dir / 'exercise-3-monitoring-compliance',
            'script': 'cloudtrail_setup.py'
        },
        {
            'name': 'Exercise 3: Monitoring Setup',
            'dir': base_dir / 'exercise-3-monitoring-compliance',
            'script': 'monitoring_dashboard.py'
        }
    ]
    
    results = []
    
    for exercise in exercises:
        print(f"\n📋 {exercise['name']}")
        print("-" * 40)
        
        success = run_exercise(exercise['dir'], exercise['script'])
        results.append({
            'name': exercise['name'],
            'success': success
        })
        
        if not success:
            print(f"⚠️  {exercise['name']} failed. You may need to run it manually.")
    
    # Summary
    print("\n📊 Setup Summary")
    print("=" * 50)
    
    for result in results:
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        print(f"{result['name']}: {status}")
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"\nCompleted: {successful}/{total} exercises")
    
    if successful == total:
        print("\n🎉 All exercises completed successfully!")
        print("Your Bedrock security framework is now set up.")
        print("\nNext steps:")
        print("1. Test the IAM roles and policies")
        print("2. Configure guardrails for your specific use case")
        print("3. Set up monitoring alerts and notifications")
        print("4. Review compliance reports regularly")
    else:
        print("\n⚠️  Some exercises failed. Please check the error messages above.")
        print("You may need to:")
        print("1. Verify AWS credentials and permissions")
        print("2. Check region availability for Bedrock services")
        print("3. Ensure required AWS services are enabled")

if __name__ == "__main__":
    main()