import customtkinter as ctk
import os
import subprocess

# --- Cores e Estilo ---
BG_CARD = "#2B2B2B"
TEXT_WHITE = "#FFFFFF"
TEXT_GRAY = "#98989D"
ACCENT_BLUE = "#0A84FF"
ACCENT_RED = "#FF453A"
PROGRESS_GREEN = "#32D74B"
BTN_OPEN_COLOR = "#3A3A3C"

class DownloadRow(ctk.CTkFrame):
    def __init__(self, parent, nome_arquivo, caminho_completo, acao_x_callback):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=10)
        self.acao_x_callback = acao_x_callback # Callback genérico para o botão X
        self.caminho_completo = caminho_completo
        
        # Grid
        self.grid_columnconfigure(0, weight=4) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=1) 
        self.grid_columnconfigure(3, weight=1) 
        self.grid_columnconfigure(4, weight=0) 

        # 1. Nome e Barra
        self.frame_info = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_info.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.lbl_nome = ctk.CTkLabel(self.frame_info, text=nome_arquivo, font=("Segoe UI", 13, "bold"), anchor="w", text_color=TEXT_WHITE)
        self.lbl_nome.pack(fill="x")
        
        self.progress = ctk.CTkProgressBar(self.frame_info, height=6, corner_radius=3, progress_color=PROGRESS_GREEN, fg_color="#424242")
        self.progress.set(0)
        self.progress.pack(fill="x", pady=(5,0))

        # 2. Tamanho
        self.lbl_size = ctk.CTkLabel(self, text="0.0 MB", font=("Consolas", 12), text_color=TEXT_GRAY)
        self.lbl_size.grid(row=0, column=1, sticky="w")

        # 3. Velocidade / Status
        self.lbl_speed = ctk.CTkLabel(self, text="0.0 MB/s", font=("Consolas", 12), text_color=ACCENT_BLUE)
        self.lbl_speed.grid(row=0, column=2, sticky="w")

        # 4. ETA / Botão Abrir
        self.lbl_eta = ctk.CTkLabel(self, text="--:--:--", font=("Consolas", 12), text_color=TEXT_GRAY)
        self.lbl_eta.grid(row=0, column=3, sticky="w")

        self.btn_abrir = ctk.CTkButton(self, text="📂 Abrir", font=("Segoe UI", 11, "bold"),
                                       height=24, width=80, corner_radius=6,
                                       fg_color=BTN_OPEN_COLOR, hover_color="#555",
                                       command=self.abrir_local)

        # 5. Botão X (Cancelar/Remover)
        self.btn_cancel = ctk.CTkButton(self, text="✕", width=30, height=30, 
                                        fg_color="transparent", hover_color=ACCENT_RED, 
                                        text_color=TEXT_GRAY, corner_radius=15,
                                        command=self.clique_x)
        self.btn_cancel.grid(row=0, column=4, padx=10)

    def clique_x(self):
        # A lógica real fica no main.py, aqui só chamamos
        self.acao_x_callback()

    def abrir_local(self):
        try:
            if os.path.exists(self.caminho_completo):
                subprocess.Popen(f'explorer /select,"{os.path.abspath(self.caminho_completo)}"')
            else:
                folder = os.path.dirname(self.caminho_completo)
                os.startfile(folder)
        except Exception as e:
            print(f"Erro ao abrir: {e}")

    def update_ui(self, progress, speed_str, size_str, eta_str, status_color=None):
        if progress >= 0: self.progress.set(progress)
        self.lbl_size.configure(text=size_str)

        # Se finalizou (100% ou status Finalizado)
        if progress >= 1.0 or speed_str == "Finalizado":
            self.lbl_speed.configure(text="Concluído", text_color=PROGRESS_GREEN)
            self.lbl_eta.grid_forget()
            self.btn_abrir.grid(row=0, column=3, sticky="w")
            self.btn_cancel.configure(state="normal", text_color="#FFFFFF", hover_color=ACCENT_RED)
        else:
            self.lbl_speed.configure(text=speed_str, text_color=ACCENT_BLUE)
            self.lbl_eta.configure(text=eta_str)
            if status_color:
                self.lbl_eta.configure(text_color=status_color)
                self.btn_cancel.configure(state="normal")