# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:57:13 2017

@author: Gromgorgel
"""
###############################################################################    
# PREAMBLE
###############################################################################

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# look up some common exceptions so we can catch them:
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
# import progressbar
from tqdm import tqdm

###############################################################################    
# SCRIPT
###############################################################################
WD = 'C:\\path\\to\\files\\folder' # unix mode
WD2 = 'C:/path/to/files/folder/' # windows mode
os.chdir(WD) #changes the current wd to 'path'
files = os.listdir(WD)


# prep web address
url = 'https://www.ncbi.nlm.nih.gov/sites/batchentrez'

# due to slow response of the webserver, some files will not be retrieved
# that's OK, we'll just run the script a bunch of times untill we succeed

maxiter = 5 # max number of times we can try to re-run the missing data stuff
itercount = 0 # keep track of nr of iterations
i_max = len(files) 

while i_max > 0:
    # we'll keep trying to fetch the data 
    itercount += 1
    print("Run iteration ", itercount)
    # keep track of all files that fail the procedure in this iteration
    rerun = []    
    # I'm going to use a progress bar to get an idea of how long this will take
    # feel free to peel of the 'with tqdm' layer if you have no needs for such fancy
    with tqdm(total = i_max, unit = 'fetch', unit_scale = True) as pbar:
        # we'll retrieve the sequences file by file:
        for file in files:
            # quick count of the number of refs in the file:
            with open(file, 'r') as sfile: 
               # quickly loop through file to determine the number of lines:
                for nref, l in enumerate(sfile):
                        pass
                nref += 1   # starts counting from zero, so we add 1
            # we construct the entire filepath in windows mode 
            path = WD2 + file
            try: # timout errors have been known to occur, so we're going to catch them
                # We'll be using Phantom as our webdriver
                driver = webdriver.PhantomJS(executable_path=r'C:\Program Files (x86)\phantomjs\bin\phantomjs.exe')
                # OR you can use chromedriver to actually see what you're doing:
                #driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe') 
                driver.set_page_load_timeout(5)     # set timeout to 5 sec
                driver.get(url)                     # go to page
                inputElement = driver.find_element_by_name("file") # find input field
                inputElement.send_keys(path)         # send file path
                # now we find the retrieve button & klick it
                retrieveElement = driver.find_element_by_name("cmd") # find input field
                retrieveElement.send_keys(Keys.ENTER)  # hit enter
                time.sleep(4) # wait for NCBI server to look up results
                # now we click the link to our records:
                retrieveElement = driver.find_element_by_partial_link_text('Retrieve') 
                retrieveElement.click()  # click link         
                # we've now arrived at our list of sequences, Standard display option is 20 per page
                # unless there are less than 10, in which case there is no display option (prompting a NoSuchElementException if we try to find it)
                # Anyway, we'll check if we need to display more (and do so if necessary)
                if nref > 20:                    
                    # so there are more than 20 refs, now we need to find the dropdown menu to change the number displayed
                    # however, there are several dropdown menus with the same ID, so we get a list of all of them (find_elements in stead of find_element)
                    elems = driver.find_elements_by_xpath("//*[@id='EntrezSystem2.PEntrez.Nuccore.Sequence_ResultsPanel.Sequence_DisplayBar.Display']")
                    # open menu and select the option we want
                    elems[1].send_keys(Keys.ENTER)  # second element changes display, we open the menu using ENTER
                    time.sleep(1) # wait for menu to appear (otherwise you get an 'element not visible' error)
                    # choose 100 per page, change if you need more   
                    driver.find_element_by_xpath("//*[@id='ps100']").click()
                # next we will click the other dropdown menu and select the fasta-text format to get the actual sequences
                elems = driver.find_elements_by_xpath("//*[@id='EntrezSystem2.PEntrez.Nuccore.Sequence_ResultsPanel.Sequence_DisplayBar.Display']") 
                elems[0].send_keys(Keys.ENTER) # the first element is the one to click
                time.sleep(1) # wait for menu to appear
                driver.find_element_by_xpath("//*[@id='fastatext']").click()
                time.sleep(5) # wait sequences to load            
            # At this point we may have encountered a couple of errors:          
            # a timeout (NCBI takes too long)
            # 'element not found' (NCBI is slow in responding and the bit we want to click isn't there yet)
            # we just add the file to be inspected & re-run. We then go on to the next file.
            except (TimeoutException, NoSuchElementException): 
                rerun.append(file)  # add to the list, will be re-run later
                driver.quit()
            else: # in case there is no error, we continue
                #let's make soup
                soup = BeautifulSoup(driver.page_source, "lxml") # turn page into soup
                driver.quit()                      # end web session (close tab)
                # The last step is writing the sequences to file
                out_file = open(file.split('.')[0] + '-seqs.txt', 'w')
                for seq in soup.find_all("pre"):
                    out_file.write(seq.text)
                out_file.close()
            pbar.update(1)   # advance progress bar by 1
    # we can now update the 'files' list for the next iteration of our run
    files = rerun
    # next we update i_max, unless we reached maxiter, then we set it at zero            
    if itercount <= maxiter:
        i_max = len(files) 
    else:
        i_max = 0
