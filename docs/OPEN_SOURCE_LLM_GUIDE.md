# Open-Source LLM Integration Guide for Intelligent Farmland Agent

## 🎯 Overview

This guide shows how to integrate open-source LLMs as an alternative to Google Gemini, providing:
- ✅ Self-hosted capabilities
- ✅ Better privacy & data sovereignty  
- ✅ Fine-tuning opportunities
- ✅ No API rate limits for local deployments

---

## 📦 Option 1: Ollama (Easiest - Recommended for Hackathon)

**Ollama** provides a simple way to run open-source LLMs locally.

### Setup

```bash
# 1. Install Ollama
# Windows/Mac/Linux: https://ollama.ai
# Or use Docker:
docker pull ollama/ollama
docker run -d --name ollama -p 11434:11434 ollama/ollama

# 2. Pull a model (first time only, takes 5-10 minutes)
ollama pull mistral  # 7B model, balanced speed/quality
# OR
ollama pull neural-chat  # Optimized for chat
# OR
ollama pull orca-mini  # Smaller, faster
```

### Integration Code

```python
# services/ai_service_ollama.py
from ollama import Client
import json
import logging

logger = logging.getLogger(__name__)

class OllamaAIService:
    """Alternative AI service using local Ollama"""
    
    def __init__(self, model='mistral', base_url='http://localhost:11434'):
        self.client = Client(host=base_url)
        self.model = model
        self.ai_available = True
        
        try:
            # Test connection
            self.client.generate('test', stream=False)
            logger.info(f"✅ Ollama connected using {model}")
        except Exception as e:
            logger.error(f"❌ Ollama not available: {e}")
            self.ai_available = False
    
    def analyze_field(self, field_data, veg_data, weather_data):
        """Analyze field using local Ollama model"""
        
        if not self.ai_available:
            return {'error': True, 'message': 'AI service unavailable'}
        
        prompt = self._build_prompt(field_data, veg_data, weather_data)
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
                system="You are an expert agricultural AI analyst."
            )
            
            # Parse response
            content = response.get('response', '')
            analysis = self._parse_analysis(content, veg_data)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Ollama analysis error: {e}")
            return {'error': True, 'message': str(e)}
    
    def _build_prompt(self, field_data, veg_data, weather_data):
        """Build analysis prompt"""
        return f"""
        Analyze this farmland and provide recommendations.
        
        FIELD DATA:
        - Name: {field_data.get('name')}
        - Crop: {field_data.get('crop_type')}
        - Size: {field_data.get('acres')} acres
        - Location: {field_data.get('latitude')}, {field_data.get('longitude')}
        
        SATELLITE DATA (NDVI):
        - Mean NDVI: {veg_data.get('mean_ndvi')}
        - Status: {veg_data.get('health_status')}
        
        WEATHER DATA:
        - Drought Risk: {weather_data.get('drought_risk')}
        - Temperature: {weather_data.get('temperature')}°C
        - Precipitation: {weather_data.get('precipitation')}mm
        
        Provide:
        1. Health assessment (0-100)
        2. Recommendations (bullet points)
        3. Risk factors
        
        Format as JSON only, no other text.
        """
    
    def _parse_analysis(self, response_text, source_data):
        """Parse LLM response into structured format"""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                analysis['source'] = 'ollama'
                return analysis
            
            return {
                'error': True,
                'message': 'Could not parse response',
                'raw_response': response_text
            }
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return {'error': True, 'message': 'Parse error'}
```

### Use in App

```python
# app.py - Use Ollama instead of Gemini
from services.ai_service_ollama import OllamaAIService

# Try local Ollama first, fallback to Gemini
try:
    ai_service = OllamaAIService()
    use_ollama = True
except:
    from services.analyzer import AnalyzerService
    ai_service = AnalyzerService()
    use_ollama = False

print(f"Using: {'Ollama (local)' if use_ollama else 'Gemini (cloud)'}")
```

---

## 📦 Option 2: Hugging Face Transformers (More Control)

For fine-tuning and custom models.

```python
# services/ai_service_hf.py
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

class HuggingFaceAIService:
    """AI service using Hugging Face models"""
    
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.1"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16,  # Quantize to 16-bit
        )
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=device
        )
        
        logger.info(f"✅ Loaded {model_name} on {device}")
    
    def analyze_field(self, field_data, veg_data, weather_data):
        """Analyze using HF model"""
        prompt = self._build_prompt(field_data, veg_data, weather_data)
        
        outputs = self.pipeline(
            prompt,
            max_length=512,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
        )
        
        return self._parse_response(outputs[0]['generated_text'])
```

---

## 🎓 Option 3: Fine-Tune for Agriculture Domain

Train on agricultural data using LoRA adapters.

```python
# fine_tune_agriculture.py
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

# 1. Load base model
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 2. Setup LoRA (Parameter-Efficient Fine-Tuning)
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# 3. Load agricultural training data
# Your dataset should have examples like:
# {
#     "text": "Field NDVI: 0.65, Status: Good. Recommendation: Continue monitoring..."
# }
train_dataset = load_dataset("your_agriculture_dataset")

# 4. Train
training_args = TrainingArguments(
    output_dir="./models/agriculture-llm",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    learning_rate=2e-4,
    save_steps=100,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()

# 5. Save and deploy
model.save_pretrained("./models/agriculture-llm-finetuned")
tokenizer.save_pretrained("./models/agriculture-llm-finetuned")
```

---

## 🔄 Switchable AI Service (Hybrid Approach)

Allow switching between Gemini and Ollama at runtime:

```python
# services/ai_service.py
from config import Config
import logging

logger = logging.getLogger(__name__)

class HybridAIService:
    """
    Intelligent AI service that can use Gemini or Ollama
    Falls back gracefully between options
    """
    
    @staticmethod
    def get_service():
        """Get appropriate AI service based on availability"""
        
        # Try Ollama first (local, no API key needed)
        try:
            from services.ai_service_ollama import OllamaAIService
            service = OllamaAIService()
            if service.ai_available:
                logger.info("✅ Using Ollama (local)")
                return service
        except Exception as e:
            logger.warning(f"Ollama unavailable: {e}")
        
        # Fallback to Gemini
        try:
            from services.analyzer import AnalyzerService
            service = AnalyzerService()
            if service.ai_available:
                logger.info("✅ Using Gemini (cloud)")
                return service
        except Exception as e:
            logger.warning(f"Gemini unavailable: {e}")
        
        # No AI available
        logger.error("❌ No AI service available")
        return None
```

---

## 🚀 Deployment with Both Options

### Docker Compose with Ollama

```yaml
# docker-compose.yml additions
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-service
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/tags"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  app:
    # ... existing config ...
    environment:
      - AI_SERVICE=ollama  # or 'gemini'
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama

volumes:
  ollama-data:
```

---

## 📊 Comparison Table

| Feature | Gemini | Ollama | HF Transformers |
|---------|--------|--------|-----------------|
| **Cost** | API calls | Free (hardware) | Free |
| **Privacy** | Cloud | Local | Local |
| **Setup** | Easy | Very Easy | Moderate |
| **Speed** | Network dependent | Fast | GPU dependent |
| **Fine-tuning** | ❌ No | ❌ No | ✅ Yes |
| **Self-hosted** | ❌ No | ✅ Yes | ✅ Yes |
| **Hackathon Score** | Good | Better | Best |

---

## ✅ Hackathon Submission

To maximize points:

1. **Implement both Gemini and Ollama** - Shows flexibility
2. **Document the approach** - Explain why you chose each
3. **Fine-tune on agriculture data** - Extra points for domain adaptation
4. **Add AB tests** - Compare outputs between models
5. **Benchmark performance** - Show latency & quality metrics

---

## 🧪 Testing Your Setup

```bash
# Test Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "What is NDVI?",
  "stream": false
}'

# Test in Python
from ollama import Client
client = Client(host='http://localhost:11434')
response = client.generate(model='mistral', prompt='test')
print(response['response'])
```

---

## 📚 Resources

- [Ollama Docs](https://ollama.ai)
- [Mistral Models](https://mistral.ai)
- [Hugging Face Docs](https://huggingface.co/docs)
- [LoRA Fine-tuning](https://huggingface.co/docs/peft/main/en/package_reference/lora)
- [Quantization Guide](https://huggingface.co/docs/transformers/quantization)

---

## ✅ Hackathon Submission Tips

1. Implement both Gemini and Ollama
2. Document model choices in README
3. Run tests and ensure validator is in place
