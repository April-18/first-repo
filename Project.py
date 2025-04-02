import sqlite3

# Constants for costs
COMPETITION_COST = 50.00  # Cost per competition
PRIVATE_COACHING_COST = 30.00  # Cost per hour of private coaching
MAX_PRIVATE_COACHING_HOURS = 5  # Max hours per week

# Connect to SQLite database (or create it)
conn = sqlite3.connect('martial_arts.db')
c = conn.cursor()

# Create table for athletes
c.execute('''
CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    martial_art TEXT,
    current_weight REAL,
    competition_weight REAL,
    competitions_entered INTEGER,
    private_coaching_hours INTEGER
)
''')
conn.commit()

def add_athlete():
    name = input("Enter athlete's name: ")
    martial_art = input("Enter martial arts studied (Judo, Jiu-Jitsu, Karate): ")
    current_weight = float(input("Enter current weight in kg: "))
    competition_weight = float(input("Enter competition weight category in kg: "))
    competitions_entered = int(input("Enter number of competitions entered this month: "))
    private_coaching_hours = int(input("Enter number of hours of private coaching (max 5): "))

    # Validate private coaching hours
    if private_coaching_hours < 0 or private_coaching_hours > MAX_PRIVATE_COACHING_HOURS:
        print("Invalid number of private coaching hours. Must be between 0 and 5.")
        return

    # Insert athlete data into the database
    c.execute('''
    INSERT INTO athletes (name, martial_art, current_weight, competition_weight, competitions_entered, private_coaching_hours)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, martial_art, current_weight, competition_weight, competitions_entered, private_coaching_hours))
    conn.commit()

    # Calculate costs
    calculate_costs(name, current_weight, competition_weight, competitions_entered, private_coaching_hours)

def calculate_costs(name, current_weight, competition_weight, competitions_entered, private_coaching_hours):
    # Calculate costs
    competition_cost = competitions_entered * COMPETITION_COST
    private_coaching_cost = private_coaching_hours * PRIVATE_COACHING_COST
    total_cost = competition_cost + private_coaching_cost

    # Weight comparison
    weight_comparison = "within" if current_weight <= competition_weight else "over"

    # Output results
    print(f"\nAthlete's Name: {name}")
    print("Itemized Costs:")
    print(f" - Competition Cost: ${competition_cost:.2f}")
    print(f" - Private Coaching Cost: ${private_coaching_cost:.2f}")
    print(f"Total Cost of Training and Competitions: ${total_cost:.2f}")
    print(f"The athlete's current weight is {weight_comparison} the competition weight category.")

def main():
    while True:
        print("\nMartial Arts Training Cost Calculator")
        print("1. Add Athlete")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_athlete()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()