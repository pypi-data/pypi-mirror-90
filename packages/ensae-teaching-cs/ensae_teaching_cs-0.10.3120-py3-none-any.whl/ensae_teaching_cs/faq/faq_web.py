# -*- coding: utf-8 -*-
"""
@file
@brief A few functions about scrapping

"""
import sys
import os
import datetime
import warnings
from pyquickhelper.loghelper import noLOG
from pymyinstall.installcustom import where_in_path, install_chromedriver, install_operadriver


default_driver = "opera"


def webshot(img, url, navigator=default_driver, add_date=False,
            size=None, fLOG=noLOG):
    """
    Uses the module :epkg:`selenium`
    to take a picture of a website.
    If url and img are lists, the function goes
    through all the urls and save webshots.

    @param      img             list of image names
    @param      url             url
    @param      navigator       firefox, chrome, (ie: does not work well)
    @param      add_date        add a date to the image filename
    @param      size            to resize the webshot (if not None)
    @param      fLOG            logging function
    @return                     list of [ ( url, image name) ]

    Check the list of available webdriver at
    `selenium/webdriver <https://github.com/SeleniumHQ/selenium/tree/master/py/selenium/webdriver>`_
    and add one to the code if needed.

    Chrome requires the `chromedriver <http://chromedriver.storage.googleapis.com/index.html>`_.
    See function `install_chromedriver <http://www.xavierdupre.fr/app/pymyinstall/helpsphinx/pymyinstall/
    installcustom/install_custom_chromedriver.html?highlight=chromedriver
    #pymyinstall.installcustom.install_custom_chromedriver.install_chromedriver>`_.
    """
    res = []
    browser = _get_selenium_browser(navigator, fLOG=fLOG)

    if size is not None:
        fLOG("set size", size)
        browser.set_window_size(size[0], size[1])

    if not isinstance(url, list):
        url = [url]
    if not isinstance(img, list):
        img = [img]
    if len(url) != len(img):
        raise Exception("different number of urls and images")
    for u, i in zip(url, img):
        fLOG("url", url, " into ", img)
        browser.get(u)
        if add_date:
            dt = datetime.datetime.now()
            a, b = os.path.splitext(i)
            i = "{0}.{1}{2}".format(a, str(dt).replace(
                ":", "-").replace("/", "-"), b)
        browser.get_screenshot_as_file(i)
        res.append((u, i))
    browser.quit()
    return res


def _get_selenium_browser(navigator, fLOG=noLOG):
    """
    Returns the associated driver with some custom settings.

    The function automatically gets chromedriver if not present (:epkg:`Windows` only).
    On :epkg:`Linux`, package *chromium-driver* should be installed:
    ``apt-get install chromium-driver``.

    .. faqref::
        :tag: web
        :title: Issue with Selenium and Firefox
        :lid: faq-web-selenium

        Firefox >= v47 does not work on Windows.
        See `Selenium WebDriver and Firefox 47 <http://www.theautomatedtester.co.uk/blog/2016/selenium-webdriver-and-firefox-47.html>`_.

        Voir `ChromeDriver download <http://chromedriver.storage.googleapis.com/index.html>`_,
        `Error message: 'chromedriver' executable needs to be available in the path
        <http://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path>`_.

    See `Selenium - Remote WebDriver example
    <https://sauceclient.readthedocs.io/en/latest/selenium_on_sauce.html#selenium-remote-webdriver-example>`_,
    see also `Running the remote driver with Selenium and python <https://gist.github.com/alfredo/1962031>`_.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ImportWarning)
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    fLOG("[webshot] navigator=", navigator)
    if navigator == "firefox":
        firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
        firefox_capabilities['marionette'] = True
        firefox_capabilities[
            'binary'] = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        browser = webdriver.Firefox(capabilities=firefox_capabilities)
    elif navigator == "chrome":
        if sys.platform.startswith("win"):
            chromed = where_in_path("chromedriver.exe")
            if chromed is None:
                install_chromedriver(fLOG=fLOG)
                chromed = where_in_path("chromedriver.exe")
                if chromed is None:
                    raise FileNotFoundError(
                        "unable to install 'chromedriver.exe'")
            else:
                fLOG("[_get_selenium_browser] found chromedriver:", chromed)
        else:
            chromed = 'chromedriver'

        start_navi = True
        if start_navi:
            fLOG("[_get_selenium_browser] start", navigator)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--verbose')
            browser = webdriver.Chrome(executable_path=chromed,
                                       chrome_options=chrome_options)
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ImportWarning)
                import selenium.webdriver.chrome.service as wservice
            fLOG("[_get_selenium_browser] create service")
            service = wservice.Service(chromed)
            fLOG("[_get_selenium_browser] start service")
            service.start()
            fLOG("[_get_selenium_browser] declare remote")
            capabilities = {'chrome.binary': chromed}
            browser = webdriver.Remote(service.service_url, capabilities)
    elif navigator == "ie":
        browser = webdriver.Ie()
    elif navigator == "opera":
        if sys.platform.startswith("win"):
            chromed = where_in_path("operadriver.exe")
            if chromed is None:
                install_operadriver(fLOG=fLOG)
                chromed = where_in_path("operadriver.exe")
                if chromed is None:
                    raise FileNotFoundError(
                        "unable to install operadriver.exe")
            else:
                fLOG("[_get_selenium_browser] found chromedriver:", chromed)
        else:
            chromed = 'operadriver'
        browser = webdriver.Opera(chromed)
    elif navigator == "edge":
        browser = webdriver.Edge()
    else:
        raise Exception(
            "unable to interpret the navigator '{0}'".format(navigator))
    fLOG("[_get_selenium_browser] navigator is started")
    return browser


def webhtml(url, navigator=default_driver, fLOG=noLOG):
    """
    Uses the module `selenium <http://selenium-python.readthedocs.io/>`_
    to retrieve the html content of a website.

    @param      url             url
    @param      navigator       firefox, chrome, (ie: does not work well)
    @param      fLOG            logging function
    @return                     list of [ ( url, html) ]

    Check the list of available webdriver at
    `selenium/webdriver
    <https://github.com/SeleniumHQ/selenium/tree/master/py/selenium/webdriver>`_
    and add one to the code if needed.
    """
    res = []
    browser = _get_selenium_browser(navigator, fLOG=fLOG)
    if not isinstance(url, list):
        url = [url]
    for u in url:
        fLOG("[webhtml] get url '{0}'".format(url))
        browser.get(u)
        i = browser.page_source
        res.append((u, i))
    browser.quit()
    return res
