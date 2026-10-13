import tkinter as tk

class LCDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hello World LCD")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        # Constantes de colores para el LCD estilo GameBoy clásico
        self.LCD_BG = "#9bbc0f"       # Verde clásico LCD
        self.LCD_FG = "#0f380f"       # Verde muy oscuro para los caracteres
        self.LCD_BORDER = "#8bac0f"   # Tono intermedio

        # Estados y variables de animación
        self.cursor_visible = True
        self.is_typing = False
        self.current_text = ""
        self.full_text = "Hello World!"
        self.cursor_timer = None
        self.typing_timer = None

        # Construcción de la interfaz
        self._crear_pantalla_lcd()
        self._crear_boton_canvas()

        # Iniciar el parpadeo del cursor inicial
        self._parpadear_cursor()

    def _crear_pantalla_lcd(self):
        """Crea el marco exterior y la pantalla LCD con borde en relieve."""
        # Marco exterior oscuro para simular el bisel del dispositivo
        outer_frame = tk.Frame(
            self.root,
            bg="#1e1e1e",
            bd=6,
            relief="ridge"
        )
        outer_frame.pack(padx=25, pady=(25, 15), fill="x")

        # Contenedor interior de la pantalla LCD
        lcd_container = tk.Frame(
            outer_frame,
            bg=self.LCD_BG,
            bd=4,
            relief="sunken"
        )
        lcd_container.pack(fill="both", expand=True)

        # Etiqueta que muestra el texto simulando la matriz LCD
        self.lcd_label = tk.Label(
            lcd_container,
            text="_",
            font=("Courier", 20, "bold"),
            bg=self.LCD_BG,
            fg=self.LCD_FG,
            height=3,
            anchor="center"
        )
        self.lcd_label.pack(fill="both", expand=True, padx=10, pady=5)

    def _crear_boton_canvas(self):
        """Crea el botón rojo redondo usando un Canvas para simular volumen y efectos 3D."""
        self.canvas_size = 140
        self.btn_canvas = tk.Canvas(
            self.root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#2b2b2b",
            highlightthickness=0,
            cursor="hand2"
        )
        self.btn_canvas.pack(pady=(10, 20))

        # Dibujar botón en estado normal
        self._dibujar_boton(pressed=False)

        # Vincular eventos de ratón
        self.btn_canvas.bind("<ButtonPress-1>", self._on_press)
        self.btn_canvas.bind("<ButtonRelease-1>", self._on_release)

    def _dibujar_boton(self, pressed=False):
        """Dibuja el botón con sombra, cuerpo circular y brillo simulado."""
        self.btn_canvas.delete("all")

        # Parámetros geométricos
        r = 50                 # Radio del círculo (~100 px de diámetro)
        cx = self.canvas_size // 2
        cy = self.canvas_size // 2
        offset = 3 if pressed else 0  # Desplazamiento hacia abajo al presionar

        # Colores del botón
        color_base = "#9a0007" if pressed else "#d32f2f"  # Rojo más oscuro al presionar
        color_borde = "#600000" if pressed else "#800c0c"
        color_sombra = "#141414"

        # 1. Sombra inferior (más visible cuando no está presionado)
        if not pressed:
            self.btn_canvas.create_oval(
                cx - r, cy - r + 5,
                cx + r, cy + r + 5,
                fill=color_sombra,
                outline=""
            )

        # 2. Borde exterior oscuro
        self.btn_canvas.create_oval(
            cx - r - 2, cy - r - 2 + offset,
            cx + r + 2, cy + r + 2 + offset,
            fill=color_borde,
            outline=""
        )

        # 3. Cuerpo principal del botón
        self.btn_canvas.create_oval(
            cx - r, cy - r + offset,
            cx + r, cy + r + offset,
            fill=color_base,
            outline=""
        )

        # 4. Brillo curvo superior para dar volumen 3D
        # Al estar presionado, el brillo se hace más sutil/pequeño
        brillo_color = "#e57373" if pressed else "#ff867c"
        self.btn_canvas.create_oval(
            cx - r + 16, cy - r + 8 + offset,
            cx + r - 16, cy - 8 + offset,
            fill=brillo_color,
            outline=""
        )
        # Tapa interior para formar una medialuna/reflejo suave
        self.btn_canvas.create_oval(
            cx - r + 17, cy - r + 13 + offset,
            cx + r - 17, cy - 3 + offset,
            fill=color_base,
            outline=""
        )

        # 5. Punto de reflejo blanco destacado en la parte superior
        if not pressed:
            self.btn_canvas.create_oval(
                cx - 15, cy - r + 12,
                cx + 15, cy - r + 22,
                fill="#ffffff",
                outline=""
            )

    def _on_press(self, event):
        """Maneja el evento de pulsar el botón (efecto visual hundido)."""
        self._dibujar_boton(pressed=True)

    def _on_release(self, event):
        """Maneja el evento de soltar el botón (restaura estado y dispara la acción)."""
        self._dibujar_boton(pressed=False)
        self._iniciar_efecto_texto()

    def _parpadear_cursor(self):
        """Mantiene el cursor '_' parpadeando cuando no se está escribiendo texto activo."""
        if not self.is_typing and not self.current_text:
            self.cursor_visible = not self.cursor_visible
            self.lcd_label.config(text="_" if self.cursor_visible else " ")
            self.cursor_timer = self.root.after(500, self._parpadear_cursor)

    def _iniciar_efecto_texto(self):
        """Reinicia la pantalla y comienza a escribir 'Hello World!' carácter a carácter."""
        # Cancelar temporizadores previos si existen
        if self.cursor_timer:
            self.root.after_cancel(self.cursor_timer)
            self.cursor_timer = None
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
            self.typing_timer = None

        self.is_typing = True
        self.current_text = ""
        self.lcd_label.config(text="")
        self._escribir_caracter(0)

    def _escribir_caracter(self, index):
        """Escribe un carácter tras otro usando after() a ~80ms."""
        if index < len(self.full_text):
            self.current_text += self.full_text[index]
            # Muestra el texto actual con un cursor al final durante la escritura
            self.lcd_label.config(text=self.current_text + "_")
            self.typing_timer = self.root.after(80, lambda: self._escribir_caracter(index + 1))
        else:
            # Terminado de escribir, dejamos el texto final limpio
            self.lcd_label.config(text=self.current_text)
            self.is_typing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = LCDApp(root)
    root.mainloop()

