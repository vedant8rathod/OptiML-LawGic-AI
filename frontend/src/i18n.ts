import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Inline resources to avoid loading issues
const resources = {
  en: {
    translation: {
      "header": {
        "askAI": "Ask AI",
        "features": "Features",
        "howItWorks": "How It Works",
        "privacy": "Privacy",
        "getStarted": "Get Started",
        "askLegalAI": "Ask Legal AI"
      },
      "brand": {
        "name": "LawGic AI"
      },
      "home": {
        "title": "AI-Powered Legal Solutions",
        "subtitle": "Get instant legal insights, document analysis, and expert guidance powered by advanced AI technology.",
        "cta": "Get Started"
      },
      "askAI": {
        "title": "Ask AI Legal Assistant",
        "modes": {
          "predict": "Quick Prediction",
          "analyze": "Deep Analysis",
          "research": "Legal Research"
        },
        "modeDescriptions": {
          "predict": "Get instant legal insights and predictions",
          "analyze": "Upload documents for thorough analysis",
          "research": "Comprehensive legal research and citations"
        },
        "placeholder": {
          "predict": "Type your legal question for a quick analysis...",
          "analyze": "Describe the document or issue. Optionally attach a file or voice note...",
          "research": "Provide the legal topic or question you'd like us to research..."
        },
        "analyzing": "Analyzing your request...",
        "uploadDocument": "Upload Document",
        "uploadVoice": "Upload Voice",
        "sendMessage": "Send Message",
        "startConversation": "Start a conversation",
        "startConversation.description": "Ask any legal question. I'll help you understand complex legal concepts in simple, clear terms."
      },
      "footer": {
        "termsOfService": "Terms of Service",
        "privacyPolicy": "Privacy Policy",
        "contact": "Contact",
        "about": "About",
        "copyright": "© 2024 LawGic AI. All rights reserved.",
        "madeWith": "Made with",
        "forJustice": "for accessible justice"
      },
      "features": {
        "title": "Features"
      },
      "common": {
        "loading": "Loading...",
        "error": "Error",
        "success": "Success",
        "uploadedFiles": "Uploaded Files",
        "document": "Document",
        "voice": "Voice",
        "remove": "Remove"
      },
      "response": {
        "risk": "Risk",
        "disclaimer": "Disclaimer",
        "analysis": "Analysis",
        "recommendation": "Recommendation",
        "summary": "Summary",
        "category": "Category",
        "documentSummary": "Document Summary",
        "keyFindings": "Key Findings",
        "riskAssessment": "Risk Assessment",
        "level": "Level",
        "factors": "Factors",
        "complianceIssues": "Compliance Issues",
        "nextSteps": "Next Steps"
      },
      "suggestions": {
        "rental": "What are my rights as a tenant in a rental dispute?",
        "tenantRights": "Can my landlord evict me without proper notice?",
        "employment": "What constitutes wrongful termination?",
        "legalDocument": "Help me understand this contract clause."
      }
    }
  },
  hi: {
    translation: {
      "header": {
        "askAI": "AI से पूछें",
        "features": "सुविधाएं",
        "howItWorks": "यह कैसे काम करता है",
        "privacy": "गोपनीयता",
        "getStarted": "शुरू करें",
        "askLegalAI": "कानूनी AI से पूछें"
      },
      "brand": {
        "name": "लॉजिक AI"
      },
      "home": {
        "title": "AI-संचालित कानूनी समाधान",
        "subtitle": "उन्नत AI तकनीक द्वारा संचालित तत्काल कानूनी अंतर्दृष्टि, दस्तावेज़ विश्लेषण और विशेषज्ञ मार्गदर्शन प्राप्त करें।",
        "cta": "शुरू करें"
      },
      "askAI": {
        "title": "AI कानूनी सहायक से पूछें",
        "modes": {
          "predict": "त्वरित पूर्वानुमान",
          "analyze": "गहन विश्लेषण",
          "research": "कानूनी अनुसंधान"
        },
        "modeDescriptions": {
          "predict": "तत्काल कानूनी अंतर्दृष्टि और पूर्वानुमान प्राप्त करें",
          "analyze": "संपूर्ण विश्लेषण के लिए दस्तावेज़ अपलोड करें",
          "research": "व्यापक कानूनी अनुसंधान और उद्धरण"
        },
        "placeholder": {
          "predict": "त्वरित विश्लेषण के लिए अपना कानूनी प्रश्न टाइप करें...",
          "analyze": "दस्तावेज़ या समस्या का वर्णन करें। वैकल्पिक रूप से एक फ़ाइल या वॉइस नोट संलग्न करें...",
          "research": "कानूनी विषय या प्रश्न प्रदान करें जिस पर आप हमसे अनुसंधान करवाना चाहते हैं..."
        },
        "analyzing": "आपके अनुरोध का विश्लेषण कर रहे हैं...",
        "uploadDocument": "दस्तावेज़ अपलोड करें",
        "uploadVoice": "आवाज़ अपलोड करें",
        "sendMessage": "संदेश भेजें",
        "startConversation": "बातचीत शुरू करें",
        "startConversation.description": "कोई भी कानूनी प्रश्न पूछें। मैं आपको जटिल कानूनी अवधारणाओं को सरल, स्पष्ट शब्दों में समझने में मदद करूंगा।"
      },
      "footer": {
        "termsOfService": "सेवा की शर्तें",
        "privacyPolicy": "गोपनीयता नीति",
        "contact": "संपर्क",
        "about": "हमारे बारे में",
        "copyright": "© 2024 लॉजिक AI. सभी अधिकार सुरक्षित।",
        "madeWith": "बनाया गया",
        "forJustice": "सुलभ न्याय के लिए"
      },
      "features": {
        "title": "सुविधाएं"
      },
      "common": {
        "loading": "लोड हो रहा है...",
        "error": "त्रुटि",
        "success": "सफलता",
        "uploadedFiles": "अपलोड की गई फ़ाइलें",
        "document": "दस्तावेज़",
        "voice": "आवाज़",
        "remove": "हटाएं"
      },
      "response": {
        "risk": "जोखिम",
        "disclaimer": "अस्वीकरण",
        "analysis": "विश्लेषण",
        "recommendation": "सिफारिश",
        "summary": "सारांश",
        "category": "श्रेणी",
        "documentSummary": "दस्तावेज़ का सारांश",
        "keyFindings": "मुख्य निष्कर्ष",
        "riskAssessment": "जोखिम मूल्यांकन",
        "level": "स्तर",
        "factors": "कारक",
        "complianceIssues": "अनुपालन मुद्दे",
        "nextSteps": "अगले कदम"
      },
      "suggestions": {
        "rental": "किराया विवाद में किरायेदार के रूप में मेरे क्या अधिकार हैं?",
        "tenantRights": "क्या मेरा मकान मालिक उचित नोटिस के बिना मुझे बेदखल कर सकता है?",
        "employment": "गलत तरीके से नौकरी से निकालना क्या है?",
        "legalDocument": "इस अनुबंध खंड को समझने में मेरी सहायता करें।"
      }
    }
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    debug: false,
    
    interpolation: {
      escapeValue: false,
    },

    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
      lookupLocalStorage: 'i18nextLng',
    },
  });

export default i18n;
