from requests import get
from pandas import DataFrame
# from plyer import notification
# def process_init():
#     notification.notify(
#         title='Process Initiated',
#         message="Getting Data From Gmaps For You Please Wait...",
#         app_name='Gmap Vigilante',
#     )
# def process_finis(text):
#     notification.notify(
#         title='Process Finished',
#         message=f"Check Downloads For {text}.xlsx",
#         app_name='Gmap Vigilante',
#     )

def main(loc):
    url = "https://maps-data.p.rapidapi.com/searchmaps.php"
    querystring = {"query":f"{loc}"}
    headers = {
        "X-RapidAPI-Key": "912fd7ecd8msh6444ef1b2239c88p1b8993jsn343eee19f83c",
        "X-RapidAPI-Host": "maps-data.p.rapidapi.com"
    }
    response = get(url, headers=headers, params=querystring)
    data=response.json()


    full_list=[]
    for i in data['data']:
        try:
            status=i['state']
            if "Open" in status or "Closed" in status:
                Status="Functioning"
            else:
                Status="Not Sure"
        except (KeyError,TypeError):
            Status=""
        full_list.append([i['name'],",".join(i['types']),Status,i['review_count'],i['rating'],i['phone_number'],i['full_address'],f'=HYPERLINK("{i["place_link"]}", "Click here")'   ])
        
    df=DataFrame(full_list,columns=["NAME","TYPE","STATUS","RATING","REVIEW_COUNT","PHONE NO.","ADDRESS","LINKS"])
    df.to_excel(f"{loc}.xlsx", index=False)