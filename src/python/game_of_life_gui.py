import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from collections import deque

class GameBoard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[random.randint(0, 1) for _ in range(columns)] for _ in range(rows)]
        # Almacenar los estados del tablero
        self.history = deque()
        self.save_state()

    def save_state(self):
        # Copia profunda de la cuadrícula actual
        state_copy = [row[:] for row in self.grid]
        self.history.append(state_copy)

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.history.clear()
        self.save_state()

    def randomize_grid(self):
        self.grid = [[random.randint(0, 1) for _ in range(self.columns)] for _ in range(self.rows)]
        self.history.clear()
        self.save_state()

    def is_valid_position(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.columns

    def count_live_neighbors(self, row, col):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if self.is_valid_position(i, j) and self.grid[i][j] == 1:
                    count += 1
        return count

    def next_generation(self):
        new_grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                live_neighbors = self.count_live_neighbors(i, j)
                if self.grid[i][j] == 1:
                    if live_neighbors in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if live_neighbors == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        
        self.grid = new_grid
        self.save_state()

    def has_live_cells(self):
        for row in self.grid:
            if 1 in row:
                return True
        return False


class TechDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, initialvalue):
        super().__init__(parent)
        self.title(title)
        self.configure(bg="#0d1117")
        self.result = initialvalue
        
        tk.Label(self, text=prompt, bg="#0d1117", fg="#00ffcc", font=("Consolas", 12, "bold")).pack(pady=15, padx=20)
        self.entry = tk.Entry(self, bg="#21262d", fg="#00ffcc", font=("Consolas", 14), insertbackground="#00ffcc", relief="flat", justify="center")
        self.entry.insert(0, str(initialvalue))
        self.entry.pack(pady=5, padx=20)
        
        btn = tk.Button(self, text="[ ACEPTAR ]", bg="#21262d", fg="#c9d1d9", activebackground="#30363d", activeforeground="#00ffcc", relief="flat", font=("Consolas", 10, "bold"), cursor="hand2", command=self.on_ok)
        btn.pack(pady=15)
        
        self.entry.focus_set()
        self.bind('<Return>', lambda e: self.on_ok())
        
        # Centrar en pantalla 
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
        self.geometry(f"+{x}+{y}")
        
        parent.wait_window(self)
        
    def on_ok(self):
        try:
            val = int(self.entry.get())
            if val >= 5:
                self.result = val
        except ValueError:
            pass
        self.destroy()

class GameOfLifeApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # Ocultar la ventana principal temporalmente
        self.root.title("Conway's Game of Life - Tech Edition")
        self.root.configure(bg="#0d1117")
        
        # Pedir dimensiones
        dialog_rows = TechDialog(self.root, "Setup", "> NÚMERO DE FILAS _", 20)
        self.rows = dialog_rows.result
        
        # Destruir si se cierra
        if not self.root.winfo_exists():
            return

        dialog_cols = TechDialog(self.root, "Setup", "> NÚMERO DE COLUMNAS _", 20)
        self.cols = dialog_cols.result
        
        if not self.root.winfo_exists():
            return

        self.root.deiconify() # Mostrar ventana principal
        self.root.minsize(600, 400) # Tamaño mínimo de la ventana

        self.cell_size = 20
        self.board = GameBoard(self.rows, self.cols)
        self.is_playing = False

        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        # Frame superior para botones
        control_frame = tk.Frame(self.root, bg="#0d1117")
        control_frame.pack(pady=10)

        btn_style = {
            "bg": "#21262d", "fg": "#c9d1d9", 
            "activebackground": "#30363d", "activeforeground": "#00ffcc",
            "relief": "flat", "font": ("Consolas", 10, "bold"),
            "cursor": "hand2", "padx": 10, "pady": 5
        }

        self.btn_next = tk.Button(control_frame, text="Siguiente Generación", command=self.next_step, **btn_style)
        self.btn_next.pack(side=tk.LEFT, padx=5)

        self.btn_play = tk.Button(control_frame, text="Auto Play", command=self.toggle_play, **btn_style)
        self.btn_play.pack(side=tk.LEFT, padx=5)

        self.btn_history = tk.Button(control_frame, text="Imprimir Historial", command=self.print_history, **btn_style)
        self.btn_history.pack(side=tk.LEFT, padx=5)

        self.btn_clear = tk.Button(control_frame, text="Borrar", command=self.clear_board, **btn_style)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        self.btn_restart = tk.Button(control_frame, text="Reiniciar", command=self.restart_board, **btn_style)
        self.btn_restart.pack(side=tk.LEFT, padx=5)

        # Etiqueta de estado (empaquetada antes del canvas para que no se oculte al achicar la ventana)
        self.lbl_status = tk.Label(self.root, text="> GENERACIÓN: 1 _", bg="#0d1117", fg="#00ffcc", font=("Consolas", 12, "bold"))
        self.lbl_status.pack(side=tk.BOTTOM, pady=5)

        # Canvas para dibujar la cuadrícula
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, 
                                bg="#0d1117", borderwidth=0, highlightthickness=2, highlightbackground="#30363d")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Permitir cambiar el estado de las celdas haciendo clic en ellas
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.canvas.bind("<Configure>", self.on_resize)

    def draw_board(self):
        self.canvas.delete("all")
        
        # Calcular offsets para centrar el tablero
        board_width = self.cols * self.cell_size
        board_height = self.rows * self.cell_size
        canvas_width = max(0, self.canvas.winfo_width() - 4)
        canvas_height = max(0, self.canvas.winfo_height() - 4)
        
        self.offset_x = max(0, (canvas_width - board_width) // 2)
        self.offset_y = max(0, (canvas_height - board_height) // 2)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = self.offset_x + j * self.cell_size
                y1 = self.offset_y + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Neon color for alive, dark background for dead
                color = "#00ffcc" if self.board.grid[i][j] == 1 else "#0d1117"
                outline_color = "#30363d"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline_color)
                
        self.lbl_status.config(text=f"> GENERACIÓN: {len(self.board.history)} _")

    def toggle_cell(self, event):
        # Calculate grid coordinates from click with offsets
        col = (event.x - getattr(self, 'offset_x', 0)) // self.cell_size
        row = (event.y - getattr(self, 'offset_y', 0)) // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.board.grid[row][col] = 1 - self.board.grid[row][col]
            self.draw_board()

    def on_resize(self, event):
        available_width = event.width - 4
        available_height = event.height - 4
        if available_width > 0 and available_height > 0:
            cell_w = available_width // self.cols
            cell_h = available_height // self.rows
            new_size = max(1, min(cell_w, cell_h))
            if new_size != self.cell_size:
                self.cell_size = new_size
                self.draw_board()

    def clear_board(self):
        if self.is_playing:
            self.toggle_play()
        self.board.clear_grid()
        self.draw_board()

    def restart_board(self):
        if self.is_playing:
            self.toggle_play()
        self.board.randomize_grid()
        self.draw_board()

    def next_step(self):
        if not self.board.has_live_cells():
            messagebox.showinfo("Fin", "Todas las células están muertas. Fin de la simulación.")
            self.is_playing = False
            self.btn_play.config(text="Auto Play")
            return

        self.board.next_generation()
        self.draw_board()

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_play.config(text="Pausar")
            self.auto_play()
        else:
            self.btn_play.config(text="Auto Play")

    def auto_play(self):
        if self.is_playing:
            self.next_step()
            if self.is_playing:  # Verificar si se detuvieron
                self.root.after(50, self.auto_play) # 50 ms de delay

    def print_history(self):
        print(f"\nMostrando un total de {len(self.board.history)} cambios de generación\n")
        history_copy = list(self.board.history)
        
        # Imprime los tableros en bloques (ej. de 4 en 4)
        for idx, state in enumerate(history_copy):
            print(f"--- Generación {idx + 1} ---")
            for row in state:
                print(" ".join(map(str, row)))
            print()
        print("Revisa la consola para ver el historial completo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLifeApp(root)
    root.mainloop()
