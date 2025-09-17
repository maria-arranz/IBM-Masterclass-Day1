# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
# Travel Companion AI Agent Challenge Solution (Basic + Bonus)
# This solution demonstrates how to create a specialized travel advisor
# using Azure AI Foundry agents with Chainlit web interface.
# ---------------------------------------------------------------------
import os
import chainlit as cl
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Environment Variables Setup
# ---------------------------------------------------------------------
azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_key = os.getenv("AI_FOUNDRY_API_KEY")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")

# 2. Authentication Setup using Azure Service Principal
# ---------------------------------------------------------------------
varCredential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
)

# 3. AI Project Client Setup
# ---------------------------------------------------------------------
project = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=varCredential
)

# 4. ChainLit Event Handlers for Travel Companion Chat
# ---------------------------------------------------------------------

@cl.on_chat_start
async def start():
    """
    This function is called when a new chat session starts.
    It initializes the Travel Companion AI Agent and collects trip details.
    """
    try:
        # Send initial welcome message
        await cl.Message(
            content="✈️ **Welcome to your AI Travel Companion!** 🌍\n\n"
                    "I'm here to help you plan an amazing trip with personalized recommendations, "
                    "local insights, and practical travel tips!\n\n"
                    "Let's start by learning about your travel plans...",
            author="Travel Agent"
        ).send()
        
        # Ask for travel destination
        destination_response = await cl.AskUserMessage(
            content="🌍 **Where are you planning to travel?** Please enter your destination:",
            timeout=60
        ).send()
        
        if not destination_response:
            await cl.Message(
                content="❌ No destination provided. Please refresh and try again.",
                author="System"
            ).send()
            return
            
        # Handle both dict and object response formats
        if isinstance(destination_response, dict):
            destination = destination_response.get("output", "Unknown destination").strip()
        else:
            destination = destination_response.content.strip()
        cl.user_session.set("destination", destination)
        
        # BONUS: Ask for additional trip details
        travel_dates_response = await cl.AskUserMessage(
            content="📅 **When are you planning to travel?** (e.g., 'March 2024', 'Summer', or 'Next month')",
            timeout=60
        ).send()
        
        budget_response = await cl.AskUserMessage(
            content="💰 **What's your approximate budget range?** (e.g., 'Budget-friendly', '$1000-2000', 'Luxury', or 'No specific budget')",
            timeout=60
        ).send()
        
        # Store trip details - handle both dict and object formats
        if isinstance(travel_dates_response, dict):
            travel_dates = travel_dates_response.get("output", "Not specified").strip() if travel_dates_response else "Not specified"
        else:
            travel_dates = travel_dates_response.content.strip() if travel_dates_response else "Not specified"
            
        if isinstance(budget_response, dict):
            budget = budget_response.get("output", "Not specified").strip() if budget_response else "Not specified"
        else:
            budget = budget_response.content.strip() if budget_response else "Not specified"
        
        cl.user_session.set("travel_dates", travel_dates)
        cl.user_session.set("budget", budget)
        cl.user_session.set("question_count", 0)
        
        # 5. Create Travel-Specialized Agent
        # ---------------------------------------------------------------------
        agent = project.agents.create_agent(
            model=azure_foundry_deployment,
            name="Travel Companion Agent",
            instructions=f"""You are an expert travel companion and advisor helping someone plan a trip to {destination}. 
            
            Your traveler is planning to visit {destination} around {travel_dates} with a {budget} budget.
            
            You specialize in providing personalized recommendations for:
            - Must-see attractions and activities in {destination}
            - Local restaurants and authentic cuisine experiences
            - Transportation options and getting around
            - Cultural tips, etiquette, and local customs
            - Budget-friendly suggestions and money-saving tips
            - Hidden gems and local favorites that tourists often miss
            - Practical travel advice (weather, what to pack, etc.)
            
            Always be enthusiastic, helpful, and provide specific actionable advice.
            Tailor all your recommendations specifically to {destination} and consider their budget range of {budget}.
            Be conversational and engaging, like a knowledgeable local friend.
            Use emojis occasionally to make responses more engaging, but don't overdo it.""",
        )
        
        # 6. Create conversation thread
        # ---------------------------------------------------------------------
        thread = project.agents.threads.create()
        
        # Store agent and thread in session
        cl.user_session.set("agent", agent)
        cl.user_session.set("thread", thread)
        
        # Send personalized welcome message with trip details
        await cl.Message(
            content=f"✈️ **Fantastic! I'm excited to help you plan your trip to {destination}!** 🎉\n\n"
                   f"📋 **Your Trip Details:**\n"
                   f"📍 **Destination:** {destination}\n"
                   f"📅 **Travel Dates:** {travel_dates}\n"
                   f"💰 **Budget:** {budget}\n\n"
                   f"🗺️ **I can help you with:**\n"
                   f"• 🏛️ Must-see attractions and activities\n"
                   f"• 🍽️ Local restaurants and food recommendations\n" 
                   f"• 🚌 Transportation and getting around\n"
                   f"• 💰 Budget-friendly tips and deals\n"
                   f"• 🎭 Cultural insights and local customs\n"
                   f"• 💎 Hidden gems and local favorites\n\n"
                   f"**What would you like to know about {destination}?**\n\n"
                   f"💡 *Tip: Type `/trip-info` anytime to see your trip details!*",
            author="Travel Agent"
        ).send()
        
        print(f"🚀 Travel session started - Destination: {destination}, Agent: {agent.id}, Thread: {thread.id}")
        
    except Exception as e:
        error_message = f"❌ Error initializing travel agent: {str(e)}"
        await cl.Message(content=error_message, author="System").send()
        print(f"Error in chat start: {e}")

@cl.on_message
async def main(message: cl.Message):
    """
    This function processes user messages and provides travel advice.
    Includes bonus features like command handling and question counting.
    """
    try:
        # BONUS: Handle special commands
        if message.content.lower() == "/trip-info":
            destination = cl.user_session.get("destination", "Not set")
            dates = cl.user_session.get("travel_dates", "Not set")
            budget = cl.user_session.get("budget", "Not set")
            question_count = cl.user_session.get("question_count", 0)
            
            await cl.Message(
                content=f"🎒 **Your Trip Information:**\n\n"
                       f"📍 **Destination:** {destination}\n"
                       f"📅 **Travel Dates:** {dates}\n"
                       f"💰 **Budget:** {budget}\n"
                       f"❓ **Questions Asked:** {question_count}\n\n"
                       f"Ready to continue planning your amazing trip to {destination}? 🌟",
                author="Travel Agent"
            ).send()
            return
        
        # Get agent and thread from session
        agent = cl.user_session.get("agent")
        thread = cl.user_session.get("thread")
        
        if not agent or not thread:
            await cl.Message(
                content="❌ Session not properly initialized. Please refresh the page.",
                author="System"
            ).send()
            return
        
        # BONUS: Increment question counter
        question_count = cl.user_session.get("question_count", 0) + 1
        cl.user_session.set("question_count", question_count)
        
        # Show thinking message
        thinking_msg = cl.Message(content="🤔 Let me think about that travel question...", author="Travel Agent")
        await thinking_msg.send()
        
        # Create user message in thread
        user_message = project.agents.messages.create(
            thread_id=thread.id, 
            role="user", 
            content=message.content
        )
        
        # Process agent response
        run = project.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=agent.id
        )
        
        # Handle errors
        if run.status == "failed":
            error_message = f"❌ Sorry, I encountered an issue: {run.last_error}"
            thinking_msg.content = ""
            await thinking_msg.stream_token(error_message)
            await thinking_msg.update()
            return
        
        # Get agent response
        messages = project.agents.messages.list(
            thread_id=thread.id, 
            order=ListSortOrder.ASCENDING
        )
        
        # Find the agent's response
        agent_response = None
        for msg in messages:
            if msg.run_id == run.id and msg.text_messages and msg.role == "assistant":
                agent_response = msg.text_messages[-1].text.value
                break
        
        if agent_response:
            # Display response
            thinking_msg.content = ""
            await thinking_msg.stream_token(agent_response)
            await thinking_msg.update()
            print(f"✅ Travel advice provided for: {message.content[:50]}...")
        else:
            error_msg = "❌ I couldn't generate travel advice right now. Please try asking again!"
            thinking_msg.content = ""
            await thinking_msg.stream_token(error_msg)
            await thinking_msg.update()
        
    except Exception as e:
        error_message = f"❌ Error processing your travel question: {str(e)}"
        try:
            thinking_msg.content = ""
            await thinking_msg.stream_token(error_message)
            await thinking_msg.update()
        except:
            await cl.Message(content=error_message, author="System").send()
        print(f"Error processing message: {e}")

@cl.on_chat_end
async def end():
    """
    This function is called when the chat session ends.
    Provides a travel summary and helpful resources.
    """
    try:
        destination = cl.user_session.get("destination", "your destination")
        question_count = cl.user_session.get("question_count", 0)
        
        # BONUS: Provide city-specific resources and trip summary
        resources_by_city = {
            "tokyo": "🗾 **Helpful Resources:**\n• Official Tokyo Tourism: https://www.gotokyo.org/\n• JR Pass Information: https://www.jrpass.com/\n• Tokyo Metro Map: Download the official app",
            "paris": "🇫🇷 **Helpful Resources:**\n• Official Paris Tourism: https://en.parisinfo.com/\n• Museum Pass: https://www.parismuseumpass.com/\n• Metro/RER Maps: Download Citymapper app",
            "london": "🇬🇧 **Helpful Resources:**\n• Visit London: https://www.visitlondon.com/\n• Oyster Card Info: https://tfl.gov.uk/\n• Theatre Tickets: https://www.officiallondontheatre.com/",
            "new york": "🗽 **Helpful Resources:**\n• NYC Tourism: https://www.nycgo.com/\n• MetroCard/OMNY: https://new.mta.info/\n• Broadway Shows: https://www.broadway.com/",
        }
        
        city_resources = ""
        destination_lower = destination.lower()
        for city, resources in resources_by_city.items():
            if city in destination_lower:
                city_resources = f"\n\n{resources}"
                break
        
        if not city_resources:
            city_resources = f"\n\n🌐 **Don't forget to:**\n• Check official tourism websites for {destination}\n• Download helpful travel apps\n• Verify visa/passport requirements\n• Check current weather forecasts"
        
        goodbye_message = (
            f"✈️ **Thank you for using your AI Travel Companion!** 🌟\n\n"
            f"📊 **Session Summary:**\n"
            f"📍 **Destination:** {destination}\n"
            f"❓ **Questions Asked:** {question_count}\n\n"
            f"🎒 **Final Travel Tips:**\n"
            f"• Double-check your travel documents\n"
            f"• Consider travel insurance\n"
            f"• Learn a few basic phrases in the local language\n"
            f"• Pack according to the weather and activities planned\n"
            f"• Keep digital and physical copies of important documents"
            f"{city_resources}\n\n"
            f"🌍 **Have an absolutely amazing trip to {destination}!** 🎉\n"
            f"Safe travels! ✈️"
        )
        
        await cl.Message(content=goodbye_message, author="Travel Agent").send()
        
        print(f"🔚 Travel session ended - {destination}, {question_count} questions asked")
        
    except Exception as e:
        print(f"Error during chat end: {e}")

# 7. Running the Application
# ---------------------------------------------------------------------
# To run this travel companion, use the command:
# chainlit run ex2-travel-companion-solution.py
#
# This creates a specialized travel advisor that:
# 1. Collects destination and trip details
# 2. Provides context-aware travel advice
# 3. Remembers user preferences throughout the conversation
# 4. Offers practical resources and tips
# 5. Maintains engaging, travel-themed interactions
# 
# The agent leverages Azure AI Foundry's conversation management
# while providing a domain-specific, personalized experience.
# ---------------------------------------------------------------------
