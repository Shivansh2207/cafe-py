import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import mysql.connector

# Update the initial connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="toor",
    database="project_db"
)


class CafeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title('Cafe Management System')
        self.root.geometry('1200x700')
        
        # Configure styles
        self.configure_styles()
        

        
        self.menu = {
    'Beverages': {
        'Espresso': 100,
        'Cappuccino': 130,
        'Latte': 140,
        'Americano': 120,
        'Cold Coffee': 150,
        'Iced Tea': 90,
        'Green Tea': 70,
        'Hot Chocolate': 150,
        'Mojito': 100,
        'Lemonade': 80,
        'Milkshake - Chocolate': 140,
        'Milkshake - Strawberry': 140,
        'Smoothie - Mango': 160,
        'Smoothie - Berry': 170
    },
    'Snacks': {
        'French Fries': 120,
        'Cheese Garlic Bread': 140,
        'Veg Sandwich': 130,
        'Club Sandwich': 160,
        'Grilled Cheese Sandwich': 150,
        'Veg Burger': 180,
        'Cheese Burger': 200,
        'Chicken Burger': 220,
        'Veg Pizza': 250,
        'Cheese Burst Pizza': 300,
        'Paneer Tikka Pizza': 280,
        'Nachos with Cheese': 170,
        'Spring Rolls': 160,
        'Crispy Corn': 150
    },
    'Desserts': {
        'Chocolate Cake': 150,
        'Cheesecake': 180,
        'Brownie': 120,
        'Waffle': 140,
        'Donut': 90,
        'Cupcake': 100,
        'Ice Cream (2 Scoops)': 100,
        'Sundae': 160,
        'Pudding': 130,
        'Mousse': 140,
        'Gulab Jamun (2 pcs)': 80
    },
    'Main Course': {
        'Paneer Butter Masala': 250,
        'Chole Bhature': 180,
        'Veg Biryani': 200,
        'Chicken Biryani': 280,
        'Dal Tadka': 160,
        'Jeera Rice': 140,
        'Butter Naan (2 pcs)': 60,
        'Veg Fried Rice': 180,
        'Veg Noodles': 170,
        'Manchurian Gravy': 190,
        'Veg Kolhapuri': 220,
        'Chicken Curry': 270
    },
    'Combos': {
        'Burger + Fries + Coke': 280,
        'Pizza + Mojito': 300,
        'Pasta + Garlic Bread': 270,
        'Sandwich + Cold Coffee': 220,
        'Biryani + Raita + Dessert': 320,
        'Waffle + Milkshake': 250
    },
    'Breakfast': {
        'Pancakes with Syrup': 160,
        'Omelette Toast': 120,
        'Aloo Paratha with Curd': 150,
        'Poha': 100,
        'Upma': 100,
        'Chai & Toast': 80,
        'English Breakfast': 280
    },
    'Salads': {
        'Green Salad': 90,
        'Caesar Salad': 130,
        'Fruit Salad': 110,
        'Sprout Salad': 100,
        'Grilled Chicken Salad': 160
    },
    'Soups': {
        'Tomato Soup': 90,
        'Sweet Corn Soup': 100,
        'Manchow Soup': 100,
        'Hot & Sour Soup': 110,
        'Cream of Mushroom Soup': 120
    },
    'Pastas': {
        'White Sauce Pasta': 200,
        'Red Sauce Pasta': 200,
        'Arrabiata Pasta': 220,
        'Pasta Alfredo': 240
    },
    'Wraps & Rolls': {
        'Veg Wrap': 120,
        'Paneer Tikka Roll': 160,
        'Chicken Roll': 180,
        'Cheese Corn Wrap': 140
    }
}


        self.selected_items = []
        self.show_welcome_page()

    def configure_styles(self):
        style = ttk.Style()
        # Configure fonts with elegant typography
        style.configure('TLabel', font=('Playfair Display', 11), foreground='#2C1810')
        style.configure('TButton', font=('Montserrat', 11, 'bold'), padding=8)
        style.configure('Heading.TLabel', font=('Playfair Display', 14, 'bold'), foreground='#2C1810')
        style.configure('Total.TLabel', font=('Montserrat', 13, 'bold'), foreground='#2C1810')
        style.configure('TLabelframe', padding=15)
        style.configure('TLabelframe.Label', font=('Playfair Display', 12, 'bold'), foreground='#2C1810')
        style.configure('Treeview', font=('Montserrat', 10), rowheight=30, background='#FFF8F3', fieldbackground='#FFF8F3')
        style.configure('Treeview.Heading', font=('Montserrat', 11, 'bold'), background='#8B4513', foreground='white')
        style.configure('Welcome.TLabel', font=('Playfair Display', 32, 'bold'), foreground='#2C1810')
        style.configure('PlaceOrder.TButton', font=('Montserrat', 18, 'bold'), padding=20)
        
        # Configure warm, cafe-themed colors
        self.root.configure(bg='#FFF8F3')  
        style.configure('TFrame', background='#FFF8F3')
        style.configure('TLabelframe', background='#FFF8F3')
        style.configure('TButton', background='#8B4513', foreground='red')  
        style.map('TButton',
                  background=[('active', '#A0522D'), ('disabled', '#D2B48C')],
                  foreground=[('disabled', '#8B4513')])

    def show_welcome_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Welcome message
        welcome_frame = ttk.Frame(self.root)
        welcome_frame.place(relx=0.5, rely=0.4, anchor='center')

        welcome_label = ttk.Label(welcome_frame, text='Welcome to Our Cafe', style='Welcome.TLabel')
        welcome_label.pack(pady=20)

        # Place Order button
        order_btn = ttk.Button(welcome_frame, text='Place Order', style='PlaceOrder.TButton',
                              command=self.show_menu_page)
        order_btn.pack(pady=30)

    def show_menu_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Left Frame for Menu
        left_frame = ttk.LabelFrame(self.root, text='Menu', padding='15')
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')

        # Menu Treeview
        self.menu_tree = ttk.Treeview(left_frame, columns=('Item', 'Price'),show='headings', height=10)
        self.menu_tree.heading('Item', text='Item')
        self.menu_tree.heading('Price', text='Price (₹)')
        self.menu_tree.grid(row=1, column=0, columnspan=2, pady=10, padx=5)
        
        # Add scrollbar to menu tree
        menu_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.menu_tree.yview)
        menu_scroll.grid(row=1, column=2, sticky='ns')
        self.menu_tree.configure(yscrollcommand=menu_scroll.set)

        # Category selection
        ttk.Label(left_frame, text='Select Category:', style='Heading.TLabel').grid(row=0, column=0, pady=10)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, values=list(self.menu.keys()),
                                    font=('Helvetica', 10), width=20)
        category_combo.grid(row=0, column=1, pady=10, padx=5)
        category_combo.bind('<<ComboboxSelected>>', self.update_menu_items)

        # Quantity spinbox
        ttk.Label(left_frame, text='Quantity:', style='Heading.TLabel').grid(row=2, column=0, pady=10)
        self.quantity_var = tk.StringVar(value='1')
        quantity_spin = ttk.Spinbox(left_frame, from_=1, to=10, textvariable=self.quantity_var,
                                  font=('Helvetica', 10), width=10)
        quantity_spin.grid(row=2, column=1, pady=10, padx=5)

        # Add to Order button
        add_btn = ttk.Button(left_frame, text='Add to Order', command=self.add_to_order, style='TButton')
        add_btn.grid(row=3, column=0, columnspan=2, pady=15, padx=10, sticky='ew')

        # Right Frame for Order Summary
        right_frame = ttk.LabelFrame(self.root, text='Order Summary', padding='15')
        right_frame.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')

        # Order Treeview
        self.order_tree = ttk.Treeview(right_frame, columns=('Item', 'Quantity', 'Price'), show='headings', height=10)
        self.order_tree.heading('Item', text='Item')
        self.order_tree.heading('Quantity', text='Quantity')
        self.order_tree.heading('Price', text='Price (₹)')
        self.order_tree.grid(row=0, column=0, columnspan=2, pady=10, padx=5)
        
        # Add scrollbar to order tree
        order_scroll = ttk.Scrollbar(right_frame, orient='vertical', command=self.order_tree.yview)
        order_scroll.grid(row=0, column=2, sticky='ns')
        self.order_tree.configure(yscrollcommand=order_scroll.set)

        # Total Amount
        self.total_label = ttk.Label(right_frame, text='Total Amount: ₹0', style='Total.TLabel')
        self.total_label.grid(row=1, column=0, columnspan=2, pady=15)

        # Generate Bill Button
        bill_btn = ttk.Button(right_frame, text='Generate Bill', command=self.generate_bill, style='TButton')
        bill_btn.grid(row=2, column=0, columnspan=2, pady=15, padx=10, sticky='ew')

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def update_menu_items(self, event=None):    
        category = self.category_var.get()
        self.menu_tree.delete(*self.menu_tree.get_children())
        if category in self.menu:
            for item, price in self.menu[category].items():
                self.menu_tree.insert('', 'end', values=(item, price))

    def add_to_order(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select an item from the menu')
            return

        item = self.menu_tree.item(selected[0])['values']
        quantity = int(self.quantity_var.get())
        total_price = item[1] * quantity

        self.order_tree.insert('', 'end', values=(item[0], quantity, total_price))
        self.update_total()

    def update_total(self):
        total = sum(float(self.order_tree.item(item)['values'][2]) for item in self.order_tree.get_children())
        self.total_label.config(text=f'Total Amount: ₹{total:.2f}')

    def generate_bill(self):
        if not self.order_tree.get_children():
            messagebox.showwarning('Warning', 'Please add items to the order first')
            return

        # Customer Information Dialog
        customer_dialog = tk.Toplevel(self.root)
        customer_dialog.title('Customer Information')
        customer_dialog.geometry('400x300')
        customer_dialog.configure(bg='#FFF8F3')

        # Customer Information Frame
        info_frame = ttk.LabelFrame(customer_dialog, text='Customer Details', padding='15')
        info_frame.pack(padx=20, pady=20, fill='x')

        # Error Label
        error_label = ttk.Label(customer_dialog, text='', foreground='red')
        error_label.pack(pady=5)

        # Customer Name
        ttk.Label(info_frame, text='Name:').grid(row=0, column=0, pady=5, padx=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=name_var)
        name_entry.grid(row=0, column=1, pady=5, padx=5)

        # Contact Number
        ttk.Label(info_frame, text='Contact No:').grid(row=1, column=0, pady=5, padx=5)
        contact_var = tk.StringVar()
        contact_entry = ttk.Entry(info_frame, textvariable=contact_var)
        contact_entry.grid(row=1, column=1, pady=5, padx=5)

        # Email
        ttk.Label(info_frame, text='Email:').grid(row=2, column=0, pady=5, padx=5)
        email_var = tk.StringVar()
        email_entry = ttk.Entry(info_frame, textvariable=email_var)
        email_entry.grid(row=2, column=1, pady=5, padx=5)

        def validate_input():
            # Contact validation (10 digits)
            contact_pattern = r'^\d{10}$'
            if not re.match(contact_pattern, contact_var.get()):
                error_label.config(text='Contact number must be exactly 10 digits')
                return False

            # Email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email_var.get()):
                error_label.config(text='Please enter a valid email address')
                return False

            # Name validation (non-empty)
            if not name_var.get().strip():
                error_label.config(text='Please enter a name')
                return False

            return True

        def submit_info():
            if validate_input():
                customer_info = {
                    'name': name_var.get().strip(),
                    'contact': contact_var.get(),
                    'email': email_var.get()
                }
                customer_dialog.destroy()
                self.complete_bill_generation(customer_info)

        # Submit Button
        submit_btn = ttk.Button(customer_dialog, text='Submit', command=submit_info)
        submit_btn.pack(pady=20)

    def complete_bill_generation(self, customer_info):
        total = float(self.total_label.cget('text').split('₹')[1])
        gst = total * 0.18  # 18% GST
        final_total = total + gst
        
        # Insert customer data into database
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO customers (name, email, contact, total_amount) VALUES (%s, %s, %s, %s)"
            values = (customer_info['name'], customer_info['email'], customer_info['contact'], final_total)
            cursor.execute(sql, values)
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to save customer data: {err}")
        
        # Generate bill content
        bill_content = 'Cafe Management System\n'
        bill_content += '=' * 40 + '\n'
        bill_content += f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        bill_content += '=' * 40 + '\n\n'
        
        # Add customer information
        bill_content += 'Customer Information:\n'
        bill_content += f"Name: {customer_info['name']}\n"
        bill_content += f"Contact: {customer_info['contact']}\n"
        bill_content += f"Email: {customer_info['email']}\n"
        bill_content += '-' * 40 + '\n\n'
        
        bill_content += 'Items Ordered:\n'
        bill_content += '-' * 40 + '\n'

        for item in self.order_tree.get_children():
            values = self.order_tree.item(item)['values']
            bill_content += f'{values[0]} x {values[1]}: ₹{values[2]}\n'

        bill_content += '\n' + '-' * 40 + '\n'
        bill_content += f'Subtotal: ₹{total:.2f}\n'
        bill_content += f'GST (18%): ₹{gst:.2f}\n'
        bill_content += f'Total Amount: ₹{final_total:.2f}\n'

        # Save bill to file
        filename = f'bill_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(bill_content)

        messagebox.showinfo('Success', f'Bill generated successfully!\nSaved as {filename}')
        self.clear_order()
        self.show_welcome_page()

    def clear_order(self):
        self.order_tree.delete(*self.order_tree.get_children())
        self.update_total()


if __name__ == '__main__':
    root = tk.Tk()
    app = CafeManagementSystem(root)
    root.mainloop()
