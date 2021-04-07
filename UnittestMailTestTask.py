from selenium import webdriver
from time import sleep
import random
import string
import unittest

# Login data
gLogin = 'romantestbez@gmail.com'
gPass = 'ababagalamaga'

mails_to_send = 15   # How many mails want to send
my_dict = {}        # Create empty dict

class MailTestCase(unittest.TestCase):

    def setUp(self):
        # Setting up web driver
        self.driver = webdriver.Chrome()

    def test_case(self):
        driver = self.driver
        driver.implicitly_wait(15)
        driver.maximize_window()

        # Checking login in mail ------------------------------------------
        driver.get('https://gmail.com')

        # Check if page open
        self.assertIn('Gmail', driver.title)

        # Login email
        driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(gLogin)
        driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        driver.find_element_by_xpath('//input[@name="password"]').send_keys(gPass)
        driver.find_element_by_id('passwordNext').click()

        # Send self emails ------------------------------------------

        # Count inbox mails before sending
        inbox = len(driver.find_elements_by_css_selector('.zA'))
        # Start sending self mails in loop with mails_to_send variable
        for a in range(mails_to_send):

            # Test Random
            random1 = ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))
            random2 = ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))
            self.assertNotEquals(random1, random2)

            # Send mails
            driver.find_element_by_xpath('//*[@class="T-I T-I-KE L3"]').click()
            sleep(1)
            driver.find_element_by_css_selector(".vO").send_keys(gLogin) # input self mail "To"
            driver.find_element_by_css_selector(".aoT").send_keys(random1) # input random in "Subject"
            driver.find_element_by_css_selector(".Am.Al.editable.LW-avf").send_keys(random2) # input random in "Massage"
            driver.find_element_by_css_selector(".T-I.J-J5-Ji.aoO.T-I-atl.L3").click() # Send mail
        sleep(1)
        # Count how many mails after sending
        new_inbox = len(driver.find_elements_by_css_selector('.zA'))
        # Check if all sent massages income
        self.assertEqual(new_inbox - mails_to_send, inbox)

        # Send final email ------------------------------------------

        # Open sending popup window
        driver.find_element_by_xpath('//*[@class="T-I T-I-KE L3"]').click()
        sleep(1)
        driver.find_element_by_css_selector(".vO").send_keys(gLogin) #input self mail adress
        driver.find_element_by_css_selector(".aoT").send_keys("MailInfo") #input subject

        # Find all inbox mails
        mails = driver.find_elements_by_css_selector('.zA')

        # Iterate through mails to find subject and text
        for i in mails:
            subject = i.find_element_by_class_name('y6').text # find subject
            text = i.find_element_by_class_name('y2').text # find massage text
            text = text.translate({ord(i): None for i in ' -\n'}) # remove no needed symbols from text

            # Adding found elements in dict (subject-key : text-value)
            my_dict[subject] = text

            # Add until we reach send quantity after break loop
            if(len(my_dict) == mails_to_send):
                break

        # Iterate through dict for key and value
        for k, v in my_dict.items():
            digits = ''.join([d for d in v if d.isdigit()]) # take only digits from value
            letters = ''.join([l for l in v if l.islower()]) # take only letters from value

            # Prepare massage using len() in format() with letters and digits to indicate quantity
            text = "Received mail on theme {} with message: {}. " \
                   "It contains {} letters and {} numbers\n".format(k, v, len(letters), len(digits))

            # Input prepared text in massage box
            driver.find_element_by_css_selector(".Am.Al.editable.LW-avf").send_keys(text)
            # Send mail
        driver.find_element_by_css_selector(".T-I.J-J5-Ji.aoO.T-I-atl.L3").click()

        # Delete all mails except last ------------------------------------------
        
        # Checkbox "check all" click
        driver.find_element_by_xpath('//div[@id=":28"]/div/span').click()
        # Checkbox last mail uncheck
        driver.find_element_by_xpath('//div[@class="Cp"]//tr/td/div').click()

        # Find delete button and click on it
        driver.find_element_by_xpath('//*[@class="T-I J-J5-Ji nX T-I-ax7 T-I-Js-Gs mA"]').click()
        sleep(1)  # rest a bit mail server no so fast:)

        # Check if we have only one massage left
        self.assertEqual(len(driver.find_elements_by_css_selector('.zA')), 1)

    def tearDown(self):
        # Close web driver
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(failfast=True, exit=False)
