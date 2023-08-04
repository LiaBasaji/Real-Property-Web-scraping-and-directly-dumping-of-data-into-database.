from bs4 import BeautifulSoup
import requests
import pandas as pd
import mysql.connector
# mydb=mysql.connector.connect(user="root",host="localhost",password="Mysql@123*",database="TMC")
# my_coursor=mydb.cursor()
data = []
for page in range (0,5):

    url = f"https://www.realproperty.pk/for-sale/homes/in-lahore-1/?page={page}/"
    a = requests.get(url)
    soup = BeautifulSoup(a.content, 'html.parser')
    property_list = soup.find('div', class_='tab-pane show active property-list')
    details = property_list.find_all('div', class_='single-property-box')
    for i in details:
        Title = i.find('div', class_="property-for-title inline").text
        location = i.find('div', class_="property-address inline").text
        Specification = i.find('p', class_='description text-truncate').text
        Area = i.find('li', id="area-unit").text.replace('\n', '')
        # bed_no = i.find('span', class_='number').text
        price = i.find('h4').text
        No_of_Baths = i.find('li').text.replace('\n', '')

        data_dict = {"location": location,
                     "Title": Title,
                     "Specification": Specification,
                     "Area": Area,
                     "No_of_Baths": No_of_Baths,
                     "price": price,
                    #  "No_of beds": bed_no
                     }
        data.append(data_dict)


        #print(location,Title,Specification,Area,No_of_Baths,price)

    df = pd.DataFrame(data)
    df.to_csv(r'C:/Users/liaqa/Documents/TMC/lahore_5pages15.csv', index=False)


    cursor=mydb.cursor()
    table_name="Lahore_property"
    for index,row in df.iterrows():
       sql= "insert into lahore_property (location,Title,Specification,Area,No_of_Baths,price) values(%s,%s,%s,%s,%s,%s)"
       val=(row['location'],row['Title'],row['Specification'],row['Area'],row['No_of_Baths'],row['price'])
       cursor.execute(sql, val)
    mydb.commit()


