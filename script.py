from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import urllib.request as u
import smtplib
import csv


# Scrape the main search results page
# Here we're getting the link to the details page
# for each search result
def scrape_listing_results(url):
	# Open the link to the page using URLLib2
	response = u.urlopen(url).read()
	# Make the page parse-able using BeautifulSoup
	soup = bs(response, "html.parser")
	# Find the link to the result's main page using BeautifulSoup
	results = soup.find_all('a', class_='result-title')

	# Create a new array with the links to detail pages
	# for each result on the search results page
	result_list = [listing['href'] for listing in results]
	return result_list

# For each link on the search results page,
# Open the details page and grab the email
def gather_listing_data(urlList):
	# Empty array that will hold the contact data
	# This essentially replaces the CSV
	contact = []
	for url in urlList:
		contactInfo = {}
		# Open the link to the page using URLLib2
		response = u.urlopen(url)

		# Make the page parse-able using BeautifulSoup
		soup = bs(response.read(), "html.parser")

		# Find the title and email on the listing page using BeautifulSoup
		listing_title = soup.find('span', id="titletextonly")

		# Create a new object using the data we got from BeauitfulSoup
		contactInfo['address'] = get_email(url)
		contactInfo['title'] = listing_title.contents[0]
		contactInfo['message'] = 'Hello I was wondering if the job was still avaible, if so my resume is attached below'
		contactInfo['message'].attach(MIMEText(file("./resume.pdf").read()))
		
		contact.append(contactInfo)
		print(contact)
	return contact

# Selenium stuff
def get_email(url):
	driver = webdriver.Chrome()
	driver.get(url)
	
	cta = driver.find_element_by_class_name('reply_button')
	cta.click()
	sleep(10)

	return driver.find_element_by_class_name('anonemail').text


# initial login
def initial_login():
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.connect('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('pythontest667@gmail.com', 'roxxy123')
	return server

# Take an entry (email address and message) and send it
def send_mail(entry, server):
	# server.sendmail('pythontest667@gmail.com', entry['address'], entry['message'])
	server.sendmail('pythontest667@gmail.com', 'pythontest667@gmail.com', entry['message'])
	print('message sent')

# Program is initialized here
def main():
	# Scrape
	primary_link = 'https://newyork.craigslist.org/search/jjj?query=barista&sort=rel'
	link_list = scrape_listing_results(primary_link)
	# print(link_list)
	details_list = gather_listing_data(link_list)
	# Log in once (rather than each time in send_mail)
	server = initial_login()

	# For each entry in the JSON file, send an email
	for entry in details_list:
		send_mail(entry, server)

# Run the program
main()