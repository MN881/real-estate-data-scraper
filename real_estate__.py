import asyncio
import json
import os
import random as rd
from bs4 import BeautifulSoup
import nodriver as uc
import csv


os.system('cls')


async def main():
  browser = await uc.start(headless=False)
  with open('propsData.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Price','Living Area(sqft)','Total Area(sqft)','Total Area unit','Beds','Baths','Address','City','State','Zip Code','Latitude','Longitude','Home Type','Days on Zillow','Images link','Proprety link','Broker','PriceReduction','Status'])
    for x in ['MN','TX','WA']:
      for y in range(1,6):
        tab = await browser.get(f'https://www.zillow.com/{x.lower()}/{y}_p')
        element =await  tab.wait_for('script#__NEXT_DATA__', timeout=20)
        await tab.sleep(rd.randint(3,4))
        if not element:
          break
        try:
          await tab.select('script#__NEXT_DATA__', timeout=10)
          await tab.sleep(rd.randint(5,6))
        except Exception:
          print('Timed out waiting for __NEXT_DATA__ (likely a CAPTCHA/bot check).')

        print('Page title:', await tab.evaluate('document.title'))

        html_content = await tab.get_content()
        soup = BeautifulSoup(html_content, 'lxml')
        tag = soup.find('script', id='__NEXT_DATA__')
        try:
          if tag:
            json_data = tag.get_text()
            dict_data = json.loads(json_data)
            if y == 1 and x == 'MN':
              with open('readable.json', 'w', encoding='utf-8') as f:
                json.dump(dict_data, f, indent=2)
            print('Success! Saved clean JSON to readable.json')
          else:
            print('Tag NOT found! Saving page HTML to debug.html so you can see why.')
        except Exception as e:
          print('JSON is broke!')
          continue
        with open('debug.html', 'w', encoding='utf-8') as f:
          f.write(html_content)
        properties_list = dict_data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']
        print(len(properties_list))
      
        for i in properties_list:
            price = i.get('price') or 0
            unformatted_price = i.get('unformattedPrice') or 0
            insided_data = i.get('hdpData','N').get('homeInfo','N')
            living_area_sqft = insided_data.get('livingArea') or 0
            lot_area_value = insided_data.get('lotAreaValue') or 0
            lot_area_unit = insided_data.get('lotAreaUnit') or 'N/A'
            if lot_area_unit == 'acres':
              if lot_area_value and float(lot_area_value) > 0:
                lot_area_value = float(lot_area_value) *  43560
                lot_area_unit = 'sqft'
              else:
                lot_area_value = 0
            elif lot_area_unit == 'sqft':
              if lot_area_value and float(lot_area_value) > 0:
                lot_area_value = lot_area_value
              else:
                lot_area_value = 0
            if lot_area_value > 0:
              per_sqft_value = round(float(unformatted_price)/float(lot_area_value),2)
            else:
              print('Area value of property is zero(0)')
            beds = i.get('beds','N/A')
            baths = i.get('baths','N/A')
            address = i.get('address','N/A')
            city = i.get('addressCity','N/A')
            state = i.get('addressState','N/A')
            zip_address = insided_data.get('zipcode') or 000
            lat,lon = insided_data.get('latitude','N/A'),insided_data.get('longitude','N/A')
            home_type = insided_data.get('homeType','N/A')
            days_on_zillow = insided_data.get('daysOnZillow','N/A')
            carousel = i.get('carouselPhotosComposable','N/A')
            if carousel and carousel != 'N/A':
              base_url = carousel.get('baseUrl')
              limited_photos = carousel['photoData'][:3]
              images_link = [
        base_url.replace("{photoKey}", item["photoKey"]) for item in limited_photos
    ]
            product_link = i.get('detailUrl') or 'Not product link'     
            broker_name = i.get('brokerName') or 'Not found'
            price_reduction = insided_data.get('priceReduction') or 'No Reduction'
            status_text = i.get('statusText') or 'No mention Status'
            writer.writerow([price,living_area_sqft,lot_area_value,lot_area_unit,beds,baths,address,city,state,zip_address,lat,lon,home_type,days_on_zillow,images_link,product_link,broker_name,price_reduction,status_text])


  browser.stop()


if __name__ == '__main__':
  uc.loop().run_until_complete(main())
