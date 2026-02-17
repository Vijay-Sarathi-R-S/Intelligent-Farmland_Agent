# Intelligent Farmland Agent (Verdex)

**Verdex - Farmland Intelligence** is an AI-powered web application that provides real-time analysis and insights for agricultural farmland using satellite imagery, weather data, and machine learning.

## 🎯 Overview

This intelligent system leverages satellite data, weather forecasting, and Google Gemini AI to analyze farmland health, detect issues, and provide actionable recommendations for farmers. The application combines multiple data sources to deliver comprehensive field analysis and automated report generation.

## ✨ Key Features

- **🛰️ Satellite Imagery Analysis**: Real-time vegetation data collection using NASA Earth and other satellite APIs
- **🌤️ Weather Intelligence**: Advanced weather forecasting and risk metrics from multiple weather services
- **🤖 AI-Powered Analysis**: Gemini AI integration for intelligent field assessment and recommendations
- **📊 Real-time Metrics**: NDVI (Normalized Difference Vegetation Index) calculations and health status monitoring
- **📄 PDF Report Generation**: Automated professional report generation with detailed insights
- **🌐 Web Interface**: User-friendly dashboard for field management and analysis
- **💾 Field Management**: Create, track, and analyze multiple farmland fields
- **⚙️ Multi-API Fallback System**: Robust API fallback mechanisms ensuring data availability

## 📁 Project Structure

```
Intelligent-Farmland_Agent/
├── app.py                    # Main Flask application
├── config.py                 # Configuration and API setup
├── requirements.txt          # Python dependencies
├── test.py                   # Testing module
├── .env                      # Environment variables (local)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── services/
│   ├── __init__.py
│   ├── analyzer.py           # Field analysis service with AI integration
│   ├── report_generator.py   # PDF report generation
│   ├── satellite.py          # Satellite data collection
│   ├── satellite_fixed.py    # Alternative satellite implementation
│   └── weather.py            # Weather data collection
└── templates/
    └── index.html            # Web interface
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (Recommended: 3.12.8)
- pip package manager
- API Keys for:
  - Google Gemini API
  - NASA Earth API
  - Other optional weather/satellite services

### Installation

1. **Clone the repository**
   ```bash
   cd Intelligent-Farmland_Agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

> `python.exe -m pip install --upgrade pip`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
```
cp .env.example .env
```
   - Add your API keys:
     ```
     GEMINI_API_KEY=your-gemini-api-key
     NASA_API_KEY=your-nasa-api-key
     SECRET_KEY=your-secret-key
     ```

### Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📚 API Endpoints

### Fields Management

- **GET** `/api/fields` - Retrieve all fields
- **POST** `/api/fields` - Create a new field
- **POST** `/api/fields/<field_id>/analyze` - Analyze a specific field

### Request Example

```json
POST /api/fields
{
  "name": "Field A",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "acres": 50,
  "crop_type": "Corn"
}
```

### Response Example

```json
{
  "success": true,
  "analysis": {
    "field_id": "abc123",
    "vegetation_health": "Healthy",
    "ndvi_value": 0.8,
    "weather_risks": {...},
    "ai_insights": "Crops appear healthy with good moisture levels...",
    "timestamp": "2026-02-17T10:30:00"
  }
}
```

## 🔧 Services Overview

### Satellite Service (`services/satellite.py`)
- Retrieves vegetation data from multiple satellite APIs
- Calculates NDVI (Normalized Difference Vegetation Index)
- Provides fallback mechanisms for API failures
- Supports NASA Earth, Land Viewer, and other satellite sources

### Weather Service (`services/weather.py`)
- Collects weather data and forecasts
- Calculates risk metrics (temperature, precipitation, etc.)
- Integrates with Open-Meteo and NASA POWER APIs
- Historical and forecast data support

### Analyzer Service (`services/analyzer.py`)
- Combines satellite and weather data
- Uses Gemini AI for intelligent analysis
- Generates health recommendations
- Validates data for environmental context

### Report Generator (`services/report_generator.py`)
- Creates professional PDF reports
- Includes charts, tables, and visualizations
- Formats analysis results for stakeholders
- Customizable styling and branding

## 🤖 AI Integration

The application uses **Google Gemini Pro** for:
- Data validation and contextual analysis
- Generating farming recommendations
- Detecting anomalies in crop health
- Providing actionable insights based on field conditions

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| flask-cors | 4.0.0 | CORS support |
| numpy | 1.24.3 | Numerical computing |
| Pillow | 10.0.0 | Image processing |
| requests | 2.31.0 | HTTP requests |
| google-generativeai | 0.3.0 | Gemini AI API |
| python-dotenv | 1.0.0 | Environment variables |
| reportlab | 4.0.4 | PDF generation |

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `NASA_API_KEY` | NASA API key | Optional |
| `SECRET_KEY` | Flask secret key | Yes |

## 📊 Data Sources

The application integrates with multiple data sources:

1. **NASA Earth API** - Satellite imagery
2. **NASA POWER API** - Weather and solar data
3. **Open-Meteo API** - Weather forecast and archive data
4. **Sentinel Hub** - Advanced satellite imagery
5. **Google Gemini AI** - Intelligent analysis

## 🧪 Testing

Run the test suite:
```bash
python test.py
```

## 💡 How It Works

1. **Field Registration**: Users register farmland fields with location and crop information
2. **Data Collection**: System automatically fetches satellite and weather data
3. **Analysis**: Combines multiple data sources with AI analysis
4. **Insights**: Generates actionable recommendations
5. **Reporting**: Creates professional PDF reports with findings

## 🌍 Use Cases

- **Crop Health Monitoring**: Track vegetation health using NDVI values
- **Yield Prediction**: Predict crop yield based on health metrics
- **Risk Assessment**: Identify weather-related risks (drought, flooding)
- **Precision Agriculture**: Optimize resource allocation
- **Insurance Claims**: Generate documented evidence for insurance purposes
- **Compliance Reporting**: Create records for regulatory requirements

## 🛠️ Development

### Project Structure Best Practices

- **Services Layer**: Separated concerns for satellite, weather, and analysis
- **Configuration Management**: Centralized config for easy deployment
- **Error Handling**: Fallback mechanisms for API reliability
- **AI Integration**: Seamless Gemini AI integration for enhanced analysis

### Extending the Application

To add new features:

1. Create a new service in `services/` directory
2. Import and initialize in `app.py`
3. Add new routes to the Flask app
4. Update the HTML interface as needed

## 📝 API Response Structure

All API responses follow a consistent structure:

```json
{
  "success": true/false,
  "data": {...},
  "error": "Error message if applicable"
}
```

## 🤝 Contributing

To contribute to this project:

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is provided as-is for hackathon purposes.

## 🆘 Troubleshooting

### API Keys Not Working
- Verify keys are correctly formatted in `.env`
- Check API key permissions and quotas
- Ensure services are initialized with valid keys

### Satellite/Weather Data Unavailable
- The system has automatic fallback mechanisms
- Check internet connectivity
- Verify API services are operational

### PDF Report Generation Issues
- Ensure ReportLab is properly installed
- Check file permissions for output directory
- Verify data is valid before report generation

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check console logs for error messages

## 🎓 Project Information

**Purpose**: Intelligent agricultural field analysis and monitoring  
**Framework**: Flask + JavaScript + AI/ML  
**Created for**: Hackathon Event  
**Status**: Active Development

---

**Made with ❤️ for smarter farming**
