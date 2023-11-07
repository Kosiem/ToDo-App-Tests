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
Test functionality of categorisation items

Prepare browser:
    1. Open chrome
    2. Insert URL
    3. Delete all cookies
    5. Maximize window
    6. Set page timeout to 5 seconds
    7. Find and save input to insert new items
    8. Create objects to handle keyboard and mouse operation
    9. Create 3 new items add it to list
    10. Localize this items and their checkbox
    11. Localize buttons which change the displayed category   
After test execution:
    1. Close browser
|-------------------------------------------------------------------------------------------------|
"""

@pytest.fixture
def openAndPrepareBrowserCategories():
    global driver, todo, keyboard_action, mouse_action, entry1, entry2, entry3, toggle_button1, toggle_button2, toggle_button3, category_all, category_active, category_completed
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
    todo.clear

    entry1 = driver.find_element(By.XPATH, "//label[text()='test1']")
    entry2 = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3 = driver.find_element(By.XPATH, "//label[text()='test3']")

    category_all = driver.find_element(By.XPATH, "//a[@href='#/all']")
    category_active = driver.find_element(By.XPATH, "//a[@href='#/active']")
    category_completed = driver.find_element(By.XPATH, "//a[@href='#/completed']")

    toggle_button1 = driver.find_element(By.XPATH, "//label[text()='test1']/preceding-sibling::input")
    toggle_button2 = driver.find_element(By.XPATH, "//label[text()='test2']/preceding-sibling::input")
    toggle_button3 = driver.find_element(By.XPATH, "//label[text()='test3']/preceding-sibling::input")

    yield
    driver.close()


"""
|-------------------------------------------------------------------------------------------------|
Test moving all items to completed category
    1. Mark items as completed
    2. Change displayed category to completed
    3. Relocate elements
    4. Check if marked items are in this category and their style got line-through
    5. Change displayed category to active
    6. Try to locate elements there (They should not be visibile in active category)
    7. Change displayed category to all
    8. Relocate elements
    9. Check if they are displayed and thier style got line-through
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.all_completed
def test_Move_All_To_Completed(openAndPrepareBrowserCategories):
    toggle_button1.click()
    toggle_button2.click()
    toggle_button3.click()
    category_completed.click()

    driver.get_screenshot_as_file("screenshots\\test_Move_All_To_Completed.png")

    entry1_completed = driver.find_element(By.XPATH, "//label[text()='test1']")
    entry2_completed = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3_completed = driver.find_element(By.XPATH, "//label[text()='test3']")

    WebDriverWait(driver,5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test1']")))
    entry1_style = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')", entry1)
    assert entry1_completed.is_displayed()
    assert "line-through" in entry1_style
    WebDriverWait(driver,5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test2']")))
    entry2_style = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')", entry2)
    assert entry2_completed.is_displayed()
    assert "line-through" in entry2_style
    WebDriverWait(driver,5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test3']")))
    entry3_style = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')", entry3)
    assert entry3_completed.is_displayed()
    assert "line-through" in entry3_style

    category_active.click()

    driver.get_screenshot_as_file("screenshots\\test_Move_All_To_Completed_ActiveCat.png")
    try:
        driver.find_elements(By.XPATH, "//ul[@class='todo-list']/li")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    category_all.click()
    driver.get_screenshot_as_file("screenshots\\test_Move_All_To_Completed_AllCat.png")

    entry1_all = driver.find_element(By.XPATH, "//label[text()='test1']")
    entry2_all = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3_all = driver.find_element(By.XPATH, "//label[text()='test3']")

    assert entry1_all.is_displayed()
    assert entry2_all.is_displayed()
    assert entry3_all.is_displayed()

    entry1_style_all = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry1_all)
    entry2_style_all = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry2_all)
    entry3_style_all = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry3_all)

    assert "line-through" in entry1_style_all
    assert "line-through" in entry2_style_all
    assert "line-through" in entry3_style_all


"""
|-------------------------------------------------------------------------------------------------|
Test moving first item to completed category
    1. Mark first item as completed
    2. Change displayed category to completed
    3. Relocate elements
    4. Check if first item is displayed and has style line-through
    5. Try to locate rest of items in there (They should not be visible in completed category)
    6. Change category to active
    7. Relocate elements
    8. Try to locate first element (It should not be visible in active category)
    8. Locate rest of items
    9. Change category to all
    10. Relocate elements
    11. Check if first item is displayed and has style line-through
    12. Check if rest of the items are displayed
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.partial_completed
def test_Move_Entry1_To_Completed(openAndPrepareBrowserCategories):
    toggle_button1.click()
    category_completed.click()
    driver.get_screenshot_as_file("screenshots\\test_Move_Entry1_To_Completed.png")
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test1']")))
    entry1_completed = driver.find_element(By.XPATH, "//label[text()='test1']")
    try:
        entry2_completed = driver.find_element(By.XPATH, "//label[text()='test2']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True
    try:
        entry3_completed = driver.find_element(By.XPATH, "//label[text()='test3']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    entry1_style = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry1_completed)
    assert entry1_completed.is_displayed()
    assert "line-through" in entry1_style

    category_active.click()
    driver.get_screenshot_as_file("screenshots\\test_Move_Entry1_To_Completed_ActiveCat.png")

    try:
        entry1_active = driver.find_element(By.XPATH, "//label[text()='test1']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    entry2_active = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3_active = driver.find_element(By.XPATH, "//label[text()='test3']")

    assert entry2_active.is_displayed()
    assert entry3_active.is_displayed()

    category_all.click()
    entry1_all = driver.find_element(By.XPATH, "//label[text()='test1']")
    entry2_all = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3_all = driver.find_element(By.XPATH, "//label[text()='test3']")

    assert entry1_all.is_displayed()
    entry1_style_all = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry1_all)
    assert "line-through" in entry1_style_all
    assert entry2_all.is_displayed()
    assert entry3_all.is_displayed()


"""
|-------------------------------------------------------------------------------------------------|
Test moving two items to completed category
    1. Mark second and third items
    2. Change displayed category to completed
    3. Relocate elements
    4. Check if second item and third item is displayed and has style line-through
    5. Try to locate first item in there (It should not be visible in completed category)
    6. Change category to active
    7. Relocate elements
    8. Try to locate second item and third item there (It should not be visible in active category)
    8. Check if first item is displayed
    9. Change category to all
    10. Relocate elements
    11. Check if all items are displayed 
    12. Check if second and third item got line-through css style
|-------------------------------------------------------------------------------------------------|
"""


@pytest.mark.partial_completed
def test_Move_Partial_To_Completed(openAndPrepareBrowserCategories):
    toggle_button2.click()
    toggle_button3.click()
    category_completed.click()
    driver.get_screenshot_as_file("screenshots\\test_Move_Partial_To_Completed_CompletedCat.png")

    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test2']")))
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//label[text()='test3']")))
    try:
        entry1_completed = driver.find_element(By.XPATH, "//label[text()='test1']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    entry2_completed = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry2_style = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry2_completed)
    entry3_completed = driver.find_element(By.XPATH, "//label[text()='test3']")
    entry3_style = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')",entry3_completed)


    assert entry2_completed.is_displayed()
    assert "line-through" in entry2_style

    assert entry3_completed.is_displayed()
    assert "line-through" in entry3_style

    category_active.click()

    entry1_active = driver.find_element(By.XPATH, "//label[text()='test1']")
    try:
        entry2_active = driver.find_element(By.XPATH, "//label[text()='test2']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    try:
        entry3_active = driver.find_element(By.XPATH, "//label[text()='test3']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    driver.get_screenshot_as_file("screenshots\\test_Move_Partial_To_Completed_ActiveCat.png")

    assert entry1_active.is_displayed()

    category_all.click()

    entry1_all = driver.find_element(By.XPATH, "//label[text()='test1']")
    entry2_all = driver.find_element(By.XPATH, "//label[text()='test2']")
    entry3_all = driver.find_element(By.XPATH, "//label[text()='test3']")

    driver.get_screenshot_as_file("screenshots\\test_Move_Partial_To_Completed_AllCat.png")

    assert entry1_all.is_displayed()

    entry2_style_all = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')", entry2_all)
    assert entry2_all.is_displayed()
    assert "line-through" in entry2_style_all

    entry3_style_all = driver.execute_script("return getComputedStyle(arguments[0]).getPropertyValue('text-decoration')", entry3_all)
    assert entry3_all.is_displayed()
    assert "line-through" in entry3_style_all


"""
|-------------------------------------------------------------------------------------------------|
Test deleting all of completed items with button to clear completed
    1. Mark second and third item
    2. Press clear completed button
    3. Change category to completed
    4. Try to locate all items (They should not be visible)
    5. Change category to active
    6. Try to locate second and third item (They should not be visible)
    7. Check if first item is displayed
    8. Change category to all
    9. Try to locate second and third item (They should not be visible)
    10. Check if first item is displayed
|-------------------------------------------------------------------------------------------------|
"""

@pytest.mark.delete_completed
def test_Clear_Completed_Todos(openAndPrepareBrowserCategories):

    toggle_button2.click()
    toggle_button3.click()

    driver.get_screenshot_as_file("screenshots\\test_Clear_Completed_Todos_BeforeDelete.png")

    clear_completed = driver.find_element(By.XPATH, "//button[@class='clear-completed']")
    clear_completed.click()

    driver.get_screenshot_as_file("screenshots\\test_Clear_Completed_Todos_AfterDelete.png")

    category_completed.click()

    driver.get_screenshot_as_file("screenshots\\test_Clear_Completed_Todos_CompletedCat.png")

    try:
        entry1_completed = driver.find_element(By.XPATH, "//label[text()='test1']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True
    try:
        entry2_completed = driver.find_element(By.XPATH, "//label[text()='test2']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True
    try:
        entry3_completed = driver.find_element(By.XPATH, "//label[text()='test3']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    category_active.click()

    entry1_active = driver.find_element(By.XPATH, "//label[text()='test1']")
    try:
        entry2_active = driver.find_element(By.XPATH, "//label[text()='test2']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True
    try:
        entry3_active = driver.find_element(By.XPATH, "//label[text()='test3']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    driver.get_screenshot_as_file("screenshots\\test_Clear_Completed_Todos_ActiveCat.png")

    assert entry1_active.is_displayed()


    category_all.click()
    driver.get_screenshot_as_file("screenshots\\test_Clear_Completed_Todos_AllCat.png")

    entry1_all = driver.find_element(By.XPATH, "//label[text()='test1']")
    try:
        entry2_all = driver.find_element(By.XPATH, "//label[text()='test2']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True
    try:
        entry3_all = driver.find_element(By.XPATH, "//label[text()='test3']")
    except selenium.common.exceptions.NoSuchElementException:
        assert True

    assert entry1_all.is_displayed()




