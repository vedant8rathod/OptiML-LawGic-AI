import React, { createContext, useContext, useState, ReactNode } from 'react';

type Language = 'en' | 'hi';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const translations = {
  en: {
    // Header
    'header.askAI': 'Ask AI',
    'header.features': 'Features',
    'header.howItWorks': 'How It Works',
    'header.privacy': 'Privacy',
    'header.getStarted': 'Get Started',
    'header.askLegalAI': 'Ask Legal AI',

    // Brand
    'brand.name': 'LawGic AI',

    // Hero Section
    'hero.badge': 'Reimagining Fairness for Everyone',
    'hero.title': 'LawGic AI',
    'hero.tagline': 'Rights Over Riches',
    'hero.description': 'AI-powered legal assistance that makes law approachable, affordable, and understandable. Get clear answers, understand your rights, and access justice with compassion.',
    'hero.askLegalAI': 'Ask Legal AI',
    'hero.exploreFeatures': 'Explore Features',
    'hero.securePrivate': 'Secure & Private',
    'hero.multilingual': 'Multilingual',
    'hero.builtForPeople': 'Built for People',

    // Features Section
    'features.title': 'Features',
    'features.subtitle': 'Everything you need for legal clarity',
    'features.description': 'A comprehensive suite of AI-powered tools designed to make legal help accessible to everyone.',
    'features.askLegalAI.title': 'Ask Legal AI',
    'features.askLegalAI.description': 'Get instant answers to legal questions in plain language. AI-powered explanations with source citations.',
    'features.documentAnalyzer.title': 'Document Analyzer',
    'features.documentAnalyzer.description': 'Upload contracts and get clause-by-clause breakdowns with risk detection and compliance suggestions.',
    'features.guidedWorkflow.title': 'Guided Legal Workflow',
    'features.guidedWorkflow.description': 'Step-by-step roadmaps from problem to solution, with forms, deadlines, and direct connections to legal aid.',
    'features.multilingual.title': 'Multilingual Support',
    'features.multilingual.description': 'Full support for English, Hindi, and regional languages with culturally aware, voice-enabled assistance.',
    'features.privacy.title': 'Privacy & Trust',
    'features.privacy.description': 'End-to-end encryption, automatic PII redaction, and transparent data handling. You\'re always in control.',
    'features.visualSummaries.title': 'Visual Legal Summaries',
    'features.visualSummaries.description': 'Transform complex case files into interactive charts, timelines, and obligation trackers.',
    'features.partnerNetwork.title': 'Partner Network',
    'features.partnerNetwork.description': 'Connect with verified legal aid NGOs, pro bono lawyers, and university legal cells for direct help.',
    'features.futureInnovations.title': 'Future Innovations',
    'features.futureInnovations.description': 'Upcoming: Court filing automation, predictive analytics, and multi-jurisdiction database expansion.',

    // How It Works
    'howItWorks.title': 'How It Works',
    'howItWorks.subtitle': 'Simple, Clear, Effective',
    'howItWorks.description': 'Getting legal help shouldn\'t be complicated. Here\'s how we make it easy.',
    'howItWorks.step1.title': 'Ask Your Question',
    'howItWorks.step1.description': 'Type or speak your legal question in any language you\'re comfortable with.',
    'howItWorks.step2.title': 'Get Clear Answers',
    'howItWorks.step2.description': 'AI analyzes your query and provides plain-language explanations with relevant laws cited.',
    'howItWorks.step3.title': 'Take Action',
    'howItWorks.step3.description': 'Download forms, connect with legal aid, or get step-by-step guidance for your situation.',

    // Trust Section
    'trust.title': 'Privacy & Trust',
    'trust.subtitle': 'Your data, your control',
    'trust.description': 'We take your privacy seriously. Here\'s how we protect you.',
    'trust.encryption.title': 'End-to-End Encryption',
    'trust.encryption.description': 'All your conversations and documents are encrypted in transit and at rest. We use industry-standard AES-256 encryption.',
    'trust.piiRedaction.title': 'Automatic PII Redaction',
    'trust.piiRedaction.description': 'Personal information is automatically detected and redacted before processing. Your identity stays private.',
    'trust.gdprCompliant.title': 'GDPR Compliant',
    'trust.gdprCompliant.description': 'We follow international privacy standards including GDPR and Digital India compliance frameworks.',
    'trust.transparentAI.title': 'Transparent AI',
    'trust.transparentAI.description': 'Every AI response includes source citations and explainable reasoning. No black box decisions.',

    // CTA Section
    'cta.title': 'Ready to understand your rights?',
    'cta.description': 'Start your journey to accessible justice today. No credit card required.',
    'cta.getStarted': 'Get Started Free',

    // Ask AI Page
    'askAI.badge1': 'AI-Powered',
    'askAI.badge2': 'Private & Secure',
    'askAI.title': 'Ask Legal AI',
    'askAI.description': 'Choose how you want to interact — quick answers, document analysis, or in-depth research — and receive real-time insights directly from the LawGic AI backend.',
    'askAI.quickAnswer': 'Quick Answer',
    'askAI.quickAnswer.description': 'Text analysis via /api/predict/',
    'askAI.documentVoice': 'Document & Voice',
    'askAI.documentVoice.description': 'Comprehensive review via /api/analyze/',
    'askAI.legalResearch': 'Legal Research',
    'askAI.legalResearch.description': 'In-depth research via /api/research/',
    'askAI.startConversation': 'Start a conversation',
    'askAI.startConversation.description': 'Ask any legal question. I\'ll help you understand complex legal concepts in simple, clear terms.',
    'askAI.uploadDocument': 'Upload Document',
    'askAI.uploadVoice': 'Upload Voice',
    'askAI.privacyNotice.title': 'Your Privacy Matters',
    'askAI.privacyNotice.description': 'All conversations are encrypted. Personal information is automatically redacted before processing. We never share your data with third parties.',
    'askAI.placeholder.predict': 'Type your legal question for a quick analysis...',
    'askAI.placeholder.analyze': 'Describe the document or issue. Optionally attach a file or voice note...',
    'askAI.placeholder.research': 'Provide the legal topic or question you\'d like us to research...',
    'askAI.fileFormats': 'Text is optional when you attach supporting files. Supported formats: PDF, DOCX, TXT, WAV, MP3, M4A, OGG.',
    'askAI.textOnlyMode': 'This mode accepts text input only and returns a quick analysis from the backend.',

    // Common
    'common.live': 'Live',
    'common.comingSoon': 'Coming Soon',
    'common.certified': 'Certified',
    'common.noItems': 'No items were returned.',
    'common.noDetails': 'No additional details were provided.',
    'common.inputSummary': 'Input Summary',
    'common.referenceId': 'Reference ID',
    'common.textAnalysisResult': 'Text Analysis Result',
    'common.comprehensiveAnalysis': 'Comprehensive Analysis', 
    'common.legalResearchSummary': 'Legal Research Summary',
    'common.textAnalysisComplete': 'Text analysis complete',
    'common.documentAnalysisComplete': 'Document analysis complete',
    'common.legalResearchReady': 'Legal research ready',
    'common.enterQuestion': 'Please enter a question before sending.',
    'common.provideInput': 'Provide text, a document, or a voice note before sending.',
    'common.document': 'Document',
    'common.voice': 'Voice',
    'common.inputSubmitted': 'Input submitted.',
    'common.requestFailed': 'The request could not be completed',
    'common.unableToProcess': 'Unable to process your request at this time.',
    'common.backendUnreachable': 'Request failed. Please verify the backend is reachable.',
    'common.fileUploaded': 'File uploaded',
    'common.voiceFileUploaded': 'Voice file uploaded',
    'common.remove': 'Remove',
    'common.uploadedFiles': 'Uploaded Files',
    
    // Response Headers
    'response.risk': 'Risk',
    'response.risks': 'Risks',
    'response.disclaimer': 'Disclaimer',
    'response.warning': 'Warning',
    'response.warnings': 'Warnings',
    'response.legalAnalysis': 'Legal Analysis',
    'response.caseSummary': 'Case Summary',
    'response.documentSummary': 'Document Summary',
    'response.recommendation': 'Recommendation',
    'response.recommendations': 'Recommendations',
    'response.nextSteps': 'Next Steps',
    'response.legalImplications': 'Legal Implications',
    'response.compliance': 'Compliance',
    'response.jurisdiction': 'Jurisdiction',
    'response.relevantLaws': 'Relevant Laws',
    'response.keyPoints': 'Key Points',
    'response.analysis': 'Analysis',
    'response.summary': 'Summary',
    'response.conclusion': 'Conclusion',
    'response.importantNote': 'Important Note',
    'response.legalAdvice': 'Legal Advice',
    'response.courtDecisions': 'Court Decisions',
    'response.statute': 'Statute',
    'response.statutes': 'Statutes',
    'response.recentDevelopments': 'Recent Developments',
    'response.actionRequired': 'Action Required',
    'response.tenantRights': 'Tenant Rights',
    'response.rentalLaws': 'Rental Laws',
    'response.employmentLaw': 'Employment Law',
    'response.contractTerms': 'Contract Terms',
    'response.legalRights': 'Legal Rights',
    'response.category': 'Category',
    'response.keyFindings': 'Key Findings',
    'response.riskAssessment': 'Risk Assessment',
    'response.level': 'Level',
    'response.factors': 'Factors',
    'response.complianceIssues': 'Compliance Issues',
    'response.nextSteps': 'Next Steps',

    // Footer
    'footer.termsOfService': 'Terms of Service',
    'footer.privacyPolicy': 'Privacy Policy',
    'footer.contact': 'Contact',
    'footer.about': 'About',
    'footer.copyright': '© 2024 LawGic AI. All rights reserved.',
    'footer.madeWith': 'Made with',
    'footer.forJustice': 'for accessible justice',
    
    // Suggestions
    'suggestions.rental': 'Explain my rental agreement in simple terms',
    'suggestions.tenantRights': 'What are my rights as a tenant?',
    'suggestions.employment': 'Help me understand this employment contract',
    'suggestions.legalDocument': 'Analyze this legal document for key issues',
  },
  hi: {
    // Header - HINDI
    'header.askAI': 'AI से पूछें',
    'header.features': 'सुविधाएं',
    'header.howItWorks': 'यह कैसे काम करता है',
    'header.privacy': 'गोपनीयता',
    'header.getStarted': 'शुरू करें',
    'header.askLegalAI': 'कानूनी AI से पूछें',

    // Brand - HINDI
    'brand.name': 'लॉजिक AI',

    // Hero Section - HINDI
    'hero.badge': 'सभी के लिए न्याय की पुनर्कल्पना',
    'hero.title': 'लॉजिक AI',
    'hero.tagline': 'अधिकार धन से ऊपर',
    'hero.description': 'AI-संचालित कानूनी सहायता जो कानून को सुलभ, किफायती और समझने योग्य बनाती है। स्पष्ट उत्तर प्राप्त करें, अपने अधिकारों को समझें, और करुणा के साथ न्याय तक पहुंच प्राप्त करें।',
    'hero.askLegalAI': 'कानूनी AI से पूछें',
    'hero.exploreFeatures': 'सुविधाएं देखें',
    'hero.securePrivate': 'सुरक्षित और निजी',
    'hero.multilingual': 'बहुभाषी',
    'hero.builtForPeople': 'लोगों के लिए बनाया गया',

    // Features Section - HINDI
    'features.title': 'सुविधाएं',
    'features.subtitle': 'कानूनी स्पष्टता के लिए आपको जो कुछ भी चाहिए',
    'features.description': 'AI-संचालित उपकरणों का एक व्यापक सूट जो सभी के लिए कानूनी सहायता सुलभ बनाने के लिए डिज़ाइन किया गया है।',
    'features.askLegalAI.title': 'कानूनी AI से पूछें',
    'features.askLegalAI.description': 'कानूनी प्रश्नों के सरल भाषा में तुरंत उत्तर प्राप्त करें। स्रोत उद्धरणों के साथ AI-संचालित स्पष्टीकरण।',
    'features.documentAnalyzer.title': 'दस्तावेज़ विश्लेषक',
    'features.documentAnalyzer.description': 'अनुबंधों को अपलोड करें और जोखिम का पता लगाने और अनुपालन सुझावों के साथ खंड-दर-खंड विवरण प्राप्त करें।',
    'features.guidedWorkflow.title': 'निर्देशित कानूनी कार्यप्रवाह',
    'features.guidedWorkflow.description': 'समस्या से समाधान तक चरण-दर-चरण रोडमैप, फॉर्म, समय सीमा, और कानूनी सहायता के लिए प्रत्यक्ष संपर्क।',
    'features.multilingual.title': 'बहुभाषी समर्थन',
    'features.multilingual.description': 'अंग्रेजी, हिंदी, और क्षेत्रीय भाषाओं के लिए पूर्ण समर्थन के साथ सांस्कृतिक रूप से जागरूक, आवाज-सक्षम सहायता।',
    'features.privacy.title': 'गोपनीयता और विश्वास',
    'features.privacy.description': 'एंड-टू-एंड एन्क्रिप्शन, स्वचालित PII संपादन, और पारदर्शी डेटा हैंडलिंग। आप हमेशा नियंत्रण में रहते हैं।',
    'features.visualSummaries.title': 'विज़ुअल कानूनी सारांश',
    'features.visualSummaries.description': 'जटिल मामले की फाइलों को इंटरैक्टिव चार्ट, टाइमलाइन और दायित्व ट्रैकर में बदलें।',
    'features.partnerNetwork.title': 'भागीदार नेटवर्क',
    'features.partnerNetwork.description': 'प्रत्यक्ष सहायता के लिए सत्यापित कानूनी सहायता NGO, प्रो बोनो वकीलों, और विश्वविद्यालय कानूनी सेल से जुड़ें।',
    'features.futureInnovations.title': 'भविष्य की नवाचार',
    'features.futureInnovations.description': 'आगामी: कोर्ट फाइलिंग ऑटोमेशन, भविष्यसूचक विश्लेषण, और बहु-न्यायाधिकार डेटाबेस विस्तार।',

    // How It Works - HINDI
    'howItWorks.title': 'यह कैसे काम करता है',
    'howItWorks.subtitle': 'सरल, स्पष्ट, प्रभावी',
    'howItWorks.description': 'कानूनी सहायता प्राप्त करना जटिल नहीं होना चाहिए। यहां बताया गया है कि हम इसे आसान कैसे बनाते हैं।',
    'howItWorks.step1.title': 'अपना प्रश्न पूछें',
    'howItWorks.step1.description': 'अपना कानूनी प्रश्न किसी भी भाषा में टाइप करें या बोलें जिसमें आप सहज हैं।',
    'howItWorks.step2.title': 'स्पष्ट उत्तर प्राप्त करें',
    'howItWorks.step2.description': 'AI आपकी क्वेरी का विश्लेषण करता है और प्रासंगिक कानूनों के उद्धरण के साथ सरल भाषा में स्पष्टीकरण प्रदान करता है।',
    'howItWorks.step3.title': 'कार्रवाई करें',
    'howItWorks.step3.description': 'फॉर्म डाउनलोड करें, कानूनी सहायता से जुड़ें, या अपनी स्थिति के लिए चरण-दर-चरण मार्गदर्शन प्राप्त करें।',

    // Trust Section - HINDI
    'trust.title': 'गोपनीयता और विश्वास',
    'trust.subtitle': 'आपका डेटा, आपका नियंत्रण',
    'trust.description': 'हम आपकी गोपनीयता को गंभीरता से लेते हैं। यहां बताया गया है कि हम आपकी सुरक्षा कैसे करते हैं।',
    'trust.encryption.title': 'एंड-टू-एंड एन्क्रिप्शन',
    'trust.encryption.description': 'आपकी सभी बातचीत और दस्तावेज़ ट्रांजिट और आराम में एन्क्रिप्टेड हैं। हम उद्योग-मानक AES-256 एन्क्रिप्शन का उपयोग करते हैं।',
    'trust.piiRedaction.title': 'स्वचालित PII संपादन',
    'trust.piiRedaction.description': 'व्यक्तिगत जानकारी स्वचालित रूप से पहचानी जाती है और प्रसंस्करण से पहले संपादित की जाती है। आपकी पहचान निजी रहती है।',
    'trust.gdprCompliant.title': 'GDPR अनुपालित',
    'trust.gdprCompliant.description': 'हम GDPR और डिजिटल इंडिया अनुपालन फ्रेमवर्क सहित अंतर्राष्ट्रीय गोपनीयता मानकों का पालन करते हैं।',
    'trust.transparentAI.title': 'पारदर्शी AI',
    'trust.transparentAI.description': 'हर AI प्रतिक्रिया में स्रोत उद्धरण और समझाने योग्य तर्क शामिल है। कोई ब्लैक बॉक्स निर्णय नहीं।',

    // CTA Section - HINDI
    'cta.title': 'अपने अधिकारों को समझने के लिए तैयार हैं?',
    'cta.description': 'आज ही सुलभ न्याय की अपनी यात्रा शुरू करें। किसी क्रेडिट कार्ड की आवश्यकता नहीं।',
    'cta.getStarted': 'मुफ्त में शुरू करें',

    // Ask AI Page - HINDI
    'askAI.badge1': 'AI-संचालित',
    'askAI.badge2': 'निजी और सुरक्षित',
    'askAI.title': 'कानूनी AI से पूछें',
    'askAI.description': 'चुनें कि आप कैसे बातचीत करना चाहते हैं — त्वरित उत्तर, दस्तावेज़ विश्लेषण, या गहन अनुसंधान — और LawGic AI बैकएंड से वास्तविक समय में अंतर्दृष्टि प्राप्त करें।',
    'askAI.quickAnswer': 'त्वरित उत्तर',
    'askAI.quickAnswer.description': '/api/predict/ के माध्यम से पाठ विश्लेषण',
    'askAI.documentVoice': 'दस्तावेज़ और आवाज',
    'askAI.documentVoice.description': '/api/analyze/ के माध्यम से व्यापक समीक्षा',
    'askAI.legalResearch': 'कानूनी अनुसंधान',
    'askAI.legalResearch.description': '/api/research/ के माध्यम से गहन अनुसंधान',
    'askAI.startConversation': 'बातचीत शुरू करें',
    'askAI.startConversation.description': 'कोई भी कानूनी प्रश्न पूछें। मैं आपको जटिल कानूनी अवधारणाओं को सरल, स्पष्ट शब्दों में समझने में मदद करूंगा।',
    'askAI.uploadDocument': 'दस्तावेज़ अपलोड करें',
    'askAI.uploadVoice': 'आवाज अपलोड करें',
    'askAI.privacyNotice.title': 'आपकी गोपनीयता मायने रखती है',
    'askAI.privacyNotice.description': 'सभी बातचीत एनक्रिप्टेड हैं। व्यक्तिगत जानकारी प्रसंस्करण से पहले स्वचालित रूप से संपादित की जाती है। हम आपका डेटा तीसरे पक्ष के साथ कभी साझा नहीं करते हैं।',
    'askAI.placeholder.predict': 'त्वरित विश्लेषण के लिए अपना कानूनी प्रश्न टाइप करें...',
    'askAI.placeholder.analyze': 'दस्तावेज़ या मुद्दे का वर्णन करें। वैकल्पिक रूप से फाइल या आवाज नोट संलग्न करें...',
    'askAI.placeholder.research': 'वह कानूनी विषय या प्रश्न प्रदान करें जिसपर आप अनुसंधान चाहते हैं...',
    'askAI.fileFormats': 'सहायक फाइलें संलग्न करते समय पाठ वैकल्पिक है। समर्थित प्रारूप: PDF, DOCX, TXT, WAV, MP3, M4A, OGG।',
    'askAI.textOnlyMode': 'यह मोड केवल पाठ इनपुट को स्वीकार करता है और बैकएंड से त्वरित विश्लेषण वापस करता है।',

    // Common - HINDI
    'common.live': 'लाइव',
    'common.comingSoon': 'जल्दी आ रहा है',
    'common.certified': 'प्रमाणित',
    'common.noItems': 'कोई आइटम वापस नहीं किया गया।',
    'common.noDetails': 'कोई अतिरिक्त विवरण प्रदान नहीं किया गया।',
    'common.inputSummary': 'इनपुट सारांश',
    'common.referenceId': 'संदर्भ आईडी',
    'common.textAnalysisResult': 'पाठ विश्लेषण परिणाम',
    'common.comprehensiveAnalysis': 'व्यापक विश्लेषण',
    'common.legalResearchSummary': 'कानूनी अनुसंधान सारांश',
    'common.textAnalysisComplete': 'पाठ विश्लेषण पूर्ण',
    'common.documentAnalysisComplete': 'दस्तावेज़ विश्लेषण पूर्ण',
    'common.legalResearchReady': 'कानूनी अनुसंधान तैयार',
    'common.enterQuestion': 'कृपया भेजने से पहले एक प्रश्न दर्ज करें।',
    'common.provideInput': 'भेजने से पहले पाठ, दस्तावेज़, या आवाज नोट प्रदान करें।',
    'common.document': 'दस्तावेज़',
    'common.voice': 'आवाज',
    'common.inputSubmitted': 'इनपुट सबमिट किया गया।',
    'common.requestFailed': 'अनुरोध पूरा नहीं हो सका',
    'common.unableToProcess': 'इस समय आपके अनुरोध को संसाधित करने में असमर्थ।',
    'common.backendUnreachable': 'अनुरोध विफल। कृपया सत्यापित करें कि बैकएंड पहुंच योग्य है।',
    'common.fileUploaded': 'फाइल अपलोड हुई',
    'common.voiceFileUploaded': 'आवाज फाइल अपलोड हुई',
    'common.remove': 'हटाएं',
    'common.uploadedFiles': 'अपलोड की गई फाइलें',
    
    // Response Headers - HINDI
    'response.risk': 'जोखिम',
    'response.risks': 'जोखिम',
    'response.disclaimer': 'अस्वीकरण',
    'response.warning': 'चेतावनी',
    'response.warnings': 'चेतावनियां',
    'response.legalAnalysis': 'कानूनी विश्लेषण',
    'response.caseSummary': 'मामले का सारांश',
    'response.documentSummary': 'दस्तावेज़ का सारांश',
    'response.recommendation': 'सिफारिश',
    'response.recommendations': 'सिफारिशें',
    'response.nextSteps': 'अगले कदम',
    'response.legalImplications': 'कानूनी प्रभाव',
    'response.compliance': 'अनुपालन',
    'response.jurisdiction': 'क्षेत्राधिकार',
    'response.relevantLaws': 'प्रासंगिक कानून',
    'response.keyPoints': 'मुख्य बिंदु',
    'response.analysis': 'विश्लेषण',
    'response.summary': 'सारांश',
    'response.conclusion': 'निष्कर्ष',
    'response.importantNote': 'महत्वपूर्ण नोट',
    'response.legalAdvice': 'कानूनी सलाह',
    'response.courtDecisions': 'अदालती फैसले',
    'response.statute': 'कानून',
    'response.statutes': 'कानून',
    'response.recentDevelopments': 'हाल के विकास',
    'response.actionRequired': 'आवश्यक कार्रवाई',
    'response.tenantRights': 'किरायेदार अधिकार',
    'response.rentalLaws': 'किराया कानून',
    'response.employmentLaw': 'रोजगार कानून',
    'response.contractTerms': 'अनुबंध की शर्तें',
    'response.legalRights': 'कानूनी अधिकार',
    'response.category': 'श्रेणी',
    'response.keyFindings': 'मुख्य निष्कर्ष',
    'response.riskAssessment': 'जोखिम मूल्यांकन',
    'response.level': 'स्तर',
    'response.factors': 'कारक',
    'response.complianceIssues': 'अनुपालन मुद्दे',
    'response.nextSteps': 'अगले कदम',

    // Footer - HINDI
    'footer.termsOfService': 'सेवा की शर्तें',
    'footer.privacyPolicy': 'गोपनीयता नीति',
    'footer.contact': 'संपर्क',
    'footer.about': 'हमारे बारे में',
    'footer.copyright': '© 2024 लॉजिक AI. सभी अधिकार सुरक्षित।',
    'footer.madeWith': 'बनाया गया',
    'footer.forJustice': 'सुलभ न्याय के लिए',
    
    // Suggestions - HINDI
    'suggestions.rental': 'मेरे किराया समझौते को सरल शब्दों में समझाएं',
    'suggestions.tenantRights': 'किरायेदार के रूप में मेरे अधिकार क्या हैं?',
    'suggestions.employment': 'इस रोजगार अनुबंध को समझने में मेरी सहायता करें',
    'suggestions.legalDocument': 'मुख्य मुद्दों के लिए इस कानूनी दस्तावेज़ का विश्लेषण करें',
  },
};

interface LanguageProviderProps {
  children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [language, setLanguage] = useState<Language>('en');

  const t = (key: string): string => {
    return translations[language][key as keyof typeof translations[Language]] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};