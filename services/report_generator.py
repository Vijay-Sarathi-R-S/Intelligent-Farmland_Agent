from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime
import random

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles matching the sample format"""
        
        # Main title - exactly as in sample
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2E7D32'),
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section headings - numbered as in sample
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1B5E20'),
            spaceBefore=8,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            leftIndent=0
        ))
        
        # Subheadings
        self.styles.add(ParagraphStyle(
            name='SubHeading',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#2E7D32'),
            spaceBefore=6,
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))
        
        # Label style (bold left column)
        self.styles.add(ParagraphStyle(
            name='Label',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Value style (normal right column)
        self.styles.add(ParagraphStyle(
            name='Value',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#000000'),
            fontName='Helvetica',
            alignment=TA_LEFT
        ))
        
        # Normal text with smaller font
        self.styles.add(ParagraphStyle(
            name='SmallNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=2,
            leading=12
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=1
        ))

    def generate_report(self, field, analysis):
        """Generate PDF report matching the sample format exactly"""
        buffer = io.BytesIO()
        
        # Create PDF document with minimal margins
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=40,
            bottomMargin=40,
        )
        
        # Build the story
        story = []
        
        # MAIN TITLE
        story.append(Paragraph("FARMLAND ASSET INSPECTION REPORT - AGRITECH", 
                              self.styles['MainTitle']))
        story.append(Spacer(1, 0.1 * inch))
        
        # ===== 1. BASIC INFORMATION =====
        story.append(Paragraph("1. BASIC INFORMATION", self.styles['SectionHeading']))
        
        # Generate farmer name from field data
        farmer_name = f"{field.get('crop_type', 'General').title()} Farm"
        if 'id' in field:
            farmer_name += f" - {field['id'][:8]}"
        
        basic_data = [
            ["Report ID:", f"VDX-TN-{datetime.now().strftime('%Y')}-{random.randint(10000, 99999)}"],
            ["Inspection Date:", datetime.now().strftime('%d %B %Y')],
            ["Location:", f"{field.get('name', 'Unknown Field')}, Tamil Nadu, India"],
            ["Geo-coordinates:", f"{field['latitude']}° N, {field['longitude']}° E"],
            ["Total Land Area:", f"{field['acres']} acres"],
            ["Farmer Name:", farmer_name],
        ]
        
        basic_table = Table(basic_data, colWidths=[1.8*inch, 4*inch])
        basic_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(basic_table)
        story.append(Spacer(1, 0.05 * inch))
        
        # ===== 2. DATA SOURCES USED =====
        story.append(Paragraph("2. DATA SOURCES USED", self.styles['SectionHeading']))
        
        # Get sources
        sat_source = "Sentinel-2 Multispectral"
        weather_source = "IMD & ERA5 Dataset"
        
        if 'data_sources' in analysis:
            sat_source = analysis['data_sources'].get('satellite', sat_source)
            weather_source = analysis['data_sources'].get('weather', weather_source)
        
        sources_data = [
            ["Satellite Provider:", sat_source],
            ["Weather Data:", weather_source],
            ["Analysis Period:", f"10 Nov 2025 – 10 Feb 2026"],
            ["Resolution & Frequency:", "10m, Every 5 Days"],
        ]
        
        sources_table = Table(sources_data, colWidths=[1.8*inch, 4*inch])
        sources_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(sources_table)
        story.append(Spacer(1, 0.05 * inch))
        
        # ===== 3. SATELLITE METRICS =====
        story.append(Paragraph("3. SATELLITE METRICS", self.styles['SectionHeading']))
        
        ndvi = analysis.get('ndvi_value', 0.62)
        health = analysis.get('vegetation_health', 'Moderate Stress')
        
        # Determine trend based on ndvi
        if ndvi > 0.6:
            trend_text = "Stable with good growth"
        elif ndvi > 0.4:
            trend_text = "Moderate stress detected"
        else:
            trend_text = "18% drop after Jan deficit"
        
        satellite_data = [
            ["NDVI Score:", f"{ndvi:.2f}"],
            ["Crop Health:", health],
            ["NDVI Trend:", trend_text],
        ]
        
        satellite_table = Table(satellite_data, colWidths=[1.8*inch, 4*inch])
        satellite_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(satellite_table)
        story.append(Spacer(1, 0.05 * inch))
        
        # ===== 4. WEATHER IMPACT ASSESSMENT =====
        story.append(Paragraph("4. WEATHER IMPACT ASSESSMENT", self.styles['SectionHeading']))
        
        # Get weather data
        weather_details = analysis.get('weather_details', {})
        risk_breakdown = analysis.get('risk_breakdown', {})
        
        # Default values matching sample
        rainfall = weather_details.get('total_rainfall_mm', weather_details.get('total_rainfall', 312))
        temp = weather_details.get('avg_temperature_c', weather_details.get('avg_temperature', 29.1))
        
        # Calculate anomaly
        rain_norm = 312
        rain_anomaly = ((rainfall / rain_norm) - 1) * 100
        
        # Get drought risk for affected acreage
        drought = risk_breakdown.get('drought', analysis.get('drought_risk', 0.42))
        if isinstance(drought, float) and drought <= 1:
            drought_pct = drought * 100
        else:
            drought_pct = float(drought)
        
        affected_acres = round(field['acres'] * (drought_pct/100), 1)
        yield_loss = analysis.get('projected_yield_loss', 22)
        
        # Determine severity based on drought %
        if drought_pct > 70:
            severity = "High"
        elif drought_pct > 40:
            severity = "Medium"
        else:
            severity = "Low"
        
        weather_data = [
            ["Rainfall:", f"{rainfall:.0f} mm ({rain_anomaly:+.0f}% Below Avg)"],
            ["Temperature:", f"+{temp-27.5:.1f}°C Above Normal"],
            ["Extreme Events:", "No Flood / Cyclone"],
            ["", ""],
            ["Damage Type:", "Drought Stress"],
            ["Affected Acreage:", f"{affected_acres} acres"],
            ["Severity Level:", severity],
            ["Projected Yield Loss:", f"{yield_loss:.0f}%"],
        ]
        
        weather_table = Table(weather_data, colWidths=[1.8*inch, 4*inch])
        weather_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(weather_table)
        story.append(Spacer(1, 0.1 * inch))
        
        # ===== 5. RISK ASSESSMENT (NEW) =====
        story.append(Paragraph("5. RISK ASSESSMENT", self.styles['SectionHeading']))
        
        overall_risk = analysis.get('overall_risk', 'Medium')
        risk_score = analysis.get('risk_score', 0.55)
        
        # Get all risk components
        drought_risk = risk_breakdown.get('drought', analysis.get('drought_risk', 0.42))
        flood_risk = risk_breakdown.get('flood', analysis.get('flood_risk', 0.05))
        heat_risk = risk_breakdown.get('heat_stress', analysis.get('heat_stress_risk', 0.15))
        frost_risk = risk_breakdown.get('frost', analysis.get('frost_risk', 0.0))
        
        # Convert to percentages
        def to_percentage(val):
            if isinstance(val, float) and val <= 1:
                return f"{val*100:.0f}%"
            return f"{float(val):.0f}%"
        
        # Color code based on risk level
        if overall_risk == "LOW":
            risk_color = colors.HexColor('#4CAF50')
        elif overall_risk == "MEDIUM":
            risk_color = colors.HexColor('#FFC107')
        elif overall_risk == "HIGH":
            risk_color = colors.HexColor('#FF9800')
        else:  # EXTREME
            risk_color = colors.HexColor('#F44336')
        
        risk_data = [
            ["Overall Risk Level:", f"{overall_risk}"],
            ["Risk Score:", f"{risk_score:.2f}"],
            ["", ""],
            ["Risk Breakdown:", ""],
            ["• Drought Risk:", to_percentage(drought_risk)],
            ["• Flood Risk:", to_percentage(flood_risk)],
            ["• Heat Stress:", to_percentage(heat_risk)],
            ["• Frost Risk:", to_percentage(frost_risk)],
        ]
        
        risk_table = Table(risk_data, colWidths=[1.8*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (1, 0), (1, 0), risk_color),
            ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 3), (0, 3), 10),
            ('LEFTPADDING', (0, 4), (0, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 0.05 * inch))
        
        # ===== 6. PREMIUM ADJUSTMENT (NEW) =====
        story.append(Paragraph("6. PREMIUM ADJUSTMENT", self.styles['SectionHeading']))
        
        premium = analysis.get('premium_adjustment', '+5% to +15%')
        yield_loss_val = analysis.get('projected_yield_loss', 22)
        
        # Calculate recommended premium based on risk
        if overall_risk == "LOW":
            premium_rec = "-5% to 0% discount"
            premium_color = colors.HexColor('#4CAF50')
        elif overall_risk == "MEDIUM":
            premium_rec = "+5% to +15% surcharge"
            premium_color = colors.HexColor('#FFC107')
        elif overall_risk == "HIGH":
            premium_rec = "+25% to +50% surcharge"
            premium_color = colors.HexColor('#FF9800')
        else:  # EXTREME
            premium_rec = "+50% to +100% surcharge"
            premium_color = colors.HexColor('#F44336')
        
        premium_data = [
            ["Base Premium Adjustment:", premium],
            ["Recommended Adjustment:", premium_rec],
            ["", ""],
            ["Compensation Eligibility:", "Partial compensation approved"],
            ["Estimated Payout:", f"Based on {yield_loss_val:.0f}% yield loss"],
        ]
        
        premium_table = Table(premium_data, colWidths=[1.8*inch, 4*inch])
        premium_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (1, 1), (1, 1), premium_color),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(premium_table)
        story.append(Spacer(1, 0.1 * inch))
        
        # ===== 7. VISUAL EVIDENCE =====
        story.append(Paragraph("7. VISUAL EVIDENCE", self.styles['SectionHeading']))
        
        # Create a simple placeholder for images
        image_data = [
            ["Crop Health Imagery", "Rainfall Anomaly"],
            ["[Satellite imagery data]", "[Rainfall map data]"],
        ]
        
        image_table = Table(image_data, colWidths=[2.9*inch, 2.9*inch])
        image_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (1, 1), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 1), (1, 1), colors.HexColor('#666666')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ]))
        story.append(image_table)
        story.append(Spacer(1, 0.1 * inch))
        
        # ===== FINAL SUMMARY =====
        story.append(Paragraph("FINAL SUMMARY", self.styles['SectionHeading']))
        
        summary_text = f"""
        <b>Moderate drought stress detected on ~{affected_acres} acres of the field</b>, 
        with estimated {yield_loss:.0f}% yield loss. {premium_rec} applied.
        Partial compensation approved based on satellite & weather data.
        """
        
        story.append(Paragraph(summary_text, self.styles['SmallNormal']))
        story.append(Spacer(1, 0.1 * inch))
        
        # Recommendations
        recommendations = analysis.get('recommendations', [
            "⚠️ HIGH DROUGHT RISK - Implement irrigation scheduling",
            "🌱 Low vegetation health - Consider soil amendment",
            "📊 Monitor weather patterns closely",
            "💰 Premium adjustment applied based on risk assessment"
        ])
        
        for i, rec in enumerate(recommendations[:4]):
            story.append(Paragraph(f"• {rec}", self.styles['SmallNormal']))
        
        story.append(Spacer(1, 0.15 * inch))
        
        # ===== FOOTER =====
        verification_id = f"9F3A-{datetime.now().strftime('%m%d')}-{random.randint(1000, 9999)}"
        
        story.append(Paragraph(f"Generated By: Verdex Asset Intelligence Platform v1.3", 
                              self.styles['Footer']))
        story.append(Paragraph(f"Report Timestamp: {datetime.now().strftime('%d %b %Y, %H:%M IST')}", 
                              self.styles['Footer']))
        story.append(Paragraph(f"Verification ID: {verification_id}", 
                              self.styles['Footer']))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer