import numpy as np
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, Text

def is_diagonally_dominant(A):

    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= row_sum:
            return False
    return True

def modify_to_diagonally_dominant(A, b):
    n = len(A)
    modified_A = A.copy()
    modified_b = b.copy()
    for i in range(n):
        diag = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= row_sum:
            modified_A[i][i] = row_sum + 1
            modified_b[i] = row_sum
    return modified_A, modified_b

def gauss_seidel(A, b, tol=1e-6, max_iter=100):
    iterations = []
    n = len(A)
    x = np.zeros(n)
    is_diagonally_dominant = True

    if not is_diagonally_dominant:
        is_diagonally_dominant = False
        modified_A, modified_b = modify_to_diagonally_dominant(A, b)
        A = modified_A
        b = modified_b

    for iteration in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        iterations.append(x_new.copy())
        if np.allclose(x, x_new, atol=tol):
            return x_new, iterations, is_diagonally_dominant
        x = x_new

    return x, iterations, is_diagonally_dominant

def update_results(result_text, result, is_dominant):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Gauss-Seidel Solver Results:\n")
    result_text.insert(tk.END, f"Is Diagonally Dominant: {is_dominant}\n\n")
    result_text.insert(tk.END, "Iterations:\n")
    for i, iteration in enumerate(result):
        result_text.insert(tk.END, f"Iteration {i + 1}: {iteration}\n")
    result_text.insert(tk.END, "\nFinal Solution:\n")
    result_text.insert(tk.END, result)
    result_text.config(state=tk.DISABLED)

def solve_equations():
    matrix_entries = []
    b_entries = []
    try:
        for i in range(matrix_size):
            row = []
            for j in range(matrix_size):
                row.append(float(matrix_entry[i][j].get()))
            matrix_entries.append(row)
            b_entries.append(float(b_entry[i].get()))
        A = np.array(matrix_entries, dtype=float)
        b = np.array(b_entries, dtype=float)
        max_iter = int(max_iter_entry.get())
        tolerance = float(tol_entry.get())

        result, iterations, is_diagonally_dominant = gauss_seidel(A, b, tol=tolerance, max_iter=max_iter)
        update_results(result_text, result, is_diagonally_dominant)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

matrix_size = 3  # Set the matrix size
root = tk.Tk()
root.title("Gauss-Seidel Solver")

matrix_frame = tk.Frame(root)
matrix_frame.pack(padx=10, pady=10)

matrix_entry = []
b_entry = []


for i in range(matrix_size):
    row_entries = []
    for j in range(matrix_size):
        Label(matrix_frame, text=f"A[{i + 1}][{j + 1}]").grid(row=i, column=j * 2)
        entry = Entry(matrix_frame)
        entry.grid(row=i, column=j * 2 + 1)
        row_entries.append(entry)
    matrix_entry.append(row_entries)


Label(matrix_frame, text="Matrix B").grid(row=matrix_size, column=0, columnspan=matrix_size * 2)
b_entry = [Entry(matrix_frame) for _ in range(matrix_size)]
for i in range(matrix_size):
    b_entry[i].grid(row=matrix_size + 1, column=i * 2)


Label(matrix_frame, text="Tolerance").grid(row=matrix_size + 2, column=0)
tol_entry = Entry(matrix_frame)
tol_entry.grid(row=matrix_size + 2, column=1)

Label(matrix_frame, text="Max Iterations").grid(row=matrix_size + 3, column=0)
max_iter_entry = Entry(matrix_frame)
max_iter_entry.grid(row=matrix_size + 3, column=1)


solve_button = Button(matrix_frame, text="Solve", command=solve_equations)
solve_button.grid(row=matrix_size + 4, column=0, columnspan=matrix_size * 2)

result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=10)

result_text = Text(result_frame, height=15, width=40)
result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
result_text.config(state=tk.DISABLED)

result_label = Label(result_frame, text="Gauss-Seidel Solver Results:")
result_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()
