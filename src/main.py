import customtkinter as ctk
import requests
import threading
import math
import colorsys
import sys
from tkinter import messagebox

# 🔴 CLOUD CONFIGURATION
# Replace this with your hosted backend URL once deployed
CLOUD_API_URL = "https://confident-emotional-dependence-dallas.trycloudflare.com"
ctk.set_appearance_mode("dark") # Switched to dark mode for a more futuristic/hacker aesthetic

class PashaQuantumEngine(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pasha Terminal")
        self.geometry("900x750")
        self.configure(fg_color="#0a0a0c") # Deep space black

        self.live_state = "idle" 
        self.initialize_interface()

    def initialize_interface(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # HEADER
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(15, 5))
        
        self.status_lbl = ctk.CTkLabel(self.header_frame, text="🟢 CLOUD UPLINK SECURE", font=("Courier New", 14, "bold"), text_color="#00ffcc")
        self.status_lbl.pack(side="left")

        # TRANSACTION BUTTON
        self.tx_btn = ctk.CTkButton(self.header_frame, text="Initiate Transaction", fg_color="#ff0055", 
                                    hover_color="#cc0044", font=("Courier New", 12, "bold"), 
                                    command=self.open_transaction_terminal)
        self.tx_btn.pack(side="right")

        # CHAT DISPLAY
        self.chat_display = ctk.CTkTextbox(self, fg_color="#121215", border_width=1, border_color="#1f1f23", 
                                           corner_radius=12, font=("Consolas", 14), text_color="#e0e0e0")
        self.chat_display.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.chat_display.configure(state="disabled")

        # FOOTER
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 25))
        self.controls_frame.grid_columnconfigure(1, weight=1)

        # 3D ORB RENDERER
        self.orb_canvas = ctk.CTkCanvas(self.controls_frame, width=60, height=60, bg="#0a0a0c", highlightthickness=0)
        self.orb_canvas.grid(row=0, column=0, padx=(0, 15), sticky="w")

        self.input_box = ctk.CTkEntry(self.controls_frame, height=50, fg_color="#121215", border_width=1, 
                                      border_color="#1f1f23", corner_radius=12, placeholder_text="Command Pasha...", 
                                      font=("Consolas", 14), text_color="#00ffcc")
        self.input_box.grid(row=0, column=1, sticky="ew", padx=(0, 15))
        self.input_box.bind("<Return>", lambda event: self.send_message())

        # MATHEMATICS FOR 3D RENDER
        self.nodes = []
        samples = 200  
        phi = math.pi * (math.sqrt(5.0) - 1.0) 
        for i in range(samples):
            y = 1 - (i / float(samples - 1)) * 2 
            radius = math.sqrt(1 - y * y) 
            theta = phi * i 
            x = math.cos(theta) * radius
            z = math.sin(theta) * radius
            self.nodes.append((x, y, z))

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.global_render_loop()

    def global_render_loop(self):
        """Enhanced High-End Graphic Loop"""
        self.orb_canvas.delete("all")
        speed = 0.03
        self.rot_x += speed
        self.rot_y += speed * 1.5
        cx, cy = 30, 30

        for x, y, z in self.nodes:
            # Vector Rotations
            y1 = y * math.cos(self.rot_x) - z * math.sin(self.rot_x)
            z1 = y * math.sin(self.rot_x) + z * math.cos(self.rot_x)
            x2 = x * math.cos(self.rot_y) + z1 * math.sin(self.rot_y)
            z2 = -x * math.sin(self.rot_y) + z1 * math.cos(self.rot_y)
            
            # Depth Projection
            focal_val = 50.0
            depth = focal_val / (focal_val + z2)
            px = cx + x2 * 20 * depth
            py = cy + y1 * 20 * depth
            
            # Dynamic coloring based on Z-depth (creates 3D shading illusion)
            color_intensity = int(max(50, min(255, 255 * depth)))
            hex_color = f"#{0:02x}{color_intensity:02x}{int(color_intensity*0.8):02x}"
            
            size = max(1, int(3 * depth))
            self.orb_canvas.create_oval(px-size, py-size, px+size, py+size, fill=hex_color, outline="")
            
        self.after(30, self.global_render_loop)

    def send_message(self):
        msg = self.input_box.get().strip()
        if not msg: return
        self.input_box.delete(0, "end")
        self.log_and_append("USER", msg)
        threading.Thread(target=self.dispatch_cloud_api, args=(msg,), daemon=True).start()

    def dispatch_cloud_api(self, msg):
        try:
            # Pointing to the remote cloud server
            r = requests.post(f"{CLOUD_API_URL}/api/chat", json={"message": msg}, timeout=10)
            res = r.json()
            self.after(0, lambda: self.log_and_append("PASHA", res.get("reply", "")))
        except requests.exceptions.RequestException:
            self.after(0, lambda: self.log_and_append("SYSTEM", "Cloud uplink failed. Waiting for connection..."))

    def open_transaction_terminal(self):
        """Simulates requesting a Stripe transaction from the Cloud API"""
        threading.Thread(target=self.process_payment, daemon=True).start()

    def process_payment(self):
        self.log_and_append("SYSTEM", "Initiating Secure Financial Tunnel...")
        try:
            r = requests.post(f"{CLOUD_API_URL}/api/transaction/stripe", json={"amount": 5000}, timeout=10)
            data = r.json()
            self.log_and_append("PASHA-PAY", f"Transaction Ready. Client Secret: {data.get('clientSecret')[:15]}...")
        except:
            self.log_and_append("ERROR", "Payment gateway unreachable.")

    def log_and_append(self, sender, message):
        self.chat_display.configure(state="normal")
        color = "cyan" if sender == "USER" else "#00ffcc" if sender == "PASHA" else "#ff0055"
        self.chat_display.insert("end", f"[{sender}] ", color)
        self.chat_display.insert("end", f"{message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    app = PashaQuantumEngine()
    app.mainloop()