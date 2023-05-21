import math

# Count the total number of operators and operands
total_operators = 0
total_operands = 0

# Set to keep track of unique operators and operands
unique_operators = set()
unique_operands = set()

with open('app.py', 'r') as file:
    for line in file:
        # Count operators
        operators = line.count('=') + line.count('>') + line.count('<') + line.count('+') + line.count('-') + \
                    line.count('*') + line.count('/') + line.count('%') + line.count('==') + line.count('!=') + \
                    line.count('>=') + line.count('<=') + line.count('and') + line.count('or') + line.count('not') + \
                    line.count('in') + line.count('is')
        total_operators += operators

        # Count operands
        words = line.split()
        for word in words:
            if word.isidentifier():
                unique_operands.add(word)
                total_operands += 1

        # Count unique operators
        unique_operators.add(operators)

# Calculate program length and vocabulary
program_length = total_operators + total_operands
vocabulary = len(unique_operators) + len(unique_operands)

# Calculate Halstead's volume
volume = program_length * math.log2(vocabulary)

print("Halstead's Volume:", volume)
