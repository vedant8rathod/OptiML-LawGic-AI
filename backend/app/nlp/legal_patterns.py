import re
from typing import List, Dict, Any, Optional

# Supported Legal Entity Categories
ENTITY_CATEGORIES = [
    "PERSON",
    "ORGANIZATION",
    "COURT",
    "LOCATION",
    "DATE",
    "MONEY",
    "PERCENTAGE",
    "EMAIL",
    "PHONE",
    "CASE_NUMBER",
    "STATUTE",
    "LEGAL_PROVISION",
    "LEGAL_ROLE",
    "ADVOCATE",
    "JUDGE",
    "LEGAL_EVENT",
]

# Common Indian Courts
COURT_PATTERNS = [
    r"\bSupreme\s+Court(?:\s+of\s+India)?\b",
    r"\b(?:High\s+Court\s+of\s+[A-Z][a-z]+|[A-Z][a-z]+\s+High\s+Court)\b",
    r"\b(?:National\s+Company\s+Law\s+Tribunal|NCLT|NCLAT)\b",
    r"\b(?:Debt\s+Recovery\s+Tribunal|DRT|DRAT)\b",
    r"\b(?:District\s+(?:and\s+Sessions\s+)?Court|Sessions\s+Court|Family\s+Court|Labour\s+Court|Consumer\s+Forum|Consumer\s+Disputes\s+Redressal\s+Commission)\b",
    r"\bCentral\s+Administrative\s+Tribunal\b",
    r"\bNational\s+Green\s+Tribunal\b",
]

# Common Indian Statutes / Acts
STATUTE_PATTERNS = [
    r"\b(?:The\s+)?Indian\s+Penal\s+Code(?:,\s*\d{4})?\b|\bIPC\b",
    r"\b(?:The\s+)?Code\s+of\s+Criminal\s+Procedure(?:,\s*\d{4})?\b|\bCrPC\b",
    r"\b(?:The\s+)?Code\s+of\s+Civil\s+Procedure(?:,\s*\d{4})?\b|\bCPC\b",
    r"\b(?:The\s+)?Constitution\s+of\s+India\b",
    r"\b(?:The\s+)?Indian\s+Contract\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Negotiable\s+Instruments\s+Act(?:,\s*\d{4})?\b|\bNI\s+Act\b",
    r"\b(?:The\s+)?Arbitration\s+and\s+Conciliation\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Companies\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Insolvency\s+and\s+Bankruptcy\s+Code(?:,\s*\d{4})?\b|\bIBC\b",
    r"\b(?:The\s+)?Consumer\s+Protection\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Information\s+Technology\s+Act(?:,\s*\d{4})?\b|\bIT\s+Act\b",
    r"\b(?:The\s+)?Transfer\s+of\s+Property\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Specific\s+Relief\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Industrial\s+Disputes\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Hindu\s+Marriage\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Motor\s+Vehicles\s+Act(?:,\s*\d{4})?\b",
    r"\b(?:The\s+)?Real\s+Estate\s+\(Regulation\s+and\s+Development\)\s+Act\b|\bRERA\b",
    r"\b[A-Z][A-Za-z\s]+(?:Act|Code|Rules|Regulations),\s*(?:18|19|20)\d{2}\b",
]

# Legal provisions (e.g., Section 138, Sec. 9, Article 21, Order 39 Rule 1, Clause 4.2)
PROVISION_PATTERNS = [
    r"\b(?:Section|Sec\.?|u/s|U/s)\s+\d+[A-Z]?(?:\s*\(\d+\)(?:\([a-z]\))?)?\b",
    r"\b(?:Article|Art\.?)\s+\d+[A-Z]?(?:\s*\(\d+\))?\b",
    r"\bOrder\s+[IVXLCDM\d]+\s+(?:Rule|R\.)\s+\d+\b",
    r"\b(?:Clause|Cl\.?)\s+\d+(?:\.\d+)*\b",
    r"\bRule\s+\d+[A-Z]?(?:\s*\(\d+\))?\b",
]

# Case citations / numbers (e.g. Writ Petition (Civil) No. 123 of 2021, AIR 1973 SC 1461, 2020 SCC OnLine SC 100)
CASE_NUMBER_PATTERNS = [
    r"\b(?:W\.?P\.?|Writ\s+Petition|Special\s+Leave\s+Petition|SLP|C\.?A\.?|Civil\s+Appeal|Criminal\s+Appeal|Crl\.?A\.?|O\.?M\.?P\.?|Company\s+Petition)\s*(?:\([A-Za-z\s]+\))?\s*(?:No\.?|Number)?\s*\d+\s*(?:of|/)\s*(?:19|20)\d{2}\b",
    r"\b(?:AIR|SCC|SCR)\s+(?:19|20)\d{2}\s+(?:SC|Del|Bom|Cal|Mad|All)?\s*\d+\b",
    r"\b(?:19|20)\d{2}\s+SCC\s+OnLine\s+[A-Za-z\s]+\d+\b",
    r"\bILR\s+(?:19|20)\d{2}\s+[A-Za-z\s]+\d+\b",
    r"\b(?:Suit|Case|FIR|Complaint)\s+No\.?\s*[:\-]?\s*\d+[\w/]*(?:\s+of\s+(?:19|20)\d{2})?\b",
]

# Indian and Global Currency Formats: ₹5,00,000, Rs. 10,000, INR 50,000, $10,000, USD 500
MONEY_PATTERNS = [
    r"(?:₹|Rs\.?|INR)\s*[\d,]+(?:\.\d{1,2})?(?:\s*(?:lakh|crore|thousand|hundred|crores|lakhs))?\b",
    r"(?:\$|USD|EUR|GBP)\s*[\d,]+(?:\.\d{1,2})?(?:\s*(?:million|billion|thousand))?\b",
    r"\b\d+(?:,\d+)*(?:\.\d{1,2})?\s*(?:Rupees|INR|Lakhs|Crores)\b",
]

# Percentage
PERCENT_PATTERNS = [
    r"\b\d+(?:\.\d+)?\s*(?:%|percent|per\s+cent)\b",
]

# Contact Info
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
PHONE_PATTERN = r"(?:\+91[\-\s]?)?[6-9]\d{4}[\-\s]?\d{5}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"

# Legal Roles (e.g. Petitioner, Respondent, Appellant, Defendant, Plaintiff, Lessor, Lessee, Employer, Employee)
LEGAL_ROLE_PATTERNS = [
    r"\b(?:Petitioner|Respondent|Appellant|Defendant|Plaintiff|Complainant|Accused|Applicant|Lessor|Lessee|Tenant|Landlord|Employer|Employee|Licensor|Licensee|Borrower|Lender|Mortgagor|Mortgagee|Purchaser|Vendor|Buyer|Seller|Indemnifier|Indemnitee|Arbitrator|Guarantor)\b",
]

# Advocates & Judges
JUDGE_PATTERNS = [
    r"\b(?:Hon'?ble\s+)?(?:Chief\s+Justice|Justice|Judge|Mr\.\s+Justice|Ms\.\s+Justice)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b",
    r"\b(?:C\.?J\.?I\.?|C\.?J\.?|J\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",
]

ADVOCATE_PATTERNS = [
    r"\b(?:Mr\.|Ms\.|Mrs\.|Shri|Dr\.)?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2},\s*(?:Senior\s+Advocate|Advocate|Learned\s+Counsel|Counsel|Standing\s+Counsel|Solicitor\s+General|Attorney\s+General)\b",
    r"\b(?:Adv\.|Advocate)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b",
]

# Legal Events
LEGAL_EVENT_PATTERNS = [
    r"\b(?:Filing|Registration|Hearing|Pronouncement|Order|Judgment|Decree|Summons|Notice|Eviction|Termination|Execution|Injunction|Arbitration\s+Proceeding|Cross-Examination|Bail\s+Hearing|Trial)\b",
]

# Standard Date patterns (supports Indian formats: 15/08/2023, 15-08-2023, 15th August 2023, August 15, 2023)
DATE_PATTERNS = [
    r"\b(?:\d{1,2}(?:st|nd|rd|th)?[\s\/\-\.]+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[\s\/\-\.]+(?:19|20)\d{2})\b",
    r"\b(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(?:19|20)\d{2})\b",
    r"\b\d{1,2}[-\/.]\d{1,2}[-\/.](?:19|20)\d{2}\b",
    r"\b(?:19|20)\d{2}[-\/.]\d{1,2}[-\/.]\d{1,2}\b",
]

# Organizations (Companies, LLPs, Ministries, Trusts, Banks)
ORG_PATTERNS = [
    r"\b[A-Z][A-Za-z0-9&.,\s]{2,40}\s+(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|Ltd\.?|Limited|LLP|Corporation|Inc\.?|Corp\.?|LLC|Bank|Insurance|Foundation|Trust|Association|Union|Authority|Board|Commission|Hospital|University)\b",
    r"\bMinistry\s+of\s+[A-Z][A-Za-z\s]+\b",
    r"\bState\s+Bank\s+of\s+India\b|\bReserve\s+Bank\s+of\s+India\b|\bLIC\b",
]

# Common Indian Cities & States for LOCATION
LOCATION_PATTERNS = [
    r"\b(?:New\s+Delhi|Delhi|Mumbai|Bengaluru|Bangalore|Chennai|Kolkata|Hyderabad|Ahmedabad|Pune|Jaipur|Lucknow|Chandigarh|Patna|Bhopal|Kochi|Cochin|Indore|Nagpur|Thiruvananthapuram|Shimla|Guwahati|Srinagar|Ranchi|Raipur|Bhubaneswar|Dehradun|Allahabad|Prayagraj)\b",
    r"\b(?:Maharashtra|Karnataka|Tamil\s+Nadu|Uttar\s+Pradesh|Gujarat|West\s+Bengal|Rajasthan|Kerala|Telangana|Andhra\s+Pradesh|Madhya\s+Pradesh|Punjab|Haryana|Bihar|Odisha|Assam|Goa|Uttarakhand|Himachal\s+Pradesh|Jharkhand|Chhattisgarh)\b",
    r"\b(?:India|United\s+States|United\s+Kingdom|Singapore|England|UAE)\b",
]

# Person honorifics and Indian names
PERSON_PATTERNS = [
    r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.|Shri|Smt\.|Kumari)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b",
]
