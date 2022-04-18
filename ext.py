import requests
from db import AppDB
import math
import requests
import json
from PIL import Image
from PIL import ImageDraw

headers = {"X-Auth-Token": 'dhugpdtz'}


class Ext():
    def draw_intensity(self, a):
        print(a)
        width = 50 * 40
        height = 50 * 30
        with Image.open("static/images/map.png") as im:
            draw = ImageDraw.Draw(im)
            for i in range(len(a)):
                print(a[i])
                r = a[i][2] * math.sqrt(2)

                draw.ellipse((int((a[i][0] * 50 + 25) - r * math.sqrt(8)), int((a[i][1] * 50 + 25) - r * math.sqrt(8)),
                              int((a[i][0] * 50 + 25) + r * math.sqrt(8)), int((a[i][1] * 50 + 25) + r * math.sqrt(8))),
                             fill=(240, 0, 0, 0), outline=(0, 0, 0))
                # draw.ellipse((100, 100, a[i][2]*10, a[i][2]*10), fill=(240, 0, 0, 0), outline=(0, 0, 0))
                pass
        im.save("static/images/output.png", "PNG")

    def go(self, path, a):
        print(a)
        width = 50 * 40
        height = 50 * 30
        with Image.open("static/images/map.png") as im:
            draw = ImageDraw.Draw(im)
            for i in range(len(path)):
                draw.ellipse((path[i][0] * 50 - 10 + 25, path[i][1] * 50 - 10 + 25, path[i][0] * 50 + 10 + 25,
                              path[i][1] * 50 + 10 + 25),
                             fill=(0, 255, 255, 0), outline=(0, 0, 0))
                # draw.ellipse((100, 100, a[i][2]*10, a[i][2]*10), fill=(240, 0, 0, 0), outline=(0, 0, 0))
                pass
            for i in range(len(a)):
                print(a[i])
                r = a[i][2] * math.sqrt(2)

                draw.ellipse((int((a[i][0] * 50 + 25) - r * math.sqrt(8)), int((a[i][1] * 50 + 25) - r * math.sqrt(8)),
                              int((a[i][0] * 50 + 25) + r * math.sqrt(8)), int((a[i][1] * 50 + 25) + r * math.sqrt(8))),
                             fill=(240, 0, 0, 0), outline=(0, 0, 0))
                # draw.ellipse((100, 100, a[i][2]*10, a[i][2]*10), fill=(240, 0, 0, 0), outline=(0, 0, 0))
                pass

        im.save("static/images/output_road.png", "PNG")

    def get_centre(self, int1, int2, int3, x1, y1, x2, y2, x3, y3):
        ox, oy = 0, 0
        int0 = -1
        best = 100
        for xk in range(0, 4000, 100):
            for yk in range(0, 3000, 100):
                x = xk / 100
                y = yk / 100
                f = abs(int1 * ((x1 - x) ** 2 + (y1 - y) ** 2) - int2 * ((x2 - x) ** 2 + (y2 - y) ** 2)) + abs(
                    int1 * ((x1 - x) ** 2 + (y1 - y) ** 2) - int3 * ((x3 - x) ** 2 + (y3 - y) ** 2)) + abs(
                    int3 * ((x3 - x) ** 2 + (y3 - y) ** 2) - int2 * ((x2 - x) ** 2 + (y2 - y) ** 2))

                if (f < best):
                    best = f
                    ox, oy, int0 = x, y, (int1 * ((x1 - x) ** 2 + (y1 - y) ** 2))
        return ox, oy, int0

    def intens_tochka(self, x, y, ans):
        otv = -1
        for i in ans:
            ox, oy, int0 = i[0], i[1], i[2]
            if ((x - ox) ** 2 + (y - oy) ** 2) == 0:
                if otv < int0:
                    otv = int0
            else:
                if otv < (int0 / ((x - ox) ** 2 + (y - oy) ** 2)):
                    otv = (int0 / ((x - ox) ** 2 + (y - oy) ** 2))
        return otv

    def update(self):
        anom = {}
        with open('static/temp/data.json') as f:
            data = json.load(f)['message']
            # print(data)
            for i in data:
                for j in i['swans']:
                    anom[j['id']] = []

            for i in data:
                for j in i['swans']:
                    anom[j['id']].append([j['rate'], i['coords'][0], i['coords'][1]])
            ans = []
            for i in anom:
                # print(i, anom[i])
                x, y, intensity = Ext().get_centre(anom[i][0][0], anom[i][1][0], anom[i][2][0], anom[i][0][1],
                                                   anom[i][0][2],
                                                   anom[i][1][1], anom[i][1][2], anom[i][2][1], anom[i][2][2])
                ans.append([x, y, intensity])
            tochki = [[0] * 30 for i in range(40)]

            Ext().draw_intensity(ans)
            tochki = [[0] * 30 for i in range(40)]

            for x in range(40):
                for y in range(30):
                    tochki[x][y] = Ext().intens_tochka(x, y, ans)

    def build(self, s_x, s_y, e_x, e_y):
        anom = {}
        with open('static/temp/data.json') as f:
            data = json.load(f)['message']
            for i in data:
                for j in i['swans']:
                    anom[j['id']] = []

            for i in data:
                for j in i['swans']:
                    anom[j['id']].append([j['rate'], i['coords'][0], i['coords'][1]])
            ans = []
            for i in anom:
                # print(i, anom[i])
                x, y, intensity = Ext().get_centre(anom[i][0][0], anom[i][1][0], anom[i][2][0], anom[i][0][1],
                                                   anom[i][0][2],
                                                   anom[i][1][1], anom[i][1][2], anom[i][2][1], anom[i][2][2])
                ans.append([x, y, intensity])
            tochki = [[0] * 30 for i in range(40)]

            for x in range(40):
                for y in range(30):
                    tochki[x][y] = Ext().intens_tochka(x, y, ans)

            d = [[1000000] * 30 for i in range(40)]
            pred = [[(-1, -1)] * 30 for i in range(40)]

            s = [(s_x, s_y, 0)]
            d[s_x][s_y] = 0

            while len(s) != 0:
                i, j, dd = s[0]
                s.pop(0)
                if (i > 0 and d[i - 1][j] > dd + 1 and tochki[i - 1][j] <= 2):
                    d[i - 1][j] = dd + 1
                    pred[i - 1][j] = (i, j)
                    s.append((i - 1, j, dd + 1))

                if (i < 39 and d[i + 1][j] > dd + 1 and tochki[i + 1][j] <= 2):
                    d[i + 1][j] = dd + 1
                    pred[i + 1][j] = (i, j)
                    s.append((i + 1, j, dd + 1))

                if (j > 0 and d[i][j - 1] > dd + 1 and tochki[i][j - 1] <= 2):
                    d[i][j - 1] = dd + 1
                    pred[i][j - 1] = (i, j)
                    s.append((i, j - 1, dd + 1))

                if (j < 29 and d[i][j + 1] > dd + 1 and tochki[i][j + 1] <= 2):
                    d[i][j + 1] = dd + 1
                    pred[i][j + 1] = (i, j)
                    s.append((i, j + 1, dd + 1))
            dd = d[e_x][e_y]
            i = e_x
            j = e_y
            paths = []
            print(dd)

            while (i != -1):
                print(i, j)
                paths.append((i, j))
                i, j = pred[i][j]
            Ext().go(paths, ans)


    def AddData(self, add_data):
        with open('static/temp/data.json') as f:
            data = json.load(f)['message']

        res = []

        for i in data:
            res.append(i)
        res.append(add_data)
        nd = {'message': res}

        with open('static/temp/data.json', 'w', encoding='utf-8') as f:
            data = json.dump(nd, f, indent=4)

    def DeleteData(self, data_id):
        with open('static/temp/data.json') as f:
            data = json.load(f)['message']

        res = []

        for i in data:
            if i['id'] != int(data_id):
                res.append(i)

        nd = {'message': res}

        with open('static/temp/data.json', 'w', encoding='utf-8') as f:
            data = json.dump(nd, f, indent=4)

    def GetLastId(self):
        with open('static/temp/data.json') as f:
            data = json.load(f)['message']

        return data[-1]['id']+1

    def UpdateData(self):
        headers = {"X-Auth-Token": 'dhugpdtz'}

        data = requests.get('https://dt.miet.ru/ppo_it_final', headers=headers).json()

        with open('static/temp/data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
