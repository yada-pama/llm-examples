from openai import OpenAI
import streamlit as st

# Sidebar สำหรับ API Key
with st.sidebar:
    openai_api_key = st.text_input("Typhoon API Key", key="chatbot_api_key", type="password")
    "[Get a Typhoon API key](https://api.opentyphoon.ai/)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Title ของหน้า
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Typhoon LLM")

# สร้าง state สำหรับเก็บข้อความสนทนา
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# แสดงข้อความสนทนาที่มีอยู่
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# กล่อง Input สำหรับพิมพ์คำถาม
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your Typhoon API key to continue.")
        st.stop()

    # สร้าง Client สำหรับเชื่อมต่อ Typhoon API
    client = OpenAI(
        base_url="https://api.opentyphoon.ai/v1",  # URL สำหรับ Typhoon
        api_key=openai_api_key
    )

    # เพิ่มข้อความของผู้ใช้
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # เรียก Typhoon LLM เพื่อประมวลผล
    try:
        response = client.chat.completions.create(
            model="typhoon-instruct",  # ชื่อโมเดล Typhoon
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
    except Exception as e:
        msg = f"Error: {e}"

    # เพิ่มข้อความตอบกลับของ Typhoon
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
