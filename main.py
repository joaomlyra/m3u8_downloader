import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import json
import threading
import requests
import re

from ui_components import DownloadRow, BG_CARD, TEXT_GRAY
from download_engine import DownloadTask

ctk.set_appearance_mode("Dark")
BG_MAIN = "#1E1E1E"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
ICON_PATH = os.path.join(BASE_DIR, "jml.ico")

class JMLApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_MAIN)
        self.title("JML Downloader")
        
        if os.path.exists(ICON_PATH):
            try: self.iconbitmap(ICON_PATH)
            except: pass
        
        config = self.carregar_config()
        self.download_folder = config.get("path", os.path.join(os.path.expanduser("~"), "Downloads"))
        
        if "geometry" in config:
            self.geometry(config["geometry"])
        else:
            self.geometry("750x600")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.opcoes_qualidade = []
        self.links_qualidade = []
        self.tasks = []

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # 1. Topo
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.btn_folder = ctk.CTkButton(self.frame_top, text=f"📂 Salvar em: {self.encurtar(self.download_folder)}", fg_color=BG_CARD, border_width=0, text_color=TEXT_GRAY, hover_color="#3A3A3C", corner_radius=8, height=28, command=self.mudar_pasta)
        self.btn_folder.pack(side="left")

        # 2. Input
        self.frame_input = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_input.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        self.ent_url = ctk.CTkEntry(self.frame_input, placeholder_text="Cole o link .m3u8 aqui...", height=35, corner_radius=10, border_width=0, fg_color=BG_CARD, text_color="white")
        self.ent_url.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_search = ctk.CTkButton(self.frame_input, text="Buscar", command=self.buscar, width=100, height=35, corner_radius=10, fg_color="#0A84FF", hover_color="#0071E3")
        self.btn_search.pack(side="left")

        # 3. Opções
        self.frame_sel = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_sel.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.combo = ctk.CTkComboBox(self.frame_sel, values=["Aguardando Link..."], width=180, state="readonly", corner_radius=10, fg_color=BG_CARD, border_width=0, button_color=BG_CARD)
        self.combo.pack(side="left", padx=(0,10))
        self.btn_add = ctk.CTkButton(self.frame_sel, text="+ Adicionar à Fila", state="disabled", command=self.add_task, height=35, corner_radius=10, fg_color=BG_CARD, hover_color="#3A3A3C", text_color="#0A84FF", font=("Segoe UI", 13, "bold"))
        self.btn_add.pack(side="left", fill="x", expand=True)

        # 4. Cabeçalho
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.header.grid(row=3, column=0, sticky="ew", padx=10, pady=(15,0))
        self.header.grid_columnconfigure(0, weight=4) 
        self.header.grid_columnconfigure(1, weight=1) 
        self.header.grid_columnconfigure(2, weight=1) 
        self.header.grid_columnconfigure(3, weight=1) 
        self.header.grid_columnconfigure(4, weight=0) 
        ctk.CTkLabel(self.header, text="  Nome do Arquivo", text_color=TEXT_GRAY, font=("Segoe UI", 11, "bold"), anchor="w").grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(self.header, text="Tamanho", text_color=TEXT_GRAY, font=("Segoe UI", 11, "bold"), anchor="w").grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(self.header, text="Velocidade", text_color=TEXT_GRAY, font=("Segoe UI", 11, "bold"), anchor="w").grid(row=0, column=2, sticky="ew")
        ctk.CTkLabel(self.header, text="ETA", text_color=TEXT_GRAY, font=("Segoe UI", 11, "bold"), anchor="w").grid(row=0, column=3, sticky="ew")
        ctk.CTkLabel(self.header, text="   ", width=30).grid(row=0, column=4)

        # 5. Lista
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

    def on_closing(self):
        running_tasks = [t for t in self.tasks if self.is_running(t)]
        if running_tasks:
            if messagebox.askokcancel("Sair", "Existem downloads rodando! Eles serão cancelados.\nSair mesmo assim?"):
                for t in self.tasks: t.stop()
                self.salvar_estado_janela()
                self.destroy()
        else:
            self.salvar_estado_janela()
            self.destroy()

    def salvar_estado_janela(self):
        data = { "path": self.download_folder, "geometry": self.geometry() }
        try: 
            with open(CONFIG_FILE, 'w') as f: json.dump(data, f)
        except: pass

    def carregar_config(self):
        if os.path.exists(CONFIG_FILE):
            try: return json.load(open(CONFIG_FILE))
            except: pass
        return {}

    def buscar(self):
        url = self.ent_url.get().strip()
        if not url: return
        self.btn_search.configure(text="...", state="disabled")
        threading.Thread(target=self._th_busca, args=(url,), daemon=True).start()

    def _th_busca(self, url):
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            lines = r.text.splitlines()
            base = url.rsplit("/", 1)[0] + "/"
            self.opcoes_qualidade = []
            self.links_qualidade = []
            for i, l in enumerate(lines):
                if l.startswith("#EXT-X-STREAM-INF"):
                    m = re.search(r'RESOLUTION=(\d+x\d+)', l)
                    q = m.group(1).split('x')[1]+"p" if m else "Original"
                    lnk = lines[i+1] if lines[i+1].startswith("http") else base + lines[i+1]
                    self.opcoes_qualidade.append(q)
                    self.links_qualidade.append(lnk)
            if not self.opcoes_qualidade:
                self.opcoes_qualidade = ["Padrão"]
                self.links_qualidade = [url]
            self.after(0, lambda: self.update_combo(True))
        except:
            self.after(0, lambda: self.update_combo(False))

    def update_combo(self, success):
        self.btn_search.configure(text="Buscar", state="normal")
        if success:
            self.combo.configure(values=self.opcoes_qualidade)
            self.combo.set(self.opcoes_qualidade[0])
            self.btn_add.configure(state="normal", fg_color=BG_CARD, text_color="#0A84FF")
        else:
            self.combo.set("Erro na busca")

    def add_task(self):
        q = self.combo.get()
        if q not in self.opcoes_qualidade: return
        idx = self.opcoes_qualidade.index(q)
        url = self.links_qualidade[idx]
        
        nome = f"video_{q}.mp4"
        c = 0
        while os.path.exists(os.path.join(self.download_folder, nome)):
            c+=1
            nome = f"video_{q}_{c}.mp4"
        
        caminho_completo = os.path.join(self.download_folder, nome)
        
        # Cria a UI e a Lógica separadamente
        row = DownloadRow(self.scroll, nome, caminho_completo, lambda: self.gerenciar_botao_x(task, row))
        row.pack(fill="x", pady=2)
        
        # Cria a Task lógica
        task = DownloadTask(url, caminho_completo, row, self.remove_task_ref)
        self.tasks.append(task)
        task.start()
        
        # Reseta inputs
        self.ent_url.delete(0, 'end')
        self.combo.set("Aguardando...")
        self.btn_add.configure(state="disabled", fg_color=BG_CARD, text_color="gray")

    def gerenciar_botao_x(self, task, row):
        # Lógica Dupla do X: Para ou Remove
        if self.is_running(task):
            task.stop() # 1º Clique: Cancela
        else:
            # 2º Clique (ou se já acabou): Remove da tela e da lista
            if task in self.tasks: self.tasks.remove(task)
            row.destroy()

    def is_running(self, task):
        # Verifica se o processo FFmpeg ainda está ativo
        if task.process and task.process.poll() is None:
            return True
        return False

    def remove_task_ref(self, task):
        # Apenas remove referência se terminar sozinho, sem apagar a UI
        pass 

    def mudar_pasta(self):
        p = filedialog.askdirectory()
        if p:
            self.download_folder = p
            self.btn_folder.configure(text=f"📂 Salvar em: {self.encurtar(p)}")
            self.salvar_estado_janela()

    def encurtar(self, p):
        return "..." + p[-40:] if len(p) > 45 else p

if __name__ == "__main__":
    app = JMLApp()
    app.mainloop()