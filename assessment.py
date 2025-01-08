
import re
from collections import Counter
import psycopg2
import random
import statistics

# Extract Colors from HTML
with open('assessment.html', 'r') as file:
    content = file.read()

# Extract colors from <td> tags 
colors = re.findall(r'<td>(\w+)</td>', content)

# Question 1: Most Worn Color (Mode)
most_worn_color = Counter(colors).most_common(1)[0][0]
print("The most worn color is:", most_worn_color)

# Question 2: Median Color
sorted_colors = sorted(colors)
median_color = sorted_colors[len(sorted_colors) // 2]
print("The median color is:", median_color)

# Question 3: Mean Color (Fixed)
# Assign unique numeric values to each color
unique_colors = list(set(colors))
color_to_num = {color: idx for idx, color in enumerate(unique_colors)}
num_to_color = {idx: color for color, idx in color_to_num.items()}

# Convert colors to numbers for mean calculation
color_numbers = [color_to_num[color] for color in colors]
mean_color_number = round(statistics.mean(color_numbers))
mean_color = num_to_color[mean_color_number]

print("The Mean color is:", mean_color)

# Question 4: Variance of Colors
color_variance = statistics.variance(color_numbers)
print("Variance of colors:", color_variance)

# Question 5: Probability of Red
red_probability = colors.count('Red') / len(colors)
print("Probability of selecting Red:", red_probability)

# Question 6: Save Colors & Frequencies to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="color_data",
        user="postgres",
        password="stephanie",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS colors (
            color TEXT PRIMARY KEY,
            frequency INTEGER
        )
    """)

    # Insert color frequencies
    color_frequencies = Counter(colors)
    for color, frequency in color_frequencies.items():
        cur.execute(
            "INSERT INTO colors (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency",
            (color, frequency)
        )

    conn.commit()
    print("Color data saved to database successfully.")

except Exception as e:
    print("Database Error:", e)

finally:
    if 'conn' in locals():
        cur.close()
        conn.close()

# Question 7: Recursive Search Algorithm
def recursive_search(lst, target, index=0):
    """Recursive function to search for a target in a list."""
    if index >= len(lst):
        return -1  # Not found
    if lst[index] == target:
        return index
    return recursive_search(lst, target, index + 1)

numbers = [1, 2, 3, 4, 5]
target = int(input("Enter a number to search: "))
result = recursive_search(numbers, target)

if result != -1:
    print(f"Number {target} found at index {result}")
else:
    print(f"Number {target} not found in the list.")

# Question 8: Generate 4-digit Binary Number and Convert to Decimal
binary_number = ''.join(random.choice('01') for _ in range(4))
decimal_number = int(binary_number, 2)

print("Binary number:", binary_number)
print("Decimal equivalent:", decimal_number)

# Question 9: Sum of First 50 Fibonacci Numbers (Optimized)
def fibonacci_sum(n):
    """Function to sum the first n Fibonacci numbers using iteration."""
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_sum = fibonacci_sum(50)
print("Sum of first 50 Fibonacci numbers:", fib_sum)



