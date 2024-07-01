import tkinter as tk
from tkinter import messagebox
from main import SSS
from sympy import isprime


class ShamirsSecretSharingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shamir's Secret Sharing")

        # Variables
        self.secret_var = tk.StringVar()
        self.num_shares_var = tk.IntVar()
        self.threshold_var = tk.IntVar()
        self.prime_var = tk.IntVar()

        # Default values
        self.secret_var.set("6")
        self.num_shares_var.set(5)
        self.threshold_var.set(3)
        self.prime_var.set(13)

        # Labels and Entry fields
        tk.Label(root, text="Enter Secret:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        tk.Entry(root, textvariable=self.secret_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Number of Shares (n):").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.num_shares_spinbox = tk.Spinbox(root, from_=2, to=10, textvariable=self.num_shares_var)
        self.num_shares_spinbox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Threshold (t):").grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.threshold_spinbox = tk.Spinbox(root, from_=2, to=10, textvariable=self.threshold_var)
        self.threshold_spinbox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(root, text="Prime (optional):").grid(row=3, column=0, sticky='w', padx=10, pady=10)
        tk.Entry(root, textvariable=self.prime_var).grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="Generate Shares", command=self.generate_shares).grid(row=4, column=0, columnspan=2, pady=20)

        # Output Label
        self.output_label = tk.Label(root, text="")
        self.output_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def generate_shares(self):
        secret = self.secret_var.get()
        num_shares = self.num_shares_var.get()
        threshold = self.threshold_var.get()
        prime = self.prime_var.get()

        try:
            secret = int(secret)
            if secret < 0:
                raise ValueError("Secret must be a positive integer.")

            if not (1 <= threshold <= num_shares):
                raise ValueError("Threshold must be between 1 and the number of shares.")

            if prime == 0:
                prime = None
            elif not isprime(prime):
                raise ValueError("Prime number entered is not prime.")

            sss = SSS(secret, num_shares, threshold, prime)
            shares, coeffs, prime = sss.get_shares()

            selected_shares = shares[:threshold]

            sss.plot_polynomial(selected_shares)

            reconstructed_secret = sss.reconstruct_secret(selected_shares)
            self.output_label.config(text=f"Reconstructed secret: {reconstructed_secret}")

        except ValueError as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ShamirsSecretSharingGUI(root)
    root.mainloop()
