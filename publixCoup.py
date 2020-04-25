# -*- coding: utf-8 -*-
# ======================================================================================
# title           : publixCoup.py
# author          : Camiren Stewart
# date            : 2020.02.04
# version         : V1.0
# version notes   : Credentials now arguments into main
#                 : Added Debug Mode, indicates in logs.
# usage           : python3 publixCoup.py
# python_version  : 3.7
# dependencies    : pip3 install splinter
#                 : pip3 install psutil
#                 : pip3 install fpdf
#                 : [Firefox Webdriver] https://github.com/mozilla/geckodriver/releases
# Assumptions     : 
# ======================================================================================

import argparse                     # ArgumentParser
import time, traceback, os, sys

import psutil   # Kills processes during cleanup.

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import constants, utl
# import util     # Picture & PDF


parser = argparse.ArgumentParser(description='A script for pulling information from a plain text file.')
parser.add_argument("-d", "--debug", help="does not execute actions", action="store_true")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-H", "--headless", help="Run Firefox Headless", action="store_true")
parser.add_argument("-u", "--username", help="Publix Username")
parser.add_argument("-p", "--password", help="Publix Password")
args = parser.parse_args()


def cleanup(driver):
    utl.verbose_print("Cleaning Up","message")
    utl.verbose_print(" .. Closing..","message")
    driver.close()
    utl.verbose_print(" .. Quiting..","message")
    driver.quit()
    utl.verbose_print(" .. Nuking..","message")
    process_name = 'firefox'
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.kill()
            utl.verbose_print(" .. Killing: {0}".format(proc.name()), "message")
    return 0


def main():
    """ Main program """
    global args

    # Navigate & Login to https://www.publix.com/
    # ======================================================================================
    # Launch Browser
    utl.verbose_print("Initializing", "message")
    options = Options()
    if args.headless:
        options.headless = True
        utl.verbose_print(" .. Launching the Headless Firefox", "message")
    else:
        utl.verbose_print(" .. Launching Firefox GUI ..", "message")

    if os.name == 'nt':
        # Windows
        driver = webdriver.Firefox(options=options)
    elif os.name == "posix":
        # unix
        # ToDo: fix getcwd because it returns path that script is executed from
        driver_path = os.path.join(os.getcwd(), "geckodriver")
        sys.path.insert(0, driver_path)         # [Unix Only] Must add geckdriver to path 
        driver = webdriver.Firefox(options=options, executable_path=driver_path)
        sys.path.pop(0)                         # [Unix Only] Remove geckodriver frompath
    else:
        os._exit(1)

    driver.get("http://publix.com")
    # driver.get("https://publix.com/savings/digital-coupons")
    utl.verbose_print(" .. Firefox Successfully Initialized", "message")
    time.sleep(3)
    driver.save_screenshot("screenshots/1-Firefox_Initialized-Not_logged_in.png")

    # Login to Publix
    # ======================================================================================
    # Find the Log In Button that is wrapped in html span tags
    utl.verbose_print("Logging In", "message")
    for element in driver.find_elements_by_css_selector('span'):
        if element.text == "LOG IN":        # You're looking for a button called "LOG IN"
            element.click()                 # When LOG IN is found, click it.
            break                           # Once clicked, break out of the for loop

    # Insert Publix Credentials
    utl.verbose_print(" .. Inserting Credentials", "message")

    if args.username:
        constants.USER = args.username
    if args.password:
        constants.PASS = args.password

    username_field = driver.find_element_by_id('tmpUserNameInput')      # Find the username field
    username_field.send_keys(constants.USER)                            # Insert Username in username field
    password_field = driver.find_element_by_id('passwordInput')         # Find the password field
    password_field.send_keys(constants.PASS)                            # Insert Password in the password field

    time.sleep(3)
    driver.save_screenshot("screenshots/2-Login_Page_with_credentials.png")

    # Find and Click the submit credentials button
    login_button = driver.find_element_by_id('submitButton')            # Find the Submit Button
    login_button.click()                                                # Click the submit button
    utl.verbose_print(" .. Successfully Logged In", "message")  # TODO: Add error checking to ensure valid credentials

    time.sleep(3)
    driver.save_screenshot("screenshots/3_Logged_In.png")

    # Navigate to Digital Coupons [https://www.publix.com/savings/digital-coupons]
    # ======================================================================================
    utl.verbose_print("Navigating to the digital coupons section", "message")
    driver.get("http://www.publix.com/savings/digital-coupons")

    utl.verbose_print(" .. Waiting 15 seconds for page to load", "message")
    time.sleep(15)
    utl.verbose_print(" .. Digital Coupons page loaded", "message")

    # Dismiss the Feedback popup, if it pops up..
    try:
        we_want_to_hear_from_you_button = driver.find_element_by_class_name('fsrButton')    # Find the no thanks button
        if we_want_to_hear_from_you_button:                                                 # Did you find it?
            we_want_to_hear_from_you_button.click()                                         # Click it!
            utl.verbose_print(" .. Publix wanted to hear from us, but we ignored them.", "message")
    except Exception:
        pass

    # Locate the "Show All" link and click it
    show_all_button = driver.find_element_by_class_name('text-link')    # Find Show-all Button
    utl.verbose_print("Clicking the show-all button","message")
    time.sleep(3)
    driver.save_screenshot("screenshots/4-About_to_click_Show_All.png")
    show_all_button.click()                                             # Click Show-all Button

    # todo: get rid of Manual Sleep and look for something on the page to trigger the next step.
    utl.verbose_print(" .. Waiting 30 Seconds for all the coupons to load on the page", "message")
    time.sleep(30)                                                      # Got bit by show-all taking a while to load.

    # Find all the "Clip Coupon" buttons and click them
    coupons_clipped = 0                                                         # Initialization
    buttons = driver.find_elements_by_xpath('//button')                         # Find all the buttons
    time.sleep(3)
    driver.save_screenshot("screenshots/5-About_to_clip_first_coupon.png")
    utl.verbose_print("Clipping Coupons. Please Stand By ..", "message")
    for button in buttons:                                                      # Loop through them all
        if button.text.lower() == "clip coupon":                                # Look for available Clip Coupons
            time.sleep(0.5)
            if args.debug:                                                      # Check debug mode
                pass                                                            # Don't clip the coupon
            else:
                button.click()                                                  # Click the available Clip Coupons
            coupons_clipped += 1                                                # Count your Clip Coupon clicks

    utl.verbose_print(" .. You clipped {0} coupons.".format(coupons_clipped), "message")
    time.sleep(3)  # Got stung by this once, started with 2sec

    # todo: Find a good way to notify user after script runs. Email PDF package, text, etc?
    #
    #  Generate Screenshots and PDF Package
    # ======================================================================================
    # utl.verbose_print("Creating PDF Package..", "Message")
    # filename = os.path.join(os.getcwd(), "screenshots", "output.png")
    # util.fullpage_screenshot(driver, filename)
    #
    # screenshot_list = glob.glob(os.path.join(os.getcwd(), "screenshots", "*.png"))
    # util.convert_img_to_pdf(screenshot_list)

    # Clean-Up
    # ======================================================================================
    utl.verbose_print("Completed Successfully.", "message")
    cleanup(driver)
    utl.verbose_print("done.","message")

    return 0


if __name__ == "__main__":
    try:
        if args.debug:
            utl.verbose_print(" -- DEBUG MODE --", "Message")

        start_time = time.time()
        utl.create_log(args.debug, args.verbose)
        utl.verbose_print(time.asctime(), 'debug')

        main()

        utl.verbose_print(time.asctime(), "message")
        utl.verbose_print('TOTAL TIME IN MINUTES: {}'.format((time.time() - start_time) / 60.0), "message")

        sys.exit(0)

    except Exception:
        utl.verbose_print('ERROR, UNEXPECTED EXCEPTION', "Error")
        traceback.print_exc()
        os._exit(1)
