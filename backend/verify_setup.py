"""
Environment verification script.
Run this to check if all required environment variables and dependencies are configured.
"""

import sys
from pathlib import Path

def check_backend_setup():
    """Check backend environment setup."""
    print("🔍 Checking Backend Setup...\n")
    
    issues = []
    
    # Check Python version
    print("✓ Python version:", sys.version.split()[0])
    
    # Check if virtual environment is active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment: Active")
    else:
        print("⚠️  Virtual environment: Not active (recommended to activate)")
        issues.append("Virtual environment not activated")
    
    # Check dependencies
    print("\n📦 Checking Dependencies...")
    required_packages = [
        'crewai',
        'firecrawl',
        'supabase',
        'dotenv',
        'pydantic',
        'pypdf',
        'playwright',
        'thefuzz',
        'openai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        issues.append(f"Missing packages: {', '.join(missing_packages)}")
    
    # Check environment variables
    print("\n🔑 Checking Environment Variables...")
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_SERVICE_KEY',
            'OPENAI_API_KEY',
        ]
        
        optional_vars = ['FIRECRAWL_API_KEY']
        
        for var in required_vars:
            if os.getenv(var):
                print(f"  ✓ {var}")
            else:
                print(f"  ✗ {var} - NOT SET")
                issues.append(f"{var} not set in .env file")
        
        for var in optional_vars:
            if os.getenv(var):
                print(f"  ✓ {var} (optional)")
            else:
                print(f"  ⚠️  {var} - NOT SET (optional but recommended)")
    
    except Exception as e:
        print(f"  ✗ Error checking environment: {e}")
        issues.append("Error reading .env file")
    
    # Check file structure
    print("\n📁 Checking File Structure...")
    backend_path = Path(__file__).parent
    
    required_files = [
        'models.py',
        'utils.py',
        'main.py',
        'requirements.txt',
        'config/settings.py',
        'tools/dsp_verification.py',
        'tools/firecrawl_extractor.py',
        'tools/llm_extractor.py',
        'tools/supabase_tool.py',
        'data/seed_urls.json'
    ]
    
    for file in required_files:
        file_path = backend_path / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NOT FOUND")
            issues.append(f"Missing file: {file}")
    
    # Check DSP PDF (optional)
    dsp_path = backend_path / 'data' / 'dsp_authorized_list.pdf'
    if dsp_path.exists():
        print(f"  ✓ data/dsp_authorized_list.pdf (optional)")
    else:
        print(f"  ⚠️  data/dsp_authorized_list.pdf - NOT FOUND (optional, verification will be limited)")
    
    # Summary
    print("\n" + "="*50)
    if not issues:
        print("✅ All checks passed! Backend is ready to run.")
        print("\nRun the scraper with: python main.py")
        return True
    else:
        print("❌ Setup incomplete. Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print("\nPlease fix the issues above and run this script again.")
        return False


def check_frontend_setup():
    """Check frontend environment setup."""
    print("\n" + "="*50)
    print("🔍 Checking Frontend Setup...\n")
    
    issues = []
    frontend_path = Path(__file__).parent.parent / 'frontend'
    
    if not frontend_path.exists():
        print("✗ Frontend directory not found")
        return False
    
    # Check if package.json exists
    package_json = frontend_path / 'package.json'
    if package_json.exists():
        print("✓ package.json found")
    else:
        print("✗ package.json not found")
        issues.append("Frontend not initialized")
    
    # Check node_modules
    node_modules = frontend_path / 'node_modules'
    if node_modules.exists():
        print("✓ node_modules installed")
    else:
        print("⚠️  node_modules not found (run 'npm install')")
        issues.append("Dependencies not installed")
    
    # Check environment file
    env_file = frontend_path / '.env.local'
    if env_file.exists():
        print("✓ .env.local configured")
    else:
        print("⚠️  .env.local not found (copy from .env.example)")
        issues.append(".env.local not configured")
    
    # Check key files
    required_files = [
        'src/lib/supabase.ts',
        'src/types/index.ts',
        'src/lib/utils.ts',
    ]
    
    print("\n📁 Checking File Structure...")
    for file in required_files:
        file_path = frontend_path / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NOT FOUND")
            issues.append(f"Missing file: {file}")
    
    # Summary
    print("\n" + "="*50)
    if not issues:
        print("✅ Frontend checks passed!")
        print("\nStart development server with: npm run dev")
        return True
    else:
        print("❌ Frontend setup incomplete. Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Funeral Directory Setup Verification")
    print("=" * 50)
    
    backend_ok = check_backend_setup()
    frontend_ok = check_frontend_setup()
    
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    print(f"Backend:  {'✅ Ready' if backend_ok else '❌ Needs attention'}")
    print(f"Frontend: {'✅ Ready' if frontend_ok else '❌ Needs attention'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Everything is set up correctly!")
        print("\nNext steps:")
        print("1. Add seed URLs to backend/data/seed_urls.json")
        print("2. Run backend scraper: cd backend && python main.py")
        print("3. Start frontend: cd frontend && npm run dev")
    else:
        print("\n📖 Refer to SETUP.md for detailed instructions")
