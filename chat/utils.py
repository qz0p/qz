import random
import requests

PASTEL_COLORS = [
    (0.2, 0.3, 0.9, 1),
    (0.2, 0.9, 0.2, 1),
    (0.9, 0.2, 0.2, 1),
    (0.9, 0.9, 0.2, 1),
    (0.2, 0.9, 0.9, 1)
]

def menu(today):
    url = "http://open.neis.go.kr/hub/mealServiceDietInfo"
    key = "e1e6f9bb23774cc2841e3ea20e47b495"
    params = {
        'KEY': key,
        'TYPE': 'json',
        'ATPT_OFCDC_SC_CODE': 'J10',
        'SD_SCHUL_CODE': '7530059',
        'MLSV_YMD': today
    }
    response = requests.get(url, params=params)
    contents = response.json()
    try:
        diet = contents['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        return diet.split('<br/>') if diet else ["없음"]
    except KeyError:
        return ["급식 정보를 가져올 수 없습니다."]

def findout(grade, cla, today):
    url = "http://open.neis.go.kr/hub/hisTimetable"
    key = "e1e6f9bb23774cc2841e3ea20e47b495"
    params = {
        'KEY': key,
        'TYPE': 'json',
        'pIndex': '1',
        'pSize': '100',
        'ATPT_OFCDC_SC_CODE': 'J10',
        'SD_SCHUL_CODE': '7530059',
        'ALL_TI_YMD': today,
        'GRADE': grade,
        'CLASS_NM': cla
    }
    response = requests.get(url, params=params)
    contents = response.json()
    try:
        timetable = []
        sche = contents['hisTimetable'][1]['row']
        for i in range(len(sche)):
            timetable.append({
                "time": sche[i]["PERIO"],
                "subject": sche[i]["ITRT_CNTNT"],
                "color": random.choice(PASTEL_COLORS)
            })
        return timetable
    except KeyError:
        return []

