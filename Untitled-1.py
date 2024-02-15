#!/usr/bin/env python
# coding: utf-8

# In[51]:


#대전시 내 인구수 대비 소아과 수를 측정하기 위해 대전시 인구 데이터와 소아과 수 데이터를 비교 분석합니다.

import streamlit as st
import pandas as pd
from functools import reduce



pd.set_option('display.max_rows', None)
pd.set_option('display.max_column', None)



# In[52]:


#대전시 자치구 연령별 인구수를 확인합니다. 데이터는 각 자치구에서 가져왔습니다.
population_yuseong = pd.read_csv("2021_yuseong.csv", thousands=',')
population_seo = pd.read_csv("2021_seo.csv", thousands=',')
population_daedeok = pd.read_csv("2021_daedok.csv", thousands=',')
population_jung = pd.read_csv("2021_jung.csv", thousands=',')
population_dong = pd.read_csv("2021_dong.csv", thousands=',')

#데이터 내 남자와 여자를 분리했지만, 본 데이터 분석에서 필요하지 않기 때문에 총 인원 수로 확인합니다.
population_yuseong = population_yuseong[population_yuseong['항목'] == '계']
population_seo = population_seo[population_seo['항목'] == '계']
population_daedeok = population_daedeok[population_daedeok['항목'] == '계']
population_jung = population_jung[population_jung['항목'] == '계']
population_dong = population_dong[population_dong['항목'] == '계']

#나이의 컬럼 데이터가 없어 기입합니다.
population_yuseong = population_yuseong.rename(columns={'Unnamed: 0' : 'age'})
population_seo = population_seo.rename(columns={'Unnamed: 0' : 'age'})
population_daedeok = population_daedeok.rename(columns={'Unnamed: 0' : 'age'})
population_jung = population_jung.rename(columns={'Unnamed: 0' : 'age'})
population_dong = population_dong.rename(columns={'Unnamed: 0' : 'age'})

#불필요한 컬럼 데이터 '항목'을 제거합니다.
population_yuseong = population_yuseong.drop(columns=['항목'])
population_seo = population_seo.drop(columns=['항목'])
population_daedeok = population_daedeok.drop(columns=['항목'])
population_jung = population_jung.drop(columns=['항목'])
population_dong = population_dong.drop(columns=['항목'])



# 

# In[53]:


#데이터를 하나로 만듭니다.
populations = [population_yuseong, population_seo, population_dong, population_jung, population_daedeok]

population = reduce(lambda left, right: pd.merge(left, right, on = 'age', how='inner'), populations)

st.title("2021년도 대전 광역시 자치구 및 연령별 인구 통계입니다.")

#나이를 데이터의 index로 합니다. 
population = population.set_index('age')
population


# In[54]:


population_summary = population[['유성구', '서구', '동구', '중구', '대덕구']]
                                 
population_summary_nonAdult = population_summary.loc['0세' : '18세']
population_summary_nonAdult_total = population_summary_nonAdult.sum()


# In[55]:


#대전 지역 내 소아과 수를 확인합니다. HIRA 빅데이터 개방포털에서 데이터를 가져왔습니다 

hospital_info_row = pd.read_csv("2021_hos_info.csv") #병원정보서비스
hospital_info_category = pd.read_csv("2021_hos_info_category.csv") #진료과목정보

hospital_info = pd.merge(hospital_info_row, hospital_info_category, on = '암호화요양기호', how='inner')
hospital_info = hospital_info.drop(columns=['암호화요양기호'])

daejon_hospital_info = hospital_info[hospital_info['시도코드명'] == '대전']

#소아과
daejon_hospital_info_pediatrics = daejon_hospital_info[daejon_hospital_info['진료과목코드'] == 11]


#의원   |   종별코드 31 == 의원
daejon_hospital_info_pediatrics_31 = daejon_hospital_info_pediatrics[daejon_hospital_info_pediatrics['종별코드'] == 31 ]
daejon_hospital_info_pediatrics_31.reset_index(drop = True, inplace = True)


#중복 등록 제거     |   의원 중 중복으로 등록한 문제가 있음
daejon_hospital_info_pediatrics_31 = daejon_hospital_info_pediatrics_31[daejon_hospital_info_pediatrics_31['과목별 전문의수'] > 0]
daejon_hospital_info_pediatrics_31.reset_index(drop=True, inplace = True)

print('대전시 내    의원    소아과 갯수: ',daejon_hospital_info_pediatrics_31.shape[0]) #대전시 내 의원의 갯수는 69개 입니다.

daejon_hospital_info_pediatrics_31_yuseong = daejon_hospital_info_pediatrics_31[daejon_hospital_info_pediatrics_31['시군구코드명'] == '대전유성구']
daejon_hospital_info_pediatrics_31_seo = daejon_hospital_info_pediatrics_31[daejon_hospital_info_pediatrics_31['시군구코드명'] == '대전서구']
daejon_hospital_info_pediatrics_31_daedeok = daejon_hospital_info_pediatrics_31[daejon_hospital_info_pediatrics_31['시군구코드명'] == '대전대덕구']
daejon_hospital_info_pediatrics_31_jung = daejon_hospital_info_pediatrics_31[daejon_hospital_info_pediatrics_31['시군구코드명'] == '대전중구']
daejon_hospital_info_pediatrics_31_dong = daejon_hospital_info_pediatrics_31[daejon_hospital_info_pediatrics_31['시군구코드명'] == '대전동구']

daejon_hospital_info_pediatrics_31_seo.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_31_yuseong.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_31_daedeok.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_31_jung.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_31_dong.reset_index(drop = True, inplace = True)

seo_31 = daejon_hospital_info_pediatrics_31_seo.shape[0]
yuseong_31 = daejon_hospital_info_pediatrics_31_yuseong.shape[0]
daedeok_31 = daejon_hospital_info_pediatrics_31_daedeok.shape[0]
d_jung_31 = daejon_hospital_info_pediatrics_31_jung.shape[0]
dong_31 = daejon_hospital_info_pediatrics_31_dong.shape[0]

daejon_hospital_info_pediatrics_31_total = pd.DataFrame({'지역' : ['서구', '유성구', '대덕구', '중구', '동구'],
                                                         '의원 수' : [seo_31, yuseong_31, daedeok_31, d_jung_31, dong_31]})
#병원 포함
daejon_hospital_info_pediatrics_ALL = daejon_hospital_info_pediatrics[daejon_hospital_info_pediatrics['과목별 전문의수'] > 0]
print("------------------\n\n")
print("대전시 내    병원 + 의원     소아과 수: ", daejon_hospital_info_pediatrics_ALL.shape[0]) # 대전시 내 총 소아과 수는 92개 입니다.

daejon_hospital_info_pediatrics_ALL_yuseong = daejon_hospital_info_pediatrics_ALL[daejon_hospital_info_pediatrics_ALL['시군구코드명'] == '대전유성구']
daejon_hospital_info_pediatrics_ALL_seo = daejon_hospital_info_pediatrics_ALL[daejon_hospital_info_pediatrics_ALL['시군구코드명'] == '대전서구']
daejon_hospital_info_pediatrics_ALL_daedeok = daejon_hospital_info_pediatrics_ALL[daejon_hospital_info_pediatrics_ALL['시군구코드명'] == '대전대덕구']
daejon_hospital_info_pediatrics_ALL_jung = daejon_hospital_info_pediatrics_ALL[daejon_hospital_info_pediatrics_ALL['시군구코드명'] == '대전중구']
daejon_hospital_info_pediatrics_ALL_dong = daejon_hospital_info_pediatrics_ALL[daejon_hospital_info_pediatrics_ALL['시군구코드명'] == '대전동구']

daejon_hospital_info_pediatrics_ALL_yuseong.reset_index(drop  = True, inplace = True)
daejon_hospital_info_pediatrics_ALL_seo.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_ALL_daedeok.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_ALL_jung.reset_index(drop = True, inplace = True)
daejon_hospital_info_pediatrics_ALL_dong.reset_index(drop = True, inplace = True)

seo_all = daejon_hospital_info_pediatrics_ALL_seo.shape[0]     
yuseong_all = daejon_hospital_info_pediatrics_ALL_yuseong.shape[0]  
daedeok_all = daejon_hospital_info_pediatrics_ALL_daedeok.shape[0]  
jung_all = daejon_hospital_info_pediatrics_ALL_jung.shape[0]     
dong_all = daejon_hospital_info_pediatrics_ALL_dong.shape[0]

daejon_hospital_info_pediatrics_all_total = pd.DataFrame({'지역' : ['서구', '유성구', '대덕구', '중구', '동구'],
                                                         '의원 + 이원수' : [seo_all, yuseong_all, daedeok_all, jung_all, dong_all]})

st.title("2021년도 대전 광역시 내 의원 소아청소년과 통계입니다.")
daejon_hospital_info_pediatrics_31


# In[56]:


# 대전 내 행정구역 별 18세 미만 나이와 소아과 수 비교

under_18 = population_summary_nonAdult_total

daejon_data_under18_pediatrics = pd.DataFrame({'지역' : ['서구', '유성구', '대덕구', '중구', '동구'],
                                           '18세 이하 인구 수' : [under_18['서구'], under_18['유성구'], under_18['대덕구'], under_18['중구'], under_18['동구']],
                                           '의원 소아과 수' : [seo_31, yuseong_31, daedeok_31, d_jung_31, dong_31],
                                           '의원 + 병원 소아과 수' : [seo_all, yuseong_all, daedeok_all, jung_all, dong_all]
                                           })
print(daejon_data_under18_pediatrics)
daejon_data_under18_pediatrics.loc[5] = ['소계', daejon_data_under18_pediatrics['18세 이하 인구 수'].sum(), daejon_data_under18_pediatrics['의원 소아과 수'].sum(), daejon_data_under18_pediatrics['의원 + 병원 소아과 수'].sum()]
daejon_data_under18_pediatrics = daejon_data_under18_pediatrics.set_index('지역')

daejon_data_under18_pediatrics['인구 수 대비 의원 소아과 수'] = daejon_data_under18_pediatrics['의원 소아과 수'] / daejon_data_under18_pediatrics['18세 이하 인구 수'] * 100
daejon_data_under18_pediatrics['인구 수 대비 의원 + 병원 소아과 수'] = daejon_data_under18_pediatrics['의원 + 병원 소아과 수'] / daejon_data_under18_pediatrics['18세 이하 인구 수'] * 100

st.title("2021년도 대전 광역시 내 소아청소년과 비율 통계입니다.")
daejon_data_under18_pediatrics


# In[65]:


# 서울시 소아과수를 확인합니다.
seoul_hospital_info = hospital_info[hospital_info['시도코드명'] == '서울']

# 소아과 진료과목코드 == 11
seoul_hospital_info_pediatrics = seoul_hospital_info[seoul_hospital_info['진료과목코드'] == 11]

# 의원 종별코드 : 31
seoul_hospital_info_pediatrics_31 = seoul_hospital_info_pediatrics[seoul_hospital_info_pediatrics['종별코드'] == 31]
seoul_hospital_info_pediatrics_31.reset_index(drop = True, inplace = True)

# 중복 등록 의원 제거
seoul_hospital_info_pediatrics_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['과목별 전문의수'] > 0]
seoul_hospital_info_pediatrics_31.reset_index(drop = True, inplace = True)

# 의원 + 병원
seoul_hospital_info_pediatrics_all = seoul_hospital_info_pediatrics[seoul_hospital_info_pediatrics['과목별 전문의수'] > 0]

# 자치구 별 비교
jongro_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '종로구']
jongro_31.reset_index(drop = True, inplace = True)

jongro_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '종로구']
jongro_all.reset_index(drop = True, inplace = True)

jung_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '중구']
jung_31.reset_index(drop = True, inplace = True)

jung_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '중구']
jung_all.reset_index(drop = True, inplace = True)

yongsan_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '용산구']
yongsan_31.reset_index(drop = True, inplace = True)

yongsan_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '용산구']
yongsan_all.reset_index(drop = True, inplace = True)

seongdong_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '서대문구']
seongdong_31.reset_index(drop = True, inplace = True)

seongdong_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '서대문구']
seongdong_all.reset_index(drop = True, inplace = True)

gwangjin_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '광진구']
gwangjin_31.reset_index(drop = True, inplace = True)

gwangjin_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '광진구']
gwangjin_all.reset_index(drop = True, inplace = True)

dongdaemoon_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '동대문구']
dongdaemoon_31.reset_index(drop = True, inplace = True)

dongdaemoon_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '동대문구']
dongdaemoon_all.reset_index(drop = True, inplace = True)

jungrang_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '중랑구']
jungrang_31.reset_index(drop = True, inplace = True)

jungrang_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '중랑구']
jungrang_all.reset_index(drop = True, inplace = True)

seongbook_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '성북구']
seongbook_31.reset_index(drop = True, inplace = True)

seongbook_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '성북구']
seongdong_all.reset_index(drop = True, inplace = True)

gangbook_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '강북구']
gangbook_31.reset_index(drop = True, inplace = True)

gangbook_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '강북구']
gangbook_all.reset_index(drop = True, inplace = True)

dobong_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '도봉구']
dobong_31.reset_index(drop = True, inplace = True)

dobong_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '도봉구']
dobong_all.reset_index(drop = True, inplace = True)

nowan_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '노원구']
nowan_31.reset_index(drop = True, inplace = True)

nowan_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '노원구']
nowan_all.reset_index(drop = True, inplace = True)

eunpyong_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '은평구']
eunpyong_31.reset_index(drop = True, inplace = True)

eunpyong_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '은평구']
eunpyong_all.reset_index(drop = True, inplace = True)

seodamoon_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '서대문구']
seodamoon_31.reset_index(drop = True, inplace = True)

seodamoon_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '서대문구']
seodamoon_all.reset_index(drop = True, inplace = True)

mapoe_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '마포구']
mapoe_31.reset_index(drop = True, inplace = True)

mapoe_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '마포구']
mapoe_all.reset_index(drop = True, inplace = True)

yangcheon_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '양천구']
yangcheon_31.reset_index(drop = True, inplace = True)

yangcheon_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '양천구']
yangcheon_all.reset_index(drop = True, inplace = True)

gangseo_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '강서구']
gangseo_31.reset_index(drop = True, inplace = True)

gangseo_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '강서구']
gangseo_all.reset_index(drop = True, inplace = True)

gooro_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '구로구']
gooro_31.reset_index(drop = True, inplace = True)

gooro_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '구로구']
gooro_all.reset_index(drop = True, inplace = True)

geumcheon_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '금천구']
geumcheon_31.reset_index(drop = True, inplace = True)

geumcheon_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '금천구']
geumcheon_all.reset_index(drop = True, inplace = True)

yeongdeungpo_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '영등포구']
yeongdeungpo_31.reset_index(drop = True, inplace = True)

yeongdeungpo_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '영등포구']
yeongdeungpo_all.reset_index(drop = True, inplace = True)

dongjak_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '동작구']
dongjak_31.reset_index(drop = True, inplace = True)

dongjak_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '동작구']
dongjak_all.reset_index(drop = True, inplace = True)

gwanwak_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '관악구']
gwangjin_31.reset_index(drop = True, inplace = True)

gwanwak_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '관악구']
gwanwak_all.reset_index(drop = True, inplace = True)

seocho_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '서초구']
seocho_31.reset_index(drop = True, inplace = True)

seocho_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '서초구']
seocho_all.reset_index(drop = True, inplace = True)

gangnam_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '강남구']
gangnam_31.reset_index(drop = True, inplace = True)

gangnam_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '강남구']
gangnam_all.reset_index(drop = True, inplace = True)

seongpa_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '송파구']
seongpa_31.reset_index(drop = True, inplace = True)

seongpa_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '송파구']
seongpa_all.reset_index(drop = True, inplace = True)

gangdong_31 = seoul_hospital_info_pediatrics_31[seoul_hospital_info_pediatrics_31['시군구코드명'] == '강동구']
gangdong_31.reset_index(drop = True, inplace = True)

gangdong_all = seoul_hospital_info_pediatrics_all[seoul_hospital_info_pediatrics_all['시군구코드명'] == '강동구']
gangdong_all.reset_index(drop = True, inplace = True)

print('서울 소아과 :', seoul_hospital_info_pediatrics_31.shape[0] - 1)
#  의원 + 병원
seoul_hospital_info_pediatrics_all = seoul_hospital_info_pediatrics[seoul_hospital_info_pediatrics['과목별 전문의수'] > 0]

print('서울 병원 + 소아과: ', seoul_hospital_info_pediatrics_all.shape[0] - 1)

print("----")

seoul_district = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구',
'관악구', '서초구', '강남구', '송파구', '강동구']

seoul_hospital_info_pediatrics_num = pd.DataFrame({'시군구코드명' : seoul_district,
                                                   '의원 소아과 수' : [jongro_31.shape[0], jung_31.shape[0], yongsan_31.shape[0], seongdong_31.shape[0], gwangjin_31.shape[0], dongdaemoon_31.shape[0], 
                                                              jungrang_31.shape[0], seongbook_31.shape[0], gangbook_31.shape[0], dobong_31.shape[0], nowan_31.shape[0], eunpyong_31.shape[0], 
                                                              seodamoon_31.shape[0], mapoe_31.shape[0], yangcheon_31.shape[0], gangseo_31.shape[0], gooro_31.shape[0], geumcheon_31.shape[0], 
                                                              yeongdeungpo_31.shape[0], dongjak_31.shape[0], gwanwak_31.shape[0], seocho_31.shape[0], gangnam_31.shape[0], seongpa_31.shape[0], 
                                                              gangdong_31.shape[0]],
                                                    '의원 + 병원 소아과 수' : [jongro_all.shape[0], jung_all.shape[0], yongsan_all.shape[0], seongdong_all.shape[0], gwangjin_all.shape[0], dongdaemoon_all.shape[0], 
                                                              jungrang_all.shape[0], seongbook_all.shape[0], gangbook_all.shape[0], dobong_all.shape[0], nowan_all.shape[0], eunpyong_all.shape[0], 
                                                              seodamoon_all.shape[0], mapoe_all.shape[0], yangcheon_all.shape[0], gangseo_all.shape[0], gooro_all.shape[0], geumcheon_all.shape[0], 
                                                              yeongdeungpo_all.shape[0], dongjak_all.shape[0], gwanwak_all.shape[0], seocho_all.shape[0], gangnam_all.shape[0], seongpa_all.shape[0], 
                                                              gangdong_all.shape[0]]
})

print(seoul_hospital_info_pediatrics_num)
seoul_hospital_info_pediatrics_num.loc[25] = ['소계', seoul_hospital_info_pediatrics_num['의원 소아과 수'].sum(), seoul_hospital_info_pediatrics_num['의원 + 병원 소아과 수'].sum()]

st.subheader("2021년도 서울시 내 소아청소년과 통계입니다.")
seoul_hospital_info_pediatrics_num


# In[66]:


# 서울시 인구 연령별 통계 정보를 확인합니다.

seoul_population_pd = pd.read_csv("2021_seoul.csv")

seoul_population_pd = seoul_population_pd[seoul_population_pd['성별'] == '계']
seoul_population_pd.reset_index(drop = True, inplace = True)

seoul_population_under18_pd = seoul_population_pd.loc[ :, : '15~19세']
seoul_population_under18_pd = seoul_population_under18_pd.drop(columns=['성별', '소계'])
seoul_population_under18_pd = seoul_population_under18_pd.rename(columns={'자치구별' : '시군구코드명'})

seoul_population_under18_pd = pd.merge(seoul_population_under18_pd, seoul_hospital_info_pediatrics_num, on='시군구코드명', how='inner')

seoul_population_under18_pd

#seoul_population_under18_pd = seoul_population_under18_pd.loc.set_index('시군구코드명')
seoul_population_under18_pd['18세 이하 인구 수'] = seoul_population_under18_pd.loc[: , '0~4세' : '15~19세'].sum(axis = 1)

seoul_data_under18_pediatrics = seoul_population_under18_pd.loc[ : , '의원 소아과 수' : '18세 이하 인구 수']
seoul_data_under18_pediatrics['자치구'] = seoul_population_under18_pd['시군구코드명']

seoul_data_under18_pediatrics = seoul_data_under18_pediatrics.set_index('자치구')

seoul_data_under18_pediatrics = seoul_data_under18_pediatrics.reindex(columns=['18세 이하 인구 수', '의원 소아과 수', '의원 + 병원 소아과 수'])

st.title("2021년도 서울시 내 소아청소년과 비율 통계입니다.")
seoul_data_under18_pediatrics['인구 대비 의원 소아과 비율'] = seoul_data_under18_pediatrics['의원 소아과 수'] / seoul_data_under18_pediatrics['18세 이하 인구 수'] * 100
seoul_data_under18_pediatrics['인구 대비 의원 + 병원 소아과 비율'] = seoul_data_under18_pediatrics['의원 + 병원 소아과 수'] / seoul_data_under18_pediatrics['18세 이하 인구 수'] * 100
seoul_data_under18_pediatrics


# In[ ]:





# In[ ]:




