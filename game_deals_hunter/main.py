import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.client import CheapSharkClient
from src.processor import DataProcessor
from src.reporter import ExcelReporter

class GameDealsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Deals Hunter")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
  
        style = ttk.Style()
        style.theme_use('clam')
        
   
        title_label = ttk.Label(root, text="Game Deals Hunter", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=20)
        
     
        input_frame = ttk.Frame(root, padding="20")
        input_frame.pack(fill=tk.BOTH, expand=True)
        
   
        ttk.Label(input_frame, text="Max Price ($):").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.price_var = tk.StringVar(value="30")
        ttk.Entry(input_frame, textvariable=self.price_var).grid(row=0, column=1, sticky=tk.EW, pady=10, padx=5)
        
    
        ttk.Label(input_frame, text="Min Metacritic (0-100):").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.score_var = tk.StringVar(value="80")
        ttk.Entry(input_frame, textvariable=self.score_var).grid(row=1, column=1, sticky=tk.EW, pady=10, padx=5)
        
       
        ttk.Label(input_frame, text="Max Results:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.limit_var = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.limit_var).grid(row=2, column=1, sticky=tk.EW, pady=10, padx=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        
        self.search_btn = ttk.Button(root, text="Find Deals", command=self.start_search_thread)
        self.search_btn.pack(pady=10, ipadx=30, ipady=5)
        

        self.status_var = tk.StringVar(value="Ready to hunt!")
        self.status_label = ttk.Label(root, textvariable=self.status_var, font=("Segoe UI", 9, "italic"))
        self.status_label.pack(pady=15)

    def start_search_thread(self):
        """Starts the search in a separate thread to keep UI responsive."""
        thread = threading.Thread(target=self.run_search)
        thread.daemon = True
        thread.start()

    def run_search(self):
        try:
           
            try:
                max_price = int(self.price_var.get())
                min_score = int(self.score_var.get())
                limit = int(self.limit_var.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
                return

            self.update_ui_state(processing=True, message="Searching API...")
            
          
            client = CheapSharkClient()
            processor = DataProcessor()
            reporter = ExcelReporter()
            
           
            raw_data = client.get_deals(
                upper_price=max_price, 
                metacritic=min_score,
                page_size=limit
            )
            
            if not raw_data:
                self.update_ui_state(processing=False, message="No deals found.")
                messagebox.showinfo("Result", "No deals found with these filters.")
                return
                
            self.update_ui_state(processing=True, message=f"Processing {len(raw_data)} deals...")
            
            
            clean_data = processor.process_deals(raw_data)
            reporter.generate_report(clean_data)
            
            self.update_ui_state(processing=False, message="Done! Report generated.")
            messagebox.showinfo("Success", f"Found {len(raw_data)} deals!\nSaved to 'game_deals_report.xlsx' in your project folder.")
            
        except Exception as e:
            self.update_ui_state(processing=False, message="Error occurred.")
            messagebox.showerror("Error", str(e))

    def update_ui_state(self, processing, message):
        """Updates the status label and enables/disables the button."""
        self.status_var.set(message)
        state = "disabled" if processing else "normal"
        self.search_btn.config(state=state)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameDealsApp(root)
    root.mainloop()