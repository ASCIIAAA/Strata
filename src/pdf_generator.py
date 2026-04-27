from fpdf import FPDF
import tempfile

class ArcheologyPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Software Archeology Engine: Legacy App Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(class_stats, god_objects, spaghetti_cycles, dead_code, microservices):
    pdf = ArcheologyPDF()
    pdf.add_page()
    
    # Summary Metrics
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Executive Summary', 0, 1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 10, f'Total Classes Analyzed: {len(class_stats)}', 0, 1)
    pdf.cell(0, 10, f'God Objects Detected: {len(god_objects)}', 0, 1)
    pdf.cell(0, 10, f'Spaghetti Cycles Detected: {len(spaghetti_cycles)}', 0, 1)
    pdf.cell(0, 10, f'Dead Ghost Methods Detected: {len(dead_code)}', 0, 1)
    pdf.cell(0, 10, f'Proposed Microservices Enclaves: {len(microservices)}', 0, 1)
    pdf.ln(5)

    # God Objects
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Phase II: God Object Analysis', 0, 1)
    pdf.set_font('helvetica', '', 10)
    if god_objects:
        for go, details in god_objects.items():
            txt = f"- {str(go)[:50]}: Score: {details.get('score', 0)} (Methods: {details.get('methods', 0)}, Responsibilities: {details.get('responsibilities', 0)})"
            pdf.write(6, txt)
            pdf.ln()
    else:
        pdf.cell(0, 10, 'No God Objects found.', 0, 1)
    pdf.ln(5)
    
    # Dead Code
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Phase III: Behavioral Excavation (Ghost Code)', 0, 1)
    pdf.set_font('helvetica', '', 10)
    if dead_code:
        for m in sorted(dead_code)[:20]:
            pdf.write(6, f"- {str(m)[:80]}")
            pdf.ln()
        if len(dead_code) > 20:
             pdf.cell(0, 6, f"... and {len(dead_code) - 20} more.", 0, 1)
    else:
        pdf.cell(0, 10, 'No Dead Code found!', 0, 1)
    pdf.ln(5)
    
    # Modernization Roadmap
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Phase IV: Modernization Roadmap (Microservice Clustering)', 0, 1)
    pdf.set_font('helvetica', '', 10)
    for i, ms in enumerate(microservices):
        if len(ms) > 0:
            valid_classes = [str(c).replace("\t", "").replace("\n", "") for c in ms]
            chunked = valid_classes[:15]
            classes_str = ", ".join(chunked)
            if len(valid_classes) > 15:
                classes_str += f" ... (+{len(valid_classes)-15} more)"
                
            pdf.write(6, f"Microservice {i+1} Classes: {classes_str}")
            pdf.ln(8)

    temp_file = tempfile.mktemp(suffix=".pdf")
    pdf.output(temp_file)
    return temp_file
