

#%%
#function to remove http from the URL (anylead looks to give better result when http is removed from the link):
def remove_http(url):
    if url.find('https://') > -1:
        url = url[8:len(url)]
    if url.find('http://') > -1:
        url = url[7:len(url)]
    if url.find('www.') > -1:
        url = url[4:len(url)]        
    return url
    
#function to create list    
def enrich_domain(list_name, website_list):
    driver.get('https://app.anyleads.com/leads/enrich-domains-to-contacts')
    time.sleep(5)
    
    #type list name
    stemp = driver.find_element_by_css_selector("#domains__enrich__list__name")
    stemp.send_keys(list_name)
    
    #select field for list of website and clear it
    stemp = driver.find_element_by_css_selector("#domains__enrich")
    stemp.clear()
    
    #type all desired website
    for website in website_list:
        website = str(website)
        #remove http
        website = remove_http(website)
        stemp.send_keys(website)
        #add line breack
        stemp.send_keys(u'\ue008'u'\ue007')
    
    #send form
    stemp = driver.find_element_by_css_selector(".trigger__domains__to__enrich")
    stemp.click()
    time.sleep(2)
 
#function to hash wide domain list in list of 100 domain
def enrich_domain_sequence(list_name_patern, website_long_list):
    x = 0
    print("0")
    while(x < len(website_long_list)):
        list_name = list_name_patern + str(x)
        
        # hash website_long_list in sublist of 100 entry
        if  (len(website_long_list) - x) > 100:
            website_list = website_long_list[x:x+100]
            
        else:
            website_list = website_long_list[x:len(website_long_list)-1]
            
        #check if last batch is completed
        reload = True
        while(reload == True):
            time.sleep(20)
            try:
                #look for orange runing buton
                stemp = driver.find_element_by_css_selector(".button__v__orange")
                #wait 10 second
                time.sleep(10)
                #reload page
                driver.refresh()
            except:
                reload = False
        
        enrich_domain(list_name, website_list)
        x = x + 100
        
    
    
#%%
# example
# you need to prepare an excel file with a column "query" containing the domain you want to enrich
import pandas as pd       
out_path = "C:\\Users\\Fab\\Documents\\DB_sample.xlsx"
contact = pd.read_excel(out_path) 
stemp = contact["query"]
#this line it to remove potential duplicate and avoid to overload anylead
stemp = list(set(stemp))

# open the web browther
import time    
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://app.anyleads.com/login/en')
time.sleep(1)

#######
#STOP#
#######
#log in to your anylead account
#after login go to the enrich domain service
#in following line replace "mylist_name" by your desired list name & execute the line

enrich_domain_sequence("mylist_name", stemp)
