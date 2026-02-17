from flask import Flask, render_template, request, jsonify, send_file  # Make sure send_file is here
from flask_cors import CORS
import uuid
from datetime import datetime
from config import Config
from services.satellite import SatelliteService
from services.weather import WeatherService
from services.analyzer import AnalyzerService
from services.report_generator import ReportGenerator


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize services
satellite = SatelliteService()
weather = WeatherService()
analyzer = AnalyzerService()
report_generator = ReportGenerator()

# In-memory database
fields_db = {}
analyses_db = {}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fields', methods=['GET'])
def get_fields():
    return jsonify({
        'success': True,
        'fields': list(fields_db.values())
    })

@app.route('/api/fields', methods=['POST'])
def create_field():
    data = request.json
    
    field = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'latitude': float(data['latitude']),
        'longitude': float(data['longitude']),
        'acres': float(data['acres']),
        'crop_type': data.get('crop_type', 'Unknown'),
        'created_at': datetime.now().isoformat()
    }
    
    fields_db[field['id']] = field
    
    return jsonify({
        'success': True,
        'field': field
    })

@app.route('/api/fields/<field_id>/analyze', methods=['POST'])
def analyze_field(field_id):
    field = fields_db.get(field_id)
    if not field:
        return jsonify({'success': False, 'error': 'Field not found'}), 404
    
    try:
        # Get satellite data
        veg_data = satellite.get_vegetation_data(
            field['latitude'], 
            field['longitude']
        )
        
        # Get weather data
        weather_risks = weather.get_risk_metrics(
            field['latitude'],
            field['longitude']
        )
        
        # Analyze everything
        analysis = analyzer.analyze_field(
            field, 
            veg_data, 
            weather_risks
        )
        
        # Add metadata
        analysis['field_id'] = field_id
        analysis['timestamp'] = datetime.now().isoformat()
        analysis['vegetation_data'] = veg_data
        analysis['weather_data'] = weather_risks
        
        # Store analysis
        analysis_id = str(uuid.uuid4())
        analyses_db[analysis_id] = analysis
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/fields/<field_id>/report/pdf', methods=['GET'])
def download_pdf_report(field_id):
    """Generate and download PDF report"""
    try:
        field = fields_db.get(field_id)
        if not field:
            return jsonify({'success': False, 'error': 'Field not found'}), 404
        
        # Get latest analysis
        field_analyses = [a for a in analyses_db.values() if a.get('field_id') == field_id]
        if not field_analyses:
            return jsonify({'success': False, 'error': 'No analysis found for this field. Please run analysis first.'}), 404
        
        latest_analysis = field_analyses[-1]
        
        try:
            # Generate PDF report
            pdf_buffer = report_generator.generate_report(field, latest_analysis)
            
            # Create filename
            filename = f"verdex_report_{field['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filename = filename.replace(' ', '_').lower()
            
            # Send file
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )
            
        except Exception as e:
            # Log the error for debugging
            print(f"PDF Generation Error: {str(e)}")
            return jsonify({
                'success': False, 
                'error': f'PDF generation failed: {str(e)}'
            }), 500
            
    except Exception as e:
        print(f"Unexpected error in PDF endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500
@app.route('/api/fields/<field_id>/report', methods=['GET'])
def generate_report(field_id):
    field = fields_db.get(field_id)
    if not field:
        return jsonify({'success': False, 'error': 'Field not found'}), 404
    
    # Get latest analysis
    field_analyses = [a for a in analyses_db.values() if a.get('field_id') == field_id]
    if not field_analyses:
        return jsonify({'success': False, 'error': 'No analysis found'}), 404
    
    latest_analysis = field_analyses[-1]
    
    # Generate report
    report = analyzer.generate_report(field, latest_analysis)
    
    return jsonify({
        'success': True,
        'report': report
    })

@app.route('/api/fields/<field_id>', methods=['DELETE'])
def delete_field(field_id):
    if field_id in fields_db:
        del fields_db[field_id]
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Field not found'}), 404

if __name__ == '__main__':
    # Add sample data
    sample_field = {
        'id': str(uuid.uuid4()),
        'name': 'Sample Field',
        'latitude': 42.0347,
        'longitude': -93.6200,
        'acres': 150,
        'crop_type': 'Corn',
        'created_at': datetime.now().isoformat()
    }
    fields_db[sample_field['id']] = sample_field
    
    app.run(debug=True, port=5000)