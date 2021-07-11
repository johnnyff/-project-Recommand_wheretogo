# -*- coding: utf-8 -*-

import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import clear_output
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import folium
from folium import IFrame
import base64
import PIL.Image as pilimg

후보=pd.read_csv("추천후보.csv",encoding='utf-8',index_col=0)

class Survey(object):

    def __init__(self):
            
        self.a1=['으으 따분해,,뭐 특별한 일 없을까?', '너무 바쁜 요즘ㅜ_ㅜ 내 일상을 돌려줘!!', '거울 속에 내 모습은 텅 빈 것처럼 공허해,,', 'ㄴr는 ズl금 새벽 3んı 감성○l○F',
        '아..쉬고싶다..애옹이 만지고 싶다..8ㅅ8', '맛!있!는!거!맛!집!맛!집']
        self.q1 = widgets.Dropdown(options=self.a1,description='A.',disabled=False)

        self.a2=['인간관계 스트레스! 혼자 있고 싶어요.. ','미쳐 날뛰는중! 사랑하고 싶어요~~']
        self.q2 = widgets.Dropdown(options=self.a2,description='A. ',disabled=False)

        self.a3=['온몸이 근질근질, 마구마구 움직이고 싶어!','난 늙고 지쳤어.. 진짜 "휴식"을 달라!']
        self.q3= widgets.Dropdown(options=self.a3,description='A. ',disabled=False)

        self.a4=[ '맛있는 음식이 아니면 의미없어!','그까이꺼 대충 ~ 가까운데서 먹자']
        self.q4= widgets.Dropdown(options=self.a4,description='A. ',disabled=False)

        self.a5=['다채로운 뉴욕','맑고 푸른 제주도','축제의 나라 브라질','따뜻한 파리의 밤', '한적하고 고요한 몰디브','디저트가 넘쳐나는 대만']
        self.q5= widgets.Dropdown(options=self.a5,description='A. ',disabled=False)

        self.a6=['매우매우 중요하지! 남는건 사진!','별로...? 추억은 사진말고 마음속에!']
        self.q6= widgets.Dropdown(options=self.a6,description='A. ',disabled=False)

        self.a7=['맛있는 음식','재미있는 활동',' 아늑한 숙소']
        self.q7= widgets.Dropdown(options=self.a7,description='A. ',disabled=False)

        self.a8=['친한 친구 몇명이서 오붓하게 보낼래','다모여! 다모여! 마셔~~']
        self.q8= widgets.Dropdown(options=self.a8,description='A. ',disabled=False)

        self.a9=['필요할때 언제든 맥주 한잔 함께할 절친을 소환하는 능력','배고플때 하루에 한번 음식 하나를 소환하는 능력']
        self.q9= widgets.Dropdown(options=self.a9,description='A. ',disabled=False)

        self.person = widgets.Button(description='당신은 어떤 여행가?')
        self.travel_recom = widgets.Button(description='당신의 추천 여행지는?')
        
    def per(self, sent, name):
        성격=sent.loc[name].idxmax()
        if 성격 == '일상':
            일상여행가=Image.open('/image/일상여행가.png')
            resized_image = 일상여행가.resize((500, 500))
            display(resized_image)
            #rotate_image = resized_image.transpose(Image.ROTATE_90)
            #display(rotate_image)
        elif 성격 == '힐링':
            힐링여행가=Image.open('/image/힐링여행가.png')
            resized_image = 힐링여행가.resize((500, 500))
            display(resized_image)
        elif 성격 == '에너지':
            에너지여행가=Image.open('/image/에너지여행가.png')
            resized_image = 에너지여행가.resize((500, 500))
            display(resized_image)
        elif 성격 == '분위기':
            분위기여행가=Image.open('/image/분위기여행가.png')
            resized_image = 분위기여행가.resize((500, 500))
            display(resized_image)
        elif 성격 == '배고픔':
            배고픔여행가=Image.open('/image/배고픔여행가.png')
            resized_image = 배고픔여행가.resize((500, 500))
            display(resized_image)
        else:
            외로움여행가=Image.open('/image/외로움여행가.png')
            resized_image = 외로움여행가.resize((500, 500))
            display(resized_image)
        
    def recom(self, sent):
        #sent=pd.DataFrame(data={'일상': [0.5], '힐링':[0.33], '분위기':[0.33], '에너지':[0], '배고픔':[0], '외로움':[0.333]},index=['name'])
        후보=pd.read_csv("추천후보.csv",encoding='utf-8',index_col=0)
        추천=pd.concat([후보, sent],axis=0,join='inner')
        dataset = 추천.values.tolist()
        name = 후보.index
        info = dict.fromkeys(name)
        loca = pd.read_excel("location2.xlsx")['좌표'].tolist()
        i = 0
        for s in info.keys():
            info[s]= loca[i].strip()
            i+=1

        cosine_dataset= cosine_similarity(dataset)
        cosine_dataset_df = pd.DataFrame(cosine_dataset)

        a = cosine_dataset_df[len(cosine_dataset)-1].sort_values(ascending = False)[1:]
        

        for i in range(3):
            print(추천.index[a.index[i]])
            self.getlocation(추천.index[a.index[i]],info[추천.index[a.index[i]]])

    def count_key1_5(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['에너지'] += 1
        else:
            if anwr==a[1]:
                sent['일상'] += 1
            else:
                if anwr==a[2]:
                    sent['외로움'] += 1
                else:
                    if anwr==a[3]:
                        sent['분위기'] +=1
                    else:
                        if anwr==a[4]:
                            sent['힐링']+=1
                        else:
                            if anwr==a[5]:
                                sent['배고픔']+=1
        return sent

    def count_key2(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['일상'] += 1; sent['힐링'] +=1; sent['에너지'] +=1
        else:
            if anwr==a[1]:
                sent['외로움'] += 1; sent['분위기'] +=1
        return sent

    def count_key3(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['에너지'] += 1; sent['외로움'] +=1
        else:
            if anwr==a[1]:
                sent['힐링'] += 1; sent['분위기'] +=1; sent['일상'] +=1
        return sent

    def count_key4(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['에너지'] += 1; sent['배고픔'] +=1
        else:
            if anwr==a[1]:
                sent['일상'] += 1
        return sent

    def count_key6(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['분위기'] += 1
        else:
            if anwr==a[1]:
                sent['일상'] += 1; sent['힐링'] +=1
        return sent

    def count_key7(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['배고픔'] += 1
        else:
            if anwr==a[1]:
                sent['에너지'] += 1
            else:
                if anwr==a[2]:
                    sent['힐링']+=1
        return sent

    def count_key8(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['분위기'] += 1
        else:
            if anwr==a[1]:
                sent['외로움'] += 1
        return sent

    def count_key9(self,q,a):
        anwr=q.value
        if anwr==a[0]:
            sent['외로움'] += 1
        else:
            if anwr==a[1]:
                sent['배고픔'] += 1
        return sent

    def count_total(self, sent):
        self.count_key1_5(self.q1,self.a1)
        self.count_key2(self.q2,self.a2)
        self.count_key3(self.q3,self.a3)
        self.count_key4(self.q4,self.a4)
        self.count_key1_5(self.q5,self.a5)
        self.count_key6(self.q6,self.a6)
        self.count_key7(self.q7,self.a7)
        self.count_key8(self.q8,self.a8)
        self.count_key9(self.q9,self.a9)
        sent['일상']=sent['일상']/6
        sent['힐링']=sent['힐링']/6
        sent['분위기']=sent['분위기']/6
        sent['에너지']=sent['에너지']/6
        sent['배고픔']=sent['배고픔']/6
        sent['외로움']=sent['외로움']/6
        return sent
    
    def getlocation(self,place, loc):
        f = folium.Figure(width=700, height=500)
        lo = loc.split(",")
        map = folium.Map(location=[lo[0], lo[1]],zoom_start=15)
        pic = base64.b64encode(open('picture/'+place+"_resized.jpg",'rb').read()).decode()
        image_tag = '<img src="data:image/jpeg;base64,{}",width=“1”,height=“1”>'.format(pic)
        iframe = folium.IFrame(image_tag, width=256, height=256)
        folium.Marker((lo[0], lo[1]),popup=folium.Popup(iframe,max_width=1000,max_height=1000)).add_to(map)
        
        f.add_child(map)
        display(f)

    def reset_sent(self, name):
        global sent
        sent=pd.DataFrame(data={'일상': [0], '힐링':[0], '분위기':[0], '에너지':[0], '배고픔':[0], '외로움':[0]},index=[name])
    
    def question(self):
        def on_bc(a):
            with output:
                clear_output()
                self.count_total(sent)
                self.per(sent, name)
        
        def on_button_click(b):
            with output2:
                clear_output()
                self.count_total(sent)
                self.recom(sent)
                self.reset_sent(name)
        
        global sent
        name=input("당신의 이름은? ")
        sent=pd.DataFrame(data={'일상': [0], '힐링':[0], '분위기':[0], '에너지':[0], '배고픔':[0], '외로움':[0]},index=[name])

        print ('Q1.지금 현재 당신의 기분은?')
        display(self.q1)

        print ('Q2.당신의 연애세포는?')
        display(self.q2)

        print ('Q3.신체 배터리 잔량은?')
        display(self.q3)

        print ('Q4.가고 싶었던 맛집이 문을 닫았을 때는?')
        display(self.q4)

        print ('Q5.당신이 떠나고 싶은 여행지는?')
        display(self.q5)

        print ('Q6.여행가서 인생샷은 나에게..?')
        display(self.q6)

        print ('Q7.여행 계획 짤 때 이건 절대 포기 못해!')
        display(self.q7)

        print ('Q8.곧 내 생일이 다가온다. 어떻게 보내지?')
        display(self.q8)

        print ('Q9.누군가가 당신에게 둘중 한가지 능력을 준다고 한다면?')
        display(self.q9)

        #display(recom(sent))

        person = widgets.Button(description='당신은 어떤 여행가?')
        
        travel_recom = widgets.Button(description='당신의 추천 여행지는?')

        output = widgets.Output()
        
        display(person,output)
        person.on_click(on_bc)
        
        output2 = widgets.Output()
        display(travel_recom,output2)
        travel_recom.on_click(on_button_click)
