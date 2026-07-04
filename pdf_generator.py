# pdf_generator.py
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License")

import re
from fpdf import FPDF

class ProfessionalPDF(FPDF):
    def header(self):
        # Header title
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(100, 116, 139)  # Muted gray
        self.cell(0, 10, 'Marketing Strategy & Campaign Copies', border=False, align='L')
        self.set_draw_color(226, 232, 240)  # Light border
        self.line(10, 18, 200, 18)
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)  # Muted gray
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def sanitize_for_pdf(text: str) -> str:
    """
    Replaces common non-latin-1 punctuation with safe alternatives
    and strips emojis to prevent FPDF Unicode Encoding exceptions.
    """
    replacements = {
        '\u201c': '"', '\u201d': '"',
        '\u2018': "'", '\u2019': "'",
        '\u2013': '-', '\u2014': '-',
        '\u2022': '*',
        '\u2026': '...',
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    
    # Keep only characters within the latin-1 range (0-255)
    sanitized_chars = []
    for char in text:
        if ord(char) < 256:
            sanitized_chars.append(char)
        else:
            # Replace emojis and complex Unicode chars with spaces or empty strings
            if char.isspace():
                sanitized_chars.append(char)
    return "".join(sanitized_chars)

def markdown_to_html(md_text: str) -> str:
    """
    Converts basic Markdown syntax (headers, bold, lists) to basic HTML tags.
    """
    # Escape simple HTML markers first
    html = md_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Headers
    html = re.sub(r'^###\s+(.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s+(.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s+(.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold / Italics
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
    html = re.sub(r'__(.*?)__', r'<b>\1</b>', html)
    html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', html)
    html = re.sub(r'_(.*?)_', r'<i>\1</i>', html)
    
    # Lists
    lines = html.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            item_text = stripped[2:]
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{item_text}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            
            # Non-empty paragraphs
            if stripped and not stripped.startswith('<h') and not stripped.startswith('<u') and not stripped.startswith('</u') and not stripped.startswith('<l'):
                new_lines.append(f'<p>{line}</p>')
            else:
                new_lines.append(line)
                
    if in_list:
        new_lines.append('</ul>')
        
    html = '\n'.join(new_lines)
    html = html.replace('\n\n', '<br/>')
    return html

def generate_pdf(client_name: str, content: str) -> bytes:
    """
    Generates a beautifully styled, professional PDF from marketing copies.
    """
    sanitized_client_name = sanitize_for_pdf(client_name)
    sanitized_content = sanitize_for_pdf(content)
    
    pdf = ProfessionalPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Subtitle with Client Info
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42)  # Slate-900
    pdf.cell(0, 10, f'Marketing Campaign Strategy', new_x="LMARGIN", new_y="NEXT", align='L')
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(71, 85, 105)  # Slate-600
    pdf.cell(0, 8, f'Client: {sanitized_client_name}', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.ln(6)
    
    # Set main body font rules
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(51, 65, 85)  # Slate-700
    
    # Render parsed HTML body
    html_content = markdown_to_html(sanitized_content)
    pdf.write_html(html_content)
    
    return bytes(pdf.output())
