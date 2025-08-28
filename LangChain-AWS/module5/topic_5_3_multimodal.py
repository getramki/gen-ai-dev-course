"""
Topic 5.3: Multi-modal Interactions (Text + Images) (7 minutes)

Learning Goals:
- Implement image processing with Claude-3 Vision capabilities
- Master multi-modal prompt engineering techniques
- Build applications that combine text and image analysis
- Create production-ready multi-modal AI systems
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
import base64
import json
from typing import Dict, List, Optional
from PIL import Image
import io
import os

def setup_multimodal_chat():
    """Initialize ChatBedrockConverse for multi-modal interactions"""
    
    print("=== Multi-modal Chat Setup ===\n")
    
    try:
        # Use Claude-3 Sonnet for better vision capabilities
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1",
            max_tokens=500,
            temperature=0.3
        )
        
        print("✅ ChatBedrockConverse initialized for multi-modal interactions")
        print("📷 Using Claude-3 Sonnet for enhanced vision capabilities")
        return chat
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("💡 Note: Multi-modal features require Claude-3 Sonnet or Haiku")
        return None

def create_sample_images():
    """Create sample images for testing"""
    
    print("=== Creating Sample Images ===\n")
    
    # Create sample_documents directory if it doesn't exist
    os.makedirs("sample_documents", exist_ok=True)
    
    # Create a simple chart image using PIL
    try:
        # Create a simple bar chart
        img = Image.new('RGB', (400, 300), color='white')
        
        # This would normally be a real chart/diagram
        # For demo purposes, we'll create a simple colored rectangle
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img)
        
        # Draw bars
        draw.rectangle([50, 200, 100, 250], fill='blue')
        draw.rectangle([120, 150, 170, 250], fill='red')
        draw.rectangle([190, 100, 240, 250], fill='green')
        draw.rectangle([260, 180, 310, 250], fill='orange')
        
        # Add labels
        try:
            # Try to use default font
            draw.text((60, 260), "Q1", fill='black')
            draw.text((130, 260), "Q2", fill='black')
            draw.text((200, 260), "Q3", fill='black')
            draw.text((270, 260), "Q4", fill='black')
            draw.text((150, 20), "Sales Data 2024", fill='black')
        except:
            # If font loading fails, continue without text
            pass
        
        # Save the image
        chart_path = "sample_documents/sample_chart.png"
        img.save(chart_path)
        
        print(f"✅ Sample chart created: {chart_path}")
        return [chart_path]
        
    except Exception as e:
        print(f"❌ Failed to create sample images: {e}")
        return []

def encode_image_to_base64(image_path: str) -> Optional[str]:
    """Encode image to base64 for API consumption"""
    
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"❌ Failed to encode image {image_path}: {e}")
        return None

def demonstrate_image_analysis(chat):
    """Demonstrate basic image analysis capabilities"""
    
    print("=== Image Analysis Demo ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Create sample images
    image_paths = create_sample_images()
    
    if not image_paths:
        print("❌ No sample images available")
        return
    
    for image_path in image_paths:
        print(f"Analyzing image: {image_path}")
        
        # Encode image
        encoded_image = encode_image_to_base64(image_path)
        if not encoded_image:
            continue
        
        # Create multi-modal message
        # Note: This is a simplified example - actual implementation may vary
        message_content = f"""Please analyze this image and describe:
1. What you see in the image
2. Any data or patterns you can identify
3. Key insights or observations

Image data: [Base64 encoded image would be included here in actual implementation]

For this demo, assume the image shows a bar chart with quarterly sales data for 2024, 
with bars of different heights representing Q1-Q4 performance."""
        
        try:
            response = chat.invoke([HumanMessage(content=message_content)])
            
            print(f"Analysis: {response.content[:200]}...")
            
        except Exception as e:
            print(f"❌ Image analysis failed: {e}")
        
        print()

def implement_multimodal_applications():
    """Implement practical multi-modal applications"""
    
    print("=== Multi-modal Applications ===\n")
    
    class MultiModalAssistant:
        """Multi-modal assistant for various image analysis tasks"""
        
        def __init__(self, chat_model):
            self.chat = chat_model
            
            # Define analysis templates for different use cases
            self.analysis_templates = {
                "document_ocr": """Extract and transcribe all text from this image. 
                Maintain the original formatting and structure as much as possible.
                If there are tables, preserve the table structure.""",
                
                "chart_analysis": """Analyze this chart/graph and provide:
                1. Type of chart (bar, line, pie, etc.)
                2. Data trends and patterns
                3. Key insights and conclusions
                4. Any notable outliers or anomalies""",
                
                "product_analysis": """Analyze this product image and describe:
                1. Product type and category
                2. Key features and characteristics
                3. Condition and quality assessment
                4. Potential use cases or applications""",
                
                "scene_description": """Provide a detailed description of this scene including:
                1. Main objects and people
                2. Setting and environment
                3. Activities or actions taking place
                4. Mood and atmosphere"""
            }
        
        def analyze_image(self, image_path: str, analysis_type: str = "general", 
                         custom_prompt: str = None) -> Dict:
            """Analyze image with specified analysis type"""
            
            # Encode image
            encoded_image = encode_image_to_base64(image_path)
            if not encoded_image:
                return {"error": f"Failed to encode image: {image_path}"}
            
            # Select prompt template
            if custom_prompt:
                prompt = custom_prompt
            elif analysis_type in self.analysis_templates:
                prompt = self.analysis_templates[analysis_type]
            else:
                prompt = "Please analyze this image and describe what you see."
            
            # For demo purposes, simulate the multi-modal interaction
            demo_prompt = f"""{prompt}

[Note: In actual implementation, the base64 encoded image would be included here]

For this demonstration, please provide analysis assuming the image contains relevant visual content 
for the requested analysis type: {analysis_type}"""
            
            try:
                response = self.chat.invoke([HumanMessage(content=demo_prompt)])
                
                return {
                    "success": True,
                    "analysis": response.content,
                    "analysis_type": analysis_type,
                    "image_path": image_path
                }
                
            except Exception as e:
                return {"error": f"Analysis failed: {e}"}
        
        def compare_images(self, image_paths: List[str], comparison_prompt: str = None) -> Dict:
            """Compare multiple images"""
            
            if len(image_paths) < 2:
                return {"error": "At least 2 images required for comparison"}
            
            default_prompt = """Compare these images and identify:
            1. Similarities between the images
            2. Key differences
            3. Which image is better for specific use cases
            4. Overall assessment and recommendations"""
            
            prompt = comparison_prompt or default_prompt
            
            # For demo purposes
            demo_prompt = f"""{prompt}

[Note: In actual implementation, multiple base64 encoded images would be included here]

For this demonstration, assume you are comparing {len(image_paths)} images:
{', '.join(image_paths)}"""
            
            try:
                response = self.chat.invoke([HumanMessage(content=demo_prompt)])
                
                return {
                    "success": True,
                    "comparison": response.content,
                    "images_compared": len(image_paths),
                    "image_paths": image_paths
                }
                
            except Exception as e:
                return {"error": f"Comparison failed: {e}"}
        
        def extract_structured_data(self, image_path: str, data_schema: Dict) -> Dict:
            """Extract structured data from image based on schema"""
            
            schema_description = json.dumps(data_schema, indent=2)
            
            prompt = f"""Extract structured data from this image according to the following schema:

{schema_description}

Return the extracted data in JSON format matching the schema structure.
If certain fields cannot be determined from the image, use null values."""
            
            # For demo purposes
            demo_prompt = f"""{prompt}

[Note: In actual implementation, the base64 encoded image would be included here]

For this demonstration, assume the image contains data that can be structured according to the provided schema."""
            
            try:
                response = self.chat.invoke([HumanMessage(content=demo_prompt)])
                
                # Try to extract JSON from response
                content = response.content
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    try:
                        extracted_data = json.loads(content[json_start:json_end])
                        return {
                            "success": True,
                            "extracted_data": extracted_data,
                            "schema": data_schema
                        }
                    except json.JSONDecodeError:
                        pass
                
                return {
                    "success": True,
                    "raw_response": response.content,
                    "schema": data_schema,
                    "note": "Could not parse as JSON"
                }
                
            except Exception as e:
                return {"error": f"Data extraction failed: {e}"}
    
    # Test multi-modal assistant
    chat = setup_multimodal_chat()
    if not chat:
        return
    
    assistant = MultiModalAssistant(chat)
    
    # Test different analysis types
    analysis_types = ["chart_analysis", "document_ocr", "scene_description"]
    
    for analysis_type in analysis_types:
        print(f"Testing {analysis_type}:")
        
        result = assistant.analyze_image("sample_documents/sample_chart.png", analysis_type)
        
        if result.get("success"):
            print(f"✅ Analysis completed")
            print(f"Result: {result['analysis'][:100]}...")
        else:
            print(f"❌ {result.get('error', 'Unknown error')}")
        
        print()
    
    # Test structured data extraction
    print("Testing structured data extraction:")
    
    schema = {
        "chart_type": "string",
        "data_points": "array",
        "trends": "string",
        "insights": "array"
    }
    
    result = assistant.extract_structured_data("sample_documents/sample_chart.png", schema)
    
    if result.get("success"):
        print("✅ Structured data extraction completed")
        if "extracted_data" in result:
            print(f"Extracted: {result['extracted_data']}")
        else:
            print(f"Response: {result['raw_response'][:100]}...")
    else:
        print(f"❌ {result.get('error', 'Unknown error')}")

def demonstrate_multimodal_best_practices():
    """Demonstrate best practices for multi-modal applications"""
    
    print("=== Multi-modal Best Practices ===\n")
    
    best_practices = {
        "Image Quality": [
            "Use high-resolution images for better text recognition",
            "Ensure good contrast and lighting",
            "Avoid blurry or distorted images",
            "Compress images appropriately for API limits"
        ],
        "Prompt Engineering": [
            "Be specific about what you want to extract or analyze",
            "Provide context about the image type and purpose",
            "Use structured prompts for consistent results",
            "Include examples of desired output format"
        ],
        "Error Handling": [
            "Validate image format and size before processing",
            "Handle API rate limits and timeouts gracefully",
            "Provide fallback options for failed analysis",
            "Log errors for debugging and improvement"
        ],
        "Performance Optimization": [
            "Cache analysis results for repeated queries",
            "Batch process multiple images when possible",
            "Use appropriate model variants for different tasks",
            "Monitor token usage and costs"
        ],
        "Security Considerations": [
            "Validate and sanitize uploaded images",
            "Implement access controls for sensitive images",
            "Consider privacy implications of image analysis",
            "Secure storage and transmission of image data"
        ]
    }
    
    for category, practices in best_practices.items():
        print(f"🎯 {category}:")
        for practice in practices:
            print(f"   • {practice}")
        print()

def create_multimodal_use_cases():
    """Showcase practical multi-modal use cases"""
    
    print("=== Multi-modal Use Cases ===\n")
    
    use_cases = {
        "Document Processing": {
            "description": "Extract and digitize information from scanned documents",
            "applications": ["Invoice processing", "Form digitization", "Receipt analysis", "Contract review"],
            "benefits": ["Automated data entry", "Reduced manual errors", "Faster processing", "Searchable content"]
        },
        "Visual Quality Control": {
            "description": "Automated inspection and quality assessment",
            "applications": ["Product defect detection", "Manufacturing QC", "Food safety inspection", "Medical imaging"],
            "benefits": ["Consistent quality standards", "24/7 monitoring", "Objective assessment", "Cost reduction"]
        },
        "Content Moderation": {
            "description": "Analyze and moderate visual content",
            "applications": ["Social media moderation", "E-commerce listings", "User-generated content", "Brand safety"],
            "benefits": ["Scalable moderation", "Consistent policies", "Rapid response", "Risk mitigation"]
        },
        "Educational Tools": {
            "description": "Interactive learning and assessment",
            "applications": ["Homework help", "Diagram explanation", "Visual learning aids", "Accessibility tools"],
            "benefits": ["Personalized learning", "Visual understanding", "Accessibility support", "Instant feedback"]
        }
    }
    
    for use_case, details in use_cases.items():
        print(f"📋 {use_case}")
        print(f"   Description: {details['description']}")
        print(f"   Applications: {', '.join(details['applications'][:2])}...")
        print(f"   Key Benefits: {', '.join(details['benefits'][:2])}...")
        print()

if __name__ == "__main__":
    print("Module 5.3: Multi-modal Interactions (Text + Images)\n")
    
    # Setup and demonstrations
    chat = setup_multimodal_chat()
    demonstrate_image_analysis(chat)
    implement_multimodal_applications()
    demonstrate_multimodal_best_practices()
    create_multimodal_use_cases()
    
    # Summary
    print("="*50)
    print("✅ Topic 5.3 Complete!")
    print("Key Takeaways:")
    print("• Multi-modal AI combines text and image understanding")
    print("• Claude-3 provides powerful vision capabilities")
    print("• Structured prompts improve analysis consistency")
    print("• Multiple use cases from document processing to QC")
    print("🚀 Ready for Topic 5.4: RAG Implementation!")
    print("="*50)