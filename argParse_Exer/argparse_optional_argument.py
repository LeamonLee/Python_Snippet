import argparse

if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="my math script"
    )

    # Add the parameters positional/optional
    parser.add_argument('-n','--num1', help="Number 1", type=float)
    parser.add_argument('-i','--num2', help="Number 2", type=float)
    parser.add_argument('-o','--operation', help="provide operator", default='+')

    # Parse the arguments
    args = parser.parse_args()
    print(args)
    result = None
    if args.operation == '+':
        result = args.num1 + args.num2
    if args.operation == '-':
        result = args.num1 - args.num2
    if args.operation == '*':
        result = args.num1 * args.num2
    if args.operation == 'pow':
        result = pow(args.num1, args.num2)

    print("Result : ", result)

# Run script with following command
#python argparse_optional_argument.py -n=84 -i=70 -o=+
#--------------------OR-----------------
#python argparse_optional_argument.py --num1 80 --num2 45 --operation -