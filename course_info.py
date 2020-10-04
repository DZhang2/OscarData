import requests
import re
import json
from bs4 import BeautifulSoup

base_url = "http://catalog.gatech.edu"
url = "http://catalog.gatech.edu/coursesaz/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
courses = soup.find('div', id="atozindex")
links = courses.find_all('a', href=True)
departments = [link.text for link in links]
hrefs = [link['href'] for link in links]
hrefs = [base_url + href for href in hrefs]

# departments = full department name + (abbreviated) in list format
# href = links to department page with course info

courses_info = {}
for department in hrefs:
    page = requests.get(department)
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find_all(class_='courseblock')
    dept_info = []
    for course in courses:
        course_title = course.find(class_='courseblocktitle').text
        course_desc = course.find(class_='courseblockdesc').text  
        identifier = course_title.split('.')[0].strip()
        identifier = identifier.replace('\xa0', ' ')
        credits = course_title.split('.')[2].strip().split()[0] if len(course_title.split('.')[2].strip()) > 0 else course_title.split('.')[3].strip()[0]
        description = re.sub(r'[^a-zA-Z0-9 \.\\/\$\+\*\(\)\?\{\}-]', "", course_desc).strip()
        course_info = {"course": identifier, "name": course_title.split('.')[1].strip(), "credits": credits, "description": description}
        dept_info.append(course_info)
    courses_info[department[36:-1].upper()] = dept_info

json.dump(courses_info, open('course_data.json', 'w'))
    
