#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

// function prototypes
void loginScreen();
void mainMenu();
std::string getPass();
std::string getName();
int getChoice();

// Holds login credentials and role for a system user.
struct Account {
    std::string name{};
    std::string pass{};
    std::string role{};
};

// Represents a single fuel dispensing transaction.
struct Transaction {
    std::string vehicle_no{};
    std::string fuel_type{};
    int litre_dispensed{};
    std::string category{};
};

// Prompts the user for transaction details and saves it to the list.
// Automatically assigns a category based on litres dispensed:
//   < 20       → Small Fill
//   20 to 49   → Regular Fill
//   50+        → Large Fill
void recordT(std::vector<Transaction> &transactions) {

    Transaction t{};
    std::cout << "Vehicle Number: ";
    std::getline(std::cin, t.vehicle_no);

    std::cout << "Fuel type: ";
    std::getline(std::cin, t.fuel_type);

    std::cout << "litre_dispensed: ";
    std::cin >> t.litre_dispensed;
    std::cin.ignore();

    if (t.litre_dispensed < 20) {
        t.category = "Small Fill";
    } else if (t.litre_dispensed >= 20 && t.litre_dispensed <= 49) {
        t.category = "Regular Fill";
    } else if (t.litre_dispensed >= 50) {
        t.category = "Large Fill";
    }

    transactions.push_back(t);
}

// Displays total transactions, total litres dispensed, and average litres per
// transaction.
void summary(const std::vector<Transaction> &transactions) {

    int numOfTransactions{static_cast<int>(transactions.size())};
    int totalLitres{};
    double averageLitres{};

    for (int i{}; i < transactions.size(); i++) {
        totalLitres += transactions[i].litre_dispensed;
    }
    averageLitres = static_cast<double>(totalLitres) / numOfTransactions;

    std::cout << "Total Number of transactions recorded : " << numOfTransactions
              << '\n';
    std::cout << "Total Litres Dispensed : " << totalLitres << '\n';
    ;
    std::cout << "Average litres per transaction : " << averageLitres << '\n';
    ;
}

// Displays all recorded transactions in a formatted table.
void displayAll(const std::vector<Transaction> &transactions) {
    for (int i{}; i < transactions.size(); i++) {
        std::string_view v = transactions[i].vehicle_no;
        std::string_view ft = transactions[i].fuel_type;
        int ld = transactions[i].litre_dispensed;
        std::string_view c = transactions[i].category;
        std::cout << std::left << "| " << std::setw(15) << v << "| "
                  << std::setw(15) << ft << "| " << std::setw(15) << ld << "| "
                  << std::setw(15) << c << "|\n";
    }
}

// Saves all transactions to fileDb.txt in CSV format, overwriting any existing
// data.
int saveToFile(const std::vector<Transaction> &transactions) {

    std::ofstream inserting{"fileDb.txt", std::ios::app};
    if (!inserting) {
        std::cerr << "Couldn't connnect to the database\n";
        return 1;
    }
    for (int i{}; i < transactions.size(); i++) {
        inserting << transactions[i].vehicle_no << ","
                  << transactions[i].fuel_type << ","
                  << transactions[i].litre_dispensed << ","
                  << transactions[i].category << "\n";
    }
    return 0;
}

// Reads and prints all transaction records from fileDb.txt.
int readFromFile() {

    std::string out{};
    std::ifstream outputing{"fileDb.txt"};

    if (!outputing) {

        std::cerr << "Failed to read from DB\n";
        return 1;
    }
    while (std::getline(outputing, out)) {
        std::cout << out << '\n';
    }
    return 0;
}

// Finds and displays only transactions categorised as Large Fill (50+ litres).
void findALFT(const std::vector<Transaction> &transactions) {

    for (int i{}; i < transactions.size(); i++) {
        if (transactions[i].category == "Large Fill") {
            std::string_view v = transactions[i].vehicle_no;
            std::string_view ft = transactions[i].fuel_type;
            int ld = transactions[i].litre_dispensed;
            std::string_view c = transactions[i].category;
            std::cout << std::left << "| " << std::setw(15) << v << "| "
                      << std::setw(15) << ft << "| " << std::setw(15) << ld
                      << "| " << std::setw(15) << c << "|\n";
        }
    }
}

int main() {

    std::vector<Account> accounts{
        {"goil_manager", "Manager@2024", "Manager"},
        {"goil_attendant", "Attend@2024", "Attendant"},
        {"goil_supervisor", "super@2024", "Supervisor"}};

    std::vector<Transaction> transactions{};

    bool proceed{true};
    int counter{};

    while (proceed) {
        loginScreen();
        std::string name{getName()};
        std::string pass{getPass()};

        bool found{false};
        for (int i{}; i < accounts.size(); i++) {
            if (name == accounts[i].name && pass == accounts[i].pass) {
                std::cout << '\n';
                std::cout << "Login successful! Welcome, " << accounts[i].role
                          << '\n';
                std::cout << std::string(38, '-') << "\n";
                std::cout << '\n';
                found = true;
                break;
            }
        }
        if (found) {
            counter = 0;
            bool loggedIn{true};
            while (loggedIn) {
                mainMenu();
                int choice{getChoice()};
                switch (choice) {
                case 1:
                    recordT(transactions);
                    break;
                case 2:
                    summary(transactions);
                    break;
                case 3:
                    std::cout << std::string(68, '=') << "\n";
                    std::cout << std::left << "| " << std::setw(15) << "Vehicle"
                              << "| " << std::setw(15) << "FuelType"
                              << "| " << std::setw(15) << "Litres"
                              << "| " << std::setw(15) << "Category"
                              << "|\n";
                    std::cout << std::string(68, '=') << "\n";
                    displayAll(transactions);
                    std::cout << std::string(68, '=') << "\n";
                    break;
                case 4:
                    std::cout << std::string(68, '=') << "\n";
                    std::cout << std::left << "| " << std::setw(15) << "Vehicle"
                              << "| " << std::setw(15) << "FuelType"
                              << "| " << std::setw(15) << "Litres"
                              << "| " << std::setw(15) << "Category"
                              << "|\n";
                    std::cout << std::string(68, '=') << "\n";
                    findALFT(transactions);
                    std::cout << std::string(68, '=') << "\n";
                    break;
                case 5:
                    saveToFile(transactions);
                    break;
                case 6:
                    readFromFile();
                    break;
                case 0:
                    std::cout << "Fare Well\n";
                    loggedIn = false;
                    break;
                default:
                    std::cout << "Invalid choice. Please enter a number from "
                                 "the menu.\n";
                    break;
                }
            }
        } else {
            counter++;
            std::cout << "Invalid credentials. Attempts remaining: "
                      << (3 - counter) << "\n";
            if (counter == 3) {
                std::cout << "You have exhausted your try count. Exiting.\n";
                proceed = false;
            }
        }
    }
    return 0;
}

// Prompts the user to enter a menu choice and returns it.
int getChoice() {
    std::cout << '\n';
    std::cout << "Enter your choice: ";
    int c{};
    std::cin >> c;
    std::cin.ignore();
    std::cout << '\n';
    return c;
}

// Prompts the user to enter their password and returns it.
std::string getPass() {
    std::cout << "Password: ";
    std::string p{};
    std::getline(std::cin, p);
    return p;
}

// Prompts the user to enter their username and returns it.
std::string getName() {
    std::cout << "Username: ";
    std::string n{};
    std::getline(std::cin, n);
    return n;
}

// Displays the login screen banner.
void loginScreen() {
    std::cout << "+===================================+\n";
    std::cout << "||GOIL COMPANY LIMITED - FUEL LOGGER||\n";
    std::cout << "||   Tema Filling station, Ghana    ||\n";
    std::cout << "+===================================+\n";
    std::cout << '\n';
    std::cout << "Please log in to continue...\n";
    std::cout << '\n';
}

// Displays the main navigation menu.
void mainMenu() {
    std::cout << '\n';
    std::cout << "+=================================+\n";
    std::cout << "|   MAIN MENU  -  FUEL LOGGER     |\n";
    std::cout << "+=================================+\n";
    std::cout << "|  1. Record a new transaction    |\n";
    std::cout << "|  2. View daily summary          |\n";
    std::cout << "|  3. Display all transactions    |\n";
    std::cout << "|  4. Find large fill transactions|\n";
    std::cout << "|  5. Save transactions to file   |\n";
    std::cout << "|  6. Load transactions from file |\n";
    std::cout << "|  0. Logout and Exit             |\n";
    std::cout << "+=================================+\n";
}
