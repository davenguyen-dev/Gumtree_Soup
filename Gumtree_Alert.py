#!/usr/local/bin/python3

#Importing required libraries
# Importing required libraries for web scraping:
from urllib.request import urlopen 
from urllib.error import HTTPError 
from urllib.error import URLError 
from bs4 import BeautifulSoup 

# Importing miscellaneous libraries
import re #To allow RegEx wildcards
import smtplib, ssl #For sending automated email
from time import sleep #Sleep function

from timeout import timeout



# Site to be scraped        
site = "https://www.gumtree.com.au/s-electronics-computer/melbourne/c20045l3001317?price-type=free"

# Error handling for HTTP and URL errors

@timeout(15)  
def error_handling():
    try:
        try:
            html = urlopen(site)
        except HTTPError as e:
            print("The server returned an HTTP error")
        except URLError as e:
            print("The server could not be found!")
        
        # If no errors, then can proceed with main code:
        else: 
            bs = BeautifulSoup(html, "html.parser") 
            nameList = bs.findAll('p', {'class': 'user-ad-row-new-design__age'})
            myList=[]
            
            # Looping through posted ad times:
            for name in nameList:
                a = name.get_text()  #a is type str
                myList.append(a)  #append to empty list myList
            
            # Now to refine myList to a usable form:
            time = [] #empty time list for times less than x minutes
            
            # Looping through myList and appending empty time variable with only entries satisfying < x minutes
            for word in myList:
                if re.search('.minutes', word): 
                    time.append(int(word[0:2].strip()))
            print("List of times found: ", time)
            
            global value #global variable for final value
            value = -1 #initial value -1
            
            # Looping through time list and allocating value=1 if time < x minutes:
            threshold = 60 #enter threshold
            for i in range(len(time)):
                if time[i] < threshold:
                    print("Found a time less than", threshold, "mins: ", time[i])
                    print("Setting value = 1")
                    value = 1
                    break
            
            if len(time)==0:
                print("No times 'in minutes' exist!")
                print("Setting value = 2")
                value = 2 
            
            if value !=1 and value !=2:
                value = 0

            # Output of final value for checking purposes
            print("Final value for export = ", value)

    except TimeoutError:
        error_handling()
    except:
        body()


def email():
    port = 465  # For SSL
    password = " " #Enter password here (Create user input prompt if security is an issue)

    smtp_server = "smtp.gmail.com"
    sender_email = " "  # Enter your address
    receiver_email = " "  # Enter receiver address
    
    # Enter the plain text message to be sent:
    message = """\
    Subject: Gumtree update

    Check Gumtree for a new posted item

    https://www.gumtree.com.au/s-clayton-melbourne/page-1/l3001603r10?price-type=free


    """
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def body():
    print("Attempting to parse site...")
    error_handling()
    if value == 1:
        print("Recent entry found. Now sending email...")
        email()
        sleep1 = 300 #enter seconds to sleep for if entry found
        print("Email sent successfully. Reconnecting in", sleep1/60, "minutes...")
        sleep(sleep1)
        body()
    elif value == 0:
        print("Recent entry satifying threshold not found. Email not sent.")
        sleep2 = 300 #enter seconds to sleep for if entry *not* found
        print("Reconnecting in" , sleep2/60 , "minutes...")
        sleep(sleep2)
        body()
    elif value == 2:
        print("Recent entry satisfying threshold not found. Email not sent.")
        sleep3 = 300 #enter seconds to sleep for if entry *not* found
        print("Reconnecting in" , sleep3/60 , "minutes...")
        sleep(sleep3)
        body()
    else:
        print("Restarting app in 5 seconds...")
        sleep(5)
        body()


if __name__ == "__main__":
    body()












