import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fill_application_form(driver):
    print("📝 Preenchendo o formulário de candidatura...")

    time.sleep(3)  # Esperar o modal abrir completamente

    # Scroll inicial no modal (apenas para garantir que campos iniciais estejam acessíveis)
    try:
        modal_content = driver.find_element(By.CLASS_NAME, 'jobs-easy-apply-modal__content')
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_content)
    except Exception as e:
        print(f"❌ Não foi possível dar scroll inicial no modal: {e}")

    while True:
        try:
            # Preencher dropdowns obrigatórios
            dropdowns = driver.find_elements(By.CSS_SELECTOR, 'select[aria-required="true"]')
            for dropdown in dropdowns:
                selected_value = dropdown.get_attribute("value")
                if selected_value and selected_value != "":
                    continue
                try:
                    options = dropdown.find_elements(By.TAG_NAME, 'option')
                    for option in options:
                        if option.get_attribute('value') not in ["", "Select an option"]:
                            dropdown.click()
                            option.click()
                            break
                except Exception as e:
                    print(f"Erro ao selecionar dropdown: {e}")

            # Preencher inputs de texto obrigatórios
            inputs = driver.find_elements(By.CSS_SELECTOR, 'input[required]')
            for input_elem in inputs:
                try:
                    current_value = input_elem.get_attribute("value")
                    if current_value and current_value.strip() != "":
                        continue
                    input_elem.clear()
                    input_elem.send_keys("0")
                except Exception as e:
                    print(f"Erro ao preencher campo de texto: {e}")

            # Selecionar primeira opção de radio se nenhuma estiver marcada
            radio_groups = driver.find_elements(By.CSS_SELECTOR, 'fieldset[data-test-form-builder-radio-button-form-component="true"]')
            for group in radio_groups:
                try:
                    selected = group.find_elements(By.CSS_SELECTOR, 'input[type="radio"]:checked')
                    if selected:
                        continue
                    first_option = group.find_element(By.CSS_SELECTOR, 'input[type="radio"]')
                    driver.execute_script("arguments[0].click();", first_option)
                except Exception as e:
                    print(f"Erro ao selecionar primeira opção do grupo: {e}")

            # Procurar botão Avançar ou Revisar
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[(contains(., 'Avançar') or contains(., 'Revisar')) and not(contains(., 'Enviar candidatura'))]"))
            )
            next_button.click()
            print("🔁 Avançando para próxima etapa...")
            time.sleep(2)

        except Exception:
            print("🛑 Nenhum botão de avanço encontrado ou chegou no final.")
            break

    # Clicar em Revisar, se existir
    try:
        revisar_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Revisar')]"))
        )
        revisar_button.click()
        print("📄 Cliquei em 'Revisar candidatura'.")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Não encontrei o botão 'Revisar candidatura': {e}")

    # Tentar clicar em "Enviar candidatura" diretamente via JavaScript
    try:
        enviar_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Enviar candidatura')]"))
        )
        driver.execute_script("arguments[0].click();", enviar_button)
        print("✅ Candidatura enviada com sucesso!")
    except Exception as e:
        print(f"⚠️ Não consegui clicar no botão 'Enviar candidatura': {e}")
    
        # Tentar clicar em "Concluído" se aparecer um modal final
    try:
        concluido_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Concluído']/ancestor::button"))
        )
        driver.execute_script("arguments[0].click();", concluido_button)
        print("✅ Cliquei em 'Concluído' para fechar o modal final.")
        time.sleep(2)
    except Exception as e:
        print("ℹ️ Modal de 'Concluído' não apareceu ou já foi fechado.")
