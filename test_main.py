import sys
import ast

def check_syntax(filepath):
    """Kiểm tra syntax của file Python"""
    try:
        with open(filepath, 'r') as file:
            source = file.read()
        
        # Compile để kiểm tra syntax
        ast.parse(source)
        print(f"✓ {filepath}: Syntax OK")
        return True
        
    except SyntaxError as e:
        print(f"✗ {filepath}: Syntax Error - {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"✗ {filepath}: Error - {e}")
        return False

def check_imports(filepath):
    """Kiểm tra imports có thể load được không"""
    try:
        # Tạm thời thêm path hiện tại
        sys.path.insert(0, '/Users/phidinh/Intrusion_Warning')
        
        # Test import
        import main
        print(f"✓ {filepath}: Imports OK")
        return True
        
    except ImportError as e:
        print(f"✗ {filepath}: Import Error - {e}")
        return False
    except Exception as e:
        print(f"✗ {filepath}: Error - {e}")
        return False

if __name__ == "__main__":
    files_to_check = [
        "main.py",
        "database_config.py", 
        "yolodetect.py"
    ]
    
    print("Checking Python files...")
    print("=" * 50)
    
    all_good = True
    for file in files_to_check:
        syntax_ok = check_syntax(file)
        if not syntax_ok:
            all_good = False
    
    print("\nChecking imports...")
    print("=" * 50)
    
    if all_good:
        import_ok = check_imports("main.py")
        if import_ok:
            print("\n✓ All checks passed! main.py should work correctly.")
        else:
            print("\n✗ Import issues found.")
    else:
        print("\n✗ Syntax errors found. Fix them first.")
