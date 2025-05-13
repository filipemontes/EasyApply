from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def find_and_apply_easy_apply_jobs(driver, max_jobs=3, fill_function=None, search_term="ciência de dados", filter_keywords=None):
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_term.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(5)

    applied_count = 0
    scrolls = 0
    applied_jobs = []

    def job_matches_keywords(job_title):
        if not filter_keywords:
            return True
        job_title_lower = job_title.lower()
        for keyword in filter_keywords:
            if keyword.lower() in job_title_lower:
                return True
        return False

    while applied_count < max_jobs and scrolls < 10:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(3)
        scrolls += 1

        job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")

        for index, card in enumerate(job_cards):
            if applied_count >= max_jobs:
                break

            try:
                job_title = card.find_element(By.TAG_NAME, "strong").text.strip()

                if not job_matches_keywords(job_title):
                    continue

                if "Candidatura simplificada" not in card.text:
                    continue

                print(f"\n➡️ Vaga {applied_count+1}: {job_title}")
                driver.execute_script("arguments[0].scrollIntoView();", card)
                card.click()
                time.sleep(3)

                try:
                    easy_apply_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Candidatura simplificada']/ancestor::button"))
                    )
                    easy_apply_btn.click()
                    print("🟢 Formulário aberto. Iniciando preenchimento...")
                    fill_function(driver)
                    applied_count += 1
                    applied_jobs.append(job_title)
                except Exception as e:
                    print(f"⚠️ Botão 'Candidatura simplificada' não clicável: {e}")
                    continue

                time.sleep(3)

            except Exception as e:
                print(f"❌ Erro ao processar o card: {e}")
                continue

    print(f"✅ Total de candidaturas feitas: {applied_count}")
    return applied_jobs
