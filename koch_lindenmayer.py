import sys

def generate_fractal(num_iterations):
    primitive = "F+F--F+F"
    result = "F"

    for _ in range(num_iterations):
        new_result = []
        for char in result:
            if char == "F":
                new_result.append(primitive)
            else:
                new_result.append(char)
        result = "".join(new_result)

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 coach_lindermayer.py <num_iterations>")
        sys.exit(1)

    try:
        num_iterations = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer for the number of iterations.")
        sys.exit(1)

    fractal = generate_fractal(num_iterations)
    print(fractal)

if __name__ == "__main__":
    main()
