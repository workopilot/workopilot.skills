# Workopilot Skills

A collection of Claude Desktop skills for integrating with WorkoPilot AI platform.

## 📖 What is Workopilot Skills?

Workopilot Skills is a comprehensive toolkit that helps developers integrate WorkoPilot's AI capabilities into their business systems. It provides automated scripts, code examples, and complete integration solutions for creating AI services, configuring digital employees, and implementing document intelligence features.

## 🚀 Quick Start

### Installation

1. **Clone this repository:**
   ```bash
   git clone git@github.com:workopilot/workopilot.skills.git
   cd workopilot.skills
   ```

2. **Configure your API credentials:**
   
   Create a `.env.workopilot` file in your project root:
   ```properties
   WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
   WORKOPILOT_API_KEY=your_api_key_here
   ```

3. **Install Python dependencies:**
   ```bash
   pip install requests python-dotenv
   ```

### Basic Usage

**Create an AI Service:**
```bash
python skills/workopilot-service-builder/scripts/create_ai_service.py --config service.json
```

**Create a Digital Employee:**
```bash
python skills/workopilot-service-builder/scripts/create_digital_employee.py --config employee.json
```

**Create Attachment Classification:**
```bash
python skills/workopilot-service-builder/scripts/create_attachment_classification.py --config classification.json
```

## 📦 What's Included

### Skills

The `skills/` directory contains Claude Desktop skills for WorkoPilot integration:

- **workopilot-service-builder** - Main skill for creating and integrating WorkoPilot services
  - AI Service creation and management
  - Digital Employee configuration
  - Attachment classification and extraction
  - Iframe skill card registration
  - Document service integration

See [skills/workopilot-service-builder/SKILL.md](skills/workopilot-service-builder/SKILL.md) for detailed documentation.

### Sample Application

The `sample/` directory contains a demo application showcasing WorkoPilot Skills integration:

- Modern SaaS-style management system
- Order management module
- Todo list module
- RESTful API backend (Flask)
- Modern UI frontend (Vue 3 + Tailwind CSS)

This sample demonstrates how to build a complete business application that can be enhanced with WorkoPilot AI capabilities.

See [sample/README.md](sample/README.md) for setup instructions.

## 🌟 Key Features

### 1. AI Service Creation
Create reusable AI capabilities with structured inputs and custom prompts:
- Text analysis (contract review, resume screening)
- Content generation (reports, emails, copywriting)
- Data transformation (unstructured → structured)

### 2. Digital Employee Configuration
Set up complete conversational AI agents with:
- MCP (Model Context Protocol) for data operations
- Skill cards (Iframe) for UI extensions
- Knowledge base integration
- Custom system prompts

### 3. Attachment Classification & Extraction ⭐
**Most Frequently Used Feature** - Automatically extract structured data from documents:
- **Direct Extraction Mode** (90% usage) - Upload contract → Extract data → Fill form
- Supports: Contracts, invoices, resumes, orders, receipts, etc.
- Two extraction methods: OCR + LLM or Vision-Language
- Configurable extraction rules with field-level descriptions

### 4. Iframe Skill Cards
Embed custom UI components in conversations or business menus:
- Display complex interfaces (forms, previews, dashboards)
- Business menu pages (history, analytics)

### 5. Document Services
File processing capabilities:
- Markdown/HTML to PDF conversion
- OCR recognition
- Excel read/write

## 🛠️ Technology Stack

**Skills:**
- Python 3.7+
- requests library
- python-dotenv

**Sample Application:**
- Backend: Flask 3.0, Flask-CORS
- Frontend: Vue 3, Vue Router, Tailwind CSS, Vite

## 📚 Documentation

### Skills Documentation
- [workopilot-service-builder/SKILL.md](skills/workopilot-service-builder/SKILL.md) - Complete skill documentation
- [references/](skills/workopilot-service-builder/references/) - Detailed API references
  - `auth-and-config.md` - Authentication and configuration
  - `ai-service.md` - AI Service integration
  - `digital-employee.md` - Digital Employee setup
  - `attachment-classification.md` - Document extraction guide ⭐
  - `iframe-embed.md` - Iframe embedding
  - `iframe-skill-card.md` - Skill card registration
  - `document-service.md` - Document processing

### Sample Documentation
- [sample/README.md](sample/README.md) - Sample application setup

## 🎯 Common Use Cases

### Case 1: Document Intelligence
**Scenario:** Automatically extract data from uploaded contracts

```bash
# 1. Create classification
python scripts/create_attachment_classification.py --config contract-classification.json

# 2. Call extraction API
curl -X POST https://agent.workopilot.com/net-api/api/attachment/extract \
  -H "API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/contract.pdf",
    "categoryCode": "contract-purchase"
  }'

# 3. Get structured data and fill form
```

### Case 2: AI Service Integration
**Scenario:** Add contract review capability to your system

```bash
# 1. Create AI service
python scripts/create_ai_service.py --config contract-review.json

# 2. Call from your application
fetch('https://agent.workopilot.com/net-api/api/aiagent/run', {
  method: 'POST',
  headers: {
    'API-KEY': process.env.WORKOPILOT_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    serviceCode: 'contract-review-001',
    inputs: {
      contract_type: 'Purchase Contract',
      contract_content: '...'
    }
  })
})
```

### Case 3: Digital Employee Embedding
**Scenario:** Embed AI assistant in your CRM system

```html
<!-- Embed digital employee iframe -->
<iframe 
  src="https://agent.workopilot.com/chat/{robotId}?token={runtimeToken}"
  width="100%"
  height="600px">
</iframe>
```

## 🔧 Development

### Project Structure
```
workopilot.skills/
├── skills/                          # Claude Desktop skills
│   └── workopilot-service-builder/ # Main integration skill
│       ├── SKILL.md                # Skill documentation
│       ├── scripts/                # Automation scripts
│       │   ├── create_ai_service.py
│       │   ├── create_digital_employee.py
│       │   ├── create_attachment_classification.py
│       │   ├── register_iframe_card.py
│       │   └── smoke_test.py
│       ├── references/             # API references
│       ├── agents/                 # Example agent configurations
│       └── evals/                  # Test cases
│
├── sample/                         # Demo application
│   ├── backend/                    # Flask backend
│   ├── frontend/                   # Vue 3 frontend
│   └── README.md                   # Setup instructions
│
└── README.md                       # This file
```

### Running Scripts

All scripts support multiple configuration methods:

**1. Environment file (Recommended):**
```bash
# Create .env.workopilot in your project root
python scripts/create_ai_service.py --config service.json
```

**2. Environment variables:**
```bash
export WORKOPILOT_API_KEY="your_key"
python scripts/create_ai_service.py --config service.json
```

**3. Command line arguments:**
```bash
python scripts/create_ai_service.py \
  --base-url https://agent.workopilot.com/net-api \
  --api-key your_key \
  --config service.json
```

### Testing

**Smoke test to verify setup:**
```bash
python skills/workopilot-service-builder/scripts/smoke_test.py
```

**Test with curl:**
```bash
curl -H "API-KEY: your_api_key" \
  https://agent.workopilot.com/net-api/api/aiagent/list
```

## 🔐 Security Best Practices

### API Key Management
- ✅ Store API keys in `.env.workopilot` or environment variables
- ✅ Add `.env.workopilot` to `.gitignore`
- ✅ Use environment variables in production
- ❌ Never hardcode API keys in source code
- ❌ Never commit API keys to Git
- ❌ Never expose API keys in frontend code

### Iframe Security
- Use HTTPS URLs for production iframe skill cards
- Test with localhost URLs during development
- Update to production URLs before publishing

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 📮 Contact

- **Project**: https://github.com/workopilot/workopilot.skills
- **Issues**: https://github.com/workopilot/workopilot.skills/issues
- **Email**: angus.wang@apright.com

## 🌐 WorkoPilot Platform

Learn more about WorkoPilot:
- Website: https://workopilot.com
- Documentation: https://docs.workopilot.com
- API Reference: https://agent.workopilot.com/docs

---

<div align="center">

**⭐ Star this repo if it helps you!**

Made with ❤️ by Workopilot Team

</div>
