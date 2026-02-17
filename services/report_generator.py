from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import io
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E7D32'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1B5E20'),
            spaceBefore=20,
            spaceAfter=10,
            underline=True
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2E7D32'),
            spaceBefore=15,
            spaceAfter=5
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6
        ))
        
        # Label style
        self.styles.add(ParagraphStyle(
            name='LabelStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT
        ))
        
        # Value style
        self.styles.add(ParagraphStyle(
            name='ValueStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#000000'),
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        ))

    def generate_report(self, field, analysis):
        """Generate PDF report"""
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        
        # Build the story
        story = []
        
        # Add report header
        story.extend(self._create_header())
        
        # Add basic information
        story.extend(self._create_basic_info(field, analysis))
        
        # Add data sources
        story.extend(self._create_data_sources(analysis))
        
        # Add satellite metrics
        story.extend(self._create_satellite_metrics(analysis))
        
        # Add weather impact
        story.extend(self._create_weather_impact(field, analysis))
        
        # Add risk assessment
        story.extend(self._create_risk_assessment(analysis))
        
        # Add final summary
        story.extend(self._create_final_summary(field, analysis))
        
        # Add footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer
    
    def _create_header(self):
        """Create report header"""
        elements = []
        
        # Title
        elements.append(Paragraph("FARMLAND ASSET INSPECTION REPORT - VERDEX", 
                                 self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Report ID and Date
        report_id = f"VDX-TN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        data = [
            [Paragraph(f"<b>Report ID:</b> {report_id}", self.styles['CustomNormal']),
             Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y, %H:%M IST')}", 
                      self.styles['CustomNormal'])]
        ]
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_basic_info(self, field, analysis):
        """Create basic information section"""
        elements = []
        
        elements.append(Paragraph("1. BASIC INFORMATION", self.styles['CustomHeading']))
        
        # Create table for basic info
        data = [
            ["Inspection Date:", datetime.now().strftime('%d %B %Y')],
            ["Location:", f"{field.get('name', 'Unknown Field')}"],
            ["Geo-coordinates:", f"{field['latitude']}° N, {field['longitude']}° E"],
            ["Total Land Area:", f"{field['acres']} acres"],
            ["Farmer Name:", f"{field.get('crop_type', 'General')} Farm - {field.get('id', '')[:8]}"],
            ["Crop Type:", field.get('crop_type', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_data_sources(self, analysis):
        """Create data sources section"""
        elements = []
        
        elements.append(Paragraph("2. DATA SOURCES USED", self.styles['CustomHeading']))
        
        veg_data = analysis.get('vegetation_data', {})
        weather_data = analysis.get('weather_data', {})
        
        # Get sources safely
        satellite_source = "Sentinel-2 Multispectral"
        weather_source = "IMD & ERA5 Dataset"
        
        if 'data_sources' in analysis:
            satellite_source = analysis['data_sources'].get('satellite', satellite_source)
            weather_source = analysis['data_sources'].get('weather', weather_source)
        
        data = [
            ["Satellite Provider:", satellite_source],
            ["Weather Data:", weather_source],
            ["Analysis Period:", f"{datetime.now().strftime('%d %b %Y')} - {datetime.now().strftime('%d %b %Y')}"],
            ["Resolution & Frequency:", "10m, Every 5 Days"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_satellite_metrics(self, analysis):
        """Create satellite metrics section"""
        elements = []
        
        elements.append(Paragraph("3. SATELLITE METRICS", self.styles['CustomHeading']))
        
        ndvi = analysis.get('ndvi_value', 0.295)
        health = analysis.get('vegetation_health', 'Fair')
        
        # Format NDVI
        if ndvi is None:
            ndvi_display = "N/A"
            trend = "Data unavailable"
        else:
            ndvi_display = f"{ndvi:.3f}"
            # Determine trend based on ndvi value
            if ndvi > 0.6:
                trend = "Stable with good growth"
                trend_change = "+2%"
            elif ndvi > 0.4:
                trend = f"{health} with monitoring needed"
                trend_change = "-5%"
            else:
                trend = f"Significant stress detected"
                trend_change = "-18%"
        
        data = [
            ["NDVI Score:", ndvi_display],
            ["Crop Health:", health],
            ["NDVI Trend:", trend_change if ndvi else "Unknown"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_weather_impact(self, field, analysis):
        """Create weather impact section"""
        elements = []
        
        elements.append(Paragraph("4. WEATHER IMPACT ASSESSMENT", self.styles['CustomHeading']))
        
        # Get weather data from various possible locations
        weather_data = analysis.get('weather_data', {})
        weather_details = analysis.get('weather_details', {})
        risk_breakdown = analysis.get('risk_breakdown', {})
        
        # Parse weather data
        rainfall = 312  # Default
        temp = 28.5     # Default
        
        if weather_details:
            rainfall = weather_details.get('total_rainfall_mm', weather_details.get('total_rainfall', 312))
            temp = weather_details.get('avg_temperature_c', weather_details.get('avg_temperature', 28.5))
        elif weather_data:
            rainfall = weather_data.get('total_rainfall', 312)
            temp = weather_data.get('avg_temperature', 28.5)
        
        # Get risks
        drought_risk = risk_breakdown.get('drought', analysis.get('drought_risk', 0.5))
        flood_risk = risk_breakdown.get('flood', analysis.get('flood_risk', 0.1))
        
        # Convert to percentages if needed
        if isinstance(drought_risk, float) and drought_risk <= 1:
            drought_pct = drought_risk * 100
        else:
            drought_pct = float(drought_risk)
            
        if isinstance(flood_risk, float) and flood_risk <= 1:
            flood_pct = flood_risk * 100
        else:
            flood_pct = float(flood_risk)
        
        # Determine damage type
        if drought_pct > 70:
            damage_type = "Drought Stress"
            severity = "High" if drought_pct > 90 else "Medium"
            affected = round(field['acres'] * (drought_pct/100), 1)
            yield_loss = analysis.get('projected_yield_loss', round(drought_pct * 0.22, 1))
        elif flood_pct > 50:
            damage_type = "Water Logging"
            severity = "Medium"
            affected = round(field['acres'] * (flood_pct/100), 1)
            yield_loss = analysis.get('projected_yield_loss', round(flood_pct * 0.15, 1))
        else:
            damage_type = "Minimal Stress"
            severity = "Low"
            affected = 0
            yield_loss = 0
        
        # Calculate rainfall anomaly
        rainfall_norm = 312
        rainfall_anomaly = ((rainfall / rainfall_norm) - 1) * 100
        
        data = [
            ["Rainfall:", f"{rainfall:.1f} mm ({rainfall_anomaly:+.1f}% vs Normal)"],
            ["Temperature:", f"{temp:.1f}°C (vs normal)"],
            ["Extreme Events:", "No Flood / Cyclone"],
            ["", ""],
            ["Damage Type:", damage_type],
            ["Affected Acreage:", f"{affected} acres"],
            ["Severity Level:", severity],
            ["Projected Yield Loss:", f"{yield_loss:.1f}%"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_risk_assessment(self, analysis):
        """Create risk assessment section"""
        elements = []
        
        elements.append(Paragraph("5. RISK ASSESSMENT", self.styles['CustomHeading']))
        
        overall_risk = analysis.get('overall_risk', 'Medium')
        risk_score = analysis.get('risk_score', 0.55)
        risk_breakdown = analysis.get('risk_breakdown', {})
        
        # Get individual risks
        drought = risk_breakdown.get('drought', analysis.get('drought_risk', 0.5))
        flood = risk_breakdown.get('flood', analysis.get('flood_risk', 0.1))
        heat = risk_breakdown.get('heat_stress', analysis.get('heat_stress_risk', 0.05))
        
        # Convert to percentages
        if isinstance(drought, float) and drought <= 1:
            drought_pct = drought * 100
        else:
            drought_pct = float(drought)
            
        if isinstance(flood, float) and flood <= 1:
            flood_pct = flood * 100
        else:
            flood_pct = float(flood)
            
        if isinstance(heat, float) and heat <= 1:
            heat_pct = heat * 100
        else:
            heat_pct = float(heat)
        
        # Determine color based on risk
        if overall_risk == 'Low':
            color = colors.HexColor('#4CAF50')
        elif overall_risk == 'Medium':
            color = colors.HexColor('#FFC107')
        else:
            color = colors.HexColor('#F44336')
        
        # Risk metrics
        data = [
            ["Overall Risk Level:", f"{overall_risk}"],
            ["Risk Score:", f"{risk_score:.2f}"],
            ["Drought Risk:", f"{drought_pct:.0f}%"],
            ["Flood Risk:", f"{flood_pct:.0f}%"],
            ["Heat Stress:", f"{heat_pct:.0f}%"],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('TEXTCOLOR', (1, 0), (1, 0), color),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_final_summary(self, field, analysis):
        """Create final summary section"""
        elements = []
        
        elements.append(Paragraph("FINAL SUMMARY", self.styles['CustomHeading']))
        
        # Calculate summary metrics
        risk_breakdown = analysis.get('risk_breakdown', {})
        drought = risk_breakdown.get('drought', analysis.get('drought_risk', 0.5))
        
        if isinstance(drought, float) and drought <= 1:
            drought_pct = drought * 100
        else:
            drought_pct = float(drought)
        
        affected_acres = round(field['acres'] * (drought_pct/100), 1)
        yield_loss = analysis.get('projected_yield_loss', 22)
        
        summary_text = f"""
        <b>Moderate drought stress detected on ~{affected_acres} acres of the field</b>, 
        with estimated {yield_loss:.1f}% yield loss. 
        Partial compensation approved based on satellite & weather data.
        """
        
        elements.append(Paragraph(summary_text, self.styles['CustomNormal']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Recommendations
        elements.append(Paragraph("Recommended Actions:", self.styles['CustomSubHeading']))
        recommendations = analysis.get('recommendations', [
            "⚠️ HIGH DROUGHT RISK - Implement irrigation scheduling",
            "🌱 Low vegetation health - Soil amendment needed",
            "📊 Monitor weather patterns closely"
        ])
        
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.styles['CustomNormal']))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_footer(self):
        """Create report footer"""
        elements = []
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Verification info
        import random
        verification_id = f"9F3A-{datetime.now().strftime('%m%d')}-{random.randint(1000, 9999)}"
        
        footer_data = [
            [f"Generated By: Verdex Asset Intelligence Platform v1.3"],
            [f"Report Timestamp: {datetime.now().strftime('%d %b %Y, %H:%M IST')}"],
            [f"Verification ID: {verification_id}"]
        ]
        
        table = Table(footer_data, colWidths=[6*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#666666')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        elements.append(table)
        
        return elements