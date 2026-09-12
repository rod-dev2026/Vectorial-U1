#!/usr/init/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:29:54 2026
@author: Rod Compañ
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pyvista as pv

class CalculoVectorialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora y Graficador de Vectores - Unidad 1 (TecNM Tuxtepec)")
        self.root.geometry("680x710+550+50")
        
        # Estado inicial del tema (True = Dark, False = Light)
        self.dark_mode = True
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.create_widgets()
        self.apply_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            # Paleta Dark / Azul
            self.bg_main = "#1e1e1e"
            self.bg_frame = "#2d2d2d"
            self.fg_light = "#ffffff"
            self.accent_blue = "#007acc"
            self.accent_hover = "#005999"
            self.text_bg = "#252526"
            self.text_fg = "#d4d4d4"
            self.label_fg = "#66b2ff"
            self.pv_bg = "#111111"
            self.pv_grid = "#444444"
            self.theme_btn_text = "☀️ Modo Claro"
        else:
            # Paleta Light / Azul institucional
            self.bg_main = "#f0f2f5"
            self.bg_frame = "#e4e7eb"
            self.fg_light = "#111111"
            self.accent_blue = "#0066cc"
            self.accent_hover = "#004080"
            self.text_bg = "#ffffff"
            self.text_fg = "#000000"
            self.label_fg = "#004080"
            self.pv_bg = "#ffffff"
            self.pv_grid = "#cccccc"
            self.theme_btn_text = "🌙 Modo Oscuro"

        # Aplicar a la ventana principal
        self.root.configure(background=self.bg_main)
        self.theme_btn.config(text=self.theme_btn_text)

        # Configurar estilos ttk
        self.style.configure(".", background=self.bg_main, foreground=self.fg_light, fieldbackground=self.text_bg)
        self.style.configure("TLabel", background=self.bg_main, foreground=self.fg_light)
        self.style.configure("TLabelframe", background=self.bg_frame, foreground=self.label_fg)
        self.style.configure("TLabelframe.Label", background=self.bg_frame, foreground=self.label_fg, font=("Arial", 10, "bold"))
        self.style.configure("TRadiobutton", background=self.bg_frame, foreground=self.fg_light, focuscolor=self.bg_frame)
        self.style.map("TRadiobutton", background=[("active", self.bg_frame)], foreground=[("active", self.label_fg)])
        
        self.style.configure("TButton", background=self.accent_blue, foreground="#ffffff", borderwidth=1, focusthickness=3, focuscolor=self.accent_hover)
        self.style.map("TButton", background=[("active", self.accent_hover), ("pressed", "#00264d")])
        
        self.style.configure("TCombobox", fieldbackground=self.text_bg, foreground=self.fg_light, selectbackground=self.accent_blue, selectforeground="#ffffff")

        # Configurar área de texto explícitamente
        self.text_output.configure(background=self.text_bg, foreground=self.text_fg, insertbackground=self.fg_light)

    def create_widgets(self):
        # Barra superior para el botón de tema
        top_bar = ttk.Frame(self.root)
        top_bar.pack(fill="x", padx=10, pady=5)

        self.theme_btn = ttk.Button(top_bar, text="☀️ Modo Claro", command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=5)

        # Marco de entrada de vectores
        input_frame = ttk.LabelFrame(self.root, text=" Componentes de Vectores y Puntos ")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Vector a / P1 (x1, y1, z1):").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.entry_a = ttk.Entry(input_frame, width=25)
        self.entry_a.insert(0, "1, 2, 3")
        self.entry_a.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(input_frame, text="Vector b / P2 (x2, y2, z2):").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.entry_b = ttk.Entry(input_frame, width=25)
        self.entry_b.insert(0, "4, 1, 2")
        self.entry_b.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(input_frame, text="Vector c / P3 (x3, y3, z3):").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.entry_c = ttk.Entry(input_frame, width=25)
        self.entry_c.insert(0, "2, 3, 5")
        self.entry_c.grid(row=2, column=1, padx=5, pady=4)

        ttk.Label(input_frame, text="Escalar (k) / Parámetro (t):").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.entry_scalar = ttk.Entry(input_frame, width=25)
        self.entry_scalar.insert(0, "2")
        self.entry_scalar.grid(row=3, column=1, padx=5, pady=4)

        # Marco de selección de operandos dinámicos
        sel_frame = ttk.LabelFrame(self.root, text=" Selector de Operandos para Operaciones Binarias / Unarias ")
        sel_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(sel_frame, text="Operando principal (Op1):").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.combo_op1 = ttk.Combobox(sel_frame, values=["a", "b", "c"], width=8, state="readonly")
        self.combo_op1.set("a")
        self.combo_op1.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        ttk.Label(sel_frame, text="Operando secundario (Op2):").grid(row=0, column=2, sticky="w", padx=15, pady=4)
        self.combo_op2 = ttk.Combobox(sel_frame, values=["a", "b", "c"], width=8, state="readonly")
        self.combo_op2.set("b")
        self.combo_op2.grid(row=0, column=3, padx=5, pady=4, sticky="w")

        # Marco de operaciones
        op_frame = ttk.LabelFrame(self.root, text=" Operaciones de la Unidad 1 ")
        op_frame.pack(fill="x", padx=10, pady=5)

        self.operation_var = tk.StringVar(value="Triple Producto Escalar")
        operations = [
            "Graficar Vector Individual (Op1)", "Suma (Op1 + Op2)", "Resta (Op1 - Op2)", 
            "Multiplicacion por Escalar (k*Op1)", "Magnitud y Vector Unitario (Op1)", 
            "Distancia entre Puntos (Op1->Op2)", "Producto Punto y Angulo", "Producto Cruz (Op1 x Op2)", 
            "Ecuacion de la Recta r(t)", "Triple Producto Escalar", "Ecuacion Vectorial del Plano"
        ]

        for i, op in enumerate(operations):
            rb = ttk.Radiobutton(op_frame, text=op, variable=self.operation_var, value=op)
            rb.grid(row=i//2, column=i%2, sticky="w", padx=10, pady=2)

        # Botones de acción
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=6)

        calc_btn = ttk.Button(btn_frame, text="Calcular y Mostrar Resultados", command=self.calcular)
        calc_btn.pack(side="left", expand=True, fill="x", padx=5)

        plot_btn = ttk.Button(btn_frame, text="Graficar en 3D (PyVista)", command=self.graficar_pyvista)
        plot_btn.pack(side="right", expand=True, fill="x", padx=5)

        # Consola de resultados
        result_frame = ttk.LabelFrame(self.root, text=" Resultados Analíticos ")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_output = tk.Text(result_frame, height=5, width=70)
        self.text_output.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.text_output.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_output.configure(yscrollcommand=scrollbar.set)

    def parse_vector(self, text):
        if not text.strip():
            return None
        try:
            return np.array([float(x.strip()) for x in text.split(",")])
        except Exception:
            return None

    def obtener_vector_por_nombre(self, nombre):
        if nombre == "a":
            return self.parse_vector(self.entry_a.get())
        elif nombre == "b":
            return self.parse_vector(self.entry_b.get())
        elif nombre == "c":
            return self.parse_vector(self.entry_c.get())
        return None

    def calcular(self):
        op = self.operation_var.get()
        name1 = self.combo_op1.get()
        name2 = self.combo_op2.get()

        v1 = self.obtener_vector_por_nombre(name1)
        v2 = self.obtener_vector_por_nombre(name2)
        v3 = self.obtener_vector_por_nombre("c")

        if v1 is None:
            messagebox.showerror("Error", f"El vector seleccionado como Operando 1 ('{name1}') es obligatorio y tiene un formato inválido.")
            return

        ops_dos_vectores = [
            "Suma (Op1 + Op2)", "Resta (Op1 - Op2)", "Distancia entre Puntos (Op1->Op2)", 
            "Producto Punto y Angulo", "Producto Cruz (Op1 x Op2)", "Ecuacion de la Recta r(t)"
        ]

        if op in ops_dos_vectores and v2 is None:
            messagebox.showerror("Error", f"La operación '{op}' requiere que el Operando 2 ('{name2}') sea válido.")
            return

        ops_tres_vectores = [
            "Triple Producto Escalar", "Ecuacion Vectorial del Plano"
        ]
        
        if op in ops_tres_vectores and (v2 is None or v3 is None):
            messagebox.showerror("Error", "Esta operación requiere que los vectores b y c estén definidos válidamente.")
            return

        try:
            k = float(self.entry_scalar.get())
        except ValueError:
            k = 1.0

        output = ""

        if op == "Graficar Vector Individual (Op1)":
            mag = np.linalg.norm(v1)
            unit = v1 / mag if mag != 0 else np.zeros_like(v1)
            output = f"Vector Individual [{name1}]: {v1}\nMagnitud ||{name1}|| = {mag:.4f}\nVector Unitario û = {unit}"
            if len(v1) == 3 and mag != 0:
                alpha = np.degrees(np.arccos(np.clip(v1[0]/mag, -1.0, 1.0)))
                beta = np.degrees(np.arccos(np.clip(v1[1]/mag, -1.0, 1.0)))
                gamma = np.degrees(np.arccos(np.clip(v1[2]/mag, -1.0, 1.0)))
                output += f"\nCosenos directores: alpha={alpha:.2f}°, beta={beta:.2f}°, gamma={gamma:.2f}°"

        elif op == "Suma (Op1 + Op2)":
            res = v1 + v2
            output = f"Suma {name1} + {name2} = {res}"

        elif op == "Resta (Op1 - Op2)":
            res = v1 - v2
            output = f"Resta {name1} - {name2} = {res}"

        elif op == "Multiplicacion por Escalar (k*Op1)":
            res = k * v1
            output = f"Multiplicación escalar {k} * {name1} = {res}"

        elif op == "Magnitud y Vector Unitario (Op1)":
            mag = np.linalg.norm(v1)
            unit = v1 / mag if mag != 0 else np.zeros_like(v1)
            output = f"Vector {name1}: {v1}\nMagnitud ||{name1}|| = {mag:.4f}\nVector Unitario û = {unit}"

        elif op == "Distancia entre Puntos (Op1->Op2)":
            dist = np.linalg.norm(v2 - v1)
            output = f"Distancia d({name1}, {name2}) = {dist:.4f}"

        elif op == "Producto Punto y Angulo":
            dot = np.dot(v1, v2)
            mag_1 = np.linalg.norm(v1)
            mag_2 = np.linalg.norm(v2)
            if mag_1 == 0 or mag_2 == 0:
                output = "Error: Magnitud cero encontrada."
            else:
                cos_theta = np.clip(dot / (mag_1 * mag_2), -1.0, 1.0)
                rad = np.arccos(cos_theta)
                deg = np.degrees(rad)
                output = f"Producto Punto ({name1} · {name2}) = {dot}\nÁngulo θ = {rad:.4f} rad ({deg:.2f}°)"

        elif op == "Producto Cruz (Op1 x Op2)":
            if len(v1) != 3 or len(v2) != 3:
                output = "Error: El producto cruz requiere vectores en R3."
            else:
                cross = np.cross(v1, v2)
                output = f"Producto Cruz {name1} x {name2} = {cross}\nMagnitud ||{name1} x {name2}|| = {np.linalg.norm(cross):.4f}"

        elif op == "Ecuacion de la Recta r(t)":
            if len(v1) != 3 or len(v2) != 3:
                output = "Error: Se requieren vectores tridimensionales."
            else:
                r_t = v1 + k * v2
                output = f"Posición en la recta r({k}) usando {name1} como punto inicial y {name2} como dirección = {r_t}"

        elif op == "Triple Producto Escalar":
            a_v = self.obtener_vector_por_nombre("a")
            b_v = self.obtener_vector_por_nombre("b")
            c_v = self.obtener_vector_por_nombre("c")
            if len(a_v) != 3 or len(b_v) != 3 or len(c_v) != 3:
                output = "Error: El triple producto escalar requiere vectores en R3."
            else:
                triple_prod = np.dot(a_v, np.cross(b_v, c_v))
                output = f"Triple Producto Escalar a · (b x c) = {triple_prod:.4f}\n(Volumen del paralelepípedo = {abs(triple_prod):.4f})"

        elif op == "Ecuacion Vectorial del Plano":
            a_v = self.obtener_vector_por_nombre("a")
            b_v = self.obtener_vector_por_nombre("b")
            c_v = self.obtener_vector_por_nombre("c")
            if len(a_v) != 3 or len(b_v) != 3 or len(c_v) != 3:
                output = "Error: La ecuación del plano requiere vectores en R3."
            else:
                n = np.cross(b_v, c_v)
                d_val = np.dot(n, a_v)
                output = f"Punto base P0 = {a_v}\nVector director 1 (u) = {b_v}\nVector director 2 (v) = {c_v}\n"
                output += f"Ecuación Vectorial: r(s, t) = {a_v} + s({b_v}) + t({c_v})\n"
                output += f"Vector Normal (n = u x v) = {n}\n"
                output += f"Ecuación General del Plano: {n[0]}x + {n[1]}y + {n[2]}z = {d_val:.4f}"

        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, output)

    def add_vector_fixed_thickness(self, plotter, start, direction, color, label=""):
        vec = np.array(direction, dtype=float)
        mag = np.linalg.norm(vec)
        if mag < 1e-6:
            return
        
        arrow = pv.Arrow(start=(0, 0, 0), direction=(0, 0, 1), 
                         shaft_radius=0.03, tip_radius=0.08, tip_length=0.25, scale=1.0)
        
        arrow.scale([1.0, 1.0, mag], inplace=True)
        
        z_axis = np.array([0.0, 0.0, 1.0])
        target_dir = vec / mag
        dot = np.dot(z_axis, target_dir)
        
        if abs(dot - 1.0) < 1e-6:
            pass 
        elif abs(dot + 1.0) < 1e-6:
            arrow.rotate_x(180, inplace=True) 
        else:
            axis = np.cross(z_axis, target_dir)
            axis = axis / np.linalg.norm(axis)
            angle = np.degrees(np.arccos(np.clip(dot, -1.0, 1.0)))
            arrow.rotate_vector(axis, angle, inplace=True)
            
        arrow.translate(start, inplace=True)
        
        plotter.add_mesh(arrow, color=color, label=label if label else None)

    def graficar_pyvista(self):
        try:
            name1 = self.combo_op1.get()
            name2 = self.combo_op2.get()
            
            v1 = self.obtener_vector_por_nombre(name1)
            v2 = self.obtener_vector_por_nombre(name2)
            
            a_full = self.obtener_vector_por_nombre("a")
            b_full = self.obtener_vector_por_nombre("b")
            c_full = self.obtener_vector_por_nombre("c")

            try:
                k = float(self.entry_scalar.get())
            except ValueError:
                k = 2.0

            if v1 is None:
                messagebox.showerror("Error", "Defina al menos el vector seleccionado como Operando 1 para graficar.")
                return

            v1_3 = np.array([v1[0], v1[1], v1[2] if len(v1) > 2 else 0.0])
            v2_3 = np.array([v2[0], v2[1], v2[2] if len(v2) > 2 else 0.0]) if v2 is not None else None

            plotter = pv.Plotter()
            # Fondo y rejilla adaptados al modo actual
            plotter.set_background(self.pv_bg)
            plotter.add_axes()
            plotter.show_grid(color=self.pv_grid)
            origin = np.array([0.0, 0.0, 0.0])

            op = self.operation_var.get()

            if op == "Graficar Vector Individual (Op1)":
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")

            elif "Suma" in op and v2_3 is not None:
                sum_vec = v1_3 + v2_3
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")
                self.add_vector_fixed_thickness(plotter, v1_3, v2_3, "#28a745", f"Vector {name2} (en punta de {name1})")
                self.add_vector_fixed_thickness(plotter, origin, sum_vec, "#dc3545", f"Suma ({name1} + {name2})")

            elif "Resta" in op and v2_3 is not None:
                diff_vec = v1_3 - v2_3
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")
                self.add_vector_fixed_thickness(plotter, origin, v2_3, "#28a745", f"Vector {name2}")
                self.add_vector_fixed_thickness(plotter, v2_3, diff_vec, "#e83e8c", f"Resta ({name1} - {name2})")

            elif "Multiplicacion por Escalar" in op:
                scaled_vec = k * v1_3
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector original {name1}")
                self.add_vector_fixed_thickness(plotter, origin, scaled_vec, "#6f42c1", f"Escalar ({k} * {name1})")

            elif "Magnitud y Vector Unitario" in op:
                mag = np.linalg.norm(v1_3)
                unit_vec = v1_3 / mag if mag != 0 else v1_3
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")
                self.add_vector_fixed_thickness(plotter, origin, unit_vec, "#17a2b8", "Vector Unitario (û)")

            elif "Distancia entre Puntos" in op and v2_3 is not None:
                line = pv.Line(v1_3, v2_3)
                tube = line.tube(radius=0.035)
                plotter.add_mesh(tube, color="#fd7e14", label=f"Distancia {name1}->{name2}")
                plotter.add_mesh(pv.Sphere(radius=0.15, center=v1_3), color="#0066cc", label=f"Punto {name1}")
                plotter.add_mesh(pv.Sphere(radius=0.15, center=v2_3), color="#28a745", label=f"Punto {name2}")

            elif "Producto Punto y Angulo" in op and v2_3 is not None:
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")
                self.add_vector_fixed_thickness(plotter, origin, v2_3, "#28a745", f"Vector {name2}")
                mag_2_sq = np.dot(v2_3, v2_3)
                if mag_2_sq > 1e-7:
                    proj = (np.dot(v1_3, v2_3) / mag_2_sq) * v2_3
                    self.add_vector_fixed_thickness(plotter, origin, proj, "#fd7e14", f"Proyeccion de {name1} sobre {name2}")

            elif "Producto Cruz" in op and v2_3 is not None:
                cross_vec = np.cross(v1_3, v2_3)
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")
                self.add_vector_fixed_thickness(plotter, origin, v2_3, "#28a745", f"Vector {name2}")
                self.add_vector_fixed_thickness(plotter, origin, cross_vec, "#fd7e14", f"Producto Cruz ({name1} x {name2})")

            elif "Ecuacion de la Recta" in op and v2_3 is not None:
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Punto inicial r0 ({name1})")
                self.add_vector_fixed_thickness(plotter, v1_3, v2_3, "#28a745", f"Vector director v ({name2})")
                t_vals = np.linspace(-2, 2, 50)
                line_points = np.array([v1_3 + t * v2_3 for t in t_vals])
                line = pv.lines_from_points(line_points)
                plotter.add_mesh(line, color="#dc3545", line_width=3, label="Recta r(t)")

            elif op == "Triple Producto Escalar" and a_full is not None and b_full is not None and c_full is not None:
                a3 = np.array([a_full[0], a_full[1], a_full[2] if len(a_full) > 2 else 0.0])
                b3 = np.array([b_full[0], b_full[1], b_full[2] if len(b_full) > 2 else 0.0])
                c3 = np.array([c_full[0], c_full[1], c_full[2] if len(c_full) > 2 else 0.0])
                
                # Dibujar los 3 vectores desde el origen
                self.add_vector_fixed_thickness(plotter, origin, a3, "#0066cc", "Vector a")
                self.add_vector_fixed_thickness(plotter, origin, b3, "#28a745", "Vector b")
                self.add_vector_fixed_thickness(plotter, origin, c3, "#fd7e14", "Vector c")

                # Generar los 8 vértices del paralelepípedo
                # Vértices: origin, a3, b3, c3, (a3+b3), (a3+c3), (b3+c3), (a3+b3+c3)
                p0 = origin
                p1 = a3
                p2 = b3
                p3 = c3
                p4 = a3 + b3
                p5 = a3 + c3
                p6 = b3 + c3
                p7 = a3 + b3 + c3

                # Aristas del paralelepípedo usando líneas de PyVista
                edges = [
                    (p0, p1), (p0, p2), (p0, p3),
                    (p1, p4), (p1, p5),
                    (p2, p4), (p2, p6),
                    (p3, p5), (p3, p6),
                    (p4, p7), (p5, p7), (p6, p7)
                ]

                for start_pt, end_pt in edges:
                    line_edge = pv.Line(start_pt, end_pt)
                    tube_edge = line_edge.tube(radius=0.02)
                    plotter.add_mesh(tube_edge, color="#6f42c1")

                # Malla volumétrica transparente para visualizar el paralelepípedo sólido
                # Construimos una estructura en malla estructurada para el cubo unitario transformado
                r_vals = np.linspace(0, 1, 10)
                s_vals = np.linspace(0, 1, 10)
                t_vals = np.linspace(0, 1, 10)
                R, S, T = np.meshgrid(r_vals, s_vals, t_vals, indexing='ij')
                
                X = R * a3[0] + S * b3[0] + T * c3[0]
                Y = R * a3[1] + S * b3[1] + T * c3[1]
                Z = R * a3[2] + S * b3[2] + T * c3[2]
                
                sgrid = pv.StructuredGrid(X, Y, Z)
                # Extraer la superficie envolvente del paralelepípedo
                shell = sgrid.extract_surface()
                plotter.add_mesh(shell, color="#6f42c1", opacity=0.3, label="Paralelepípedo (Volumen)")

            elif "Ecuacion Vectorial del Plano" in op and a_full is not None and b_full is not None and c_full is not None:
                a3 = np.array([a_full[0], a_full[1], a_full[2] if len(a_full) > 2 else 0.0])
                b3 = np.array([b_full[0], b_full[1], b_full[2] if len(b_full) > 2 else 0.0])
                c3 = np.array([c_full[0], c_full[1], c_full[2] if len(c_full) > 2 else 0.0])
                self.add_vector_fixed_thickness(plotter, origin, a3, "#0066cc", "Punto P0")
                self.add_vector_fixed_thickness(plotter, a3, b3, "#28a745", "Vector director u")
                self.add_vector_fixed_thickness(plotter, a3, c3, "#fd7e14", "Vector director v")
                
                s_vals = np.linspace(-1.5, 1.5, 20)
                t_vals = np.linspace(-1.5, 1.5, 20)
                S, T = np.meshgrid(s_vals, t_vals)
                X = a3[0] + S * b3[0] + T * c3[0]
                Y = a3[1] + S * b3[1] + T * c3[1]
                Z = a3[2] + S * b3[2] + T * c3[2]
                plane_grid = pv.StructuredGrid(X, Y, Z)
                plotter.add_mesh(plane_grid, color="#0066cc", opacity=0.5, label="Plano r(s,t)")

            else:
                self.add_vector_fixed_thickness(plotter, origin, v1_3, "#0066cc", f"Vector {name1}")

            plotter.add_legend()
            plotter.title = f"Visualizacion 3D - {op}"
            plotter.reset_camera()
            plotter.show()
        except Exception as e:
            messagebox.showerror("Error de Renderizado 3D", f"No se pudo mostrar la gráfica:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculoVectorialApp(root)
    root.mainloop()