from django.shortcuts import render
from bs4 import BeautifulSoup as bs
import requests

# Create your views here.
def fun(data):
    lst = []
    for text in data:
        counter = 0
        res = requests.get('https://collegedunia.com/e-search?query=' + text + '&c=all')

        soup = bs(res.text, 'lxml')

        a = soup.find('a', {"class": "ga-listing-snippet college_name"})
        # print(a['href'])

        res = requests.get(a['href'] + 'reviews')

        soup = bs(res.text, 'lxml')

        span = soup.find_all('span', {'class': 'rating_value'})
        lst1 = []
        for index, value in enumerate(span):
            lst1.append(float(value.text[1:4]))
        lst.append(lst1)

    return lst ,data


def indexView(request):
    x = None
    if request.GET.get('search'):
        x,data = fun(request.GET['search'].split(','))
    if x:
        for index,value in enumerate(x):
            value.append("%.1f"%(sum(value)/6))
            value.insert(0,data[index])



    return render(request,'main-file.html',{'values':x})