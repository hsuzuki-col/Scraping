import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


class Scraping:

    def roomList(self, *suumo_urls):
        #各ページから部屋の詳細のURLを取得
        for each_suumo_url in suumo_urls:
            request = rq.get(each_suumo_url)
            soup = bs(request.text, "html.parser")
            details = soup.find_all("div", class_="cassetteitem-item")
            room_info = []
            #部屋ごとの詳細タブ内
            for detail in details:
                url = detail.find("td", class_="ui-text--midium ui-text--bold")
                #部屋の詳細ページURL
                room_url = "https://suumo.jp/" + url.find("a").get("href")
                #家賃
                rent = detail.find("span", class_="cassetteitem_other-emphasis ui-text--bold").text
                #管理費・共益費
                mane_cost = detail.find("span", class_="cassetteitem_price cassetteitem_price--administration").text
                #敷金
                deposit = detail.find("span", class_="cassetteitem_price cassetteitem_price--deposit").text
                #礼金
                reward = detail.find("span", class_="cassetteitem_price cassetteitem_price--gratuity").text
                #詳細ページ内
                request = rq.get(room_url)
                soup = bs(request.text, "html.parser")
                for i in range(8):
                    title = soup.find_all("th", class_="property_view_table-title")[i].text
                    #所在地
                    if title == "所在地":
                        address = soup.find_all("td", class_="property_view_table-body")[i].text
                    #駅徒歩
                    if title == "駅徒歩":
                        dist_body = soup.find_all("td", class_="property_view_table-body")[i].text
                        dist_lists = soup.find_all("div", class_="property_view_table-read")
                        distance = "-"
                        for dist_list in dist_lists:
                            if "北千住" in dist_list.text:
                                distance = dist_list.text
                    #専有面積
                    if title == "専有面積":
                        area = soup.find_all("td", class_="property_view_table-body")[i].text
                    #階数
                    if title == "階":
                        floor = soup.find_all("td", class_="property_view_table-body")[i].text
                    #向き
                    elif title == "向き":
                        direction = soup.find_all("td", class_="property_view_table-body")[i].text
                room_info.append([rent, mane_cost, deposit, reward, address, distance, area, floor, direction])
                time.sleep(1)
        df = pd.DataFrame(room_info, columns=["家賃", "管理費・共益費", "敷金", "礼金", "所在地", "駅徒歩", "専有面積", "階数", "向き"])
        #csvファイルとして保存
        df.to_csv("/Users/hss_512/スクレイピング/room_detail/room_detail.csv", encoding="utf-8")
        #/Users/hss_512/Library/Mobile\ Documents/com~apple~CloudDocs/scrayping/room_detail/room_detail.csv
        print(room_info)



    def getUrl(self):
        #検索条件のURLからページ数を取得
        suumo_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=20&smk=r01&po1=25&po2=99&shkr1=03&shkr2=03&shkr3=03&shkr4=03&rn=0030&ek=003011310&ra=013&cb=6.5&ct=7.0&co=1&md=02&md=03&et=10&mb=0&mt=9999999&cn=9999999&tc=0400901&tc=0400301&tc=0400101&tc=0400801&tc=0400503&tc=0401301&fw2="
        request = rq.get(suumo_url)
        soup = bs(request.text, "html.parser")
        div = soup.find("div", class_="pagination pagination_set-nav")
        ol = div.find("ol", class_="pagination-parts")
        page_num = 0
        #aタグにページ数が記載されている。その中から最大値を取得
        for ahref in ol.find_all("a"):
            if page_num < int(ahref.text):
                page_num = int(ahref.text)

        #ページ数より各ページのURLを取得し、suumo_urlsに格納
        suumo_urls = []
        suumo_urls.append(suumo_url)
        for pg_num in range(page_num-1):
            each_url = suumo_url + "&page=" + str(pg_num+2)
            suumo_urls.append(each_url)
        self.roomList(*suumo_urls)


if __name__ == '__main__':
    kitasenju = Scraping()
    kitasenju.getUrl()
