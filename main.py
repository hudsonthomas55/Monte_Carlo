from tkinter import *
import random
import numpy as np

# ---------------------------------------------- WINDOW SETUP ---------------------------------------------- #
window = Tk()
window.minsize(width=500, height=500)
window.title("Retirement Calculator")
window.config(padx=50, pady=50)

# -------------------------------------------- REFERENCES---------------------------------------- #
beginning_age = 0
retirement_age = 0
current_income = 0
current_balance = 0
yearly_contributions = 0
employer_match = 0

lowest_balance = 0
avg_balance = 0
highest_balance = 0


# -------------------------------------------- FUNCTIONS---------------------------------------- #
def clear_frame():
    for widget in window.winfo_children():
        widget.destroy()


# -------------------------------------- MONTE CARLO SECTION ---------------------------------------- #
def monte_carlo():
    # Set the number of simulations
    num_sims = 1000

    # Set the investment parameters
    investment_amount = (int(yearly_contributions) + employer_match)
    num_years = int(retirement_age) - int(beginning_age)

    # Initialize the variable
    sim_results = np.zeros((num_sims, num_years + 1))

    # Run the Monte Carlo simulations
    for i in range(num_sims):
        # Initialize the variable
        sim_results[i, 0] = current_balance

        # Loop through the years
        for j in range(num_years):
            # Generate the random returns
            rate = np.random.normal(loc=0.07, scale=0.03)

            # Calculate the returns
            sim_results[i, j + 1] = sim_results[i, j] + sim_results[i, j] * rate + investment_amount

    # Calculate the average ending balance
    avg_ending_balance = sim_results[:, -1].mean()
    global avg_balance
    avg_balance = avg_ending_balance
    # Calculate the lowest ending balance
    lowest_ending_balance = sim_results[:, -1].min()
    global lowest_balance
    lowest_balance = lowest_ending_balance
    # Calculate the highest ending balance
    highest_ending_balance = sim_results[:, -1].max()
    global highest_balance
    highest_balance = highest_ending_balance

    # Return values in separate screen
    return_screen()


# -------------------------------------- RETURN SCREEN  ---------------------------------------- #
def return_screen():
    clear_frame()

    back_button = Button(text="Go Back", width=3, command=main_screen)
    back_button.grid(row=0, column=0)
    spacer_label = Label(text="\n\n\n\n\n")
    spacer_label.grid(row=1, column=0)

    lowest_label = Label(text="The lowest ending balance is: ")
    lowest_label.grid(row=2, column=1)
    lowest_return = Label(text="${:,.2f}".format(lowest_balance), font=("default", 14, "bold"))
    lowest_return.grid(row=2, column=2)

    avg_label = Label(text="The average ending balance is: ")
    avg_label.grid(row=3, column=1)
    avg_return = Label(text="${:,.2f}".format(avg_balance), font=("default", 14, "bold"))
    avg_return.grid(row=3, column=2)

    high_label = Label(text="The highest ending balance is: ")
    high_label.grid(row=4, column=1)
    high_return = Label(text="${:,.2f}".format(highest_balance), font=("default", 14, "bold"))
    high_return.grid(row=4, column=2)


# ------------------------------------- MAIN SCREEN ------------------------------------- #
def main_screen():
    clear_frame()

    # Submit button function
    def submit_button():
        # Get ages:
        cur_age = current_age_entry.get()
        ret_age = ret_age_entry.get()
        # Get current income:
        cur_income = cur_income_entry.get()
        income = float(cur_income.replace("$", "").replace(",", ""))
        # Get retirement balance:
        ret_bal = cur_ret_entry.get()
        retirement_bal = float(ret_bal.replace("$", "").replace(",", ""))
        # Get retirement contributions
        cont = ret_cont_entry.get()
        contribution = float(cont.replace("$", "").replace(",", ""))
        # Get employer match
        employ_match = er_match_entry.get()
        dollar_match = ((float(employ_match.replace("%", "")) / 100) * income)
        match = float(employ_match.replace("%", ""))

        # Get and update global variables
        global beginning_age
        global retirement_age
        global current_income
        global current_balance
        global yearly_contributions
        global employer_match
        beginning_age = cur_age
        retirement_age = ret_age
        current_income = income
        current_balance = retirement_bal
        yearly_contributions = contribution
        employer_match = dollar_match

        # Tie to Monte Carlo function here
        monte_carlo()

    # Screen setup
    welcome_label = Label(text="Welcome! \n Let's review some retirement returns: \n\n", font=("Arial", 30))
    welcome_label.grid(row=0, column=0, columnspan=3)

    # Current Age
    current_age_label = Label(text="What is your current age? ")
    current_age_label.grid(row=1, column=0, sticky="E")
    current_age_entry = Entry(width=15)
    current_age_entry.insert(END, string="35")
    current_age_entry.grid(row=1, column=1, columnspan=3)
    current_age_entry.focus_set()

    # Retirement Age
    ret_age_label = Label(text="What age would you like to retire?")
    ret_age_label.grid(row=2, column=0, sticky="E")
    ret_age_entry = Entry(width=15)
    ret_age_entry.insert(END, string="65")
    ret_age_entry.grid(row=2, column=1, columnspan=3)
    ret_age_entry.focus_set()

    # Current Income
    cur_income_label = Label(text="What is your current gross (pre-tax) income?")
    cur_income_label.grid(row=3, column=0, sticky="E")
    cur_income_entry = Entry(width=15)
    cur_income_entry.insert(END, string="$100,000")
    cur_income_entry.grid(row=3, column=1, columnspan=3)
    cur_income_entry.focus_set()

    # Current Retirement
    cur_ret_label = Label(text="What is your current retirement account(s) balance?")
    cur_ret_label.grid(row=4, column=0, sticky="E")
    cur_ret_entry = Entry(width=15)
    cur_ret_entry.insert(END, string="$33,000")
    cur_ret_entry.grid(row=4, column=1, columnspan=3)
    cur_ret_entry.focus_set()

    # Retirement Contributions
    ret_cont_label = Label(text="How much do you contribute each year to retirement accounts?\n"
                                "(not including employer match)", justify=RIGHT)
    ret_cont_label.grid(row=5, column=0, sticky="E")
    ret_cont_entry = Entry(width=15)
    ret_cont_entry.insert(END, string="$6,000")
    ret_cont_entry.grid(row=5, column=1, columnspan=3)
    ret_cont_entry.focus_set()

    # Employer Match
    er_match_label = Label(text="Does your employer match your contributions? If so, what %?")
    er_match_label.grid(row=6, column=0, sticky="E")
    er_match_entry = Entry(width=15)
    er_match_entry.insert(END, string="3%")
    er_match_entry.grid(row=6, column=1, columnspan=3)
    er_match_entry.focus_set()

    # Submit Button
    spacer_label = Label(text="\n\n")
    spacer_label.grid(row=10, column=0)
    return_label = Label(text="", justify=LEFT, anchor="w")
    return_label.grid(row=11, column=0, columnspan=4)
    submit_button = Button(text="Run Simulations", width=30, command=submit_button)
    submit_button.grid(row=12, column=0, columnspan=2)


# ---------------------------------------- KEEP WINDOW OPEN ---------------------------------------- #
main_screen()
window.mainloop()

