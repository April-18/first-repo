import sqlite3

connection = sqlite3.connect("athletes.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    martial_arts TEXT,
    weight REAL,
    comp_category TEXT,
    competitions INTEGER,
    private_hours INTEGER
)
""")
connection.commit()

#error handling

def get_input(prompt, data_type, min_value=None, max_value=None):
    while True:
        try:
            value = data_type(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}. Try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please try again.")

# weight category

def get_weight_category(weight):
    if weight > 100:
        return "heavyweight"
    elif weight > 90:
        return "half-heavyweight"
    elif weight > 81:
        return "middleweight"
    elif weight > 73:
        return "half-middleweight"
    elif weight > 66:
        return "lightweight"
    else:
        return "half-lightweight"

# Calculate fees

def calculate_costs(martial_arts_count, competitions, private_hours):
    # Monthly fee based on number of martial arts
    if martial_arts_count == 1:
        monthly_fee = 25.00
    elif martial_arts_count == 2:
        monthly_fee = 30.00
    else:
        monthly_fee = 35.00

    # Competition fee: $22.00 each
    comp_fee = competitions * 22.00

    # Private coaching: assume 4 weeks in a month
    private_fee = private_hours * 9.50 * 4

    total = monthly_fee + comp_fee + private_fee
    return monthly_fee, comp_fee, private_fee, total




print("\nWelcome to the Athlete Training System!\n")

# 1. Get athlete's name
name = input("Enter athlete's name: ")

# 2. Martial arts selection
martial_arts = []
arts_list = ["Judo", "Jiu-Jitsu", "Karate"]

print("\nChoose martial arts studied:")
for art in arts_list:
    choice = input(f"Does the athlete study {art}? (yes/no): ").strip().lower()
    if choice == 'yes':
        martial_arts.append(art)

if len(martial_arts) == 0:
    print("At least one martial art must be selected. Exiting...")
    exit()

# 3. Get current weight
weight = get_input("Enter current weight in kg: ", float, min_value=1)

# 4. Get competition category
comp_category = input("Enter competition weight category: ")

# 5. Competitions this month
competitions = get_input("Number of competitions this month: ", int, min_value=0)

# 6. Private coaching hours (limit to 0–5)
private_hours = get_input("Private coaching hours per week (0-5): ", int, 0, 5)

# 7. Store in database
cursor.execute('''
INSERT INTO athletes (name, martial_arts, weight, comp_category, competitions, private_hours)
VALUES (?, ?, ?, ?, ?, ?)
''', (name, ", ".join(martial_arts), weight, comp_category, competitions, private_hours))
connection.commit()

# 8. Calculate all costs
monthly_fee, comp_fee, private_fee, total_cost = calculate_costs(len(martial_arts), competitions, private_hours)

# 9. Determine actual weight category
actual_category = get_weight_category(weight)

# Output

print("\n----- Athlete Summary -----")
print(f"Name: {name}")
print(f"Martial Arts Studied: {', '.join(martial_arts)}")
print(f"Current Weight: {weight:.2f} kg")
print(f"Weight Category (based on weight): {actual_category}")
print(f"Competition Category Entered: {comp_category}")

print("\n----- Cost Breakdown -----")
print(f"Monthly Training Fee: ${monthly_fee:.2f}")
print(f"Competition Fees:     ${comp_fee:.2f}")
print(f"Private Coaching:     ${private_fee:.2f}")
print(f"Total Monthly Cost:   ${total_cost:.2f}")


connection.close()
