import openai
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import time

# Load environment variables from .env file
load_dotenv()
# Ensure your API key is in .env

# Math Solution Analyzer Class
class MathSolutionAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key="apiKey")  # Modern client instantiation
        self.model = "gpt-4"  # Specify your model here

    def analyze(self, solution):
        """Analyze the math solution using OpenAI API."""
        prompt = f"""
        You are an AI designed to analyze written math solutions. Your task is to evaluate the solution below based on:
        - Clarity and coherence of reasoning and logic (does it follow a logical flow?).
        - Presentation quality (grammar, formatting, readability).
        Do NOT evaluate the mathematical accuracy. Provide a concise summary, an analysis in bullet points, 
        and assign scores (1-5) for reasoning and presentation. The first statement should be whether there are any inconsistencies or calculation errors. At the ends, rate the solution over 10 and put is score in 3 angle brackets e.g <<<score>>>

        Solution to analyze:
        "{solution}"
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except openai.APIError as e:
            return f"Error: Unable to analyze solution. {str(e)}"

    def format_analysis(self, analysis):
        """Format the analysis as bullet points."""
        lines = analysis.split('\n')
        formatted = "Analysis of the Math Solution:\n"
        for line in lines:
            if line.strip():
                formatted += f"- {line.strip()}\n"
        return formatted

# Desktop App Class
class MathAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Solution Analyzer")
        self.root.geometry("600x500")
        self.analyzer = MathSolutionAnalyzer()

        # GUI Components
        self.label = tk.Label(root, text="Enter your math solution below:")
        self.label.pack(pady=5)

        self.input_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
        self.input_text.pack(pady=5)

        self.analyze_button = tk.Button(root, text="Analyze", command=self.analyze_solution)
        self.analyze_button.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
        self.output_text.pack(pady=5)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_fields)
        self.clear_button.pack(pady=5)

    def analyze_solution(self):
        """Handle the analysis process."""
        solution = self.input_text.get("1.0", tk.END).strip()
        if not solution:
            messagebox.showwarning("Input Error", "Please enter a math solution to analyze.")
            return

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Analyzing...\n")
        self.root.update()

        raw_analysis = self.analyzer.analyze(solution)
        formatted_analysis = self.analyzer.format_analysis(raw_analysis)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, formatted_analysis)

    def clear_fields(self):
        """Clear input and output fields."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

# Main Function to Run the App
def main():
    root = tk.Tk()
    app = MathAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()