import json
import base64
import re
from typing import Dict, Any
from openai import OpenAI
from config import Config

class DocumentExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_document_data(self, image_path: str) -> Dict[str, Any]:
        """Extract text and data from document image"""
        try:
            base64_image = self.encode_image(image_path)
            
            # Simple, direct prompt for text extraction
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": "Extract ALL text you can see in this image. List everything clearly, including names, numbers, emails, addresses, and any other text. Be thorough."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            # Get the raw text response
            extracted_text = response.choices[0].message.content.strip()
            
            # Process the extracted text to find structured data
            structured_data = self._process_extracted_text(extracted_text)
            
            return {
                "status": "success",
                "image_file": image_path,
                "extraction": {
                    "document_type": structured_data["document_type"],
                    "extracted_text": extracted_text,
                    "structured_fields": structured_data["fields"],
                    "entities": structured_data["entities"],
                    "confidence": "high" if extracted_text else "low",
                    "metadata": {"processing_method": "direct_text_extraction"}
                },
                "metadata": {
                    "model": "gpt-4o-vision",
                    "processor": "document_extractor"
                }
            }
            
        except Exception as e:
            print(f"Document extraction error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "image_file": image_path,
                "extraction": {
                    "document_type": "unknown",
                    "extracted_text": f"Error: {str(e)}",
                    "structured_fields": {},
                    "entities": [],
                    "confidence": "low",
                    "metadata": {"error": True}
                },
                "metadata": {
                    "model": "gpt-4o-vision",
                    "processor": "document_extractor",
                    "error": str(e)
                }
            }
    
    def _process_extracted_text(self, text: str) -> Dict[str, Any]:
        """Process extracted text to find structured information"""
        if not text:
            return {
                "document_type": "unknown",
                "fields": {},
                "entities": []
            }
        
        # Detect document type based on content
        text_lower = text.lower()
        if any(word in text_lower for word in ["business card", "card", "contact"]):
            doc_type = "business_card"
        elif any(word in text_lower for word in ["invoice", "bill", "receipt"]):
            doc_type = "invoice"
        elif any(word in text_lower for word in ["form", "application"]):
            doc_type = "form"
        elif any(word in text_lower for word in ["license", "id", "passport"]):
            doc_type = "identification"
        else:
            doc_type = "document"
        
        # Extract structured fields using regex
        fields = {}
        entities = []
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            fields["email"] = emails[0]
            entities.extend(emails)
        
        # Phone number extraction
        phone_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US format
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',      # (123) 456-7890
            r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}'  # International
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                fields["phone"] = phones[0]
                entities.extend(phones)
                break
        
        # Website/URL extraction
        url_pattern = r'https?://[^\s]+|www\.[^\s]+'
        urls = re.findall(url_pattern, text)
        if urls:
            fields["website"] = urls[0]
            entities.extend(urls)
        
        # Address extraction (simple pattern)
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)'
        addresses = re.findall(address_pattern, text, re.IGNORECASE)
        if addresses:
            fields["address"] = addresses[0]
            entities.extend(addresses)
        
        # Name extraction (lines that look like names)
        lines = text.split('\n')
        potential_names = []
        for line in lines:
            line = line.strip()
            # Look for lines with 2-3 capitalized words (likely names)
            if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?$', line):
                potential_names.append(line)
        
        if potential_names:
            fields["name"] = potential_names[0]
            entities.extend(potential_names)
        
        # Company/Organization (lines with common business words)
        business_words = ["company", "corp", "inc", "llc", "ltd", "organization", "group"]
        for line in lines:
            line_lower = line.lower()
            if any(word in line_lower for word in business_words):
                fields["company"] = line.strip()
                entities.append(line.strip())
                break
        
        return {
            "document_type": doc_type,
            "fields": fields,
            "entities": list(set(entities))  # Remove duplicates
        }


# # Alternative even simpler version if needed
# class SimpleDocumentExtractor:
#     def __init__(self):
#         self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
#     def encode_image(self, image_path: str) -> str:
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode('utf-8')
    
#     def extract_document_data(self, image_path: str) -> Dict[str, Any]:
#         try:
#             base64_image = self.encode_image(image_path)
            
#             response = self.client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": [
#                             {"type": "text", "text": "What text do you see in this image? List all text clearly."},
#                             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
#                         ]
#                     }
#                 ],
#                 max_tokens=500
#             )
            
#             extracted_text = response.choices[0].message.content.strip()
            
#             return {
#                 "status": "success",
#                 "image_file": image_path,
#                 "extraction": {
#                     "document_type": "document",
#                     "extracted_text": extracted_text,
#                     "structured_fields": {"raw_text": extracted_text},
#                     "entities": [extracted_text] if extracted_text else [],
#                     "confidence": "medium",
#                     "metadata": {"simple_extraction": True}
#                 },
#                 "metadata": {
#                     "model": "gpt-4o-vision",
#                     "processor": "simple_document_extractor"
#                 }
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "image_file": image_path,
#                 "extraction": {
#                     "document_type": "error",
#                     "extracted_text": "",
#                     "structured_fields": {},
#                     "entities": [],
#                     "confidence": "low",
#                     "metadata": {"error": True}
#                 },
#                 "metadata": {"model": "gpt-4o-vision", "processor": "simple_document_extractor"}
#             }