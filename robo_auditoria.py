from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.implicitly_wait(10)

try:
    # ABA 0
    driver.get("https://the-internet.herokuapp.com/dropdown")
    abas = driver.window_handles

    # ABA 1
    driver.execute_script(
        "window.open('https://the-internet.herokuapp.com/dynamic_loading/2', '_blank');"
    )

    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > len(abas)
    )

    abas = driver.window_handles

    # ABA 2
    driver.execute_script(
        "window.open('https://pt.wikipedia.org', '_blank');"
    )

    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > 2
    )

    abas = driver.window_handles

    # DROPDOWN
    driver.switch_to.window(abas[0])

    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 1")

    valor = dropdown.first_selected_option.get_attribute("value")
    print("Valor selecionado:", valor)

    # ABA 1
    driver.switch_to.window(abas[1])

    driver.find_element(By.TAG_NAME, "button").click()

    resultado = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    print("Texto carregado:", resultado.text)

    # ABA 2
    driver.switch_to.window(abas[2])

    pesquisa = driver.find_element(By.NAME, "search")
    pesquisa.send_keys("Automação")

    link = driver.find_element(By.LINK_TEXT, "Artigo destacado")

    print("Texto do link:", link.text)
    print("Destino:", link.get_attribute("href"))

    driver.save_screenshot("evidencia_wiki.png")
    print("Print salvo com sucesso!")

finally:
    driver.quit()