"""
Export calculation results to PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, Optional


class PDFExporter:
    """PDF export service for calculation results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles for PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#0080FF'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#374151'),
            spaceAfter=10,
            leading=16
        ))
    
    def generate_result_pdf(
        self,
        calculator_name: str,
        calculator_category: str,
        input_data: Dict[str, Any],
        result_value: float,
        interpretation: str,
        performed_at: datetime,
        user_name: Optional[str] = None
    ) -> BytesIO:
        """Generate PDF report for calculation result"""
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        
        story = []
        
        # Title
        title = Paragraph("Медицинский калькулятор", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Subtitle with calculator name
        subtitle = Paragraph(f"<b>{calculator_name}</b>", self.styles['CustomSubtitle'])
        story.append(subtitle)
        story.append(Spacer(1, 0.3*cm))
        
        # Metadata
        meta_data = [
            ['Категория:', calculator_category],
            ['Дата расчета:', performed_at.strftime('%d.%m.%Y %H:%M')],
        ]
        if user_name:
            meta_data.append(['Пациент:', user_name])
        
        meta_table = Table(meta_data, colWidths=[5*cm, 10*cm])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6B7280')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 1*cm))
        
        # Result section
        result_header = Paragraph("Результат расчета", self.styles['SectionHeader'])
        story.append(result_header)
        
        result_text = Paragraph(
            f"<font size=20><b>{result_value:.2f}</b></font>",
            self.styles['CustomBody']
        )
        story.append(result_text)
        story.append(Spacer(1, 0.5*cm))
        
        # Interpretation section
        interp_header = Paragraph("Интерпретация", self.styles['SectionHeader'])
        story.append(interp_header)
        
        interp_text = Paragraph(interpretation, self.styles['CustomBody'])
        story.append(interp_text)
        story.append(Spacer(1, 0.8*cm))
        
        # Input parameters section
        params_header = Paragraph("Входные параметры", self.styles['SectionHeader'])
        story.append(params_header)
        
        params_data = [[key.replace('_', ' ').title(), str(value)] 
                       for key, value in input_data.items()]
        
        params_table = Table(params_data, colWidths=[8*cm, 7*cm])
        params_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#E5E7EB')),
        ]))
        story.append(params_table)
        story.append(Spacer(1, 1*cm))
        
        # Disclaimer
        disclaimer_text = Paragraph(
            "<b>Медицинское предупреждение:</b><br/>"
            "Этот результат носит исключительно информационный характер и не должен заменять "
            "профессиональный медицинский совет. Всегда консультируйтесь с квалифицированным "
            "врачом для диагностики и лечения.",
            ParagraphStyle(
                name='Disclaimer',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#6B7280'),
                leftIndent=1*cm,
                rightIndent=1*cm,
                alignment=TA_LEFT,
                leading=12,
                borderColor=colors.HexColor('#0080FF'),
                borderWidth=1,
                borderPadding=10
            )
        )
        story.append(disclaimer_text)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer


# Initialize singleton
pdf_exporter = PDFExporter()
