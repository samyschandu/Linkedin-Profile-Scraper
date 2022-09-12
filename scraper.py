#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
from time import sleep
import requests

list_of_name = []
list_of_experience = []
list_of_about = []
list_of_address = []
list_of_job_title = []
list_of_description = []

profile_address = open('C:/Users/tejal/OneDrive/Desktop/LinkedIn_Scraper/profile_address.txt')
urls = profile_address.read().split('\n')
total_profile=len(urls)

credential = open('C:/Users/tejal/OneDrive/Desktop/LinkedIn_Scraper/credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
credential.close()
print('- Finish importing the login credentials')
sleep(2)

s = Service('C:/Users/tejal/OneDrive/Desktop/LinkedIn_Scraper/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://www.linkedin.com')
sleep(3)
driver.find_element(By.ID, 'session_key').send_keys(username)
driver.find_element(By.ID, 'session_password').send_keys(password)
sleep(2)
log_in_button = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button")
sleep(1)
log_in_button.click()
sleep(10)

for profile_link in urls:
    print('------------------')
    driver.get(profile_link)
    sleep(10)

#NAME
    name = driver.find_element(By.XPATH, "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']")
    list_of_name.append(name.text)
    sleep(5)
    
# TITLE
    title = driver.find_element(By.XPATH, "//div[@class='text-body-medium break-words']")
    list_of_job_title.append(title.text)
    
# ADDRESS
    address = driver.find_elements(By.XPATH, "//span[@class='text-body-small inline t-black--light break-words']")
    location=[]
    for j in address:
        location.append(j.text)
        list_of_address.append(location)
    

#-----------------------------------BeautifulSoup--------------------------
    src = driver.page_source
    doc = BeautifulSoup(src, 'html.parser')
    div = doc.find_all('section', class_='artdeco-card ember-view relative break-words pb3 mt2')

# ABOUT
    about_section_present= False
    for section in div:
        about_section = section.find_all('div', {'id': 'about'})
        if len(about_section) != 0:
            about_section_present=True
            about_text= section.find_all('span', {'class': 'visually-hidden'})
            about_each=[]
            for bio in about_text:
                about_each.append(bio.text)
            list_of_about.append(about_each)
            break;
    if about_section_present == False: 
        about_each=[]
        list_of_about.append(about_each)
    


#EXPERIENCE
    for section in div:
        exp_section = section.find_all('div', {'id': 'experience'})
        if len(exp_section) != 0:
            exp_list=section.find_all('li', {'class': 'artdeco-list__item'})
            experience_per_person=[]
            for each_exp in exp_list:
                text_line_list= each_exp.find_all('span', {'class': 'visually-hidden'})
                partition_list=[]
                for text_line in text_line_list:
                    partition_list.append(text_line.text)
                experience_per_person.append(partition_list)
            list_of_experience.append(experience_per_person)
            break;
    
print(list_of_name)
print(list_of_job_title) 
print(list_of_address)
print(list_of_about)
print(list_of_experience)
sleep(5)
driver.quit()


# In[9]:


Column_Names=['LinkedIn Profile', 'Name', 'Title', 'Location', 'About', 'Job 1', 'Job 2', 'Job 3', 'Job 4', 'Job 5']
f = open('C:/Users/tejal/OneDrive/Desktop/LinkedIn_Scraper/linkedin_data_v1.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(Column_Names)
for count in range(total_profile):
    Profile_Row =[]
    Profile_Row.append(urls[count])
    Profile_Row.append(list_of_name[count])
    Profile_Row.append(list_of_job_title[count])
    Profile_Row.append(list_of_address[count][0])
    if(len(list_of_about[count])==2):
        Profile_Row.append(list_of_about[count][1])
    else:
        Profile_Row.append("")
    for jobcount in range(len(list_of_experience[count])):
        Profile_Row.append("\n".join(list_of_experience[count][jobcount]))
    writer.writerow(Profile_Row)
f.close()


# In[ ]:




