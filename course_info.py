import requests
import re
import json
import csv
from bs4 import BeautifulSoup

url = "http://catalog.gatech.edu/coursesaz/"
base_url = "http://catalog.gatech.edu"

def get_hrefs():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find('div', id="atozindex")
    links = courses.find_all('a', href=True)
    hrefs = [link['href'] for link in links]
    hrefs = [base_url + href for href in hrefs]
    return hrefs

def generate_course_data():
    hrefs = get_hrefs()
    # generate_json(hrefs)
    generate_csv(hrefs)

def generate_json(hrefs):
    courses_info = {}
    for department in hrefs:
        page = requests.get(department)
        soup = BeautifulSoup(page.content, 'html.parser')
        courses = soup.find_all(class_='courseblock')
        dept_info = []
        for course in courses:
            course_title = course.find(class_='courseblocktitle').text.strip()
            course_desc = course.find(class_='courseblockdesc').text 
            identifier = course_title.split('.')[0].strip()
            identifier = identifier.replace('\xa0', ' ')
            name = course_title.split('.')[1:-2]
            course_name = ""
            for n in name:
                course_name += n
            credits = course_title.split('.')[-2].split()[0]
            description = re.sub(r'[^a-zA-Z0-9\s\.\\/\$\+\*\(\)\?\{\}-]', "", course_desc).strip()
            description = description.replace("\'", r"\'")
            course_info = {"course": identifier, "name": course_name, "credits": credits, "description": description}
            dept_info.append(course_info)
        courses_info[department[36:-1].upper()] = dept_info
    json.dump(courses_info, open('course_data.json', 'w'))

def generate_csv(hrefs):
    course_info = []
    for department in hrefs:
        page = requests.get(department)
        soup = BeautifulSoup(page.content, 'html.parser')
        courses = soup.find_all(class_='courseblock')
        for course in courses:
            course_title = course.find(class_='courseblocktitle').text.strip()
            course_desc = course.find(class_='courseblockdesc').text 
            identifier = course_title.split('.')[0].strip()
            identifier = identifier.replace('\xa0', ' ')
            name = course_title.split('.')[1:-2]
            course_name = ""
            for n in name:
                course_name += n
            course_name = course_name.replace("\'", r"\'").strip()  # needed for sql
            course_name = course_name.replace(",", " ")    #remove , for sql bulk insert purposes
            credits = course_title.split('.')[-2].split()[0]
            credits = credits.replace(",", "-")    
            if not credits[0].isnumeric():
                print(f"We have something weird here course title is: {course_title}")
            description = re.sub(r'[^a-zA-Z0-9\s\.\\/\$\+\*\(\)\?\{\}-]', "", course_desc).strip()
            description = description.replace("\'", r"\'")
            description = description.replace(",", "")
            course_info.append([identifier, course_name, credits, description])
    with open('course_data.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(course_info)


generate_course_data()
    
