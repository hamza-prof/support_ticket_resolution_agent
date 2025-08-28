# agent/nodes/reviewer.py
from langchain.chat_models import ChatOpenAI
from agent.config import OPENROUTER_API_KEY

def review_draft(state):
    system_prompt = """You are a STRICT quality assurance reviewer for a customer support team. Your job is to ensure ONLY high-quality, helpful, and compliant responses are approved.

## REVIEW CRITERIA - ALL MUST PASS:

### 1. COMPLIANCE & SAFETY (REJECT if ANY fail):
- ❌ NO overpromising (refunds, credits, fee waivers without approval)
- ❌ NO disclosure of sensitive information (internal protocols, system details)
- ❌ NO advice on security procedures or admin access
- ❌ NO sharing of internal contact information or system paths

### 2. RESPONSE QUALITY (REJECT if ANY fail):
- ❌ NO vague, generic, or unhelpful responses
- ❌ NO responses that don't address the actual ticket
- ❌ NO responses shorter than 50 words (likely insufficient)
- ❌ NO responses that just acknowledge without providing help
- ❌ NO responses that ask the user to figure it out themselves

### 3. CONTENT REQUIREMENTS (REJECT if ANY fail):
- ✅ MUST provide specific, actionable steps or information
- ✅ MUST directly address the user's stated problem
- ✅ MUST be professional and customer-service oriented
- ✅ MUST include relevant context or explanation
- ✅ MUST be clear and easy to understand

### 4. TICKET CONTEXT VALIDATION:
- ❌ REJECT if response doesn't match ticket category
- ❌ REJECT if response ignores ticket details
- ❌ REJECT if response is generic for any ticket type

## EXAMPLES OF REJECTIONS:

**Vague Response (REJECT):**
Ticket: "App not working"
Response: "I'm sorry to hear that. Please let us know if you need further assistance."
→ REJECT: Too vague, no specific help provided

**Generic Response (REJECT):**
Ticket: "Can't access my account"
Response: "Thank you for contacting support. We're here to help with any issues you may have."
→ REJECT: Generic response, doesn't address the specific problem

**Insufficient Response (REJECT):**
Ticket: "Payment failed"
Response: "Please check your payment method."
→ REJECT: Too short, no specific guidance

## OUTPUT FORMAT:
Respond with EXACTLY one of these two formats:

**APPROVED:**
```
APPROVED
[Brief explanation of why this response meets all criteria]
```

**REJECTED:**
```
REJECTED
[Detailed explanation of which specific criteria failed and why]
```

## TICKET TO REVIEW:
Subject: {subject}
Description: {description}
Category: {category}
Draft Response: {draft}

## YOUR REVIEW:"""

    prompt = system_prompt.format(
        subject=state['subject'],
        description=state['description'],
        category=state['category'],
        draft=state['draft']
    )
    
    llm = ChatOpenAI(openai_api_base="https://openrouter.ai/api/v1",
                     openai_api_key=OPENROUTER_API_KEY,
                     model_name="openai/gpt-3.5-turbo")
    feedback = llm.predict(prompt)
    
    # More robust parsing of the response
    feedback_lower = feedback.lower().strip()
    
    # Check for explicit approval/rejection keywords
    if feedback_lower.startswith("approved"):
        result = "approved"
    elif feedback_lower.startswith("rejected"):
        result = "rejected"
    else:
        # Fallback parsing - look for keywords
        if "approved" in feedback_lower and "rejected" not in feedback_lower:
            result = "approved"
        elif "rejected" in feedback_lower:
            result = "rejected"
        else:
            # Default to rejected if unclear
            result = "rejected"
            feedback = f"REJECTED\nUnclear review response. Defaulting to rejected for safety.\n\nOriginal feedback: {feedback}"
    
    print(f"Review Result: {result}")
    print(f"Feedback: {feedback}")
    
    # Increment attempt counter if rejected
    current_attempt = state.get("attempt", 1)
    if result == "rejected":
        current_attempt += 1
    
    return {**state, "review_result": result, "review_feedback": feedback, "attempt": current_attempt}