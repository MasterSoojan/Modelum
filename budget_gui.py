
import tkinter as tk
from tkinter import ttk, messagebox

class BudgetEstimatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MODELUM - Budget Estimator")
        self.geometry("450x350")

        # Costs per square foot for different quality levels
        self.cost_per_sqft = {'Low': 110, 'Medium': 165, 'High': 250}
        # Multiplier to account for complexity of multi-story buildings
        self.floor_cost_multiplier = {1: 1.0, 2: 1.15, 3: 1.25, 4: 1.35, 5: 1.45}

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)

        # --- Input Widgets ---
        ttk.Label(main_frame, text="Total Square Footage:").grid(row=0, column=0, sticky="w", pady=5)
        self.sqft_var = tk.IntVar(value=2000)
        ttk.Entry(main_frame, textvariable=self.sqft_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(main_frame, text="Number of Floors:").grid(row=1, column=0, sticky="w", pady=5)
        self.floors_var = tk.IntVar(value=2)
        ttk.Spinbox(main_frame, from_=1, to=5, textvariable=self.floors_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(main_frame, text="Construction Quality:").grid(row=2, column=0, sticky="w", pady=5)
        self.quality_var = tk.StringVar(value='Medium')
        ttk.Combobox(main_frame, textvariable=self.quality_var, values=['Low', 'Medium', 'High']).grid(row=2, column=1, sticky="ew")

        # --- Calculate Button ---
        calculate_button = ttk.Button(main_frame, text="Estimate Budget", command=self.calculate_budget)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=20)

        # --- Result Display ---
        self.result_label = ttk.Label(main_frame, text="Estimated Cost: $", font=("Manrope", 14, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=2)

    def calculate_budget(self):
        try:
            sqft = self.sqft_var.get()
            num_floors = self.floors_var.get()
            quality = self.quality_var.get()

            if sqft <= 0 or num_floors <= 0:
                messagebox.showerror("Invalid Input", "Square footage and floors must be positive numbers.")
                return

            base_cost = sqft * self.cost_per_sqft[quality]
            total_cost = base_cost * self.floor_cost_multiplier.get(num_floors, 1.5)

            # Update the result label with the formatted cost
            self.result_label.config(text=f"Estimated Cost: ${total_cost:,.2f}")

        except tk.TclError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for square footage and floors.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = BudgetEstimatorApp()
    app.mainloop()
