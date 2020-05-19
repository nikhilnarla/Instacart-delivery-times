from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import request, parse
import json

try:
	pass

	# The store for which you want to check the delivery times
	store = input("Enter store name : ")

	# Specify the path to the chromedriver similar  to the example shown below
	driver = webdriver.Chrome("C:\\Users\\narla\\Downloads\\chromedriver.exe")

	# Can be configured based on your internet speeds. Please increase it in case your internet connection is too slow.
	driver.implicitly_wait(20)

	# To open the instacart URL
	driver.get('https://www.instacart.com/');

	# To click on log in
	login = driver.find_element_by_xpath("//button[text()='Log in']")
	login.click()

	username = driver.find_element_by_id('nextgen-authenticate.all.log_in_email')

	# Enter your username
	username.send_keys("test@test.com")

	password = driver.find_element_by_id('nextgen-authenticate.all.log_in_password')

	# Enter your password
	password.send_keys("samplepassword")

	# clicks on submit to log in
	driver.find_element_by_xpath("//button[@type='submit']").click()

	# Clicks on stores to be able to select the store taken as input
	driver.find_element_by_xpath("//a[@class='primary-nav-link' and text()='Stores']").click()

	# Clicks on the store provided in the input by the user
	driver.find_element_by_xpath(f'//div[contains(text(),"{store}")]').click()

	# Gets the delivery times available
	text = driver.find_element_by_xpath("//a/span[@title]").text

	# IF slots are available the user will be notified to his slack channel.
	if text != "See delivery times":

		post = {"text": f"Instacart delivery is now available for {store} : {text} "}

		try:
			json_data = json.dumps(post)
			req = request.Request("https://hooks.slack.com/services/*your ID*", # Please provide your channel specific webhook here.
			data=json_data.encode('ascii'),
			headers={'Content-Type': 'application/json'})
			resp = request.urlopen(req)
		except Exception as em:
			print("EXCEPTION: " + str(em))
	else:
		driver.quit()

except Exception as em:
	print("EXCEPTION: " + str(em))
	driver.quit()
