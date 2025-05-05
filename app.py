from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar o ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.linkedin.com/login")

input("Faz login manualmente e pressiona Enter quando estiveres na homepage...")

# Ir para a página de empregos
search_url = "https://www.linkedin.com/jobs/search/?keywords=ciência%20de%20dados"
driver.get(search_url)
time.sleep(5)

# Rolar para carregar mais anúncios
for _ in range(3):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)

# Obter os cartões de vaga
job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")

# Procurar o primeiro com "Candidatura simplificada"
for card in job_cards:
    try:
        if "Candidatura simplificada" in card.text:
            driver.execute_script("arguments[0].scrollIntoView();", card)
            card.click()
            time.sleep(2)

            # Obter o título da vaga
            try:
                title_elem = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__job-title"))
                )
                job_title = title_elem.text.strip()
            except:
                job_title = "Título não encontrado"

            print(f"\n➡️ Vaga com candidatura simplificada: **{job_title}**")

            # Clicar no botão "Candidatura simplificada"
            simplified_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Candidatura simplificada']/ancestor::button"))
            )
            simplified_button.click()
            print("🟢 Formulário de candidatura aberto com sucesso!")
            break

    except Exception as e:
        print(f"❌ Erro ao processar o card: {e}")
        continue

# Espera o formulário carregar
time.sleep(3)

# Selecionar todos os dropdowns obrigatórios e escolher a primeira opção válida
dropdowns = driver.find_elements(By.CSS_SELECTOR, 'select[aria-required="true"]')
for dropdown in dropdowns:
    try:
        options = dropdown.find_elements(By.TAG_NAME, 'option')
        for option in options:
            if option.get_attribute('value') not in ["", "Select an option"]:
                dropdown.click()
                option.click()
                break
    except Exception as e:
        print(f"Erro ao selecionar dropdown: {e}")

# Preencher inputs de texto obrigatórios com "0"
inputs = driver.find_elements(By.CSS_SELECTOR, 'input[required]')
for input_elem in inputs:
    try:
        input_elem.clear()
        input_elem.send_keys("0")
    except Exception as e:
        print(f"Erro ao preencher campo de texto: {e}")

# Selecionar a primeira opção de múltipla escolha (radio)
radio_groups = driver.find_elements(By.CSS_SELECTOR, 'fieldset[data-test-form-builder-radio-button-form-component="true"]')
for group in radio_groups:
    try:
        first_option = group.find_element(By.CSS_SELECTOR, 'input[type="radio"]')
        driver.execute_script("arguments[0].click();", first_option)
    except Exception as e:
        print(f"Erro ao selecionar primeira opção do grupo: {e}")

# Scroll dentro do modal para garantir que o botão “Avançar” esteja visível
try:
    modal = driver.find_element(By.CLASS_NAME, 'jobs-easy-apply-modal')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
except:
    print("Não foi possível dar scroll no modal.")

# Loop para continuar clicando em "Avançar" ou "Revisar candidatura" até chegar no final
while True:
    try:
        # Tenta encontrar o botão que NÃO seja "Enviar candidatura"
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[(contains(., 'Avançar') or contains(., 'Revisar')) and not(contains(., 'Enviar candidatura'))]"
            ))
        )
        next_button.click()
        print("🔁 Avançando para próxima etapa...")
        time.sleep(2)

        # Preencher novamente campos obrigatórios na nova etapa
        dropdowns = driver.find_elements(By.CSS_SELECTOR, 'select[aria-required="true"]')
        for dropdown in dropdowns:
            try:
                options = dropdown.find_elements(By.TAG_NAME, 'option')
                for option in options:
                    if option.get_attribute('value') not in ["", "Select an option"]:
                        dropdown.click()
                        option.click()
                        break
            except Exception as e:
                print(f"Erro ao selecionar dropdown: {e}")

        # Preencher inputs de texto obrigatórios com "0"
        inputs = driver.find_elements(By.CSS_SELECTOR, 'input[required]')
        for input_elem in inputs:
            try:
                input_elem.clear()
                input_elem.send_keys("0")
            except Exception as e:
                print(f"Erro ao preencher campo de texto: {e}")

        # Selecionar a primeira opção de múltipla escolha (radio)
        radio_groups = driver.find_elements(By.CSS_SELECTOR, 'fieldset[data-test-form-builder-radio-button-form-component="true"]')
        for group in radio_groups:
            try:
                first_option = group.find_element(By.CSS_SELECTOR, 'input[type="radio"]')
                driver.execute_script("arguments[0].click();", first_option)
            except Exception as e:
                print(f"Erro ao selecionar primeira opção do grupo: {e}")

    except Exception as e:
        print("🛑 Nenhum botão de avanço encontrado ou chegou no final.")
        break

# Tenta clicar em "Revisar candidatura" se aparecer
try:
    revisar_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH, "//button[contains(., 'Revisar')]"
        ))
    )
    revisar_button.click()
    print("📄 Cliquei em 'Revisar candidatura'.")
except Exception as e:
    print(f"⚠️ Não encontrei botão 'Revisar candidatura': {e}")

# Espera 20 segundos antes de encerrar ou prosseguir
print("⏳ Aguardando 20 segundos antes de fechar...")
time.sleep(20)

# driver.quit()  # <- Descomenta esta linha se quiser que o navegador feche após os 20s
