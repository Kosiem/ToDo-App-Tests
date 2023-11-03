import pytest
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

"""
|-------------------------------------------------------------------------------------------------|
Test functionality of deleting items from list

Prepare browser:
    1. Open chrome
    2. Insert URL
    3. Delete all cookies
    5. Maximize window
    6. Set page timeout to 5 seconds
    7. Find and save input to insert new items
    8. Create objects to handle keyboard and mouse operation
    9. Create 3 new items add it to list
    10. Localize this items and their destroy button
After test execution:
    1. Close browser
|-------------------------------------------------------------------------------------------------|
"""

@pytest.fixture
def openAndPrepareBrowser():
    global driver, todo, keyboard_action, mouse_action, entry1, entry2, entry3, delete_button1, delete_button2, delete_button3
    driver = webdriver.Chrome()
    driver.get("https://todomvc.com/examples/vue/")
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.set_page_load_timeout(5)
    todo = driver.find_element(By.XPATH, "//input[@class='new-todo']")

    mouse_action = ActionChains(driver)
    keyboard_action = ActionChains(driver)

    todo.send_keys("test1")
    keyboard_action.send_keys(Keys.ENTER).perform()
    todo.clear()
    todo.send_keys("test2")
    keyboard_action.send_keys(Keys.ENTER).perform()
    todo.clear()
    todo.send_keys("test3")
    keyboard_action.send_keys(Keys.ENTER).perform()
    todo.clear()

    entry1 = driver.find_element(By.XPATH, "//label[text()='test1']")
    entry2 = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3 = driver.find_element(By.XPATH, "//label[text()='test3']")

    delete_button1 = driver.find_element(By.XPATH, "//label[text()='test1']/following-sibling::button")
    delete_button2 = driver.find_element(By.XPATH, "//label[text()='test2']/following-sibling::button")
    delete_button3 = driver.find_element(By.XPATH, "//label[text()='test3']/following-sibling::button")

    mouse_action = ActionChains(driver)

    yield
    driver.close()


"""
|-------------------------------------------------------------------------------------------------|
Test deleting all added items to list
Steps:
    1. Delete all items
    2. Try to check it they exist
    3. If not - test passed
|-------------------------------------------------------------------------------------------------|
"""


@pytest.mark.DeleteAll
def test_Delete_All_ToDos(openAndPrepareBrowser):
    mouse_action.move_to_element(entry1).perform()
    delete_button1.click()

    mouse_action.move_to_element(entry2).perform()
    delete_button2.click()

    mouse_action.move_to_element(entry3).perform()
    delete_button3.click()

    driver.get_screenshot_as_file("screenshots\\test_Delete_All_ToDos.png")

    try:
        entry1
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    try:
        entry2
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    try:
        entry3
    except selenium.common.exceptions.NoSuchElementException:
        assert True


"""
|-------------------------------------------------------------------------------------------------|
Test deleting an item located between two other items
Steps:
    1. Delete item
    2. Try to check it it exist
    3. Check if another two items still exists
|-------------------------------------------------------------------------------------------------|
"""


@pytest.mark.DeleteChoosen
def test_Delete_From_Between(openAndPrepareBrowser):
    mouse_action.move_to_element(entry2).perform()
    delete_button2.click()

    driver.get_screenshot_as_file("screenshots\\test_Delete_From_Between.png")

    try:
        entry2
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    assert entry1
    assert entry3


"""
|-------------------------------------------------------------------------------------------------|
Test deleting first item
Steps:
    1. Delete first item
    2. Try to check it it exist
    3. Check if another two items exist
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.DeleteChoosen
def test_Delete_First_One(openAndPrepareBrowser):
    mouse_action.move_to_element(entry1).perform()
    delete_button1.click()

    driver.get_screenshot_as_file("screenshots\\test_Delete_First_One.png")

    try:
        entry1
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    assert entry2
    assert entry3


"""
|-------------------------------------------------------------------------------------------------|
Test deleting last item
Steps:
    1. Delete last item
    2. Try to check it it exist
    3. Check if another two items exist
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.DeleteChoosen
def test_Delete_Last_One(openAndPrepareBrowser):
    mouse_action.move_to_element(entry3).perform()
    delete_button3.click()

    driver.get_screenshot_as_file("screenshots\\test_Delete_Last_One.png")

    try:
        entry3
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    assert entry1
    assert entry2

