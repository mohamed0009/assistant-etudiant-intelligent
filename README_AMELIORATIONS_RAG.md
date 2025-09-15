# Enhanced RAG System - Professional AI Chatbot

A production-ready RAG (Retrieval-Augmented Generation) system built with professional-grade architecture, optimized for educational content and completely free to use.

## 🌟 Key Features

### 🚀 Professional Architecture

- **Multiple Model Support**: HuggingFace Transformers, Ollama, and fallback systems
- **Advanced Document Processing**: Enhanced PDF, DOCX, TXT, JSON processing with metadata extraction
- **Intelligent Vector Store**: FAISS-based with multiple index types and optimization
- **Document Reranking**: Semantic similarity reranking for better results
- **Smart Caching**: Document and embedding caching for improved performance

### 🎓 Educational Focus

- **Comprehensive Knowledge Base**: Pre-computed responses for 40+ educational concepts
- **Multi-Subject Support**: Mathematics, Physics, Chemistry, Electronics, Biology, and more
- **Smart Subject Detection**: Automatic categorization and filtering
- **Context-Aware Responses**: Combines document knowledge with educational explanations

### 🔧 Production Features

- **Performance Monitoring**: Real-time metrics and benchmarking
- **Error Handling**: Comprehensive error recovery and logging
- **API Documentation**: Full OpenAPI/Swagger documentation
- **Database Integration**: SQLAlchemy-based conversation persistence
- **Export Capabilities**: JSON, CSV, PDF export formats

## 📋 System Requirements

- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: 4GB minimum (8GB+ recommended)
- **Disk Space**: 2GB free space
- **OS**: Windows, macOS, or Linux

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd assistant-etudiant-intelligent
python setup_enhanced_system.py
```

### 2. Start the System

```bash
# Windows
start_enhanced.bat

# Linux/macOS
./start_enhanced.sh

# Or directly
python api.py
```

### 3. Access the System

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📁 Project Structure

```
assistant-etudiant-intelligent/
├── src/                           # Core system modules
│   ├── document_loader.py         # Enhanced document processing
│   ├── vector_store.py           # Professional vector store
│   ├── rag_engine.py             # Advanced RAG engine
│   ├── precomputed_responses.py   # Educational knowledge base
│   └── ...
├── data/                          # Your documents (PDF, DOCX, TXT)
├── enhanced_vector_store/         # Vector embeddings storage
├── exports/                       # Export files
├── logs/                         # System logs
├── cache/                        # Processing cache
├── config/                       # Configuration files
├── api.py                       # Enhanced API server
├── install_enhanced.py           # Professional setup script
└── requirements_enhanced.txt     # Optimized dependencies
```

## 🔧 Configuration

### Environment Variables

Copy `config/config.env.example` to `.env` and customize:

```env
# Model Configuration
MODEL_TYPE=auto                    # auto, ollama, huggingface
USE_RERANKING=true                # Enable document reranking
MAX_SOURCES=5                     # Maximum sources per query
CHUNK_SIZE=1000                   # Document chunk size
CHUNK_OVERLAP=200                 # Overlap between chunks

# Performance
ENABLE_CACHE=true                 # Enable caching
ENABLE_MONITORING=true            # Enable performance monitoring

# Optional: Advanced Models
HUGGINGFACE_API_TOKEN=your_token  # For additional models
OPENAI_API_KEY=your_key          # For premium features
```

### Model Options

#### 1. HuggingFace (Default - Free)

- **Models**: DialoGPT, GPT-2, DistilGPT-2
- **Pros**: Free, good performance, wide compatibility
- **Setup**: Automatic (included in requirements)

#### 2. Ollama (Recommended for Best Performance)

- **Models**: Llama 2, Mistral, CodeLlama
- **Pros**: Excellent quality, local processing, privacy
- **Setup**:

  ```bash
  # Install Ollama (one-time)
  curl https://ollama.ai/install.sh | sh  # Linux
  brew install ollama                      # macOS
  # Windows: Download from ollama.ai

  # Pull models
  ollama pull llama2
  ollama pull mistral
  ```

#### 3. Fallback System

- **Built-in**: Template-based responses
- **Pros**: Always works, educational content
- **Use**: Automatic when other models fail

## 📚 Usage Guide

### Adding Documents

1. Place your documents in the `data/` folder
2. Supported formats: PDF, DOCX, DOC, TXT, MD, JSON
3. The system will automatically process and index them

### API Endpoints

#### Ask Questions

```bash
POST /api/ask
{
    "question": "Explain Ohm's law",
    "subject_filter": "Électricité",
    "use_reranking": true,
    "max_sources": 5
}
```

#### System Status

```bash
GET /api/status
```

#### Upload Documents

```bash
POST /api/documents/upload
# Upload files via form-data
```

#### Performance Benchmark

```bash
GET /api/performance/benchmark
```

### Example Questions

The system excels at educational questions:

- **Mathematics**: "Explain derivatives step by step"
- **Physics**: "What are Newton's laws with examples?"
- **Electronics**: "How does a transistor work?"
- **Chemistry**: "What is pH and how to calculate it?"
- **General**: "Explain [concept] from my course documents"

## 🎯 Advanced Features

### Document Reranking

Improves answer quality by reordering retrieved documents based on semantic similarity:

```python
# Automatically enabled, or configure:
use_reranking = True
```

### Performance Monitoring

Real-time system monitoring:

- Response times
- Confidence scores
- Model performance
- Error rates

### Smart Caching

Multiple caching layers:

- Document processing cache
- Embedding cache
- Response cache

### Export Capabilities

Export conversations and data:

- JSON format for data analysis
- CSV format for spreadsheet use
- PDF format for reports

## 🔍 Troubleshooting

### Common Issues

#### 1. Slow Performance

```bash
# Check system status
GET /api/health

# Run benchmark
GET /api/performance/benchmark

# Solutions:
- Enable caching: ENABLE_CACHE=true
- Reduce chunk size: CHUNK_SIZE=800
- Use faster model: MODEL_TYPE=huggingface
```

#### 2. Memory Issues

```bash
# Solutions:
- Reduce max_sources: MAX_SOURCES=3
- Smaller chunks: CHUNK_SIZE=500
- Clear cache: POST /api/cache/clear
```

#### 3. Model Loading Failures

```bash
# Check logs in logs/ directory
# Fallback will automatically activate

# Solutions:
- Install Ollama for better models
- Use MODEL_TYPE=huggingface
- Check internet connection for downloads
```

### Debugging Tools

#### Health Check

```bash
curl http://localhost:8000/api/health
```

#### Validate Documents

```bash
POST /api/documents/validate
```

#### View Logs

```bash
tail -f logs/enhanced_rag.log
```

## 📊 Performance Optimization

### Hardware Recommendations

#### Minimum Setup

- **CPU**: Any modern processor
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Expected Performance**: 1-3 seconds per query

#### Optimal Setup

- **CPU**: Multi-core processor
- **RAM**: 8GB+
- **GPU**: CUDA-compatible (optional)
- **Storage**: SSD with 5GB+ free space
- **Expected Performance**: 0.1-0.5 seconds per query

### Software Optimizations

#### 1. Model Selection

```env
# Fast but basic
MODEL_TYPE=huggingface

# Best quality (requires Ollama)
MODEL_TYPE=ollama

# Automatic selection
MODEL_TYPE=auto
```

#### 2. Chunk Optimization

```env
# For small documents
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# For large documents
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
```

#### 3. Vector Store Tuning

```python
# In code configuration
index_type = "flat"     # Fast, exact search
index_type = "ivf"      # Faster for large datasets
index_type = "hnsw"     # Fastest approximate search
```

## 🧪 Testing

### Run Test Suite

```bash
python test_enhanced_system.py
```

### Manual Testing

```bash
# Test document loading
python -c "from src.document_loader import EnhancedDocumentLoader; loader = EnhancedDocumentLoader(); docs = loader.load_documents(); print(f'Loaded {len(docs)} documents')"

# Test vector store
python -c "from src.vector_store import EnhancedVectorStore; store = EnhancedVectorStore(); print('Vector store initialized')"

# Test RAG engine
python -c "from src.rag_engine import create_professional_rag_engine; print('RAG engine available')"
```

## 🚀 Deployment

### Development

```bash
python api.py
```

### Production with Docker

```bash
docker build -t enhanced-rag .
docker run -p 8000:8000 -v $(pwd)/data:/app/data enhanced-rag
```

### Production with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

## 📈 Monitoring & Analytics

### Built-in Metrics

- Query response times
- Confidence scores
- Model performance
- Error rates
- Cache hit rates

### Custom Monitoring

```python
# Access metrics via API
GET /api/metrics

# Performance data
GET /api/performance/benchmark
```

## 🔒 Security & Privacy

### Data Privacy

- **Local Processing**: All data stays on your machine
- **No External APIs**: Optional (OpenAI integration available)
- **Secure Storage**: Local database and file storage

### API Security

- CORS configuration
- Input validation
- Error handling without data leakage

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repo-url>
cd assistant-etudiant-intelligent

# Setup development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements_enhanced.txt

# Install development tools
pip install black flake8 pytest

# Run tests
python test_enhanced_system.py
```

### Code Quality

- **Formatting**: Black
- **Linting**: Flake8
- **Testing**: Pytest
- **Documentation**: Docstrings and type hints

## 📞 Support

### Documentation

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **Status**: http://localhost:8000/api/status

### Debugging

1. Check logs in `logs/enhanced_rag.log`
2. Run health check endpoint
3. Validate documents: `POST /api/documents/validate`
4. Clear cache if needed: `POST /api/cache/clear`

### Common Solutions

- **Performance Issues**: Enable caching, reduce chunk size
- **Memory Problems**: Lower max_sources, use smaller models
- **Model Failures**: Install Ollama or use fallback mode

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:

- **LangChain**: RAG framework
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **FastAPI**: Web API framework
- **Transformers**: Language models

---

**🎓 Perfect for students, educators, and professionals who need a powerful, free RAG system for educational content!**
