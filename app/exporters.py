import os
from datetime import datetime
from fpdf import FPDF

EXPORT_FOLDER = "static/exports"
FONT_PATH = "static/fonts/DejaVuSans.ttf"

class PDF(FPDF):
    pass

def save_pdf(layout: list) -> str:
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    if os.path.exists(FONT_PATH):
        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
        pdf.set_font('DejaVu', '', 12)
    else:
        pdf.set_font('Arial', '', 12)

    for panel in layout:
        image_path = panel['image_path']
        story_text = panel['text']
        
        pdf.add_page()
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True, align="C")
        
        y_image = 30
        image_height = 100
        
        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=y_image, w=pdf.w - 20, h=image_height)
        else:
            pdf.set_y(y_image)
            pdf.multi_cell(0, 10, f"Image missing: {image_path}")
            
        pdf.set_y(y_image + image_height + 15)
        story_lines = story_text.strip().splitlines()
        if story_lines and story_lines[0].strip().lower().startswith("**panel"):
            story_lines = story_lines[1:]
        cleaned_text = "\n".join(story_lines).strip()
        pdf.multi_cell(0, 10, cleaned_text)
        
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)
    
    return pdf_path