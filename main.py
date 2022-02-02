from Functions import GetMessages, GetCourse, word_in_file
import csv
import time

#while True:
    #try:
urls = GetMessages()
print(urls)
for url in urls:
    print(url)
    if word_in_file('Courses.csv',url)==False:
        GetCourse(url)
        with open('Courses.csv', mode='a') as CoursesFile:
            CourseWrite = csv.writer(CoursesFile)
            CourseWrite.writerow([url])
    else:
        print('Already Exists In DB!')
    #except:
    #    print('Trying again')
    #    continue