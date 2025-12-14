import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

from parse_hh import get_html, extract_vacancy_data, extract_resume_data

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

with open('system_prompt.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

SYSTEM_PROMPT = file_content.strip()

def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content

# UI
st.title('ОЦЕНКА СООТВЕТСТВИЯ РЕЗЮМЕ ЗАДАННОЙ ВАКАНСИИ')

job_description = st.text_area('Введите ссылку на вакансию')
cv = st.text_area('Введите ссылку на резюме')

if st.button("Проанализировать соответствие"):
    with st.spinner("Парсим данные и отправляем в GPT..."):
        try:
            job_html = get_html(job_description).text
            resume_html = get_html(cv).text

            job_text = extract_vacancy_data(job_html)
            resume_text = extract_resume_data(resume_html)

            prompt = f"# ВАКАНСИЯ\n{job_text}\n\n# РЕЗЮМЕ\n{resume_text}"
            response = request_gpt(SYSTEM_PROMPT, prompt)

            st.subheader("📊 Результат анализа:")
            st.markdown(response)

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")