import csv
import os

# ─────────────────────────────────────────
#  Data "structs" (plain dicts / dataclass)
# ─────────────────────────────────────────

# Mirrors the C++ Account struct
accounts = [
    {"name": "goil_manager",    "pass": "Manager@2024", "role": "Manager"},
    {"name": "goil_attendant",  "pass": "Attend@2024",  "role": "Attendant"},
    {"name": "goil_supervisor", "pass": "super@2024",   "role": "Supervisor"},
]

# Mirrors std::vector<Transaction>
transactions = []

DB_FILE = "fileDb.csv"


# ─────────────────────────────────────────
#  Helper: category logic  (same as C++)
# ─────────────────────────────────────────

def get_category(litres: int) -> str:
    """
    Mirrors the if/else in recordT():
      < 20      → Small Fill
      20 – 49   → Regular Fill
      50+       → Large Fill
    """
    if litres < 20:
        return "Small Fill"
    elif litres <= 49:
        return "Regular Fill"
    else:
        return "Large Fill"


# ─────────────────────────────────────────
#  CRUD-style functions  (mirror C++ fns)
# ─────────────────────────────────────────

def record_transaction():
    """Mirrors recordT() — prompts user and appends to the list."""
    vehicle_no      = input("Vehicle Number: ")
    fuel_type       = input("Fuel Type: ")
    litre_dispensed = int(input("Litres Dispensed: "))

    t = {
        "vehicle_no":      vehicle_no,
        "fuel_type":       fuel_type,
        "litre_dispensed": litre_dispensed,
        "category":        get_category(litre_dispensed),
    }
    transactions.append(t)
    print("Transaction recorded.\n")


def display_all():
    """Mirrors displayAll() — prints a formatted table."""
    if not transactions:
        print("No transactions recorded yet.\n")
        return

    header = f"{'Vehicle':<17}{'Fuel Type':<17}{'Litres':<17}{'Category':<17}"
    print("=" * 68)
    print(header)
    print("=" * 68)
    for t in transactions:
        row = (f"| {t['vehicle_no']:<15}"
               f"| {t['fuel_type']:<15}"
               f"| {t['litre_dispensed']:<15}"
               f"| {t['category']:<15}|")
        print(row)
    print("=" * 68)


def summary():
    """Mirrors summary() — totals and average."""
    if not transactions:
        print("No transactions to summarise.\n")
        return

    total    = len(transactions)
    t_litres = sum(t["litre_dispensed"] for t in transactions)
    average  = t_litres / total

    print(f"Total transactions recorded : {total}")
    print(f"Total litres dispensed      : {t_litres}")
    print(f"Average litres/transaction  : {average:.2f}\n")


def find_large_fills():
    """Mirrors findALFT() — shows only Large Fill transactions."""
    large = [t for t in transactions if t["category"] == "Large Fill"]

    if not large:
        print("No large fill transactions found.\n")
        return

    print("=" * 68)
    print(f"{'Vehicle':<17}{'Fuel Type':<17}{'Litres':<17}{'Category':<17}")
    print("=" * 68)
    for t in large:
        row = (f"| {t['vehicle_no']:<15}"
               f"| {t['fuel_type']:<15}"
               f"| {t['litre_dispensed']:<15}"
               f"| {t['category']:<15}|")
        print(row)
    print("=" * 68)


def save_to_file():
    """Mirrors saveToFile() — appends transactions to a CSV file."""
    with open(DB_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["vehicle_no", "fuel_type",
                                               "litre_dispensed", "category"])
        writer.writerows(transactions)
    print(f"Saved {len(transactions)} transaction(s) to {DB_FILE}.\n")


def read_from_file():
    """Mirrors readFromFile() — reads and prints the CSV file."""
    if not os.path.exists(DB_FILE):
        print("Database file not found.\n")
        return

    with open(DB_FILE, newline="") as f:
        for line in f:
            print(line.strip())
    print()


# ─────────────────────────────────────────
#  Login + Menu  (mirrors main())
# ─────────────────────────────────────────

def login_screen():
    print("+===================================+")
    print("||GOIL COMPANY LIMITED - FUEL LOGGER||")
    print("||   Tema Filling station, Ghana    ||")
    print("+===================================+")
    print("\nPlease log in to continue...\n")


def main_menu():
    print("\n+=================================+")
    print("|   MAIN MENU  -  FUEL LOGGER     |")
    print("+=================================+")
    print("|  1. Record a new transaction    |")
    print("|  2. View daily summary          |")
    print("|  3. Display all transactions    |")
    print("|  4. Find large fill transactions|")
    print("|  5. Save transactions to file   |")
    print("|  6. Load transactions from file |")
    print("|  0. Logout and Exit             |")
    print("+=================================+")


def main():
    proceed = True
    counter = 0

    while proceed:
        login_screen()
        name = input("Username: ")
        pwd  = input("Password: ")

        user = next((a for a in accounts
                     if a["name"] == name and a["pass"] == pwd), None)

        if user:
            counter = 0
            print(f"\nLogin successful! Welcome, {user['role']}")
            print("-" * 38 + "\n")

            logged_in = True
            while logged_in:
                main_menu()
                choice = input("\nEnter your choice: ").strip()

                if   choice == "1": record_transaction()
                elif choice == "2": summary()
                elif choice == "3": display_all()
                elif choice == "4": find_large_fills()
                elif choice == "5": save_to_file()
                elif choice == "6": read_from_file()
                elif choice == "0":
                    print("Fare Well")
                    logged_in = False
                else:
                    print("Invalid choice. Please enter a number from the menu.\n")
        else:
            counter += 1
            remaining = 3 - counter
            print(f"Invalid credentials. Attempts remaining: {remaining}")
            if counter == 3:
                print("You have exhausted your try count. Exiting.")
                proceed = False


if __name__ == "__main__":
    main()
