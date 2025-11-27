#!/usr/bin/env python
"""
Azure App Service startup script for Django application.
This script handles initialization tasks before starting the Django server.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main startup function for Azure App Service"""
    
    # Set up environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hair_project.settings')
    
    # Add the project directory to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    print("🚀 Starting Azure App Service initialization...")
    
    try:
        # Import Django and check if it's working
        import django
        django.setup()
        print("✅ Django imported successfully")
        
        # Run migrations
        print("📊 Running database migrations...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate', '--noinput'
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully")
        else:
            print(f"⚠️ Migration warnings: {result.stderr}")
        
        # Collect static files
        print("📁 Collecting static files...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Static files collected successfully")
        else:
            print(f"⚠️ Static files warning: {result.stderr}")
            
        # Test ML dependencies
        print("🧠 Testing ML dependencies...")
        try:
            import torch
            import transformers
            import cv2
            import numpy as np
            from PIL import Image
            print("✅ All ML dependencies available")
        except ImportError as e:
            print(f"❌ ML dependency missing: {e}")
            
        print("🎉 Initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
