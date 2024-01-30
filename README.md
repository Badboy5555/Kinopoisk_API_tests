**POM testing. WebUI example**  

This project implements Python WebUI autotest for https://www.kinopoisk.ru.  
A tech stack: Python + Selenium + Pytest  

 
 # Installation
1. Install Python 3.11
2. Clone the project `git clone https://gitlab.com/Badboy5555/{}.git`
3. Install requirements for project:   
   using CLI, navigate to project directory and run command `pip install -r requirements.txt`
   
# Tests runnig
To run all test, using CLI navigate to project directory and run command: `python -m pytest tests --alluredir=allure-results`

# Report 
1. Install allure reporter for special OS [link](https://github.com/allure-framework/allure2)
2. To generate testrun report, using CLI, navigate to project directory and run command: `allure serve allure-results`