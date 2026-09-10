import os
import time
from fpdf import FPDF

class CrowdReportPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('Arial', 'B', 16)
        self.set_text_color(248, 250, 252)
        self.cell(0, 10, 'REAL-TIME HUMAN DETECTION & CROWD REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(148, 163, 184)
        self.cell(0, 5, f'Generated on: {time.strftime("%Y-%m-%d %H:%M:%S")} | Team 23 - IIIT Kottayam', 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()} | Faster R-CNN Inception v2 Analytics Engine', 0, 0, 'C')

def generate_pdf_report(max_count, avg_count, avg_accuracy, total_frames, crowd_status, enum_plot_path=None, acc_plot_path=None, output_path="Crowd_Report.pdf"):
    pdf = CrowdReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Executive Summary Box
    pdf.set_fill_color(30, 41, 59)
    pdf.set_draw_color(51, 65, 85)
    pdf.rect(10, 38, 190, 45, 'DF')
    
    pdf.set_xy(15, 42)
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, 'EXECUTIVE CROWD METRICS SUMMARY', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(50, 50, 50)
    
    pdf.set_xy(15, 52)
    pdf.cell(90, 7, f'Maximum Humans Detected: {max_count}', 0, 0)
    pdf.cell(90, 7, f'Average Detection Accuracy: {avg_accuracy * 100:.1f}%', 0, 1)
    
    pdf.set_xy(15, 60)
    pdf.cell(90, 7, f'Average Humans / Frame: {avg_count:.2f}', 0, 0)
    pdf.cell(90, 7, f'Total Frames Analyzed: {total_frames}', 0, 1)
    
    pdf.set_xy(15, 68)
    pdf.set_font('Arial', 'B', 11)
    if crowd_status == "High Density":
        pdf.set_text_color(239, 68, 68)
    else:
        pdf.set_text_color(16, 185, 129)
    pdf.cell(180, 7, f'Crowd Density Classification: {crowd_status.upper()}', 0, 1)
    
    pdf.ln(20)
    
    # Analytical Plots Section
    if enum_plot_path and os.path.exists(enum_plot_path):
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 8, '1. Human Enumeration Trend Over Time', 0, 1)
        pdf.image(enum_plot_path, x=15, w=180)
        pdf.ln(10)
        
    if acc_plot_path and os.path.exists(acc_plot_path):
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 8, '2. Model Detection Accuracy Trend Over Time', 0, 1)
        pdf.image(acc_plot_path, x=15, w=180)
        pdf.ln(10)
        
    pdf.output(output_path)
    return output_path
