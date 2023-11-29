import time
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

# Set Chrome options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# chrome_options = Options()

# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
# Create a new instance of the Chrome driver
# driver = webdriver.Chrome(options=chrome_options)
def test_battle_roll():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8090/battle?userPokemon=magnemite&randomPokemon=grimer")
    elements = driver.find_elements(by=By.ID, value='rollButton')
    time.sleep(3)
    main_window = driver.current_window_handle
    all_windows = driver.window_handles
    print(len(all_windows))
    for element in elements:
        # Do something with each element
        print(element.text)

        if element.text == 'Roll':
            element.click()
            break
    time.sleep(3)
    all_windows = driver.window_handles
    print(len(all_windows))
    # Switch to the newly opened window
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)

    print(driver.page_source)
    time.sleep(1)
    user_input = driver.find_element(By.ID, 'userInput')
    user_input.send_keys('25')
    time.sleep(3)

    # Find the submit button and click it using explicit wait
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
    submit_button.click()
    # вот тут окно должно пропадать но не пропадает
    # вот с этого момента не работает
    print('click')
    time.sleep(3)

    # Switch back to the main window
    driver.switch_to.window(main_window)
    print('switch to the main window')
    time.sleep(3)
    print('switch to alert')
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(3)
    driver.quit()

def test_battle_fast_fight():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8090/battle?userPokemon=magnemite&randomPokemon=grimer")
    elements = driver.find_elements(by=By.ID, value='fastFight')
    time.sleep(3)
    all_windows = driver.window_handles
    print(len(all_windows))
    for element in elements:
        # Do something with each element
        print(element.text)

        if element.text == 'Fast fight':
            element.click()
            break
    time.sleep(3)
    all_windows = driver.window_handles
    print(len(all_windows))
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    # вот с этого момента не работает
    print(driver.page_source)
    # print(type(driver.page_source))
    # Perform actions in the new window
    email_input = driver.find_element(by=By.ID, value='fastFight')
    email_input.send_keys('malysh_mikhail_s@mail.ru')

    send_button = driver.find_element(by=By.TAG_NAME, value="button")
    send_button.click()
    time.sleep(5)
    driver.quit()

def test_search_pagination_and_pokemon_detail_save():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8090/")
    time.sleep(3)
    elements=driver.find_elements(by=By.CLASS_NAME, value='pagination-link')
    for element in elements:
        print(element.text)
        if element.text=='5':
            element.click()
            break
    time.sleep(3)
    elements = driver.find_elements(by=By.TAG_NAME, value='a')
    for element in elements:
        print(element.text)
        if element.text=='magnemite':
            element.click()
            break
    time.sleep(3)
    elements=driver.find_elements(by=By.TAG_NAME, value='button')
    for element in elements:
        print(element.text)
        if element.text=='Save Pokemon':
            element.click()
            break
    time.sleep(3)
    searchInput=driver.find_element(by=By.ID, value='searchInput')
    searchInput.send_keys('mega')
    elements = driver.find_elements(by=By.TAG_NAME, value='button')
    for element in elements:
        print(element.text)
        if element.text=='Search':
            element.submit()
            break
    time.sleep(5)
    driver.quit()
# test_battle_roll()
test_battle_fast_fight()
# test_search_pagination_and_pokemon_detail_save()



