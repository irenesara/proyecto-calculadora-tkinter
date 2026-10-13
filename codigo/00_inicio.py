"""
Calculadora de escritorio elegante con CustomTkinter.
Diseñada para aprender conceptos esenciales de Python:
- Interfaz gráfica (GUI) con CustomTkinter y layout grid.
- Manejo de entradas del usuario, limpieza de strings y conversiones numéricas.
- Botones interactivos con estado activo/inactivo (+ − × ÷).
- Animación de conteo numérico fluido con after() sin congelar la ventana.
- Manejo de excepciones con try/except (ValueError, ZeroDivisionError).
"""

import math
import customtkinter as ctk

# ==========================================
# PALETA DE COLORES Y CONSTANTES DE DISEÑO
# ==========================================
COLOR_FONDO_VENTANA = "#0b0c10"
COLOR_TARJETA = "#151821"
COLOR_DISPLAY = "#0d0f15"

# Colores de acento (Neón / Brillo)
COLOR_CIAN = "#00e5ff"
COLOR_CIAN_HOVER = "#6effff"
COLOR_BOTON_INACTIVO = "#1f2433"
COLOR_BOTON_INACTIVO_HOVER = "#2a3145"
COLOR_BORDE_NORMAL = "#262b3a"
COLOR_TEXTO_MUTED = "#8a93a5"
COLOR_ROJO_ERROR = "#ff4d6d"

# Variable global para guardar la operación seleccionada
operacion_actual = "+"
diccionario_botones_op = {}
timer_conteo = None


# ==========================================
# LÓGICA MATEMÁTICA
# ==========================================
def calcular(a, b, operacion):
    """
    Realiza la operación aritmética indicada entre dos números 'a' y 'b'.
    Devuelve el resultado numérico.
    Lanza ZeroDivisionError si se divide entre 0 o ValueError si el resultado no es finito.
    """
    if operacion == "+":
        resultado = a + b
    elif operacion in ("-", "−"):
        resultado = a - b
    elif operacion == "×":
        resultado = a * b
    elif operacion == "÷":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        resultado = a / b
    else:
        raise ValueError("Operación no válida")

    # Rechazar NaN o Infinito
    if not math.isfinite(resultado):
        raise ValueError("El resultado no es un número válido")

    return resultado


def formatear_numero(valor):
    """
    Convierte el número a formato legible:
    - Sin decimales si es entero (ej: 15 en lugar de 15,0).
    - Con coma decimal en lugar de punto (ej: 3,5 en lugar de 3.5).
    """
    if valor.is_integer():
        return str(int(valor))
    
    # Redondeamos a máximo 6 decimales para evitar artefactos binarios
    valor_redondeado = round(valor, 6)
    texto = str(valor_redondeado)
    return texto.replace(".", ",")


# ==========================================
# SELECCIÓN DE OPERACIÓN (+ − × ÷)
# ==========================================
def seleccionar_operacion(op):
    """
    Cambia la operación activa e ilumina el botón seleccionado con color cian,
    dejando los demás botones en gris oscuro.
    """
    global operacion_actual
    operacion_actual = op

    for simbolo, boton in diccionario_botones_op.items():
        if simbolo == op:
            boton.configure(
                fg_color=COLOR_CIAN,
                hover_color=COLOR_CIAN_HOVER,
                text_color="#0b0c10",
                border_color=COLOR_CIAN
            )
        else:
            boton.configure(
                fg_color=COLOR_BOTON_INACTIVO,
                hover_color=COLOR_BOTON_INACTIVO_HOVER,
                text_color="#ffffff",
                border_color=COLOR_BORDE_NORMAL
            )


# ==========================================
# ANIMACIONES CON after()
# ==========================================
def animar_conteo(valor_final, paso=0, total_pasos=15):
    """
    Anima el resultado haciendo que los números suban o cambien rápidamente
    desde 0 hasta el valor final en ~400 ms.
    """
    global timer_conteo
    if paso < total_pasos:
        # Interpolación lineal entre 0 y el valor final
        progreso = paso / total_pasos
        valor_intermedio = valor_final * progreso
        
        # Muestra el número temporal
        etiqueta_resultado.configure(
            text=formatear_numero(valor_intermedio),
            text_color=COLOR_CIAN
        )
        # Siguiente paso cada 25 ms (~375-400 ms en total)
        timer_conteo = ventana.after(25, lambda: animar_conteo(valor_final, paso + 1, total_pasos))
    else:
        # Al terminar, mostramos el valor final exacto
        etiqueta_resultado.configure(
            text=formatear_numero(valor_final),
            text_color=COLOR_CIAN
        )
        animar_brillo_exito()


def animar_brillo_exito(paso=0):
    """Parpadeo suave del marco del display al completar un cálculo exitoso."""
    colores = [COLOR_CIAN, "#a259ff", COLOR_CIAN, COLOR_BORDE_NORMAL]
    if paso < len(colores):
        frame_display.configure(border_color=colores[paso])
        ventana.after(100, lambda: animar_brillo_exito(paso + 1))


def animar_borde_error():
    """Pone el borde de la pantalla en rojo temporalmente."""
    frame_display.configure(border_color=COLOR_ROJO_ERROR)
    ventana.after(600, lambda: frame_display.configure(border_color=COLOR_BORDE_NORMAL))


# ==========================================
# CONTROLADORES DE EVENTOS
# ==========================================
def procesar_calculo(event=None):
    """
    Coordina la validación, cálculo y animación:
    1. Lee los campos con get() y strip().
    2. Valida tipos, coma decimal, campos vacíos y math.isfinite.
    3. Calcula y ejecuta la animación de conteo numérico.
    """
    global timer_conteo
    # Cancelar animación previa si estaba en curso
    if timer_conteo:
        ventana.after_cancel(timer_conteo)
        timer_conteo = None

    texto1 = entrada_num1.get().strip()
    texto2 = entrada_num2.get().strip()

    try:
        if not texto1 or not texto2:
            raise ValueError("Por favor, rellena ambos campos")

        # Permitir coma decimal
        num1_limpio = texto1.replace(",", ".")
        num2_limpio = texto2.replace(",", ".")

        num1 = float(num1_limpio)
        num2 = float(num2_limpio)

        if not math.isfinite(num1) or not math.isfinite(num2):
            raise ValueError("Número no válido")

        # Operación matemática
        res = calcular(num1, num2, operacion_actual)

        # Iniciar animación de conteo numérico
        animar_conteo(res)

    except ZeroDivisionError as error:
        etiqueta_resultado.configure(text=str(error), text_color=COLOR_ROJO_ERROR)
        animar_borde_error()

    except ValueError:
        etiqueta_resultado.configure(text="Entrada inválida (solo números)", text_color=COLOR_ROJO_ERROR)
        animar_borde_error()


def limpiar_campos():
    """Borra ambos campos de texto, resetea el display y enfoca el primer campo."""
    global timer_conteo
    if timer_conteo:
        ventana.after_cancel(timer_conteo)
        timer_conteo = None

    entrada_num1.delete(0, "end")
    entrada_num2.delete(0, "end")
    etiqueta_resultado.configure(text="0", text_color=COLOR_TEXTO_MUTED)
    frame_display.configure(border_color=COLOR_BORDE_NORMAL)
    entrada_num1.focus_set()


# Iluminación de campos al ganar o perder foco
def iluminar_foco(widget):
    widget.configure(border_color=COLOR_CIAN)

def apagar_foco(widget):
    widget.configure(border_color=COLOR_BORDE_NORMAL)


# ==========================================
# CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Calculadora")
ventana.geometry("440x530")
ventana.resizable(False, False)
ventana.configure(fg_color=COLOR_FONDO_VENTANA)

# Tarjeta central con esquinas redondeadas y borde neón
tarjeta = ctk.CTkFrame(
    ventana,
    fg_color=COLOR_TARJETA,
    corner_radius=20,
    border_width=2,
    border_color=COLOR_CIAN
)
tarjeta.pack(padx=18, pady=18, fill="both", expand=True)

tarjeta.grid_columnconfigure(0, weight=1)
tarjeta.grid_columnconfigure(1, weight=1)

# 1. CABECERA CON TÍTULO Y SUBTÍTULO
frame_cabecera = ctk.CTkFrame(tarjeta, fg_color="transparent")
frame_cabecera.grid(row=0, column=0, columnspan=2, pady=(16, 8))

titulo = ctk.CTkLabel(
    frame_cabecera,
    text="Calculadora",
    font=("Segoe UI", 24, "bold"),
    text_color=COLOR_CIAN
)
titulo.pack()

subtitulo = ctk.CTkLabel(
    frame_cabecera,
    text="Hecha en Python",
    font=("Segoe UI", 12),
    text_color=COLOR_TEXTO_MUTED
)
subtitulo.pack()

# 2. PANTALLA TIPO DISPLAY (Fuente Consolas / Courier New en negrita)
frame_display = ctk.CTkFrame(
    tarjeta,
    fg_color=COLOR_DISPLAY,
    corner_radius=14,
    border_width=2,
    border_color=COLOR_BORDE_NORMAL
)
frame_display.grid(row=1, column=0, columnspan=2, padx=18, pady=(4, 14), sticky="ew")

etiqueta_resultado = ctk.CTkLabel(
    frame_display,
    text="0",
    font=("Consolas", 28, "bold"),
    text_color=COLOR_TEXTO_MUTED,
    height=55
)
etiqueta_resultado.pack(padx=12, pady=6)

# 3. CAMPOS DE ENTRADA CON SUS ETIQUETAS
# Número 1
label_num1 = ctk.CTkLabel(
    tarjeta,
    text="Número 1",
    font=("Segoe UI", 12, "bold"),
    text_color=COLOR_TEXTO_MUTED
)
label_num1.grid(row=2, column=0, padx=18, pady=(4, 2), sticky="w")

entrada_num1 = ctk.CTkEntry(
    tarjeta,
    placeholder_text="Ej: 12",
    height=38,
    corner_radius=12,
    border_width=2,
    border_color=COLOR_BORDE_NORMAL,
    fg_color="#1a1d28",
    text_color="#ffffff",
    font=("Segoe UI", 14)
)
entrada_num1.grid(row=3, column=0, padx=18, pady=(0, 10), sticky="ew")
entrada_num1.bind("<FocusIn>", lambda e: iluminar_foco(entrada_num1))
entrada_num1.bind("<FocusOut>", lambda e: apagar_foco(entrada_num1))

# Número 2
label_num2 = ctk.CTkLabel(
    tarjeta,
    text="Número 2",
    font=("Segoe UI", 12, "bold"),
    text_color=COLOR_TEXTO_MUTED
)
label_num2.grid(row=2, column=1, padx=18, pady=(4, 2), sticky="w")

entrada_num2 = ctk.CTkEntry(
    tarjeta,
    placeholder_text="Ej: 3",
    height=38,
    corner_radius=12,
    border_width=2,
    border_color=COLOR_BORDE_NORMAL,
    fg_color="#1a1d28",
    text_color="#ffffff",
    font=("Segoe UI", 14)
)
entrada_num2.grid(row=3, column=1, padx=18, pady=(0, 10), sticky="ew")
entrada_num2.bind("<FocusIn>", lambda e: iluminar_foco(entrada_num2))
entrada_num2.bind("<FocusOut>", lambda e: apagar_foco(entrada_num2))

# 4. BOTONES REDONDOS DE OPERACIÓN (+ − × ÷) EN FILA
frame_operaciones = ctk.CTkFrame(tarjeta, fg_color="transparent")
frame_operaciones.grid(row=4, column=0, columnspan=2, pady=(2, 14))

simbolos_operaciones = ["+", "−", "×", "÷"]
for simbolo in simbolos_operaciones:
    btn_op = ctk.CTkButton(
        frame_operaciones,
        text=simbolo,
        width=46,
        height=46,
        corner_radius=23,  # Radio = mitad de ancho/alto -> botón circular
        font=("Segoe UI", 20, "bold"),
        border_width=1,
        border_color=COLOR_BORDE_NORMAL,
        command=lambda s=simbolo: seleccionar_operacion(s)
    )
    btn_op.pack(side="left", padx=7)
    diccionario_botones_op[simbolo] = btn_op

# Seleccionamos '+' por defecto
seleccionar_operacion("+")

# 5. BOTONES "Calcular" y "Limpiar"
boton_calcular = ctk.CTkButton(
    tarjeta,
    text="Calcular",
    command=procesar_calculo,
    height=44,
    corner_radius=14,
    font=("Segoe UI", 14, "bold"),
    fg_color=COLOR_CIAN,
    hover_color=COLOR_CIAN_HOVER,
    text_color="#0b0c10"
)
boton_calcular.grid(row=5, column=0, columnspan=2, padx=18, pady=(2, 6), sticky="ew")

boton_limpiar = ctk.CTkButton(
    tarjeta,
    text="Limpiar",
    command=limpiar_campos,
    height=34,
    corner_radius=12,
    font=("Segoe UI", 12),
    fg_color="transparent",
    hover_color="#1f2433",
    border_width=1,
    border_color=COLOR_BORDE_NORMAL,
    text_color=COLOR_TEXTO_MUTED
)
boton_limpiar.grid(row=6, column=0, columnspan=2, padx=18, pady=(0, 14), sticky="ew")

# Atajo de teclado Enter
ventana.bind("<Return>", procesar_calculo)

# Foco inicial
entrada_num1.focus_set()

# ==========================================
# PUNTO DE ENTRADA PRINCIPAL
# ==========================================
if __name__ == "__main__":
    ventana.mainloop()
