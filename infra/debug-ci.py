from selenium import webdriver

webdriver.Firefox().quit()
# options = webdriver.FirefoxOptions()
# service = webdriver.FirefoxService(executable_path="/usr/local/bin/geckodriver")
# webdriver.Firefox(options=options, service=service).quit()
print("All good")
