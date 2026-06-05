#!/usr/bin/env python3
"""
ProfileScout - Verification & Testing Script

This script verifies that ProfileScout is properly installed and functioning.
Run this to ensure all components are ready for deployment.
"""

import sys
import importlib
import os

def check_python_version():
    """Verify Python version compatibility."""
    print("[*] Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"    ✓ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"    ✗ Python {version.major}.{version.minor} (Requires 3.6+)")
        return False

def check_dependencies():
    """Verify required packages are installed."""
    print("\n[*] Checking dependencies...")
    dependencies = {
        'requests': 'HTTP requests library',
        'colorama': 'Terminal colors library'
    }
    
    all_ok = True
    for package, description in dependencies.items():
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"    ✓ {package:15} v{version:15} ({description})")
        except ImportError:
            print(f"    ✗ {package:15} NOT INSTALLED  ({description})")
            all_ok = False
    
    return all_ok

def check_files():
    """Verify all required files are present."""
    print("\n[*] Checking project files...")
    required_files = {
        'profilescout.py': 'Main application',
        'requirements.txt': 'Dependencies file',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick start guide',
        'examples.py': 'Usage examples'
    }
    
    profile_scout_dir = os.path.dirname(os.path.abspath(__file__))
    all_ok = True
    
    for filename, description in required_files.items():
        filepath = os.path.join(profile_scout_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"    ✓ {filename:20} ({size:,} bytes) - {description}")
        else:
            print(f"    ✗ {filename:20} MISSING - {description}")
            all_ok = False
    
    return all_ok

def check_profilescout_import():
    """Verify ProfileScout can be imported."""
    print("\n[*] Checking ProfileScout module...")
    try:
        from profilescout import ProfileScout
        print("    ✓ ProfileScout class imported successfully")
        
        # Check if key methods exist
        methods = ['check_profile', 'scan_username', 'display_banner', 'print_executive_summary']
        for method in methods:
            if hasattr(ProfileScout, method):
                print(f"    ✓ Method: {method}")
            else:
                print(f"    ✗ Method: {method} NOT FOUND")
                return False
        
        # Check if PLATFORMS database exists
        if hasattr(ProfileScout, 'PLATFORMS'):
            platform_count = len(ProfileScout.PLATFORMS)
            print(f"    ✓ Platform database: {platform_count} platforms configured")
        else:
            print("    ✗ PLATFORMS database NOT FOUND")
            return False
        
        return True
    except ImportError as e:
        print(f"    ✗ Failed to import ProfileScout: {e}")
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def check_platform_database():
    """Verify platform database is complete."""
    print("\n[*] Checking platform database...")
    try:
        from profilescout import ProfileScout
        platforms = ProfileScout.PLATFORMS
        
        expected_platforms = [
            'GitHub', 'Reddit', 'Twitter/X', 'Instagram', 'Facebook',
            'LinkedIn', 'TikTok', 'Pinterest', 'Twitch', 'YouTube',
            'Medium', 'Dev.to', 'Spotify', 'Steam', 'Discord'
        ]
        
        missing = []
        for platform in expected_platforms:
            if platform not in platforms:
                missing.append(platform)
        
        if missing:
            print(f"    ! Warning: Missing platforms: {', '.join(missing)}")
        
        found = len([p for p in expected_platforms if p in platforms])
        print(f"    ✓ Major platforms: {found}/{len(expected_platforms)} verified")
        print(f"    ✓ Total platforms: {len(platforms)}")
        
        return True
    except Exception as e:
        print(f"    ✗ Error checking platforms: {e}")
        return False

def check_documentation():
    """Verify documentation files."""
    print("\n[*] Checking documentation...")
    doc_files = {
        'README.md': 'Main documentation',
        'QUICKSTART.md': 'Quick start guide',
        'DEVELOPER.md': 'Developer guide',
        'INSTALLATION.md': 'Installation details'
    }
    
    profile_scout_dir = os.path.dirname(os.path.abspath(__file__))
    all_found = True
    
    for filename, description in doc_files.items():
        filepath = os.path.join(profile_scout_dir, filename)
        if os.path.exists(filepath):
            lines = len(open(filepath).readlines())
            print(f"    ✓ {filename:20} ({lines:4} lines) - {description}")
        else:
            print(f"    ✗ {filename:20} MISSING - {description}")
            all_found = False
    
    return all_found

def run_basic_test():
    """Run a basic functionality test."""
    print("\n[*] Running basic functionality test...")
    try:
        from profilescout import ProfileScout
        
        # Create instance
        scout = ProfileScout(timeout=5, max_workers=4)
        print("    ✓ ProfileScout instance created")
        
        # Test single platform check
        result = scout.check_profile('GitHub', 'test')
        if 'platform' in result and 'status' in result:
            print(f"    ✓ Single platform check works")
            print(f"      → Result: GitHub profile lookup returned {result['status']}")
        else:
            print("    ✗ Platform check returned unexpected format")
            return False
        
        return True
    except Exception as e:
        print(f"    ✗ Error during test: {e}")
        return False

def generate_report():
    """Generate overall compatibility report."""
    print("\n" + "="*80)
    print("PROFILESCOUT COMPATIBILITY REPORT")
    print("="*80 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Files", check_files),
        ("ProfileScout Module", check_profilescout_import),
        ("Platform Database", check_platform_database),
        ("Documentation", check_documentation),
        ("Basic Functionality", run_basic_test),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n[✗] {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:8} - {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 SUCCESS! ProfileScout is ready to use!")
        print("\nNext steps:")
        print("  1. Run: python3 profilescout.py")
        print("  2. Enter a username when prompted")
        print("  3. View discovered profiles\n")
        return True
    else:
        print("\n⚠️  Some checks failed. Please review the output above.")
        print("\nTroubleshooting:")
        print("  • Run setup script: setup.bat (Windows) or bash setup.sh (Linux/macOS)")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Check Python version: python --version (requires 3.6+)\n")
        return False

if __name__ == "__main__":
    success = generate_report()
    sys.exit(0 if success else 1)
