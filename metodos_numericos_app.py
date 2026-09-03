import math
import tkinter as tk
from tkinter import ttk


MAX_ITER = 50
TOL = 0.01

INK = "#18202a"
MUTED = "#5b6675"
LINE = "#d9dee7"
PAPER = "#fbfcfe"
PANEL = "#ffffff"
ACCENT = "#0c7a7a"
ACCENT_DARK = "#075e5e"
ACCENT_2 = "#b44b34"
SOFT = "#edf7f6"
WARM = "#fffaf7"


def punto_fijo():
    def g(temp):
        return 18 + 8 * math.exp(-0.15 * temp)

    temp = 20
    rows = []

    for i in range(1, MAX_ITER + 1):
        next_value = g(temp)
        ea = abs((next_value - temp) / next_value) * 100
        rows.append(
            {
                "i": i,
                "x": next_value,
                "fx": next_value - g(next_value),
                "ea": ea,
            }
        )
        if ea <= TOL:
            break
        temp = next_value

    return rows


def newton_raphson():
    def f(time):
        return time**3 - 7 * time - 5

    def df(time):
        return 3 * time**2 - 7

    time = 3
    rows = []

    for i in range(1, MAX_ITER + 1):
        next_value = time - f(time) / df(time)
        ea = abs((next_value - time) / next_value) * 100
        rows.append({"i": i, "x": next_value, "fx": f(next_value), "ea": ea})
        if ea <= TOL:
            break
        time = next_value

    return rows


def secante():
    def f(x_value):
        return math.exp(-x_value) - x_value**2 + 0.2

    x0 = 0
    x1 = 1
    rows = []

    for i in range(1, MAX_ITER + 1):
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        ea = abs((x2 - x1) / x2) * 100
        rows.append({"i": i, "x": x2, "fx": f(x2), "ea": ea})
        if ea <= TOL:
            break
        x0 = x1
        x1 = x2

    return rows


def format_number(value, digits=6):
    if not math.isfinite(value):
        return "-"
    if abs(value) < 0.000001:
        return f"{value:.3e}"
    return f"{value:.{digits}f}"


SOURCE_CODES = {
    "fixed": """def punto_fijo():
    def g(temp):
        return 18 + 8 * math.exp(-0.15 * temp)

    temp = 20
    rows = []

    for i in range(1, 51):
        next_value = g(temp)
        ea = abs((next_value - temp) / next_value) * 100
        rows.append((i, next_value, next_value - g(next_value), ea))
        if ea <= 0.01:
            break
        temp = next_value

    return rows""",
    "newton": """def newton_raphson():
    def f(time):
        return time**3 - 7 * time - 5

    def df(time):
        return 3 * time**2 - 7

    time = 3
    rows = []

    for i in range(1, 51):
        next_value = time - f(time) / df(time)
        ea = abs((next_value - time) / next_value) * 100
        rows.append((i, next_value, f(next_value), ea))
        if ea <= 0.01:
            break
        time = next_value

    return rows""",
    "secant": """def secante():
    def f(x_value):
        return math.exp(-x_value) - x_value**2 + 0.2

    x0 = 0
    x1 = 1
    rows = []

    for i in range(1, 51):
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        ea = abs((x2 - x1) / x2) * 100
        rows.append((i, x2, f(x2), ea))
        if ea <= 0.01:
            break
        x0 = x1
        x1 = x2

    return rows""",
}


PROBLEMS = {
    "fixed": {
        "title": "Metodo de punto fijo - Control de temperatura",
        "description": "Se busca la temperatura de equilibrio de una sala de servidores.",
        "equation": "T = 18 + 8e^(-0.15T),   T0 = 20",
        "rows": punto_fijo(),
        "variable": "T",
        "unit": " C",
        "result_label": "Temperatura",
        "analysis": (
            "Interpretacion: la temperatura se estabiliza cerca de 18.499 C, "
            "dentro de un rango adecuado para operacion continua.\n"
            "Convergencia: g'(T) = -1.2e^(-0.15T); alrededor de la raiz su valor "
            "absoluto es menor que 1, por eso el metodo converge desde T0 = 20."
        ),
    },
    "newton": {
        "title": "Metodo de Newton-Raphson - Sistema de almacenamiento",
        "description": "Se calcula el tiempo positivo de respuesta del sistema.",
        "equation": "f(t) = t^3 - 7t - 5 = 0,   t0 = 3",
        "rows": newton_raphson(),
        "variable": "t",
        "unit": " ms",
        "result_label": "Tiempo",
        "analysis": (
            "Interpretacion: la raiz positiva indica un tiempo promedio de respuesta "
            "de aproximadamente 2.949 ms.\n"
            "Eleccion inicial: t0 = 3 es conveniente porque f(2) < 0, f(3) > 0 "
            "y f'(3) no es cero."
        ),
    },
    "secant": {
        "title": "Metodo de la secante - Rendimiento de servidor",
        "description": (
            "Se estima el nivel de carga normalizado que define el punto de operacion."
        ),
        "equation": "f(x) = e^(-x) - x^2 + 0.2 = 0,   x0 = 0, x1 = 1",
        "rows": secante(),
        "variable": "x",
        "unit": "",
        "result_label": "Carga",
        "analysis": (
            "Interpretacion: el servidor alcanza el punto de operacion en x = 0.80454, "
            "es decir, cerca del 80.45% de carga normalizada.\n"
            "Eleccion inicial: se usan x0 = 0 y x1 = 1 porque f(0) > 0 y f(1) < 0; "
            "el cambio de signo encierra la raiz."
        ),
    },
}


class ScrollFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg=PAPER, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, style="Page.TFrame")

        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._fit_inner_width)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _fit_inner_width(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class NumericMethodsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metodos Numericos - Sesion 3")
        self.geometry("1120x760")
        self.minsize(860, 620)
        self.configure(bg=PAPER)
        self.source_windows = {}

        self._configure_styles()
        self._build_header()
        self.scroll = ScrollFrame(self)
        self.scroll.pack(fill="both", expand=True)
        self.solution_container = ttk.Frame(self.scroll.inner, style="Page.TFrame")

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Page.TFrame", background=PAPER)
        style.configure("Panel.TFrame", background=PANEL, relief="solid", borderwidth=1)
        style.configure("PanelBody.TFrame", background=PANEL)
        style.configure("Soft.TFrame", background=SOFT)
        style.configure("Warm.TFrame", background=WARM)
        style.configure("Title.TLabel", background=PAPER, foreground=INK, font=("Arial", 22, "bold"))
        style.configure("Subtitle.TLabel", background=PAPER, foreground=MUTED, font=("Arial", 11))
        style.configure("PanelTitle.TLabel", background=PANEL, foreground=INK, font=("Arial", 13, "bold"))
        style.configure("Text.TLabel", background=PANEL, foreground=INK, font=("Arial", 10))
        style.configure("Muted.TLabel", background=PANEL, foreground=MUTED, font=("Arial", 10))
        style.configure("Equation.TLabel", background="#f8fbfd", foreground=INK, font=("Courier New", 10))
        style.configure("FactTitle.TLabel", background=PANEL, foreground=MUTED, font=("Arial", 8, "bold"))
        style.configure("FactValue.TLabel", background=PANEL, foreground=INK, font=("Arial", 11, "bold"))
        style.configure("SectionTitle.TLabel", background=PANEL, foreground=INK, font=("Arial", 11, "bold"))
        style.configure("Analysis.TLabel", background=WARM, foreground=INK, font=("Arial", 10))
        style.configure("Resolve.TButton", font=("Arial", 11, "bold"), padding=(16, 9))
        style.map("Resolve.TButton", background=[("active", ACCENT_DARK)], foreground=[("active", "#ffffff")])
        style.configure(
            "Treeview",
            rowheight=25,
            font=("Arial", 9),
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=INK,
        )
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"), foreground=MUTED, background="#f5f7fa")

    def _build_header(self):
        header = tk.Frame(self, bg=PAPER, highlightbackground=LINE, highlightthickness=1)
        header.pack(fill="x")

        content = ttk.Frame(header, style="Page.TFrame", padding=(36, 24, 36, 18))
        content.pack(fill="x")

        ttk.Label(content, text="Raices de ecuaciones no lineales", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            content,
            text=(
                "Punto fijo, Newton-Raphson y secante con error relativo porcentual "
                "menor o igual a 0.01%."
            ),
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        resolve_button = tk.Button(
            content,
            text="Resolver",
            command=self.show_solution,
            bg=ACCENT,
            fg="#ffffff",
            activebackground=ACCENT_DARK,
            activeforeground="#ffffff",
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2",
            font=("Arial", 11, "bold"),
        )
        resolve_button.pack(anchor="w")

    def show_solution(self):
        if self.solution_container.winfo_ismapped():
            self.solution_container.focus_set()
            return

        self.solution_container.pack(fill="both", expand=True, padx=34, pady=(24, 34))
        for problem_id, data in PROBLEMS.items():
            self._build_problem_panel(self.solution_container, problem_id, data)

        note = ttk.Label(
            self.solution_container,
            text=(
                "Criterio de parada aplicado: error relativo aproximado menor o igual "
                "a 0.01% o maximo de 50 iteraciones."
            ),
            style="Subtitle.TLabel",
        )
        note.pack(anchor="w", pady=(2, 0))
        self.after(100, lambda: self.scroll.canvas.yview_moveto(0.0))

    def _build_problem_panel(self, parent, problem_id, data):
        panel = tk.Frame(parent, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        panel.pack(fill="x", pady=(0, 20))

        head = ttk.Frame(panel, style="PanelBody.TFrame", padding=18)
        head.pack(fill="x")
        head.columnconfigure(0, weight=3)
        head.columnconfigure(1, weight=2)

        info = ttk.Frame(head, style="PanelBody.TFrame")
        info.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        ttk.Label(info, text=data["title"], style="PanelTitle.TLabel").pack(anchor="w")
        ttk.Label(info, text=data["description"], style="Text.TLabel").pack(anchor="w", pady=(5, 6))
        equation = ttk.Label(info, text=data["equation"], style="Equation.TLabel", padding=(10, 7))
        equation.pack(anchor="w")

        facts_frame = ttk.Frame(head, style="PanelBody.TFrame")
        facts_frame.grid(row=0, column=1, sticky="nsew")
        facts_frame.columnconfigure(0, weight=1)
        facts_frame.columnconfigure(1, weight=1)
        self._build_facts(facts_frame, data)

        separator = ttk.Separator(panel, orient="horizontal")
        separator.pack(fill="x")

        body = ttk.Frame(panel, style="PanelBody.TFrame", padding=18)
        body.pack(fill="x")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        chart_box = ttk.Frame(body, style="PanelBody.TFrame")
        chart_box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ttk.Label(chart_box, text="Grafica de convergencia", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 8))
        chart = tk.Canvas(chart_box, height=280, bg="#ffffff", highlightbackground=LINE, highlightthickness=1)
        chart.pack(fill="x")
        chart.bind("<Configure>", lambda event, rows=data["rows"]: self._draw_chart(event.widget, rows))

        table_box = ttk.Frame(body, style="PanelBody.TFrame")
        table_box.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ttk.Label(table_box, text="Tabla de iteraciones", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self._build_table(table_box, data)

        analysis = tk.Label(
            body,
            text=data["analysis"],
            bg=WARM,
            fg=INK,
            justify="left",
            anchor="w",
            wraplength=980,
            padx=14,
            pady=12,
            font=("Arial", 10),
            highlightbackground=LINE,
            highlightthickness=1,
        )
        analysis.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(16, 12))

        source_button = tk.Button(
            body,
            text="Codigo fuente comentado",
            command=lambda key=problem_id: self._show_source_window(key),
            bg="#f9fbfd",
            fg=INK,
            activebackground=SOFT,
            relief="solid",
            bd=1,
            padx=12,
            pady=8,
            cursor="hand2",
            font=("Arial", 10, "bold"),
        )
        source_button.grid(row=2, column=0, columnspan=2, sticky="ew")

    def _build_facts(self, parent, data):
        last = data["rows"][-1]
        values = [
            (data["result_label"], f"{format_number(last['x'])}{data['unit']}"),
            ("Iteraciones", str(len(data["rows"]))),
            (f"f({data['variable']})", format_number(last["fx"], 8)),
            ("Error final", f"{format_number(last['ea'], 6)}%"),
        ]

        for index, (label, value) in enumerate(values):
            frame = tk.Frame(parent, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
            frame.grid(row=index // 2, column=index % 2, sticky="nsew", padx=5, pady=5)
            frame.columnconfigure(0, weight=1)
            tk.Label(
                frame,
                text=label.upper(),
                bg=PANEL,
                fg=MUTED,
                font=("Arial", 8, "bold"),
                anchor="w",
            ).pack(fill="x", padx=10, pady=(9, 2))
            tk.Label(
                frame,
                text=value,
                bg=PANEL,
                fg=INK,
                font=("Arial", 11, "bold"),
                anchor="w",
            ).pack(fill="x", padx=10, pady=(0, 9))

    def _build_table(self, parent, data):
        columns = ("i", "x", "fx", "ea")
        table = ttk.Treeview(parent, columns=columns, show="headings", height=max(4, len(data["rows"])))
        table.heading("i", text="i")
        table.heading("x", text=data["variable"])
        table.heading("fx", text=f"f({data['variable']})")
        table.heading("ea", text="ea (%)")
        table.column("i", width=42, anchor="center", stretch=False)
        table.column("x", width=120, anchor="e")
        table.column("fx", width=130, anchor="e")
        table.column("ea", width=120, anchor="e")

        for row in data["rows"]:
            table.insert(
                "",
                "end",
                values=(
                    row["i"],
                    format_number(row["x"], 6),
                    format_number(row["fx"], 8),
                    format_number(row["ea"], 6),
                ),
            )

        table.pack(fill="both", expand=True)

    def _draw_chart(self, canvas, rows):
        width = max(canvas.winfo_width(), 420)
        height = max(canvas.winfo_height(), 260)
        pad_left = 74
        pad_right = 28
        pad_top = 36
        pad_bottom = 48
        plot_width = width - pad_left - pad_right
        plot_height = height - pad_top - pad_bottom

        errors = [max(row["ea"], 0.000001) for row in rows]
        min_log = math.floor(math.log10(min(errors)))
        max_log = math.ceil(math.log10(max(errors)))
        log_span = max(1, max_log - min_log)

        canvas.delete("all")
        canvas.create_rectangle(0, 0, width, height, fill="#ffffff", outline="")

        for step in range(log_span + 1):
            log_value = min_log + step
            y = pad_top + plot_height - ((log_value - min_log) / log_span) * plot_height
            canvas.create_line(pad_left, y, width - pad_right, y, fill=LINE)
            canvas.create_text(30, y, text=f"1e{log_value}", fill=MUTED, font=("Arial", 9), anchor="w")

        canvas.create_line(pad_left, pad_top, pad_left, height - pad_bottom, fill=INK)
        canvas.create_line(pad_left, height - pad_bottom, width - pad_right, height - pad_bottom, fill=INK)

        def x_for(index):
            if len(rows) == 1:
                return pad_left + plot_width / 2
            return pad_left + (index / (len(rows) - 1)) * plot_width

        def y_for(error):
            return pad_top + plot_height - ((math.log10(error) - min_log) / log_span) * plot_height

        points = []
        for index, error in enumerate(errors):
            points.extend((x_for(index), y_for(error)))

        if len(points) >= 4:
            canvas.create_line(*points, fill=ACCENT, width=3, smooth=True)

        for index, error in enumerate(errors):
            x_pos = x_for(index)
            y_pos = y_for(error)
            canvas.create_oval(x_pos - 5, y_pos - 5, x_pos + 5, y_pos + 5, fill=ACCENT_2, outline=ACCENT_2)
            canvas.create_text(x_pos, height - 24, text=str(rows[index]["i"]), fill=INK, font=("Arial", 9))

        canvas.create_text(pad_left, 16, text="ea (%) - escala log", fill=INK, font=("Arial", 11, "bold"), anchor="w")
        canvas.create_text(
            pad_left + plot_width / 2,
            height - 8,
            text="Iteracion",
            fill=INK,
            font=("Arial", 9),
        )

    def _show_source_window(self, problem_id):
        existing = self.source_windows.get(problem_id)
        if existing and existing.winfo_exists():
            existing.lift()
            return

        window = tk.Toplevel(self)
        window.title("Codigo fuente comentado")
        window.geometry("720x520")
        window.configure(bg=PAPER)
        self.source_windows[problem_id] = window

        text = tk.Text(
            window,
            bg="#ffffff",
            fg=INK,
            insertbackground=INK,
            wrap="none",
            font=("Courier New", 10),
            padx=12,
            pady=12,
        )
        text.insert("1.0", SOURCE_CODES[problem_id])
        text.configure(state="disabled")
        text.pack(fill="both", expand=True, padx=14, pady=14)


if __name__ == "__main__":
    app = NumericMethodsApp()
    app.mainloop()
