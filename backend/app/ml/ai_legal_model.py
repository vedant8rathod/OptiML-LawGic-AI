import json
import os
from datetime import datetime
from typing import Any, List, Dict

class AiLegalAssistantModel:
    """
    AI Legal Assistant Model with demo fallback capabilities.
    Provides contract analysis and legal guidance with structured responses.
    """
    
    def __init__(self, task: str = "legal_analysis"):
        self.task = task
        
    def _analyze_contract(self, text: str) -> Dict[str, Any]:
        """Analyze contract text and return structured analysis."""
        text_lower = text.lower()
        
        # Identify potential issues in contracts
        risk_indicators = {
            "high": ["terminate without notice", "no refund", "unlimited liability", "exclusive jurisdiction"],
            "medium": ["late fees", "automatic renewal", "binding arbitration", "limitation of liability"],
            "low": ["30 days notice", "reasonable efforts", "mutual agreement", "standard terms"]
        }
        
        findings = []
        overall_risk = "Low"
        
        for risk_level, indicators in risk_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    clause_text = f"Found clause containing: '{indicator}'"
                    risk = risk_level.title()
                    if risk_level == "high":
                        overall_risk = "High"
                        rewrite = f"Consider revising clause about '{indicator}' to include more balanced terms."
                    elif risk_level == "medium" and overall_risk != "High":
                        overall_risk = "Medium"
                        rewrite = f"Review clause about '{indicator}' for potential modifications."
                    else:
                        rewrite = f"Clause about '{indicator}' appears standard."
                    
                    explanation = f"This clause may impact your rights and obligations. {rewrite}"
                    
                    findings.append({
                        "clause": clause_text,
                        "risk": risk,
                        "rewrite": rewrite,
                        "explanation": explanation
                    })
        
        # Default findings if no specific indicators found
        if not findings:
            findings = [{
                "clause": "General contract terms reviewed",
                "risk": "Low",
                "rewrite": "Standard contract language appears to be used",
                "explanation": "This contract appears to use standard terms. Consider having it reviewed by a legal professional for specific concerns."
            }]
        
        return {
            "analysis_type": "contract_review",
            "overall_risk": overall_risk,
            "findings": findings[:5],  # Limit to top 5 findings
            "recommendations": [
                "Have the contract reviewed by a qualified attorney",
                "Negotiate any unfavorable terms before signing",
                "Keep copies of all contract-related communications",
                "Understand your termination and dispute resolution options"
            ]
        }
    
    def _analyze_legal_query(self, text: str) -> Dict[str, Any]:
        """Analyze general legal query and provide guidance."""
        text_lower = text.lower()
        
        # Categorize query
        categories = {
            "tenant_rights": ["rent", "landlord", "tenant", "eviction", "lease", "housing"],
            "employment": ["job", "work", "employer", "salary", "wage", "termination", "harassment"],
            "contract": ["contract", "agreement", "terms", "breach", "obligation"],
            "criminal": ["arrest", "police", "court", "criminal", "charges", "bail"],
            "family": ["divorce", "custody", "child support", "marriage", "domestic"]
        }
        
        category = "general"
        for cat, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                category = cat
                break
        
        # Generate category-specific advice
        advice_templates = {
            "tenant_rights": {
                "summary": "This appears to be a tenant rights issue.",
                "key_points": [
                    "Tenants have right to habitable living conditions",
                    "Landlords must follow proper legal procedures",
                    "Security deposits have specific legal protections",
                    "Local tenant protection laws may apply"
                ],
                "next_steps": [
                    "Document all communications with your landlord",
                    "Research your local tenant rights laws",
                    "Contact local tenant rights organizations",
                    "Consider consulting with a tenant rights attorney"
                ]
            },
            "employment": {
                "summary": "This appears to be an employment law matter.",
                "key_points": [
                    "Employees have rights to fair wages and safe working conditions",
                    "Discrimination and harassment are prohibited by law",
                    "Termination procedures must follow legal requirements",
                    "Workers may have rights to unemployment benefits"
                ],
                "next_steps": [
                    "Document all workplace incidents and communications",
                    "Review your employee handbook and contract",
                    "Contact your HR department if appropriate",
                    "Consider consulting with an employment attorney"
                ]
            },
            "criminal": {
                "summary": "This appears to involve criminal law matters.",
                "key_points": [
                    "You have the right to remain silent",
                    "You have the right to legal representation",
                    "You are presumed innocent until proven guilty",
                    "Police must follow proper procedures"
                ],
                "next_steps": [
                    "Contact a criminal defense attorney immediately",
                    "Do not speak to police without an attorney present",
                    "Gather all relevant documents and evidence",
                    "Understand your bail and court appearance requirements"
                ]
            },
            "general": {
                "summary": "This appears to be a general legal inquiry.",
                "key_points": [
                    "Legal issues can be complex and fact-specific",
                    "Professional legal advice is often necessary",
                    "Documentation is crucial in legal matters",
                    "Time limits may apply to legal actions"
                ],
                "next_steps": [
                    "Consult with a qualified attorney in the relevant area of law",
                    "Gather all relevant documents and evidence",
                    "Research applicable laws in your jurisdiction",
                    "Act promptly as legal deadlines may apply"
                ]
            }
        }
        
        template = advice_templates.get(category, advice_templates["general"])
        
        return {
            "analysis_type": "legal_guidance",
            "category": category.replace("_", " ").title(),
            "summary": template["summary"],
            "key_points": template["key_points"],
            "recommendations": template["next_steps"],
            "disclaimer": "This is general information only and not legal advice. Consult with a qualified attorney for advice specific to your situation."
        }
    
    def predict(self, X: Any) -> List[str]:
        """
        Main prediction method that returns JSON string responses.
        """
        if isinstance(X, str):
            inputs = [X]
        elif isinstance(X, list):
            inputs = X
        else:
            inputs = [str(X)]
        
        results = []
        for text in inputs:
            try:
                # Determine analysis type based on content
                if any(keyword in text.lower() for keyword in ["contract", "agreement", "terms", "clause"]):
                    analysis = self._analyze_contract(text)
                else:
                    analysis = self._analyze_legal_query(text)
                
                # Add metadata (no demo markers)
                analysis.update({
                    "model_version": "heuristic_v1.0",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                
                results.append(json.dumps(analysis, indent=2))
                
            except Exception as e:
                error_response = {
                    "error": f"Analysis failed: {str(e)}",
                    "demo_note": "This is a demo response due to an error in analysis."
                }
                results.append(json.dumps(error_response))
        
        return results