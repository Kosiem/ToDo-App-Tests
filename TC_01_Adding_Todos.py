import pytest
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


"""
|-------------------------------------------------------------------------------------------------|
Test functionality of adding new item to list

Prepare browser:
    1. Open chrome
    2. Insert URL
    3. Delete all cookies
    4. Maximize window
    5. Set page timeout to 5 seconds
    6. Find and save input to insert new items
    7. Create objects to handle keyboard and mouse operation
After test execution:
    1. Close browser
|-------------------------------------------------------------------------------------------------|
"""

@pytest.fixture
def openBrowser():
    global driver, todo, keyboard_action, mouse_action
    driver = webdriver.Chrome()
    driver.get("https://todomvc.com/examples/vue/")
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.set_page_load_timeout(5)
    todo = driver.find_element(By.XPATH, "//input[@class='new-todo']")
    keyboard_action = ActionChains(driver)
    mouse_action = ActionChains(driver)
    yield
    driver.close()


"""
|-------------------------------------------------------------------------------------------------|
Test adding new item
Steps:
    1. Add new item to list
    2. Check if it is displayed
    3. Check if the text of it equals to sent one
    4. Check if there are checkbox and button appearing 
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.correctTodo
def test_Add_New_ToDo(openBrowser):
    todo.send_keys("New ToDo1")
    keyboard_action.send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='New ToDo1']")))
    new_entry = driver.find_element(By.XPATH, "//label[text()='New ToDo1']")
    assert new_entry.is_displayed()
    assert new_entry.text == "New ToDo1"

    mouse_action.move_to_element(new_entry).perform()
    driver.get_screenshot_as_file("screenshots\\test_Add_New_ToDo.png")

    assert WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//label[text()='New ToDo1']/following-sibling::button")))
    assert WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='New ToDo1']/preceding-sibling::input")))


"""
|-------------------------------------------------------------------------------------------------|
Try to add empty item
Steps:
    1. Try to add empty item to list
    2. Try to check if it exists
    3. If not - then test is passed
|-------------------------------------------------------------------------------------------------|    
"""


@pytest.mark.negativeTodo
def test_Add_EmptyToDo(openBrowser):
    todo.send_keys(" ")
    keyboard_action.send_keys(Keys.ENTER).perform()

    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()=' ']")))
    except selenium.common.TimeoutException:
        assert True

    driver.get_screenshot_as_file("screenshots\\test_Add_EmptyToDo.png")


"""
|-------------------------------------------------------------------------------------------------|
Test adding new item with high characters count 
Steps:
    1. Add new item to list
    2. Check if it is displayed
    3. Check if the text of it equals to sent one
    4. Check if there are checkbox and button appearing 
|-------------------------------------------------------------------------------------------------|    
"""


@pytest.mark.correctToDo
def test_Add_Todo_With_More_Than_100_Characters(openBrowser):
    big_data = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
    todo.send_keys(big_data)
    keyboard_action.send_keys(Keys.ENTER).perform()

    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[contains(text(), 'omnis')]")))
    new_entry = driver.find_element(By.XPATH, "//label[contains(text(), 'omnis')]")
    assert new_entry.is_displayed()
    assert new_entry.text == big_data
    mouse_action.move_to_element(new_entry).perform()

    driver.get_screenshot_as_file("screenshots\\test_Add_Todo_With_More_Than_100_Characters.png")

    assert WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'omnis')]/following-sibling::button")))
    assert WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[contains(text(), 'omnis')]/preceding-sibling::input")))


"""
|-------------------------------------------------------------------------------------------------|
Test adding new item with special characters
Steps:
    1. Add new item to list
    2. Check if it is displayed
    3. Check if the text of it equals to sent one
    4. Check if there are checkbox and button appearing
|-------------------------------------------------------------------------------------------------|     
"""

@pytest.mark.correctToDo
def test_Add_ToDo_With_Special_Characters(openBrowser):
    data = "ążźć?!>#%^ó"
    todo.send_keys(data)
    keyboard_action.send_keys(Keys.ENTER).perform()

    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='ążźć?!>#%^ó']")))
    new_entry = driver.find_element(By.XPATH, "//label[text()='ążźć?!>#%^ó']")
    assert new_entry.is_displayed()
    assert new_entry.text == data

    mouse_action.move_to_element(new_entry).perform()
    driver.get_screenshot_as_file("screenshots\\test_Add_ToDo_With_Special_Characters.png")

    assert WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//label[text()='ążźć?!>#%^ó']/following-sibling::button")))
    assert WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='ążźć?!>#%^ó']/preceding-sibling::input")))


"""
|-------------------------------------------------------------------------------------------------|
Test adding multiple items to list
Steps:
    1. Add new items to list
    2. Check if they are displayed
    3. Check if the text of them equals to sent one
    4. Check if there are checkbox and button appearing on them
|-------------------------------------------------------------------------------------------------|    
"""


@pytest.mark.correctToDo
def test_Add_Multiple_Todo(openBrowser):
    data1 = "test1"
    data2 = "test2"
    data3 = "test3"

    todo.send_keys(data1)
    keyboard_action.send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test1']")))
    entry1 = driver.find_element(By.XPATH, "//label[text()='test1']")
    assert entry1.is_displayed()
    assert entry1.text == data1
    todo.clear()
    mouse_action.move_to_element(entry1).perform()
    assert WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//label[text()='test1']/following-sibling::button")))
    assert WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test1']/preceding-sibling::input")))

    todo.send_keys(data2)
    keyboard_action.send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test2']")))
    entry2 = driver.find_element(By.XPATH, "//label[text()='test2']")
    assert entry2.is_displayed()
    assert entry2.text == data2
    todo.clear()
    mouse_action.move_to_element(entry2).perform()
    assert WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//label[text()='test2']/following-sibling::button")))
    assert WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test2']/preceding-sibling::input")))

    todo.send_keys(data3)
    keyboard_action.send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test3']")))
    entry3 = driver.find_element(By.XPATH, "//label[text()='test3']")
    assert entry3.is_displayed()
    assert entry3.text == data3
    todo.clear()
    mouse_action.move_to_element(entry3).perform()
    assert WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//label[text()='test3']/following-sibling::button")))
    assert WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test3']/preceding-sibling::input")))

    driver.get_screenshot_as_file("screenshots\\test_Add_Multiple_Todo.png")


