import tkinter as tk
from tkinter import messagebox, ttk

class MiniSuperMarketInventory:
    def __init__(self):
        self.inventory = {}
        self.total_sales = 0
        self.total_profit = 0
        self.total_loss = 0
        self.worker_accounts = {"owner": "ownerpass"}  # Owner's credentials

    # Inventory management methods
    def add_item(self, item_name, quantity, cost_price, selling_price):
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] += quantity
        else:
            self.inventory[item_name] = {
                'quantity': quantity,
                'cost_price': cost_price,
                'selling_price': selling_price
            }

    def update_quantity(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] += quantity
            if self.inventory[item_name]['quantity'] < 0:
                self.inventory[item_name]['quantity'] = 0
        else:
            messagebox.showerror("Error", f"Item {item_name} does not exist in the inventory.")

    def purchase_item(self, item_name, quantity):
        if item_name in self.inventory:
            if self.inventory[item_name]['quantity'] >= quantity:
                cost_price = self.inventory[item_name]['cost_price']
                selling_price = self.inventory[item_name]['selling_price']
                total_purchase_price = selling_price * quantity
                self.total_sales += total_purchase_price

                profit_loss_per_item = selling_price - cost_price
                total_profit_loss = profit_loss_per_item * quantity
                if profit_loss_per_item > 0:
                    self.total_profit += total_profit_loss
                else:
                    self.total_loss += abs(total_profit_loss)

                self.inventory[item_name]['quantity'] -= quantity
            else:
                messagebox.showerror("Error", f"Insufficient stock of {item_name}.")
        else:
            messagebox.showerror("Error", f"Item {item_name} does not exist in the inventory.")

    def get_inventory_data(self):
        return self.inventory

    def get_financial_summary(self):
        return self.total_sales, self.total_profit, self.total_loss

    # Worker account management methods
    def add_worker_account(self, username, password):
        if username in self.worker_accounts:
            messagebox.showerror("Error", "Worker with this username already exists.")
        else:
            self.worker_accounts[username] = password
            messagebox.showinfo("Success", "Worker account created successfully.")

    def remove_worker_account(self, username):
        if username in self.worker_accounts:
            del self.worker_accounts[username]
            messagebox.showinfo("Success", "Worker account removed successfully.")
        else:
            messagebox.showerror("Error", "Worker does not exist.")

    def get_worker_accounts(self):
        return self.worker_accounts

    def change_owner_password(self, new_password):
        self.worker_accounts["owner"] = new_password
        messagebox.showinfo("Success", "Owner password changed successfully.")

class OwnerGUI:
    def __init__(self, root, inventory_system):
        self.root = root
        self.inventory_system = inventory_system
        self.root.title("Owner - Mini Supermarket Management")

        # Add a frame for decoration
        self.frame = tk.Frame(root, bg="lightblue", padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        # Tab setup
        tab_control = ttk.Notebook(self.frame)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        self.tab3 = ttk.Frame(tab_control)
        self.tab4 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text="Add/Update Items")
        tab_control.add(self.tab2, text="Sell Items")
        tab_control.add(self.tab3, text="Inventory & Financials")
        tab_control.add(self.tab4, text="Worker Management")
        tab_control.pack(expand=1, fill="both")

        # Add/Update Items tab
        self.setup_add_update_tab()

        # Sell Items tab
        self.setup_sell_tab()

        # Inventory & Financials tab
        self.setup_inventory_financial_tab()

        # Worker Management tab
        self.setup_worker_management_tab()

        # Logout Button
        tk.Button(self.frame, text="Logout", command=self.logout, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

        # Change Owner Password Button
        tk.Button(self.frame, text="Change Password", command=self.change_owner_password, bg="yellow", font=("Arial", 12)).pack(pady=10)

    def setup_add_update_tab(self):
        tk.Label(self.tab1, text="Item Name").grid(row=0, column=0)
        tk.Label(self.tab1, text="Quantity").grid(row=1, column=0)
        tk.Label(self.tab1, text="Cost Price").grid(row=2, column=0)
        tk.Label(self.tab1, text="Selling Price").grid(row=3, column=0)

        self.item_name_entry = tk.Entry(self.tab1)
        self.quantity_entry = tk.Entry(self.tab1)
        self.cost_price_entry = tk.Entry(self.tab1)
        self.selling_price_entry = tk.Entry(self.tab1)

        self.item_name_entry.grid(row=0, column=1)
        self.quantity_entry.grid(row=1, column=1)
        self.cost_price_entry.grid(row=2, column=1)
        self.selling_price_entry.grid(row=3, column=1)

        tk.Button(self.tab1, text="Add/Update Item", command=self.add_update_item, bg="green", fg="white").grid(row=4, column=1)

    def setup_sell_tab(self):
        tk.Label(self.tab2, text="Item Name").grid(row=0, column=0)
        tk.Label(self.tab2, text="Quantity to Sell").grid(row=1, column=0)

        self.sell_item_name_entry = tk.Entry(self.tab2)
        self.sell_quantity_entry = tk.Entry(self.tab2)

        self.sell_item_name_entry.grid(row=0, column=1)
        self.sell_quantity_entry.grid(row=1, column=1)

        tk.Button(self.tab2, text="Sell Item", command=self.sell_item, bg="blue", fg="white").grid(row=2, column=1)

    def setup_inventory_financial_tab(self):
        self.inventory_display = tk.Text(self.tab3, width=60, height=15)
        self.inventory_display.grid(row=0, column=0, columnspan=2)

        tk.Button(self.tab3, text="Show Inventory", command=self.display_inventory, bg="lightgreen", font=("Arial", 12)).grid(row=1, column=0)
        tk.Button(self.tab3, text="Show Financials", command=self.display_financials, bg="lightgreen", font=("Arial", 12)).grid(row=1, column=1)

    def setup_worker_management_tab(self):
        tk.Label(self.tab4, text="Worker Username").grid(row=0, column=0)
        tk.Label(self.tab4, text="Password").grid(row=1, column=0)

        self.worker_username_entry = tk.Entry(self.tab4)
        self.worker_password_entry = tk.Entry(self.tab4, show="*")
        self.worker_username_entry.grid(row=0, column=1)
        self.worker_password_entry.grid(row=1, column=1)

        tk.Button(self.tab4, text="Add Worker", command=self.add_worker, bg="orange", font=("Arial", 12)).grid(row=2, column=0)
        tk.Button(self.tab4, text="Remove Worker", command=self.remove_worker, bg="orange", font=("Arial", 12)).grid(row=2, column=1)

        self.worker_list = tk.Text(self.tab4, width=30, height=10)
        self.worker_list.grid(row=3, column=0, columnspan=2)
        self.display_workers()

    def add_update_item(self):
        item_name = self.item_name_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            cost_price = float(self.cost_price_entry.get())
            selling_price = float(self.selling_price_entry.get())
            self.inventory_system.add_item(item_name, quantity, cost_price, selling_price)
            messagebox.showinfo("Success", f"Item '{item_name}' added/updated successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid quantity, cost price, and selling price.")

    def sell_item(self):
        item_name = self.sell_item_name_entry.get()
        try:
            quantity = int(self.sell_quantity_entry.get())
            self.inventory_system.purchase_item(item_name, quantity)
            messagebox.showinfo("Success", f"Sold {quantity} of '{item_name}' successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity.")

    def display_inventory(self):
        inventory_data = self.inventory_system.get_inventory_data()
        self.inventory_display.delete("1.0", tk.END)
        for item_name, item_info in inventory_data.items():
            self.inventory_display.insert(tk.END, f"Item: {item_name}, Quantity: {item_info['quantity']}, "
                                                  f"Cost Price: {item_info['cost_price']}, Selling Price: {item_info['selling_price']}\n")

    def display_financials(self):
        total_sales, total_profit, total_loss = self.inventory_system.get_financial_summary()
        self.inventory_display.delete("1.0", tk.END)
        self.inventory_display.insert(tk.END, f"Total Sales: {total_sales}\n")
        self.inventory_display.insert(tk.END, f"Total Profit: {total_profit}\n")
        self.inventory_display.insert(tk.END, f"Total Loss: {total_loss}\n")

    def add_worker(self):
        username = self.worker_username_entry.get()
        password = self.worker_password_entry.get()
        if username and password:
            self.inventory_system.add_worker_account(username, password)
            self.display_workers()
        else:
            messagebox.showerror("Input Error", "Please enter a username and password for the worker.")

    def remove_worker(self):
        username = self.worker_username_entry.get()
        if username:
            self.inventory_system.remove_worker_account(username)
            self.display_workers()
        else:
            messagebox.showerror("Input Error", "Please enter the username of the worker to remove.")

    def display_workers(self):
        workers = self.inventory_system.get_worker_accounts()
        self.worker_list.delete("1.0", tk.END)
        self.worker_list.insert(tk.END, "Current Workers:\n")
        for username in workers:
            self.worker_list.insert(tk.END, f"{username}\n")

    def change_owner_password(self):
        new_password = self.worker_password_entry.get()
        if new_password:
            self.inventory_system.change_owner_password(new_password)
        else:
            messagebox.showerror("Input Error", "Please enter a new password.")

    def logout(self):
        self.root.destroy()  # Close current window
        login_window = tk.Tk()
        LoginWindow(login_window, self.inventory_system)
        login_window.mainloop()

class WorkerGUI:
    def __init__(self, root, inventory_system):
        self.root = root
        self.inventory_system = inventory_system
        self.root.title("Worker - Mini Supermarket Sales")

        self.frame = tk.Frame(root, bg="lightyellow", padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Item Name").grid(row=0, column=0)
        tk.Label(self.frame, text="Quantity to Sell").grid(row=1, column=0)

        self.sell_item_name_entry = tk.Entry(self.frame)
        self.sell_quantity_entry = tk.Entry(self.frame)

        self.sell_item_name_entry.grid(row=0, column=1)
        self.sell_quantity_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Sell Item", command=self.sell_item, bg="blue", fg="white").grid(row=2, column=1)

        # Logout Button
        tk.Button(self.frame, text="Logout", command=self.logout, bg="red", fg="white", font=("Arial", 12)).grid(pady=10)

    def sell_item(self):
        item_name = self.sell_item_name_entry.get()
        try:
            quantity = int(self.sell_quantity_entry.get())
            self.inventory_system.purchase_item(item_name, quantity)
            messagebox.showinfo("Success", f"Sold {quantity} of '{item_name}' successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity.")

    def logout(self):
        self.root.destroy()  # Close current window
        login_window = tk.Tk()
        LoginWindow(login_window, self.inventory_system)
        login_window.mainloop()

class LoginWindow:
    def __init__(self, root, inventory_system):
        self.root = root
        self.inventory_system = inventory_system
        self.root.title("Login")

        # Login styling
        self.frame = tk.Frame(root, bg="lightblue", padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)

        self.username_label = tk.Label(self.frame, text="Username")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.frame, text="Password")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.frame, text="Login", command=self.check_login, bg="green", fg="white")
        self.login_button.grid(row=2, column=1)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "owner" and password == "ownerpass":
            self.root.destroy()  # Close login window
            main_window = tk.Tk()
            OwnerGUI(main_window, self.inventory_system)
            main_window.mainloop()
        elif username in self.inventory_system.worker_accounts and self.inventory_system.worker_accounts[username] == password:
            self.root.destroy()  # Close login window
            main_window = tk.Tk()
            WorkerGUI(main_window, self.inventory_system)
            main_window.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Main Program
if __name__ == "__main__":
    inventory_system = MiniSuperMarketInventory()
    login_window = tk.Tk()
    LoginWindow(login_window, inventory_system)
    login_window.mainloop()
