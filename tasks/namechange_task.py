import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from core.celery_manager import app
from core.mysql import DatabaseManager

def wait_for_element_present(driver, selector, by = By.CSS_SELECTOR, timeout = 5):
    wait_function = lambda driver : driver.find_element(by = by, value = selector)

    return WebDriverWait(driver, timeout).until(wait_function,
        "Element %s was not present in %s seconds" % (selector, timeout))

@app.task
def change_name(whom):
    # get user info
    if whom not in ['pope', 'rau']:
        raise Exception('who the fuck are you')

    query = "SELECT team_id, email, password FROM Nicks WHERE name = %(name)s"
    result = DatabaseManager().fetchone_query_and_close(query, {'name': whom})
    team_id, email, password = result

    # get team names
    query = "SELECT name FROM Sportsballs WHERE 1"
    results = DatabaseManager().fetchall_query_and_close(query, {})
    names = []
    for result in results:
        names.append(result[0])

    # pick one
    new_name = random.choice(names)
    new_logo_id = random.choice(range(1, 13))

    # do the thing
    DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
    desired_caps = DesiredCapabilities.PHANTOMJS.copy()
    desired_caps['javascriptEnabled'] = True 
    driver = webdriver.PhantomJS(desired_capabilities = desired_caps)

    # use for local debugging
    # break glass in case of fuckery
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0')    
    # driver = webdriver.Firefox(profile)

    try:
        #login 
        driver.get("http://football.fantasysports.yahoo.com/f1/936352")
        wait_for_element_present(driver, '#login-username')
        driver.find_element_by_css_selector('#login-username').send_keys(email)
        driver.find_element_by_css_selector('#login-passwd').send_keys(password)
        driver.find_element_by_css_selector('#login-signin').click()
        
        #edit info
        driver.get('http://football.fantasysports.yahoo.com/f1/936352/%s/editteaminfo' % team_id)
        wait_for_element_present(driver, 'form#editteaminfoform input[name=TN]')
        driver.find_element_by_css_selector('form#editteaminfoform input[name=TN]').clear()
        driver.find_element_by_css_selector('form#editteaminfoform input[name=TN]').send_keys(new_name)
        driver.find_element_by_css_selector('form#editteaminfoform label#LG_%s' % new_logo_id).click()
        driver.find_element_by_css_selector('input[name=jsubmit]').click()
        wait_for_element_present(driver, '#team_card_info')
    except Exception, e:
        driver.get_screenshot_as_file('wtf.png')
        print str(e)

    driver.quit()
