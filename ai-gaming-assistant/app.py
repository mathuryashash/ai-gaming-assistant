import customtkinter as ctk
import threading
from data_collector import record_gameplay
from train import train_model_logic
from play import start_ai_gameplay

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GamingBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("AI Game Assistant")
        self.stop_ai_event = threading.Event()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.frame, text="AI Game Pilot", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.frame, text="Status: Idle", text_color="gray")
        self.status_label.pack(pady=5)

        # 1. Observe Button
        self.btn_observe = ctk.CTkButton(self.frame, text="1. Start Observation Mode", command=self.run_observation, height=40)
        self.btn_observe.pack(pady=10, fill="x", padx=50)

        # 2. Train Button
        self.btn_train = ctk.CTkButton(self.frame, text="2. Train AI Model", command=self.run_training, height=40, fg_color="#E59400", hover_color="#B37400")
        self.btn_train.pack(pady=10, fill="x", padx=50)

        # 3. Play Button
        self.btn_play = ctk.CTkButton(self.frame, text="3. Start AI Gameplay", command=self.run_ai, height=40, fg_color="#2CC985", hover_color="#228B5E")
        self.btn_play.pack(pady=10, fill="x", padx=50)
        
        # Stop Button
        self.btn_stop = ctk.CTkButton(self.frame, text="Stop AI", command=self.stop_ai, fg_color="red", state="disabled")
        self.btn_stop.pack(pady=20)

    def run_observation(self):
        self.status_label.configure(text="Status: Recording... Switch to Game! Press ESC to stop.", text_color="yellow")
        # Run in thread to not freeze UI
        t = threading.Thread(target=self._observation_thread)
        t.start()

    def _observation_thread(self):
        record_gameplay()
        self.status_label.configure(text="Status: Recording Saved.", text_color="green")

    def run_training(self):
        self.status_label.configure(text="Status: Training AI... (Check Terminal)", text_color="orange")
        t = threading.Thread(target=self._training_thread)
        t.start()

    def _training_thread(self):
        result = train_model_logic()
        self.status_label.configure(text=f"Status: Training {result}", text_color="white")

    def run_ai(self):
        self.stop_ai_event.clear()
        self.btn_play.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status_label.configure(text="Status: AI Playing... Switch to Game!", text_color="#2CC985")
        
        t = threading.Thread(target=self._play_thread)
        t.start()

    def _play_thread(self):
        start_ai_gameplay(self.stop_ai_event)
        self.status_label.configure(text="Status: AI Stopped", text_color="gray")
        self.btn_play.configure(state="normal")
        self.btn_stop.configure(state="disabled")

    def stop_ai(self):
        self.stop_ai_event.set()

if __name__ == "__main__":
    app = GamingBotApp()
    app.mainloop()
    