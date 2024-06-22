import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 coach_lindermayer.py <num_iterations>")
        sys.exit(1)
    
    try:
        num_iterations = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer for the number of iterations.")
        sys.exit(1)

    # Define the axiom and rule
    axiom = "F"
    rule = "F+F--F+F"
    result = axiom

    # Apply the rule for the specified number of iterations
    for i in range(num_iterations):
        result = result.replace("F", rule)

    print(result)

if __name__ == "__main__":
    main()
