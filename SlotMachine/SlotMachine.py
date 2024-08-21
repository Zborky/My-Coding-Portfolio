import tkinter as tk
from tkinter import messagebox
import random
from tkinter import simpledialog


# Constants
MAX_LINES = 3  # Maximum number of lines to bet on
MAX_BET = 1000  # Maximum bet per line
MIN_BET = 1  # Minimum bet per line
ROWS = 3  # Number of rows in the slot machine grid
COLS = 3  # Number of columns in the slot machine grid

# Symbol distribution on the reels
symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}
# Symbol value when winning
symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}

class SlotMachineApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Slot Machine")  # Title of the window

        # Initial balance setup
        self.balance = self.prompt_initial_deposit()  # Ask the user for an initial deposit amount

        # Top frame to display the balance
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        # Frame for the slot machine grid (3x3 grid)
        self.slot_frame = tk.Frame(root)
        self.slot_frame.pack()

        # Frame for control buttons and inputs (bet, lines, spin)
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        # Label to display the current balance
        self.balance_label = tk.Label(self.top_frame, text=f"Balance: ${self.balance}", font=('Arial', 12))
        self.balance_label.pack()

        # Creating the slot machine grid (3x3) using labels
        self.slot_labels = [[tk.Label(self.slot_frame, text=" ", font=('Arial', 24), width=4, height=2, relief="groove") for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].grid(row=r, column=c)

        # Label and entry for the bet per line
        self.bet_label = tk.Label(self.control_frame, text="Bet per line: $", font=('Arial', 12))
        self.bet_label.grid(row=0, column=0)

        self.bet_entry = tk.Entry(self.control_frame, width=5)
        self.bet_entry.grid(row=0, column=1)

        # Label and entry for the number of lines to bet on
        self.lines_label = tk.Label(self.control_frame, text="Number of lines: ", font=('Arial', 12))
        self.lines_label.grid(row=0, column=2)

        self.lines_entry = tk.Entry(self.control_frame, width=5)
        self.lines_entry.grid(row=0, column=3)

        # Spin button to start the game
        self.spin_button = tk.Button(self.control_frame, text="Spin", command=self.spin)
        self.spin_button.grid(row=0, column=4, padx=10)

        # Deposit button to add money to the balance
        self.deposit_button = tk.Button(self.control_frame, text="Deposit", command=self.deposit)
        self.deposit_button.grid(row=0, column=5, padx=10)

    def prompt_initial_deposit(self):
        """
        Function to prompt the user for an initial deposit when the game starts.
        
        Returns:
            int: The initial deposit amount to start the game with.
        """
        while True:
            deposit_amount = tk.simpledialog.askinteger("Initial Deposit", "Enter initial deposit amount:")
            if deposit_amount is not None and deposit_amount > 0:
                return deposit_amount  # Return the valid deposit amount
            else:
                messagebox.showerror("Invalid Deposit", "Please enter a valid deposit amount.")

    def deposit(self):
        """
        Function to handle deposit action. It prompts the user to input a deposit amount,
        adds it to the balance, and updates the balance display.
        """
        deposit_amount = tk.simpledialog.askinteger("Deposit", "Enter deposit amount:")
        if deposit_amount and deposit_amount > 0:
            self.balance += deposit_amount  # Add deposit to balance
            self.update_balance()  # Update the displayed balance
        else:
            messagebox.showerror("Invalid Deposit", "Please enter a valid deposit amount.")

    def update_balance(self):
        """
        Function to update the balance label with the current balance.
        """
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def get_slot_machine_spin(self):
        """
        Function to generate a random spin result for the slot machine.
        
        Returns:
            list: A list of columns, each being a list of symbols representing a vertical strip of the slot machine.
        """
        all_symbols = []
        for symbol, count in symbol_count.items():
            all_symbols.extend([symbol] * count)  # Create a list with the symbols repeated according to their count

        columns = []
        for _ in range(COLS):
            column = random.sample(all_symbols, ROWS)  # Randomly select ROWS number of symbols for each column
            columns.append(column)

        return columns

    def display_slots(self, slots):
        """
        Function to display the slot machine's symbols on the grid.
        
        Parameters:
            slots (list): The current spin result of the slot machine.
        """
        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].config(text=slots[c][r])

    def check_winnings(self, columns, lines, bet):
        """
        Function to check if the spin resulted in any winning lines.
        
        Parameters:
            columns (list): The current spin result (columns of symbols).
            lines (int): The number of lines the player has bet on.
            bet (int): The amount of money bet per line.
        
        Returns:
            tuple: Total winnings and the list of winning lines.
        """
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                if column[line] != symbol:
                    break
            else:
                winnings += symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines

    def spin(self):
        """
        Function to handle the spin action. It checks the user's bet, generates a spin result,
        checks for winnings, and updates the balance accordingly.
        """
        try:
            bet = int(self.bet_entry.get())  # Get bet amount from input
            lines = int(self.lines_entry.get())  # Get number of lines from input
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid bet and line numbers.")
            return

        # Check if the bet is within allowed limits
        if bet < MIN_BET or bet > MAX_BET:
            messagebox.showerror("Invalid Bet", f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
            return
        # Check if the number of lines is within allowed limits
        if lines < 1 or lines > MAX_LINES:
            messagebox.showerror("Invalid Lines", f"Lines must be between 1 and {MAX_LINES}.")
            return

        total_bet = bet * lines  # Calculate total bet
        if total_bet > self.balance:
            messagebox.showerror("Insufficient Funds", "You do not have enough balance to place this bet.")
            return

        self.balance -= total_bet  # Deduct total bet from balance
        self.update_balance()  # Update the displayed balance

        slots = self.get_slot_machine_spin()  # Generate the spin result
        self.display_slots(slots)  # Display the spin result on the grid

        winnings, winning_lines = self.check_winnings(slots, lines, bet)  # Check for winnings
        self.balance += winnings  # Add winnings to balance
        self.update_balance()  # Update the displayed balance

        if winnings > 0:
            messagebox.showinfo("You Won!", f"You won ${winnings} on lines {', '.join(map(str, winning_lines))}.")
        else:
            messagebox.showinfo("No Win", "No winning lines this time.")

if __name__ == "__main__":
    # Main loop to start the application
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
