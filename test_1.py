#######################################################################
## Author    : Yazan Abd-Al-Majeed
## Content   : Testing Whole Options of https://the-internet.herokuapp.com Website
## Copyright : Mafee4 :)
#######################################################################

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 1  # 1=allow, 2=block
    })
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
    

def test_ab_testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[text()='A/B Testing']").click()
    wait = WebDriverWait(driver, 10)
    Heading = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='A/B Test Variation 1']")))
    Heading_Text = Heading.text
    assert "A/B Test" in Heading_Text



def test_Add_Remove_Elements(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'add')]").click()
    wait = WebDriverWait(driver, 10)
    Add_Elem_Btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text() = 'Add Element']")))
    Add_Elem_Btn.click()
    Add_Elem_Btn.click()
    Delete_Btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class = 'added-manually']")))
    Delete_Btn.click()
    BTNs_Number = driver.find_elements(By.XPATH, "//button[@class = 'added-manually']")
    assert len(BTNs_Number) == 1

def test_Basic_Auth_True_Cred_Test(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'basic')]").click()
    driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    wait = WebDriverWait(driver, 10) 
    Congrats_Text = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Congratulations!')]")))
    assert "Congratulations!" in Congrats_Text.text

def test_Basic_Auth_Wrong_Cred_Test(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'basic')]").click()
    driver.get("https://admin:adminn@the-internet.herokuapp.com/basic_auth")
    assert "Congratulations!" not in driver.page_source

def test_Broken_Photos_Test(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'broken')]").click()
    wait = WebDriverWait(driver, 10)
    Photos = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    assert requests.get(Photos[0].get_attribute("src")).status_code == 200
    assert requests.get(Photos[1].get_attribute("src")).status_code != 200
    assert requests.get(Photos[2].get_attribute("src")).status_code != 200

def test_Challenging_DOM_Edit_Delete_BTNs_Work(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'challenging')]").click()
    wait = WebDriverWait(driver, 10)
    Edit_BTN = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text() = 'edit']")))
    Edit_BTN.click()
    URL1 = driver.current_url
    driver.find_element(By.XPATH, "//a[text() = 'delete']").click()
    URL2 = driver.current_url
    assert URL1 == "https://the-internet.herokuapp.com/challenging_dom#edit"
    assert URL2 == "https://the-internet.herokuapp.com/challenging_dom#delete"


def test_Challenging_DOM_Pressing_BTN_Changes_ItsName(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'challenging')]").click()
    wait = WebDriverWait(driver, 10)
    BTN1 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'large-2 columns']/child::a")))
    BTN_Text1 = BTN1.text
    BTN1.click()
    wait.until(EC.staleness_of(BTN1))
    BTN2 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'large-2 columns']/child::a")))
    BTN2.click()
    wait.until(EC.staleness_of(BTN2))
    BTN3 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'large-2 columns']/child::a")))
    BTN_Text3 = BTN3.text
    assert BTN_Text1 != BTN_Text3

def test_Challenging_DOM_CheckBox_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/checkboxes']").click()
    wait = WebDriverWait(driver, 10)
    Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    Title_Text = Title.text
    # Valid Weather Checkbox can be Unchecked
    CheckBox1 = driver.find_element(By.XPATH, "//input[@type = 'checkbox']")
    CheckBox1.click()
    CheckBox1_Status = CheckBox1.is_selected()
    # Valid Weather Checkbox can be Unchecked
    CheckBox2 = driver.find_elements(By.XPATH, "//input[@type = 'checkbox']")
    CheckBox2[1].click()
    CheckBox2_Status = CheckBox2[1].is_selected()

    assert Title_Text == "Checkboxes"
    assert CheckBox1_Status == True
    assert CheckBox2_Status == False
    
def test_Challenging_DOM_Pressing_BTN_Changes_ItsName(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'challenging')]").click()
    wait = WebDriverWait(driver, 10)
    BTN1 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'large-2 columns']/child::a")))
    BTN_Text1 = BTN1.text
    BTN1.click()
    wait.until(EC.staleness_of(BTN1))
    BTN2 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'large-2 columns']/child::a")))
    BTN2.click()
    wait.until(EC.staleness_of(BTN2))
    BTN3 = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'large-2 columns']/child::a")))
    BTN_Text3 = BTN3.text
    assert BTN_Text1 != BTN_Text3

def test_Challenging_DOM_CheckBox_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/context_menu']").click()
    wait = WebDriverWait(driver, 10)
    Box = wait.until(EC.presence_of_element_located((By.ID, "hot-spot")))
    # Perform right-click (context click) on the box
    actions = ActionChains(driver)
    actions.context_click(Box).perform()
    Alert = wait.until(EC.alert_is_present())
    assert Alert.text == "You selected a context menu"
    Alert.accept()

def test_Challenging_DOM_CheckBox_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/digest_auth']").click()
    wait = WebDriverWait(driver, 10)
    driver.get("https://the-internet.herokuapp.com/digest_auth")
    
def test_Disappearing_Elements_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/disappearing_elements']").click()
    wait = WebDriverWait(driver, 10)
    Home_BTN = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text() = 'Home']")))
    Home_BTN.click()
    Welcome_Page = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    Welcome_Page_Text = Welcome_Page.text
    assert Welcome_Page_Text == "Welcome to the-internet"
    driver.find_element(By.XPATH, "//a[@href = '/disappearing_elements']").click()
    wait = WebDriverWait(driver, 5)
    About_BTN = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text() = 'About']")))
    About_BTN.click()
    NOT_FOUND_Page = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    NOT_FOUND_Page_Text = NOT_FOUND_Page.text
    assert NOT_FOUND_Page_Text == "Not Found"
    driver.back()
    Contact_BTN = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text() = 'Contact Us']")))
    Contact_BTN.click()
    NOT_FOUND_Page = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    NOT_FOUND_Page_Text = NOT_FOUND_Page.text
    assert NOT_FOUND_Page_Text == "Not Found"
    driver.back()
    Portfolio_BTN = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text() = 'Portfolio']")))
    Portfolio_BTN.click()
    NOT_FOUND_Page = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    NOT_FOUND_Page_Text = NOT_FOUND_Page.text
    assert NOT_FOUND_Page_Text == "Not Found"
    driver.back()
    for _ in range(5):
        try:
            Gallery_BTN = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[text() = 'Gallery']"))
            )
            Gallery_BTN.click()
            NOT_FOUND_Page = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            assert NOT_FOUND_Page.text == "Not Found"
            break

        except TimeoutException:
            driver.refresh()

def test_DragandDrop_Elements_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, '/drag')]").click()
    wait = WebDriverWait(driver, 10)
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "//h3")))
    assert Page_Title.text == "Drag and Drop"

def test_Dynamic_Content_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[contains(@href, 'content')]").click()
    wait = WebDriverWait(driver, 10)
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Dynamic Content"

    #Test weather photos are changing

    img1 = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    img_url1 = img1[1].get_attribute("src")
    for _ in range(4):
        driver.refresh()
        time.sleep(0.5)
    img2 = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    img_url2 = img2[1].get_attribute("src")
    assert img_url1 != img_url2

    #Test weather Texts are changing

    photo_text1 = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class= 'large-10 columns']")))
    Text1 = photo_text1[1].text
    for _ in range(4):
        driver.refresh()
        time.sleep(0.5)
    photo_text2 = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class= 'large-10 columns']")))
    Text2 = photo_text2[1].text
    assert Text1 != Text2

def test_Dropdown_List_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/dropdown']").click()
    wait = WebDriverWait(driver, 10)
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Dropdown List"

    driver.find_element(By.XPATH, "//select[@id = 'dropdown']").click()
    Please_Select_Text = wait.until(EC.presence_of_element_located((By.XPATH, "//option[contains(text(), 'option')]")))
    assert Please_Select_Text.text == "Please select an option"

    Option1 = driver.find_element(By.XPATH, "//option[@value = '1']")
    Option1.click()
    Option1_Status = Option1.get_attribute("selected")
    assert Option1_Status == "true"

def test_Dynamic_Controls_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/dynamic_controls']").click()
    wait = WebDriverWait(driver, 10)
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h4")))
    assert Page_Title.text == "Dynamic Controls"

    Remove_Add_Text = driver.find_element(By.XPATH, "//h4[text() = 'Remove/add']")
    assert Remove_Add_Text.text == "Remove/add"

    CheckBox = driver.find_element(By.XPATH, "//input[@type = 'checkbox']")
    CheckBox.click()
    assert CheckBox.is_selected()

    driver.find_element(By.XPATH, "//button[text() = 'Remove']").click()
    Loading_Text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id = 'loading']")))
    assert Loading_Text.text == "Wait for it..."

    Loading_Photo = driver.find_element(By.XPATH, "//img[contains(@src, 'r.gif')]")
    assert Loading_Photo.get_attribute("src") == "https://the-internet.herokuapp.com/img/ajax-loader.gif"

    Remove_Done_MSG = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'gone')]")))
    assert Remove_Done_MSG.text == "It's gone!" 



    driver.find_element(By.XPATH, "//button[text() = 'Add']").click()
    Loading_Text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id = 'loading']")))
    assert Loading_Text.text == "Wait for it..."
    Loading_Photo = driver.find_element(By.XPATH, "//img[contains(@src, 'r.gif')]")
    assert Loading_Photo.get_attribute("src") == "https://the-internet.herokuapp.com/img/ajax-loader.gif"
    Done_MSG = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'back')]")))
    assert Done_MSG.text == "It's back!" 
    CheckBox = driver.find_element(By.XPATH, "//input[@type = 'checkbox']")
    CheckBox.click()
    CheckBoxStatus = CheckBox.is_selected()
    assert CheckBoxStatus == True

def test_Entry_Ad_Testing(driver):
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/entry_ad']").click()
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    Ad_Window = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'window')]")))
    assert "WINDOW" in Ad_Window.text
    driver.find_element(By.XPATH, "//p[text() = 'Close']").click()
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Entry Ad"

def test_File_Upload_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/upload']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "File Uploader"

    #Positive 2
    file_path = os.path.expanduser("~/Desktop/ID.jpeg")
    assert os.path.exists(file_path), f"File not found: {file_path}"
    File_Upload = driver.find_element(By.XPATH, "//input[@id = 'file-upload']")
    File_Upload.send_keys(file_path)
    driver.find_element(By.ID, "file-submit").click()
    Status_MSG = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Status_MSG.text == "File Uploaded!"
    File_Check = driver.find_element(By.ID, "uploaded-files")
    assert File_Check.text == "ID.jpeg"

    #Negative 1
    driver.get("https://the-internet.herokuapp.com/upload")
    Upload_Button = wait.until(EC.presence_of_element_located((By.ID, "file-submit")))
    Upload_Button.click()
    Error_MSG = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert Error_MSG.text == "Internal Server Error"

def test_Floating_Menu_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/floating_menu']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Floating Menu"

    Paragraphs = driver.find_elements(By.TAG_NAME, "p")
    assert len(Paragraphs) == 10

    Home = driver.find_element(By.XPATH, "//a[@href = '#home']")
    Home.click()
    Home_URL = driver.current_url
    assert Home_URL == "https://the-internet.herokuapp.com/floating_menu#home"

    News = driver.find_element(By.XPATH, "//a[@href = '#news']")
    News.click()
    News_URL = driver.current_url
    assert News_URL == "https://the-internet.herokuapp.com/floating_menu#news"
    
    Contact = driver.find_element(By.XPATH, "//a[@href = '#contact']")
    Contact.click()
    Contact_URL = driver.current_url
    assert Contact_URL == "https://the-internet.herokuapp.com/floating_menu#contact"

    About = driver.find_element(By.XPATH, "//a[@href = '#about']")
    About.click()
    About_URL = driver.current_url
    assert About_URL == "https://the-internet.herokuapp.com/floating_menu#about"

    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(5)
    BTN_Status = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href = '#home']")))
    assert BTN_Status is not None

def test_Forgot_Password_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/forgot_password']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
    assert Page_Title.text == "Forgot Password"
    ###########################################
    driver.find_element(By.XPATH, "//button[@class = 'radius']").click()
    Error_MSG = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert Error_MSG.text == "Internal Server Error"
    ###########################################
    driver.get("https://the-internet.herokuapp.com/forgot_password")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("Ahmed123@gmail.com")
    driver.find_element(By.XPATH, "//button[@class = 'radius']").click()
    Error_MSG = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert Error_MSG.text == "Internal Server Error"
    ###########################################
    driver.get("https://the-internet.herokuapp.com/forgot_password")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("Dammy")
    driver.find_element(By.XPATH, "//button[@class = 'radius']").click()
    Error_MSG = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert Error_MSG.text == "Internal Server Error"

def test_Geolocation_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/geolocation']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Geolocation"


    #Positive 2
    driver.find_element(By.XPATH, "//button[@onclick = 'getLocation()']").click()
    time.sleep(0.5)
    Location = wait.until(EC.presence_of_element_located((By.ID, "demo")))
    assert "Latitude:" in Location.text
    assert "Longitude:" in Location.text

    Lat_Value = driver.find_element(By.XPATH, "//div[@id = 'lat-value']")
    Long_Value = driver.find_element(By.XPATH, "//div[@id = 'long-value']")
    assert Lat_Value.text is not 0
    assert Long_Value.text is not 0

    Google_Maps = driver.find_element(By.XPATH, "//a[contains(text(), 'Google')]")
    assert Google_Maps.text == "See it on Google"
    Google_Maps.click()
    Google_Maps_URL = driver.current_url
    assert "https://www.google.com/maps" in Google_Maps_URL

def test_Horizontal_Slider_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/horizontal_slider']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Horizontal Slider"

    #Positive 2
    driver.find_element(By.XPATH, "//input[@type = 'range']").click()
    Actions = ActionChains(driver)
    Actions.send_keys(Keys.ARROW_RIGHT).perform()

    Value = driver.find_element(By.XPATH, "//span[@id = 'range']")
    assert Value.text is not 0

def test_Hover_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/hovers']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Hovers"
    ########################################
    Users = driver.find_elements(By.XPATH, "//div[@class = 'figure']")
    Actions = ActionChains(driver)
    Actions.move_to_element(Users[0]).perform()

    User1_Info = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='figure'][1]//h5[text()='name: user1']")))
    assert User1_Info.text == "name: user1"

    View_Profile_Link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='figure'][1]//a[@href='/users/1']")))
    View_Profile_Link.click()

    Not_Found_MSG = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert "/users/1" in driver.current_url
    assert Not_Found_MSG.text == "Not Found"

def test_Infinite_Scroll_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.nfind_element(By.XPATH, "//a[@href = '/infinite_scroll']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Infinite Scroll"

    for i in range(10):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(0.25)

    Paragraphs = driver.find_elements(By.XPATH, "//div[@class = 'jscroll-added']")    
    assert len(Paragraphs) > 7

def test_Inputs_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/inputs']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "Inputs"

    Number = driver.find_element(By.TAG_NAME, "p")
    assert Number.text == "Number"

def test_JavaScript_Alerts_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/javascript_alerts']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "JavaScript Alerts"
    ######################################################
    Buttons = driver.find_elements(By.XPATH, "//button")
    Buttons[0].click()
    Alert = wait.until(EC.alert_is_present())
    Alert.accept()
    Result = wait.until(EC.text_to_be_present_in_element((
        By.XPATH, "//p[@id = 'result']"), "You successfully"))
    assert Result == True
    ######################################################
    Buttons[1].click()
    Alert = wait.until(EC.alert_is_present())
    Alert.accept()
    Result = wait.until(EC.text_to_be_present_in_element((
        By.XPATH, "//p[@id = 'result']"), "You clicked: Ok"))
    assert Result == True
    ######################################################
    Buttons[1].click()
    Alert = wait.until(EC.alert_is_present())
    Alert.dismiss()
    Result = wait.until(EC.text_to_be_present_in_element((
        By.XPATH, "//p[@id = 'result']"), "You clicked: Cancel"))
    assert Result == True
    ######################################################
    Buttons[2].click()
    Alert = wait.until(EC.alert_is_present())
    Alert.send_keys("Hello")
    Alert.accept()
    Result = wait.until(EC.text_to_be_present_in_element((
        By.XPATH, "//p[@id = 'result']"), "You entered: Hello"))
    assert Result == True

def test_JavaScript_Alerts_Testing(driver):
    #Positive 1
    driver.get("https://the-internet.herokuapp.com/")
    driver.find_element(By.XPATH, "//a[@href = '/javascript_alerts']").click()
    wait = WebDriverWait(driver, 10)  
    Page_Title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert Page_Title.text == "JavaScript Alerts"