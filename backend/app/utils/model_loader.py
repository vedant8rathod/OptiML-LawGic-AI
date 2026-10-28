import os
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional


MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "model.pkl"
model = None
if MODEL_PATH.exists():
    try:
        import joblib

        model = joblib.load(MODEL_PATH)
        print(f"INFO: Loaded local trained model from {MODEL_PATH}")
    except Exception as exc:
        model = None
        print(f"WARNING: Local model found but failed to load: {exc}")
else:
    # Local model is an optional offline artifact (e.g., custom scikit-learn classifier).
    # When absent, the application gracefully routes through Gemini (live) or the fallback heuristic assistant.
    print(f"INFO: Optional local model not present at {MODEL_PATH}; using live Gemini / fallback pipeline.")


try:
    from app.ml.ai_legal_model import AiLegalAssistantModel

    ai_model = AiLegalAssistantModel()
    print("INFO: AI Legal Assistant Model loaded as fallback")
except Exception as exc:
    ai_model = None
    print(f"WARNING: AI Legal Model failed to load: {exc}")


# Gemini SDK setup - Supporting modern google-genai SDK with backward compatibility for google.generativeai
genai_client = None
legacy_genai = None

try:
    from google import genai
    from google.genai import types as genai_types
    GENAI_MODERN = True
except ImportError:
    genai = None
    genai_types = None
    GENAI_MODERN = False
    try:
        import google.generativeai as legacy_genai
    except ImportError:
        legacy_genai = None


GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY") or "").strip()
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_MODEL_NAME = None

def _sanitize_model_name(name: str) -> str:
    """Ensure Gemini model names are clean and consistent across SDK versions."""
    cleaned = name.strip()
    if not cleaned:
        return DEFAULT_GEMINI_MODEL
    # google-genai prefers 'gemini-2.5-flash', but handles 'models/gemini-2.5-flash'
    return cleaned


if GEMINI_API_KEY:
    GEMINI_MODEL_NAME = _sanitize_model_name(os.getenv("GEMINI_MODEL_NAME") or DEFAULT_GEMINI_MODEL)
    if GENAI_MODERN and genai is not None:
        try:
            genai_client = genai.Client(api_key=GEMINI_API_KEY)
            print(f"INFO: Modern Gemini Client ready for live analysis using '{GEMINI_MODEL_NAME}'")
        except Exception as exc:
            genai_client = None
            print(f"WARNING: Modern Gemini Client initialization failed: {exc}")
    elif legacy_genai is not None:
        try:
            legacy_genai.configure(api_key=GEMINI_API_KEY)
            print(f"INFO: Legacy Gemini model '{GEMINI_MODEL_NAME}' configured as fallback")
        except Exception as exc:
            print(f"WARNING: Legacy Gemini configuration failed: {exc}")
    else:
        print("WARNING: Neither google-genai nor google-generativeai installed. Live AI responses disabled.")
else:
    print("INFO: Set GEMINI_API_KEY or AI_API_KEY to enable Gemini responses")



def predict(text: str, language: str = "en") -> Dict[str, Any]:
    """Return legal analysis using the best available model (legacy behavior)."""
    if not text or not text.strip():
        error_msg = "No input text provided" if language == "en" else "कोई इनपुट टेक्स्ट प्रदान नहीं किया गया"
        demo_msg = "Please provide text for legal analysis" if language == "en" else "कृपया कानूनी विश्लेषण के लिए टेक्स्ट प्रदान करें"
        return {
            "error": error_msg,
            "demo_note": demo_msg,
        }

    cleaned_text = text.strip()

    if model is not None:
        try:
            result = model.predict([cleaned_text])[0]
            if isinstance(result, str):
                try:
                    return json.loads(result)
                except json.JSONDecodeError:
                    return {"analysis": result}
            if isinstance(result, dict):
                return result
            return {"analysis": result}
        except Exception as exc:
            print(f"WARNING: Real model prediction failed: {exc}")

    # Try Gemini first (highest priority)
    gemini_result = _predict_with_gemini(cleaned_text, task="analysis", language=language)
    if gemini_result is not None:
        return gemini_result

    # Fall back to heuristic analysis
    return analyze_legal_text_fallback(cleaned_text, language)

def predict_analyze(text: str, language: str = "en") -> Dict[str, Any]:
    """Return comprehensive legal analysis for analyze endpoint."""
    if not text or not text.strip():
        error_msg = "No input text provided" if language == "en" else "कोई इनपुट टेक्स्ट प्रदान नहीं किया गया"
        demo_msg = "Please provide text for legal analysis" if language == "en" else "कृपया कानूनी विश्लेषण के लिए टेक्स्ट प्रदान करें"
        return {
            "error": error_msg,
            "demo_note": demo_msg,
        }

    cleaned_text = text.strip()

    # Try Gemini first (highest priority)
    gemini_result = _predict_with_gemini(cleaned_text, task="analysis", language=language)
    if gemini_result is not None:
        return gemini_result

    # Fall back to heuristic analysis
    return analyze_legal_text_fallback(cleaned_text, language)

def predict_research(text: str, language: str = "en") -> Dict[str, Any]:
    """Return legal research with cases and laws using the best available model."""
    if not text or not text.strip():
        error_msg = "No research query provided" if language == "en" else "कोई अनुसंधान प्रश्न प्रदान नहीं किया गया"
        demo_msg = "Please provide a legal topic for research" if language == "en" else "कृपया अनुसंधान के लिए एक कानूनी विषय प्रदान करें"
        return {
            "error": error_msg,
            "demo_note": demo_msg,
        }

    cleaned_text = text.strip()

    # Try Gemini first for research (highest priority)
    gemini_result = _predict_with_gemini(cleaned_text, task="research", language=language)
    if gemini_result is not None:
        return gemini_result

    # Fall back to heuristic research
    return research_legal_topic_fallback(cleaned_text, language)


def _predict_with_gemini(text: str, task: str = "analysis", language: str = "en") -> Optional[Dict[str, Any]]:
    """Generate structured analysis or research via Gemini using the modern google-genai SDK or legacy fallback."""
    if not GEMINI_API_KEY or (genai_client is None and legacy_genai is None):
        return None

    try:
        # Language-specific prompts
        lang_instruction = "" if language == "en" else "Respond in Hindi language. "
        
        # Different prompts for different tasks
        if task == "research":
            if language == "hi":
                system_instruction = (
                    lang_instruction +
                    "आप LawGic AI हैं, कानूनी अनुसंधान सहायक। दिए गए कानूनी विषय के लिए भारतीय 3 प्रासंगिक मामलों के साथ JSON में व्यापक अनुसंधान: {"
                    "\"topic\": \"विषय हिंदी में\", "
                    "\"relevant_cases\": [हिंदी में case_name, year, court, summary के साथ 3 भारतीय मामले], "
                    "\"relevant_statutes\": [हिंदी में act_name, year, section, summary के साथ भारतीय कानून], "
                    "\"legal_principles\": [हिंदी में मुख्य कानूनी सिद्धांत], "
                    "\"jurisdiction\": \"हिंदी में भारतीय क्षेत्राधिकार जानकारी\", "
                    "\"analysis\": \"हिंदी में विस्तृत कानूनी विश्लेषण\", "
                    "\"remedies\": [हिंदी में उपलब्ध कानूनी उपाय], "
                    "\"recent_developments\": \"हिंदी में कानून में हाल के बदलाव\", "
                    "\"references\": [हिंदी में अतिरिक्त कानूनी स्रोत]\"} "
                    "भारतीय कानूनी प्रणाली पर ध्यान दें - केवल सुप्रीम कोर्ट, हाई कोर्ट और भारतीय कानून।"
                )
            else:
                system_instruction = (
                    "You are LawGic AI, a specialized Indian legal research assistant. For the given legal topic, "
                    "provide a comprehensive legal research summary with EXACTLY 3 relevant Indian court cases (post-1950) as JSON: {"
                    "\"topic\": \"string\", "
                    "\"relevant_cases\": [3 objects with case_name, year, court, summary - ALL INDIAN CASES], "
                    "\"relevant_statutes\": [array of Indian laws/acts with act_name, year, section, summary], "
                    "\"legal_principles\": [array of key legal principles], "
                    "\"jurisdiction\": \"Indian jurisdiction info\", "
                    "\"analysis\": \"detailed legal analysis\", "
                    "\"remedies\": [array of available legal remedies], "
                    "\"recent_developments\": \"recent changes in law\", "
                    "\"references\": [array of additional legal sources]\"} "
                    "Focus on Indian legal system - Supreme Court, High Courts, and Indian statutes only."
                )
        else:  # analysis task
            if language == "hi":
                system_instruction = (
                    lang_instruction +
                    "आप LawGic AI हैं, कानूनी दस्तावेज़ विश्लेषण सहायक। दस्तावेज़ का विश्लेषण करके हिंदी में JSON में दें: {"
                    "\"category\": \"हिंदी में श्रेणी\", "
                    "\"document_summary\": \"हिंदी में संक्षिप्त पेशेवर सारांश\", "
                    "\"key_findings\": [हिंदी में महत्वपूर्ण कानूनी बिंदु], "
                    "\"risk_assessment\": {\"level\": \"उच्च/मध्यम/कम\", \"factors\": [हिंदी में जोखिम कारक]}, "
                    "\"recommendations\": [हिंदी में कार्ययोग्य कानूनी सलाह], "
                    "\"compliance_issues\": [हिंदी में संभावित अनुपालन समस्याएं], "
                    "\"next_steps\": [हिंदी में सुझाए गए कार्य], "
                    "\"disclaimer\": \"हिंदी में पेशेवर कानूनी अस्वीकरण\"}"
                )
            else:
                system_instruction = (
                    "You are LawGic AI, a legal document analysis assistant. Analyze the document and return formatted JSON: {"
                    "\"category\": \"string\", "
                    "\"document_summary\": \"brief professional summary (not copy of original)\", "
                    "\"key_findings\": [array of important legal points], "
                    "\"risk_assessment\": {\"level\": \"High/Medium/Low\", \"factors\": [array of risk factors]}, "
                    "\"recommendations\": [array of actionable legal advice], "
                    "\"compliance_issues\": [array of potential compliance problems], "
                    "\"next_steps\": [array of suggested actions], "
                    "\"disclaimer\": \"professional legal disclaimer\"}"
                )

        payload = ""

        # Method 1: Modern google-genai Client
        if genai_client is not None:
            config = genai_types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                max_output_tokens=2048,
                response_mime_type="application/json",
            )
            response = genai_client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=text,
                config=config,
            )
            payload = response.text or ""
        # Method 2: Legacy fallback
        elif legacy_genai is not None:
            legacy_model = legacy_genai.GenerativeModel(
                model_name=GEMINI_MODEL_NAME,
                system_instruction=system_instruction,
            )
            generation_config = legacy_genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=2048,
                response_mime_type="application/json",
            )
            response = legacy_model.generate_content(
                text,
                generation_config=generation_config,
            )
            payload = _extract_gemini_text(response)

        if not payload:
            return None

        cleaned_output = _strip_json_code_fences(payload.strip())
        parsed = json.loads(cleaned_output)
        if isinstance(parsed, dict):
            return parsed
        return {"analysis": parsed}
    except json.JSONDecodeError as exc:
        print(f"WARNING: Gemini JSON decode failed: {exc}")
        return None
    except Exception as exc:
        print(f"WARNING: Gemini prediction failed: {exc}")
        return None


def _extract_gemini_text(response: Any) -> str:
    """Pull the textual JSON payload from a Gemini response."""
    try:
        if getattr(response, "text", None):
            return response.text

        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", []) or []
            for part in parts:
                text_value = getattr(part, "text", None)
                if text_value:
                    return text_value
    except Exception:
        pass
    return ""


def _strip_json_code_fences(content: str) -> str:
    """Remove Markdown code fences so JSON can be parsed reliably."""
    if content.startswith("```"):
        content = re.sub(r"^```json?", "", content, flags=re.IGNORECASE).strip()
        content = content.rstrip("`").strip()
    return content


def analyze_legal_text_fallback(text: str, language: str = "en") -> Dict[str, Any]:
    """Heuristic legal analysis when no live model is available."""
    text_lower = text.lower()

    contract_keywords = [
        "contract",
        "agreement",
        "terms",
        "conditions",
        "party",
        "obligation",
    ]
    tenant_keywords = [
        "rent",
        "lease",
        "tenant",
        "landlord",
        "property",
        "eviction",
    ]
    employment_keywords = [
        "employment",
        "job",
        "salary",
        "termination",
        "workplace",
        "employee",
    ]
    criminal_keywords = [
        "crime",
        "criminal",
        "court",
        "judge",
        "conviction",
        "sentence",
    ]

    analysis: Dict[str, Any] = {
        "category": "General Legal Query",
        "confidence": 0.85,
        "key_points": [],
        "recommendations": [],
    }

    if any(keyword in text_lower for keyword in contract_keywords):
        analysis["category"] = "Contract Law"
        analysis["key_points"] = [
            "Contract terms and obligations identified",
            "Party responsibilities outlined",
            "Potential breach areas noted",
        ]
        analysis["recommendations"] = [
            "Review all contract clauses carefully",
            "Ensure mutual obligations are clear",
            "Consider legal consultation for complex terms",
        ]
    elif any(keyword in text_lower for keyword in tenant_keywords):
        analysis["category"] = "Tenant/Landlord Law"
        analysis["key_points"] = [
            "Rental agreement provisions analyzed",
            "Tenant and landlord rights identified",
            "Local housing laws may apply",
        ]
        analysis["recommendations"] = [
            "Know your local tenant rights",
            "Document all communications with landlord",
            "Check local housing authority guidelines",
        ]
    elif any(keyword in text_lower for keyword in employment_keywords):
        analysis["category"] = "Employment Law"
        analysis["key_points"] = [
            "Employment terms and conditions reviewed",
            "Worker rights and protections noted",
            "Workplace policies analyzed",
        ]
        analysis["recommendations"] = [
            "Understand your employment rights",
            "Keep records of workplace communications",
            "Consult HR or legal counsel if needed",
        ]
    elif any(keyword in text_lower for keyword in criminal_keywords):
        analysis["category"] = "Criminal Law"
        analysis["key_points"] = [
            "Criminal law matters identified",
            "Legal procedures and rights noted",
            "Court processes outlined",
        ]
        analysis["recommendations"] = [
            "Seek qualified legal representation immediately",
            "Know your constitutional rights",
            "Do not proceed without legal counsel",
        ]
    else:
        analysis["key_points"] = [
            "Legal document or query analyzed",
            "General legal principles apply",
            "Professional review recommended",
        ]
        analysis["recommendations"] = [
            "Consult with a qualified attorney",
            "Gather all relevant documents",
            "Consider your specific jurisdiction's laws",
        ]

    return analysis


def research_legal_topic_fallback(text: str, language: str = "en") -> Dict[str, Any]:
    """Indian legal research fallback when no live model is available."""
    text_lower = text.lower()
    
    # Determine topic category
    research_topic = "General Legal Research"
    if any(keyword in text_lower for keyword in ["contract", "agreement", "breach"]):
        research_topic = "Contract Law in India"
    elif any(keyword in text_lower for keyword in ["employment", "workplace", "labor", "discrimination"]):
        research_topic = "Employment and Labour Law in India"
    elif any(keyword in text_lower for keyword in ["criminal", "crime", "ipc", "crpc"]):
        research_topic = "Criminal Law in India"
    elif any(keyword in text_lower for keyword in ["property", "real estate", "land", "immovable"]):
        research_topic = "Property Law in India"
    elif any(keyword in text_lower for keyword in ["constitutional", "fundamental rights", "directive principles"]):
        research_topic = "Constitutional Law in India"
    
    # Indian cases and statutes based on topic
    indian_cases = []
    indian_statutes = []
    
    if "contract" in research_topic.lower():
        indian_cases = [
            {
                "case_name": "Satyabrata Ghose v. Mugneeram Bangur & Co.",
                "year": "1954",
                "court": "Supreme Court of India",
                "summary": "Landmark case establishing the doctrine of frustration of contract under Indian Contract Act"
            },
            {
                "case_name": "Kailash Nath Associates v. Delhi Development Authority",
                "year": "2015",
                "court": "Supreme Court of India", 
                "summary": "Recent ruling on breach of contract and compensation in government contracts"
            },
            {
                "case_name": "Indian Oil Corporation Ltd. v. Amritsar Gas Service",
                "year": "1991",
                "court": "Supreme Court of India",
                "summary": "Established principles of unfair terms in standard form contracts"
            }
        ]
        indian_statutes = [
            {
                "act_name": "Indian Contract Act",
                "year": "1872",
                "section": "Section 1-266",
                "summary": "Primary legislation governing contracts in India"
            },
            {
                "act_name": "Sale of Goods Act",
                "year": "1930",
                "section": "Section 1-66",
                "summary": "Governs sale of goods and related contracts"
            }
        ]
    elif "employment" in research_topic.lower():
        indian_cases = [
            {
                "case_name": "Vishaka v. State of Rajasthan",
                "year": "1997",
                "court": "Supreme Court of India",
                "summary": "Landmark judgment establishing guidelines for workplace sexual harassment prevention"
            },
            {
                "case_name": "Secretary, State of Karnataka v. Umadevi",
                "year": "2006",
                "court": "Supreme Court of India",
                "summary": "Important case on regularization of temporary and contractual employees"
            },
            {
                "case_name": "Workmen of American Express International Banking Corporation v. Management",
                "year": "1985",
                "court": "Supreme Court of India",
                "summary": "Established principles for retrenchment compensation and due process"
            }
        ]
        indian_statutes = [
            {
                "act_name": "Industrial Disputes Act",
                "year": "1947",
                "section": "Section 1-40",
                "summary": "Primary legislation for industrial relations and dispute resolution"
            },
            {
                "act_name": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act",
                "year": "2013",
                "section": "Section 1-26",
                "summary": "Comprehensive law addressing workplace harassment"
            }
        ]
    else:
        # General Indian legal cases
        indian_cases = [
            {
                "case_name": "Kesavananda Bharati v. State of Kerala",
                "year": "1973",
                "court": "Supreme Court of India",
                "summary": "Established the basic structure doctrine of the Constitution"
            },
            {
                "case_name": "Maneka Gandhi v. Union of India",
                "year": "1978",
                "court": "Supreme Court of India",
                "summary": "Expanded the scope of Article 21 and established procedural due process"
            },
            {
                "case_name": "K.S. Puttaswamy v. Union of India",
                "year": "2017",
                "court": "Supreme Court of India",
                "summary": "Recognized privacy as a fundamental right under Indian Constitution"
            }
        ]
        indian_statutes = [
            {
                "act_name": "Constitution of India",
                "year": "1950",
                "section": "Articles 1-395",
                "summary": "Supreme law of India establishing fundamental rights and governance structure"
            },
            {
                "act_name": "Code of Civil Procedure",
                "year": "1908",
                "section": "Section 1-158",
                "summary": "Procedural law governing civil litigation in India"
            }
        ]
    
    return {
        "topic": research_topic,
        "relevant_cases": indian_cases,
        "relevant_statutes": indian_statutes,
        "legal_principles": [
            "Indian legal system follows common law principles with statutory modifications",
            "Supreme Court judgments are binding on all lower courts (Article 141)",
            "High Court decisions are binding within their territorial jurisdiction",
            "Parliamentary supremacy subject to constitutional basic structure"
        ],
        "jurisdiction": "Indian legal system with Supreme Court as apex court and 25 High Courts",
        "analysis": f"Comprehensive analysis of {research_topic.lower()} showing evolution of legal principles through landmark judgments and statutory developments in the Indian context.",
        "remedies": [
            "Civil remedies under respective statutes",
            "Constitutional remedies through writ jurisdiction (Articles 32, 226)",
            "Alternative dispute resolution mechanisms",
            "Regulatory and administrative remedies"
        ],
        "recent_developments": "Recent judicial trends emphasize constitutional values, digital jurisprudence, and alternative dispute resolution mechanisms.",
        "references": [
            "AIR (All India Reporter) citations",
            "Supreme Court Cases (SCC) database",
            "Indian Law Reports",
            "Manupatra and SCC Online databases"
        ]
    }

def get_simple_legal_answer(text: str) -> str:
    """Simple legal answer fallback for quick predict endpoint."""
    text_lower = text.lower()
    
    if any(keyword in text_lower for keyword in ["tenant", "rent", "landlord", "lease"]):
        return (
            "**Tenant Rights Overview:**\n\n"
            "As a tenant in India, you have several key rights:\n\n"
            "• **Right to peaceful enjoyment** - Your landlord cannot disturb you unnecessarily\n"
            "• **Protection from arbitrary eviction** - Proper notice periods must be followed\n"
            "• **Right to basic amenities** - Water, electricity, and habitable conditions\n"
            "• **Security deposit protection** - Landlord must return deposit as per agreement\n\n"
            "**Important:** Check your state's rent control laws as they vary across India. "
            "Keep all rental agreements and payment receipts for your records."
        )
    
    elif any(keyword in text_lower for keyword in ["employment", "job", "workplace", "salary"]):
        return (
            "**Employment Rights in India:**\n\n"
            "Key employment rights include:\n\n"
            "• **Minimum wage protection** - As per state minimum wage laws\n"
            "• **Working hours limits** - Generally 8 hours per day, 48 hours per week\n"
            "• **Protection from discrimination** - Based on gender, caste, religion\n"
            "• **Right to form associations** - Trade unions and collective bargaining\n"
            "• **Termination protection** - Notice periods and due process requirements\n\n"
            "**Tip:** Keep employment contracts, payslips, and communications documented."
        )
    
    elif any(keyword in text_lower for keyword in ["contract", "agreement", "legal document"]):
        return (
            "**Contract Review Basics:**\n\n"
            "When reviewing any contract, focus on:\n\n"
            "• **Key terms and conditions** - Payment, delivery, duration\n"
            "• **Termination clauses** - How either party can exit\n"
            "• **Liability and risk allocation** - Who is responsible for what\n"
            "• **Dispute resolution** - Courts, arbitration, or mediation\n\n"
            "**Red flags:** Unfair termination clauses, excessive penalties, unclear terms.\n\n"
            "**Advice:** Have legal documents reviewed by a qualified lawyer before signing."
        )
    
    elif any(keyword in text_lower for keyword in ["consumer", "product", "service", "warranty"]):
        return (
            "**Consumer Rights in India:**\n\n"
            "Under the Consumer Protection Act 2019:\n\n"
            "• **Right to information** - Clear details about products/services\n"
            "• **Right to choose** - Access to variety of goods at competitive prices\n"
            "• **Right to seek redressal** - Compensation for defective goods/services\n"
            "• **Right to consumer education** - Awareness about rights and remedies\n\n"
            "**Filing complaints:** Consumer courts handle disputes up to ₹1 crore value.\n"
            "**Timeline:** Most complaints should be filed within 2 years of cause of action."
        )
    
    else:
        return (
            "**General Legal Guidance:**\n\n"
            "For your legal question, consider these steps:\n\n"
            "• **Document everything** - Keep records, receipts, and communications\n"
            "• **Know your rights** - Research applicable laws and regulations\n"
            "• **Seek professional help** - Consult a qualified lawyer for complex matters\n"
            "• **Explore alternatives** - Mediation, arbitration, or consumer forums\n\n"
            "**Important:** Laws vary by state and situation. This is general information only.\n"
            "**Always consult a qualified legal professional for advice specific to your case.**"
        )
