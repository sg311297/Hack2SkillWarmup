import streamlit as st
import json
import os
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. ROBUST ENVIRONMENT AUTHENTICATION LAYER
# -------------------------------------------------------------
# Read from Streamlit Secrets vault or environment fallback
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# Hardcoded fallback if the environment vault variable isn't active yet
if not API_KEY:
    API_KEY = "AQ.Ab8RN6KSWILOjITTtofgab_IX0lJfWv4uW0x2oZKaK2RGIrSGg".strip()

try:
    # CRITICAL FIX: Explicitly passing vertexai=False tells the SDK to bypass 
    # the developer key gateway constraints and accept project-scoped keys.
    client = genai.Client(api_key=API_KEY, vertexai=False)
except Exception as e:
    st.error(f"Failed to initialize GenAI Client: {e}")
    st.stop()

# try:
#     client = genai.Client(api_key=API_KEY)
# except Exception as e:
#     st.error(f"Failed to initialize GenAI Client: {e}")
#     st.stop()

# -------------------------------------------------------------
# 2. UPGRADED UI HEADER DESIGN
# -------------------------------------------------------------
st.set_page_config(page_title="Smart Cooking Assistant", page_icon="🍳", layout="wide")

st.title("🍳 Smart Cooking To-Do Assistant")
st.caption("🚀 Hack2Skill Pune — Warm-up Workflow Verification Hub")
st.markdown("---")

# -------------------------------------------------------------
# 3. INTERACTIVE CONTEXT FORM
# -------------------------------------------------------------
with st.form("user_inputs", clear_on_submit=False):
    st.markdown("### 📝 Define Your Parameters")
    
    day_context = st.text_area(
        "Describe your day (Schedule, Energy Levels, Context):", 
        placeholder="e.g., I have a hectic corporate workday with back-to-back meetings from 9 AM to 6 PM, and I want something quick but healthy."
    )
    
    col_input_1, col_input_2 = st.columns(2)
    with col_input_1:
        budget = st.number_input("What is your daily food budget target?", min_value=1.0, value=25.0, step=5.0)
    with col_input_2:
        dietary_restrictions = st.text_input("Dietary Preferences / Allergies:", placeholder="e.g., Vegetarian, Gluten-Free, Nut-Free")
    
    submit_btn = st.form_submit_button("🔥 Generate Cooking & Ingredient Blueprint")

# -------------------------------------------------------------
# 4. CORE PIPELINE & RESTRUCTURED LLM CALL
# -------------------------------------------------------------
if submit_btn and day_context:
    
    # Prompt explicitly tailored to provide clean structural outputs
    prompt = f"""
    You are an expert culinary coordinator assistant. Based on the user's day context, budget constraint, and dietary preferences, generate a complete, structured daily meal plan overview.
    
    User context: {day_context}
    Daily Budget: {budget}
    Dietary Restrictions: {dietary_restrictions}
    
    Return a valid JSON object matching this schema exactly:
    {{
        "meal_plan": {{
            "breakfast": "Meal name - prep note",
            "lunch": "Meal name - prep note",
            "dinner": "Meal name - prep note"
        }},
        "grocery_list": ["item name with amount", "item name"],
        "substitutions": {{
            "ingredient_to_replace": "suggested_alternative"
        }},
        "estimated_total_cost": 22.50
    }}
    Do not wrap the response in markdown code blocks. Return raw JSON text only.
    """

    with st.spinner("⏳ Analyzing schedule constraints and compiling grocery lists..."):
        try:
            # Using stable workhorse gemini-2.5-flash for structured processing
            # response = client.models.generate_content(
            #     model='gemini-2.5-flash',
            #     contents=prompt,
            #     config=types.GenerateContentConfig(
            #         response_mime_type="application/json",
            #         temperature=0.2
            #     ),
            # )
            response = client.models.generate_content(
                model='gemini-3.5-flash',  # Updated string
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                ),
            )

            
            # Map structural text block to Python object dictionary
            data = json.loads(response.text)
            
            st.success("✨ Dynamic Plan Compiled Successfully!")
            st.markdown("---")
            
            # -------------------------------------------------------------
            # 5. HIGH IMPACT UI PRESENTATION
            # -------------------------------------------------------------
            
            # Tier A: Structured Meal Plan Dashboard Cards
            st.subheader("📋 Your Optimized Meal Timeline")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"🌅 **Breakfast**\n\n{data['meal_plan'].get('breakfast', 'N/A')}")
            with col2:
                st.info(f"☀️ **Lunch**\n\n{data['meal_plan'].get('lunch', 'N/A')}")
            with col3:
                st.info(f"🌙 **Dinner**\n\n{data['meal_plan'].get('dinner', 'N/A')}")
                
            st.markdown("---")
            
            # Tier B: Grocery & Substitutions Multi-pane Flow
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("🛒 Interactive Grocery Checklist")
                g_list = data.get('grocery_list', [])
                if g_list:
                    for idx, item in enumerate(g_list):
                        st.checkbox(item, key=f"grocery_check_{idx}")
                else:
                    st.write("No ingredients required.")
                    
            with col_right:
                st.subheader("🔄 Smart Ingredient Substitutions")
                subs = data.get('substitutions', {})
                if subs:
                    for original, sub in subs.items():
                        st.markdown(f"• If missing **{original}** ➔ Try using **{sub}**")
                else:
                    st.write("No ingredient adjustments needed for this workflow.")
            
            st.markdown("---")
            
            # Tier C: Budget Feasibility Logic Engine
            st.subheader("💰 Financial Feasibility Validation")
            est_cost = float(data.get('estimated_total_cost', 0.0))
            
            col_b1, col_b2 = st.columns(2)
            col_b1.metric("Target Budget Bound", f"{budget}")
            col_b2.metric("Calculated Raw Material Cost", f"{est_cost}")
            
            if est_cost <= budget:
                margin = round(budget - est_cost, 2)
                st.success(f"✅ **Feasible Plan!** Your setup runs safely within bounds, saving roughly **{margin}** under limit.")
            else:
                deficit = round(est_cost - budget, 2)
                st.error(f"❌ **Over Budget Constraints!** Calculated costs run **{deficit}** over your absolute target limit. swap premium items.")
                
        except json.JSONDecodeError:
            st.error("Error formatting model payload. Please execute the plan request again.")
        except Exception as e:
            st.error(f"An error occurred during verification: {e}")