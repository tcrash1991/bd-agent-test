from functions.run_python import run_python_file

def main():
    # Test 1: Run calculator with no args (should show usage)
    print("run_python_file(\"calculator\", \"main.py\"):")
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    print()
    
    # Test 2: Run calculator with args (should calculate 3 + 5)
    print("run_python_file(\"calculator\", \"main.py\", [\"3 + 5\"]):")
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result2)
    print()
    
    # Test 3: Run tests
    print("run_python_file(\"calculator\", \"tests.py\"):")
    result3 = run_python_file("calculator", "tests.py")
    print(result3)
    print()
    
    # Test 4: Try to run file outside working directory (should error)
    print("run_python_file(\"calculator\", \"../main.py\"):")
    result4 = run_python_file("calculator", "../main.py")
    print(result4)
    print()
    
    # Test 5: Try to run non-existent file (should error)
    print("run_python_file(\"calculator\", \"nonexistent.py\"):")
    result5 = run_python_file("calculator", "nonexistent.py")
    print(result5)

if __name__ == "__main__":
    main()