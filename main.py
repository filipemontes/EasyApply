import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from job_search import find_and_apply_easy_apply_jobs
from form_filler import fill_application_form

from streamlit_tags import st_tags

def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login_linkedin(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )
        st.success("🔐 Login realizado com sucesso!")
    except Exception as e:
        st.error(f"❌ Falha no login: {e}")
        raise

st.set_page_config(page_title="AutoApply LinkedIn", layout="centered")
st.title("🤖 LinkedIn AutoApply Bot")
st.write("Automatize candidaturas com um clique.")

with st.form("login_form"):
    email = st.text_input("Email do LinkedIn", placeholder="exemplo@email.com")
    password = st.text_input("Senha", type="password")
    search_term = st.text_input("Palavra-chave para busca de vagas", value="ciência de dados")

    filter_keywords = st_tags(
        label='🧠 Palavras-chave para **filtrar** títulos de vaga:',
        text='Digite e pressione Enter',
        value=['dados', 'analista'],
        suggestions=['data', 'analyst', 'cientista', 'engenheiro'],
        maxtags=10,
        key="filter_keywords_input"
    )

    max_jobs = st.slider("Número máximo de candidaturas", 1, 20, 3)

    submitted = st.form_submit_button("🚀 Iniciar processo")

if submitted:
    if not email or not password:
        st.warning("⚠️ Preencha email e senha.")
    elif not filter_keywords:
        st.warning("⚠️ Informe ao menos uma palavra-chave para filtro.")
    else:
        with st.status("Inicializando navegador...", expanded=True) as status:
            driver = start_driver()
            try:
                login_linkedin(driver, email, password)
                st.info("🔍 Procurando vagas e aplicando automaticamente...")
                applied_jobs = find_and_apply_easy_apply_jobs(
                    driver,
                    max_jobs=max_jobs,
                    fill_function=fill_application_form,
                    search_term=search_term,
                    filter_keywords=filter_keywords
                )
                st.success("✅ Candidaturas finalizadas com sucesso!")

                if applied_jobs:
                    st.write("📄 Vagas aplicadas:")
                    for job in applied_jobs:
                        st.markdown(f"- ✅ **{job}**")
                else:
                    st.info("ℹ️ Nenhuma candidatura foi realizada.")

            finally:
                driver.quit()
            status.update(label="Processo concluído", state="complete")
