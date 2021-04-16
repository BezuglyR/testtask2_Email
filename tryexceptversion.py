from selenium import webdriver
from time import sleep
import random
import string

driver = webdriver.Chrome()
driver.implicitly_wait(15)

mails_to_sent = 15
my_dict = {}

gLogin = 'romantestbez@gmail.com'
gPass = 'ababagalamaga'

def random_text():
    return ''.join(random.choice(string.letters.lower() + string.digits * 3) for i in range(10))

def login():
    try:
        driver.get('https://gmail.com')
        driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(gLogin)
        driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        driver.find_element_by_xpath('//input[@name="password"]').send_keys(gPass)
        driver.find_element_by_id('passwordNext').click()

        print ('Login PASS')
        sendMail()
    except:
        print ('Login FAILED')
        driver.close()

def sendMail():
    try:
        income = len(driver.find_elements_by_css_selector('.zA'))
        for a in range(mails_to_sent):
            driver.find_element_by_xpath('//*[@class="T-I T-I-KE L3"]').click()
            sleep(0.5)
            driver.find_element_by_css_selector(".vO").send_keys(gLogin)
            driver.find_element_by_css_selector(".aoT").send_keys(random_text())
            driver.find_element_by_css_selector(".Am.Al.editable.LW-avf").send_keys(random_text())
            driver.find_element_by_css_selector(".T-I.J-J5-Ji.aoO.T-I-atl.L3").click()
        sleep(1)
        newincome = len(driver.find_elements_by_css_selector('.zA'))
        if ((newincome - mails_to_sent) == income):
            print ('All {} mails received').format(mails_to_sent)
            print ('Send mail PASS')
        sendLastMail()
    except:
        print('Send mail FAILED')
        driver.close()
        
def sendLastMail():
    try:
        driver.find_element_by_xpath('//*[@class="T-I T-I-KE L3"]').click()
        sleep(0.5)
        driver.find_element_by_css_selector(".vO").send_keys(gLogin)
        driver.find_element_by_css_selector(".aoT").send_keys("MailInfo")

        mails = driver.find_elements_by_css_selector('.zA')

        for i in mails:
            subject = i.find_element_by_class_name('y6').text
            text = i.find_element_by_class_name('y2').text
            text = text.translate({ord(i): None for i in ' -\n'})

            my_dict[subject] = text
            if(len(my_dict) == mails_to_sent):
                break

        for k, v in my_dict.items():
            digits = ''.join([n for n in v if n.isdigit()])
            letters = ''.join([i for i in v if i.islower()])

            text = "Received mail on theme {} with message: {}. It contains {} letters and {} numbers\n".format(k, v, len(letters), len(digits))
            driver.find_element_by_css_selector(".Am.Al.editable.LW-avf").send_keys(text)
        driver.find_element_by_css_selector(".T-I.J-J5-Ji.aoO.T-I-atl.L3").click()
        print ('Send last mail PASS')
        delete_mails()
    except:
        print('Send last mail FAILED')
        driver.close()


def delete_mails():
    try:
        sleep(3)
        j = 0
        check = driver.find_elements_by_xpath("//*[@role='checkbox']")
        for i in check:
            i.click()
            j += 1
            if (j == 2):
                break

        driver.find_element_by_xpath('//*[@class="T-I J-J5-Ji nX T-I-ax7 T-I-Js-Gs mA"]').click()
        print ('Mail deleting PASS')
    except:
        print('Mail deleting FAILED')

login()
