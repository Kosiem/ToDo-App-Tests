import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


"""
|-------------------------------------------------------------------------------------------------|
Stress the todo app

Prepare browser:
    1. Open chrome
    2. Insert URL
    3. Delete all cookies
    5. Maximize window
    6. Set implicitly wait to 10 seconds
    7. Delete all cookies
    6. Set page timeout to 5 seconds
    7. Find and save input to insert new items
    8. Create objects to handle keyboard and mouse operation
    9. Localize buttons which change the displayed category   
After test execution:
    1. Close browser
|-------------------------------------------------------------------------------------------------|
"""

@pytest.fixture()
def openBrowserStress():
    global driver, todo, keyboard_action, mouse_action, category_all, category_active, category_completed
    driver = webdriver.Chrome()
    driver.get("https://todomvc.com/examples/vue/")
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.delete_all_cookies()
    driver.set_page_load_timeout(5)
    todo = driver.find_element(By.XPATH, "//input[@class='new-todo']")
    keyboard_action = ActionChains(driver)
    mouse_action = ActionChains(driver)

    category_all = driver.find_element(By.XPATH, "//a[@href='#/all']")
    category_active = driver.find_element(By.XPATH, "//a[@href='#/active']")
    category_completed = driver.find_element(By.XPATH, "//a[@href='#/completed']")
    yield
    driver.close()

"""
|-------------------------------------------------------------------------------------------------|
Test adding 100 items
    1. Add 100 items
    2. Check if there are 100 items in todo-list
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.add
def test_Add_100_ToDos(openBrowserStress):

    for i in range(1,101):
        data = "test" + str(i)
        todo.send_keys(data)
        keyboard_action.send_keys(Keys.ENTER).perform()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_ToDos.png")
    todos_list = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")
    assert len(todos_list) == 100

"""
|-------------------------------------------------------------------------------------------------|
Test adding 100 items and delete them
    1. Add 100 items
    2. Check if there are 100 items in todo-list
    3. Locate destroy button for each of item
    4. Delete each item
    5. Check if there are 0 items in todo-list
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.delete
def test_Add_100_Todos_And_Delete(openBrowserStress):
    for i in range(1, 101):
        data = "test" + str(i)
        todo.send_keys(data)
        keyboard_action.send_keys(Keys.ENTER).perform()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_And_Delete_Before.png")
    todos_list = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list) == 100

    for i in range(1, 101):
        label = "test" + str(i)
        mouse_action.move_to_element(driver.find_element(By.XPATH, "//label[text()='" + label + "']")).perform()
        xpath = "//label[text()='" + label + "']/following-sibling::button"
        destroy_button = driver.find_element(By.XPATH, xpath)
        destroy_button.click()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_And_Delete_After.png")
    todos_destroyed_list = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")
    assert len(todos_destroyed_list) == 0


"""
|-------------------------------------------------------------------------------------------------|
Test adding 100 items and marking them as completed
    1. Add 100 items
    2. Check if there are 100 items in todo-list
    3. Mark every one of them as completed
    4. Change category to completed
    5. Relocate elements
    6. Check if there are 100 items in todo-list
    7. Change category to active
    8. Relocate elements
    9. Check if there are 0 items in todo-list
    10. Change category to all
    11. Relocate elements
    12. Check if there are 100 items in todo-list
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.completed
def test_Add_100_Todos_Mark_Completed(openBrowserStress):
    for i in range(1, 101):
        data = "test" + str(i)
        todo.send_keys(data)
        keyboard_action.send_keys(Keys.ENTER).perform()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_And_Mark_Completed_Before.png")
    todos_list = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list) == 100

    for i in range(1, 101):
        label = "test" + str(i)
        mouse_action.move_to_element(driver.find_element(By.XPATH, "//label[text()='" + label + "']")).perform()
        xpath = "//label[text()='" + label + "']/preceding-sibling::input"
        mark_completed = driver.find_element(By.XPATH, xpath)
        mark_completed.click()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_And_Mark_Completed_After_Mark.png")
    todos_list = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list) == 100

    category_active.click()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_And_Mark_Completed_After_Mark_ActiveCat.png")

    todos_list_active = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list_active) == 0

    category_completed.click()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_And_Mark_Completed_After_Mark_CompletedCat.png")

    todos_list_completed= driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list_completed) == 100


"""
|-------------------------------------------------------------------------------------------------|
Test adding 100 items, marking them as completed and deleting them using clear completed button
    1. Add 100 items
    2. Check if there are 100 items in todo-list
    3. Mark each item as completed
    4. Click clear completed button
    6. Relocate elements
    5. Check it there are 0 items in todo-list
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.completed
def test_Add_100_Todos_Mark_Completed_And_Delete_At_Once(openBrowserStress):
    for i in range(1, 101):
        data = "test" + str(i)
        todo.send_keys(data)
        keyboard_action.send_keys(Keys.ENTER).perform()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_Mark_Completed_And_Delete_At_Once_Before.png")
    todos_list = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list) == 100

    for i in range(1, 101):
        label = "test" + str(i)
        mouse_action.move_to_element(driver.find_element(By.XPATH, "//label[text()='" + label + "']")).perform()
        xpath = "//label[text()='" + label + "']/preceding-sibling::input"
        mark_completed = driver.find_element(By.XPATH, xpath)
        mark_completed.click()

    driver.get_screenshot_as_file("screenshots\\test_Add_100_Todos_Mark_Completed_And_Delete_At_Once_After_Mark.png")
    clear_completed = driver.find_element(By.XPATH, "//button[@class='clear-completed']")

    clear_completed.click()

    todos_list_marked = driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")

    assert len(todos_list_marked) == 0
