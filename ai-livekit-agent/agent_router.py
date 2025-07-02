from together_handler import get_llm_response
import re

class AgentRouter:
    def __init__(self):
        self.agents = {
            "sales": SalesAgent(),
            "technical": TechnicalAgent(), 
            "general": GeneralAgent(),
            "billing": BillingAgent()
        }
        self.current_agent = "sales"  # Default agent
        self.conversation_history = []
    
    def route_query(self, user_input):
        """Main routing logic to handle user queries"""
        print(f"🤖 Current Agent: {self.current_agent.upper()}")
        
        # Add to conversation history
        self.conversation_history.append(f"User: {user_input}")
        
        # Get response from current agent
        current_agent_obj = self.agents[self.current_agent]
        response = current_agent_obj.handle_query(user_input, self.conversation_history)
        
        # Check if transfer is needed
        if response.get("transfer_needed"):
            new_agent = response.get("transfer_to")
            if new_agent and new_agent in self.agents:
                print(f"🔄 Transferring call from {self.current_agent} to {new_agent}")
                self.current_agent = new_agent
                
                # Get response from new agent
                new_agent_obj = self.agents[new_agent]
                transfer_response = new_agent_obj.handle_transfer(user_input, self.conversation_history)
                
                self.conversation_history.append(f"Agent({new_agent}): {transfer_response['message']}")
                return f"🔄 Call transferred to {new_agent} agent.\n{transfer_response['message']}"
        
        # Normal response
        self.conversation_history.append(f"Agent({self.current_agent}): {response['message']}")
        return response["message"]

class BaseAgent:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
    
    def should_transfer(self, query):
        """Override in child classes to define transfer logic"""
        return False, None
    
    def handle_query(self, query, history):
        """Handle user query and decide if transfer needed"""
        transfer_needed, transfer_to = self.should_transfer(query)
        
        if transfer_needed:
            return {
                "transfer_needed": True,
                "transfer_to": transfer_to,
                "message": f"I'll transfer you to our {transfer_to} specialist who can better help you."
            }
        
        # Generate response using AI
        context = f"You are a {self.specialization}. Recent conversation: {' '.join(history[-3:])}"
        prompt = f"{context}\nUser: {query}\nRespond professionally:"
        
        response = get_llm_response(prompt)
        return {
            "transfer_needed": False,
            "message": response
        }
    
    def handle_transfer(self, query, history):
        """Handle transferred calls"""
        context = f"You are a {self.specialization}. This call was transferred to you. Recent conversation: {' '.join(history[-3:])}"
        prompt = f"{context}\nUser: {query}\nGreet them and provide help:"
        
        response = get_llm_response(prompt)
        return {"message": response}

class SalesAgent(BaseAgent):
    def __init__(self):
        super().__init__("Sales Agent", "sales specialist focused on product demos, pricing, and closing deals")
    
    def should_transfer(self, query):
        # Technical keywords that should go to technical agent
        technical_keywords = ["api", "integration", "bug", "error", "technical", "code", "development", "sdk"]
        billing_keywords = ["billing", "payment", "invoice", "refund", "subscription", "cancel", "upgrade"]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in technical_keywords):
            return True, "technical"
        elif any(keyword in query_lower for keyword in billing_keywords):
            return True, "billing"
        
        return False, None

class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__("Technical Agent", "technical specialist for API, integrations, troubleshooting, and development support")
    
    def should_transfer(self, query):
        sales_keywords = ["price", "cost", "buy", "purchase", "demo", "trial", "discount"]
        billing_keywords = ["billing", "payment", "invoice", "refund", "subscription", "charged", "charge", "credit card", "bank", "cancel", "upgrade", "downgrade"]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in billing_keywords):
            return True, "billing"
        elif any(keyword in query_lower for keyword in sales_keywords):
            return True, "sales"
        
        return False, None

class BillingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Billing Agent", "billing specialist for payments, subscriptions, invoices, and account management")
    
    def should_transfer(self, query):
        technical_keywords = ["api", "integration", "bug", "error", "technical", "code"]
        sales_keywords = ["demo", "trial", "new features", "product info"]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in technical_keywords):
            return True, "technical"
        elif any(keyword in query_lower for keyword in sales_keywords):
            return True, "sales"
        
        return False, None

class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__("General Agent", "general support agent for basic queries and routing")
    
    def should_transfer(self, query):
        # General agent transfers most specific queries
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["api", "technical", "integration", "bug"]):
            return True, "technical"
        elif any(word in query_lower for word in ["price", "buy", "demo", "sales"]):
            return True, "sales"
        elif any(word in query_lower for word in ["billing", "payment", "invoice"]):
            return True, "billing"
        
        return False, None 