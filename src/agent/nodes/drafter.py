# agent/nodes/drafter.py
from langchain.chat_models import ChatOpenAI
from agent.config import OPENROUTER_API_KEY

def generate_draft(state):
    # Check if this is a retry attempt
    current_attempt = state.get("attempt", 1)
    
    if current_attempt == 1:
        # First attempt - generate initial response
        system_prompt = """You are an expert customer support agent. Your job is to provide helpful, specific, and actionable responses to customer tickets.

## RESPONSE REQUIREMENTS:

### 1. ALWAYS provide specific, actionable help:
- Give step-by-step instructions when possible
- Include relevant context from the knowledge base
- Be professional and empathetic
- Address the specific issue mentioned

### 2. For vague or unclear tickets:
- Politely ask for more specific information
- Provide general guidance based on the category
- Suggest common solutions for that ticket type
- Ask clarifying questions to better assist

### 3. Response structure:
- Acknowledge the issue
- Provide specific help or ask for clarification
- Include relevant context from knowledge base
- End with next steps or offer further assistance

### 4. Quality standards:
- Minimum 50 words for substantive responses
- No generic acknowledgments
- Must be helpful and actionable
- Professional customer service tone

## TICKET CONTEXT:
Category: {category}
Knowledge Base Context: {context}

## CUSTOMER TICKET:
Subject: {subject}
Description: {description}

## YOUR RESPONSE:"""
    else:
        # Retry attempt - use reviewer feedback to improve
        system_prompt = """You are an expert customer support agent. This is a RETRY attempt to improve a previously rejected response.

## PREVIOUS ATTEMPT FEEDBACK:
{review_feedback}

## IMPROVEMENT REQUIREMENTS:
- Address ALL issues mentioned in the reviewer feedback
- Ensure the response meets quality standards
- Be more specific and helpful than the previous attempt
- Fix any compliance or safety issues identified

## RESPONSE REQUIREMENTS:

### 1. ALWAYS provide specific, actionable help:
- Give step-by-step instructions when possible
- Include relevant context from the knowledge base
- Be professional and empathetic
- Address the specific issue mentioned

### 2. Response structure:
- Acknowledge the issue
- Provide specific help or ask for clarification
- Include relevant context from knowledge base
- End with next steps or offer further assistance

### 3. Quality standards:
- Minimum 50 words for substantive responses
- No generic acknowledgments
- Must be helpful and actionable
- Professional customer service tone

## TICKET CONTEXT:
Category: {category}
Knowledge Base Context: {context}

## CUSTOMER TICKET:
Subject: {subject}
Description: {description}

## YOUR IMPROVED RESPONSE:"""

    # Format the prompt based on attempt number
    if current_attempt == 1:
        prompt = system_prompt.format(
            category=state['category'],
            context=state['context'],
            subject=state['subject'],
            description=state['description']
        )
    else:
        prompt = system_prompt.format(
            review_feedback=state.get('review_feedback', 'No specific feedback provided'),
            category=state['category'],
            context=state['context'],
            subject=state['subject'],
            description=state['description']
        )
    
    llm = ChatOpenAI(openai_api_base="https://openrouter.ai/api/v1",
                     openai_api_key=OPENROUTER_API_KEY,
                     model_name="openai/gpt-3.5-turbo")
    draft = llm.predict(prompt)
    
    # Increment attempt counter for next iteration
    return {**state, "draft": draft, "attempt": current_attempt}