# Tests for To-Do Web Application

A collection of tests carried out on the web application at the link - [To-Do App](https://todomvc.com/examples/vue/) on the to-do list available there.

Created in Python with Selenium and PyTest, as an exercise and adaptation to the aforementioned tools.

<h3>The tests were divided into 4 categories:</h3>
- Adding new things to the list<br>
- Removing things from the list<br>
- Categorising things into completed / active<br>
- Stress tests<br>
<br>
Each test is described in terms of what it does and the steps involved in its completion and execution.
<br>

```python
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
```
<br>
Tests also take screenshots as they are executed, so that you can see exactly what the application looks like while they are running, which can be useful if you catch any failures.
They are all located in screenshots directory, and their names are equal to tests names.<br>
<br>
Test reports are generated using an option within PyTest to automatically generate reports during execution.

``` cmd
pytest .\TC_01_Adding_Todos.py --html="TC_01_Adding_Todos_report.html"
```
To run the tests, you will need the Selenium library and PyTest

```cmd
pip install selenium
```
```cmd
pip install pytest
```

<b>Example run</b>:<br>
Go to directory in which you have this project and simply run:
```cmd
pytest .\TC_01_Adding_Todos.py
```
Or any other that you want.
