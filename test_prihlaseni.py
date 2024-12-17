import pytest
from playwright.sync_api import sync_playwright
import re

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000
        )  # Set headless=False to see the browser actions
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def is_valid_email(email):
    # Regular expression for a basic email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Match the regex with the provided email
    if re.match(email_regex, email):
        return True
    return False

@pytest.mark.parametrize("email, expected", [
        ("lumilat1@seznam.cz", True),
        ("aaaaaaa", False),
        ("aaaaaaa@", False),
        ("aaaaaaa@bbbbbb", False),
        ("aaaaaaa@seznam.cc", True),
        ("aaaaaaa@seznam.cz", True)
    ])
def test_mailbox(email, expected):
        assert is_valid_email(email) == expected

def test_google_search_result(page):
    query = "bezedná miska"
    print("read in google")
    page.goto("https://www.google.com")

    print("Přijmout vše?")
    page.wait_for_selector('#L2AGLb', timeout=60000)
    button = page.query_selector('#L2AGLb')
    print("kliknutí na button")
    button.click()

    # zadání vyhledávání v Google
    print("Waiting for search input")
    page.wait_for_selector('#APjFqb',timeout=60000)
    print("Filling search input")
    page.fill('#APjFqb', query)
    page.press('#APjFqb', "Enter")

    print("Waiting for search results")
    page.wait_for_selector('a[jsname="UWckNb"]',timeout=600000)
    sources = page.query_selector_all('a[jsname="UWckNb"]')  # vybere všechny odkazy od Google

    sources[0].click() # vybere první odkaz

# odkliknutí křížku na prvním otevřeném odkazu
    page.wait_for_selector('#mlctr7926 > ml-object > ml-main > ml-close', timeout=60000)
    button1 = page.query_selector('#mlctr7926 > ml-object > ml-main > ml-close')
    button1.click()
    
# odkliknutí cookies na bezedné
    page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll') 
    button2 = page.query_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    button2.click()

# odkliknutí přihlášení
    page.wait_for_selector('#sticky-wrapper > div > div.container > div > div.header-icons-wrap > div.box-small-account.notlogged.btn-group > button', timeout=60000)
    button3 = page.query_selector('#sticky-wrapper > div > div.container > div > div.header-icons-wrap > div.box-small-account.notlogged.btn-group > button')
    button3.click()

# odkliknutí nové registrace
    page.wait_for_selector('#desktop_rightLogin_Register', timeout=60000)
    button4 = page.query_selector('#desktop_rightLogin_Register')
    button4.click()

# odkliknutí mailového pole     
    print("zadávání email adresy0")
    page.wait_for_selector('#contact_oxuser__oxusername', timeout=60000)
    button5 = page.query_selector('#contact_oxuser__oxusername')
    button5.click()
    page.wait_for_selector('#contact_oxuser__oxfon', timeout=60000)
    button6 = page.query_selector('#contact_oxuser__oxfon')
    button6.click()
    button5.click()