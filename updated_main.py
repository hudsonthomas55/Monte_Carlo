import tkinter as tk
from tkinter import Button, Entry, Label
import numpy as np

class RetirementCalculator:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.setup_variables()
        self.main_screen()

    def setup_window(self):
        self.master.minsize(width=500, height=500)
        self.master.title("Retirement Calculator")
        self.master.config(padx=50, pady=50)

    def setup_variables(self):
        self.beginning_age = tk.StringVar(value="35")
        self.retirement_age = tk.StringVar(value="65")
        self.current_income = tk.StringVar(value="$100,000")
        self.current_balance = tk.StringVar(value="$33,000")
        self.yearly_contributions = tk.StringVar(value="$6,000")
        self.employer_match = tk.StringVar(value="3%")

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def monte_carlo(self):
        num_sims = 1000
        investment_amount = (
            int(self.yearly_contributions.get().replace("$", "").replace(",", ""))
            + (float(self.employer_match.get().replace("%", "")) / 100)
            * float(self.current_income.get().replace("$", "").replace(",", ""))
        )
        num_years = int(self.retirement_age.get()) - int(self.beginning_age.get())

        sim_results = self.run_simulations(num_sims, investment_amount, num_years)

        avg_ending_balance = np.mean(sim_results[:, -1])
        lowest_ending_balance = np.min(sim_results[:, -1])
        highest_ending_balance = np.max(sim_results[:, -1])

        self.return_screen(lowest_ending_balance, avg_ending_balance, highest_ending_balance)

    def run_simulations(self, num_sims, investment_amount, num_years):
        sim_results = []
        for _ in range(num_sims):
            sim_result = [float(self.current_balance.get().replace("$", "").replace(",", ""))]
            for _ in range(num_years):
                rate = np.random.normal(loc=0.07, scale=0.03)
                sim_result.append(sim_result[-1] + sim_result[-1] * rate + investment_amount)
            sim_results.append(sim_result)
        return np.array(sim_results)

    def return_screen(self, lowest_balance, avg_balance, highest_balance):
        self.clear_frame()

        back_button = Button(self.master, text="Go Back", width=3, command=self.main_screen)
        back_button.grid(row=0, column=0)

        labels = ["The lowest ending balance is:", "The average ending balance is:", "The highest ending balance is:"]
        values = ["${:,.2f}".format(lowest_balance), "${:,.2f}".format(avg_balance), "${:,.2f}".format(highest_balance)]

        for i, (label, value) in enumerate(zip(labels, values), start=2):
            label_widget = Label(self.master, text=label)
            label_widget.grid(row=i, column=1)
            value_widget = Label(self.master, text=value, font=("default", 14, "bold"))
            value_widget.grid(row=i, column=2)

    def main_screen(self):
        self.clear_frame()

        welcome_label = Label(
            self.master, text="Welcome! \n Let's review some retirement returns: \n\n", font=("Arial", 30)
        )
        welcome_label.grid(row=0, column=0, columnspan=3)

        labels = [
            "Current Age:",
            "Retirement Age:",
            "Current Income:",
            "Current Retirement Balance:",
            "Retirement Contributions:",
            "Employer Match:",
        ]
        entry_vars = [
            self.beginning_age,
            self.retirement_age,
            self.current_income,
            self.current_balance,
            self.yearly_contributions,
            self.employer_match,
        ]

        for i, (label, entry_var) in enumerate(zip(labels, entry_vars), start=1):
            label_widget = Label(self.master, text=label)
            label_widget.grid(row=i, column=0, sticky="E")
            entry_widget = Entry(self.master, width=15, textvariable=entry_var)
            entry_widget.grid(row=i, column=1, columnspan=3)
            entry_widget.focus_set()

        submit_button = Button(self.master, text="Run Simulations", width=30, command=self.monte_carlo)
        submit_button.grid(row=8, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = RetirementCalculator(root)
    root.mainloop()
