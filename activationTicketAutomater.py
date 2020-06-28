#! python3
import sys
import time
import argparse
import logging
from settings import EMAIL, PASSWORD, NAME
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


#looks at the caller's department and determines if it is a student or not.
#the comments will have an additional paragraph about bypassing the device if student       
def is_student(driver):
    dept = driver.find_element_by_xpath("//*[@id='sys_display.incident.caller_id.department']")
    deptstr = dept.get_attribute("value")
    if deptstr == 'Student':
        return True
    return False

#returns the first name of the caller to address the comments     
def get_caller(driver):
    #caller = driver.find_element_by_xpath("//*[@id='sys_display.incident.caller_id']")
    caller = driver.find_element_by_id('incident.caller_id')
    caller_full_name = caller.get_attribute("value")
    caller_firstname = caller_full_name.partition(' ')[0]
    return caller_firstname

#fills the worknotes with the optional string from the command line, if provided
def fill_worknotes(driver, message):
    #worknotes = driver.find_element_by_xpath("/html/body/div[2]/form/span[2]/span/div/div[2]/div/div[2]/div[2]/textarea")
    if len(message) > 0:
        worknotes = driver.find_element_by_id('incident.work_notes')
        worknotes.send_keys(message)
        logging.info('Filled in worknotes section')

#fills the comments with an email message including optional jack info from command line if present
def fill_comments(driver, jack):
    caller = get_caller(driver)
    comments = driver.find_element_by_id('incident.comments')
    
    if is_student(driver):
        ise = 'If your device has a browser, such as a laptop or desktop computer, please go to https://tinyurl.com/WiredBypass'\
        'to activate your device. If not (such as a gaming console or TV), you\'ll need to find the wired MAC/hardware address'\
        'for your device (usually in network settings). Then you will need to register your device by '\
        'contacting Help Desk (help@up.edu) and giving them the MAC/hardware address'
        
        message = 'Hello ' + caller + ',\n\nYour Ethernet port ' + jack + ' has been activated\n\n' + ise + '\n\nThanks,\n\n' + NAME
        comments.send_keys(message)
        logging.info('Filled in comments section for a student activation')
        
    else:
        message = 'Hello ' + caller + ',\n\nYour Ethernet port ' + jack + ' has been activated. Let us know if there are any issues.'\
        ' If we do not hear otherwise in a week, this ticket will be resolved.\n\nThanks,\n\n' + NAME
        comments.send_keys(message)
        logging.info('Filled in comments section for staff activation')
    
    
#changes state to Awaiting Customer Response if it is not already
def change_state(driver):
    state = driver.find_element_by_id('incident.state')
    if state.get_attribute("value") != '4':
        select = Select(state)
        select.select_by_value('4') #awaiting customer response
        logging.info('Changed state to Awaiting Customer Response')

#hits the update button to save the changes we have made to the ticket
def save(driver):
    save_button = driver.find_element_by_id('sysverb_update')
    save_button.click()
    logging.info('Saving changes. You should see an email update shortly')

#handles initial login to the service with student worker's microsoft account    
def microsoft_login(driver):
    next = driver.find_element_by_id('i0116')
    next.send_keys(EMAIL)
    next.send_keys(Keys.RETURN)
    time.sleep(1)
    next = driver.find_element_by_id('i0118')
    next.send_keys(PASSWORD)
    next.send_keys(Keys.RETURN)
    time.sleep(1)
    next = driver.find_element_by_id('idSIButton9')
    next.click()
    logging.info('Logged in with your info from settings.py')
    
def main():
    
    #parsing the command line arguments
    my_parser = argparse.ArgumentParser(description='Automating filling out an activation ticket')
    my_parser.add_argument('url',
                       metavar='url',
                       type=str,
                       help='url of the activation ticket')
    my_parser.add_argument('-j', '--jack_label', nargs='?', action='store', type=str, dest='jack_label', default='', help='optional jack label and/or description in double quotes, e.g. "CR-2A-J-041 (left side)"')
    my_parser.add_argument('-w', '--worknotes', nargs='?', action='store', type=str, dest='worknotes', default='', help='optional worknotes in double quotes, e.g. "Activated to WH-4A-2960-01 Gi1/0/34"')
    my_parser.add_argument('-l', '--logging', action='store_true', dest='log_flag', default=False, help='Show logging info if you want to see what is going on during execution')
    my_parser.set_defaults(feature=False)
    args = my_parser.parse_args()
    
    #turn on logging if desired
    if args.log_flag:    
        logging.basicConfig(level=logging.INFO)
        
    logging.info('Setting everything up')
    
    #setup selenium ChromeDriver, we don't need to see the window
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('--silent')
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=op)
    type(driver)
    driver.get(args.url) #go to the ticket url from the command line

    microsoft_login(driver)
    iframe = driver.find_element_by_name('gsft_main')
    driver.switch_to.frame(iframe)
    fill_worknotes(driver, args.worknotes)
    fill_comments(driver, args.jack_label)
    change_state(driver)
    save(driver)
    driver.quit()
    
main()