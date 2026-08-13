import tkinter as tk
from tkinter import ttk, messagebox

# ===================== FUNCIONES DE CONVERSIÓN =====================

def convertir_longitud_metrica(valor, origen, destino):
    a_metros = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
    de_metros = {"mm": 1000.0, "cm": 100.0, "m": 1.0, "km": 0.001}
    if origen not in a_metros or destino not in de_metros:
        return None
    return valor * a_metros[origen] * de_metros[destino]


def convertir_masa(valor, origen, destino):
    a_gramos = {"mg": 0.001, "g": 1.0, "kg": 1000.0}
    de_gramos = {"mg": 1000.0, "g": 1.0, "kg": 0.001}
    if origen not in a_gramos or destino not in de_gramos:
        return None
    return valor * a_gramos[origen] * de_gramos[destino]


def convertir_tiempo(valor, origen, destino):
    a_segundos = {"ms": 0.001, "s": 1.0}
    de_segundos = {"ms": 1000.0, "s": 1.0}
    if origen not in a_segundos or destino not in de_segundos:
        return None
    return valor * a_segundos[origen] * de_segundos[destino]


def convertir_longitud_otros(valor, origen, destino):
    a_metros = {
        "m": 1.0,
        "km": 1000.0,
        "millas": 1609.344,
        "pies": 0.3048,
        "pulgadas": 0.0254
    }
    de_metros = {
        "m": 1.0,
        "km": 0.001,
        "millas": 1 / 1609.344,
        "pies": 1 / 0.3048,
        "pulgadas": 1 / 0.0254
    }
    if origen not in a_metros or destino not in de_metros:
        return None
    return valor * a_metros[origen] * de_metros[destino]


# ===================== INTERFAZ GRÁFICA =====================

class ConversorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Unidades - Actividad IA")
        self.root.geometry("480x420")
        self.root.resizable(False, False)

        # Título
        titulo = tk.Label(root, text="Conversor de Unidades", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # Selector de tipo de conversión
        tk.Label(root, text="Tipo de conversión:", font=("Arial", 11)).pack()
        self.tipo = ttk.Combobox(root, values=[
            "1. Longitud métrica (mm, cm, m, km)",
            "2. Masa (mg, g, kg)",
            "3. Tiempo (ms, s)",
            "4. Longitud otros sistemas (m, km, millas, pies, pulgadas)"
        ], state="readonly", width=50)
        self.tipo.current(0)
        self.tipo.pack(pady=5)
        self.tipo.bind("<<ComboboxSelected>>", self.actualizar_unidades)

        # Valor
        tk.Label(root, text="Valor:", font=("Arial", 11)).pack(pady=(15, 0))
        self.entrada_valor = tk.Entry(root, font=("Arial", 12), width=20, justify="center")
        self.entrada_valor.pack(pady=5)

        # Unidades
        frame_unidades = tk.Frame(root)
        frame_unidades.pack(pady=10)

        tk.Label(frame_unidades, text="De:", font=("Arial", 11)).grid(row=0, column=0, padx=10)
        self.origen = ttk.Combobox(frame_unidades, state="readonly", width=12)
        self.origen.grid(row=0, column=1, padx=5)

        tk.Label(frame_unidades, text="A:", font=("Arial", 11)).grid(row=0, column=2, padx=10)
        self.destino = ttk.Combobox(frame_unidades, state="readonly", width=12)
        self.destino.grid(row=0, column=3, padx=5)

        # Botón convertir
        btn = tk.Button(root, text="Convertir", font=("Arial", 12, "bold"),
                        bg="#4CAF50", fg="white", width=15, command=self.convertir)
        btn.pack(pady=15)

        # Resultado
        self.resultado = tk.Label(root, text="", font=("Arial", 13), fg="#1565C0", wraplength=420)
        self.resultado.pack(pady=10)

        # Cargar unidades iniciales
        self.actualizar_unidades()

    def actualizar_unidades(self, event=None):
        opcion = self.tipo.current()
        if opcion == 0:
            unidades = ["mm", "cm", "m", "km"]
        elif opcion == 1:
            unidades = ["mg", "g", "kg"]
        elif opcion == 2:
            unidades = ["ms", "s"]
        else:
            unidades = ["m", "km", "millas", "pies", "pulgadas"]

        self.origen["values"] = unidades
        self.destino["values"] = unidades
        self.origen.current(0)
        self.destino.current(1 if len(unidades) > 1 else 0)

    def convertir(self):
        try:
            valor = float(self.entrada_valor.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")
            return

        origen = self.origen.get()
        destino = self.destino.get()
        opcion = self.tipo.current()

        if opcion == 0:
            res = convertir_longitud_metrica(valor, origen, destino)
        elif opcion == 1:
            res = convertir_masa(valor, origen, destino)
        elif opcion == 2:
            res = convertir_tiempo(valor, origen, destino)
        else:
            res = convertir_longitud_otros(valor, origen, destino)

        if res is None:
            messagebox.showerror("Error", "Unidades no válidas.")
            return

        # Redondear de forma inteligente
        if res == int(res):
            texto = f"{valor} {origen} = {int(res)} {destino}"
        else:
            texto = f"{valor} {origen} = {round(res, 6)} {destino}"

        self.resultado.config(text=texto)


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorApp(root)
    root.mainloop()