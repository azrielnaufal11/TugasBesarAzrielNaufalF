"""
Aplikasi Streamlit untuk menggambarkan informasi seputar data produksi minyak mentah dari berbagai negara di seluruh dunia
Sumber data berasal dari file “produksi_minyak_mentah.csv”, dimana nama lengkap negaranya dapat dilihat pada file “kode_negara_lengkap.json”
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference

"""
#IMPORT 

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image
import json as j
import csv as c

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah dari Berbagai Negara di Dunia")
st.markdown("*Sumber data berasal dari file “produksi_minyak_mentah.csv” dan file “kode_negara_lengkap.json”")
############### title ###############)

############### sidebar ###############
image = Image.open('download.jpg')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)



## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
#Mengambil data dari csv dan json
raw = []
list_tahun = []
list_kodeNegara = []
list_namaNegara = []
read = c.reader(open("produksi_minyak_mentah.csv"))
for row in read:
    raw.append(row)
for any in raw:
    if any[1] not in list_tahun:
        list_tahun.append(any[1])
temp = []
for any in raw:
    temp.append(any[0])
for any in temp:
    if any not in list_kodeNegara:
        list_kodeNegara.append(any)
with open("kode_negara_lengkap.json") as any:
    kodeNegara = j.load(any)
for any in list_kodeNegara:
    for kode in kodeNegara:
        if kode["alpha-3"]==any:
            list_namaNegara.append(kode["name"])
del list_kodeNegara[0]
del list_tahun[0]

namaNegara = st.sidebar.selectbox("Pilih negara", list_namaNegara)
pilihanTahun = st.sidebar.selectbox("Pilih tahun", list_tahun)
n_tampil = st.sidebar.number_input("Jumlah baris dalam tabel peringkat produksi terbesar yang ditampilkan", min_value=1, max_value=None, value=3)
############### sidebar ###############

############### bottom column ###############
ordinat = []
absis = []
for any in raw:
    for kode in kodeNegara:
        if any[0]==kode["alpha-3"]:
            any.insert(0,kode["name"])
for any in raw:
    if any[0]==namaNegara:
        ordinat.append(float(any[3]))
        absis.append(any[2])
st.header("Produksi Minyak Mentah "+namaNegara+" dari Tahun 1971-2015")
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(list_tahun)]
fig, ax = plt.subplots()
ax.plot(absis, ordinat)
ax.grid()
fig.set_figwidth(50)
fig.set_figheight(20)
ax.set_xticklabels(absis, rotation=0, fontsize=20)
ax.set_yticklabels(ordinat, rotation=0, fontsize=20)
ax.set_xlabel("Tahun", fontsize=32)
ax.set_ylabel("Total Produksi", fontsize=32)
st.pyplot(fig)


############### bottom column ###############

############### upper left column ###############
raw2 = []
ordinat2 = []
absis2 = []
for any in raw:
    if any[2]==str(pilihanTahun):
        raw2.append((float(any[3]),any[0]))
raw2.sort(reverse=True)
for num in range(int(n_tampil)):
    ordinat2.append(raw2[num][0])
    absis2.append(raw2[num][1])

cmap_name = 'tab10'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:int(n_tampil)]
left_col.header(str(n_tampil)+" Negara dengan Produksi Terbesar pada Tahun "+str(pilihanTahun))
fig, ax = plt.subplots()
ax.bar(absis2, ordinat2, color=colors)
ax.set_xlabel("Produksi Minyak Mentah", fontsize=12)
left_col.pyplot(fig)


############### upper left column ###############

############### upper right column ###############
dict1 = dict()
raw3 = []
absis3 = []
ordinat3 = []
for name in list_namaNegara:
    for any in raw:
        sum = 0
        if any[0]==name:
            sum = sum+float(any[3])
            dict1[name] = sum

for name,integer in dict1.items():
    rev = integer,name
    raw3.append(rev)
raw3.sort(reverse=True)

for num in range(int(n_tampil)):
    absis3.append(raw3[num][1])
    ordinat3.append(raw3[num][0])

cmap_name = 'tab10'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:int(n_tampil)]
right_col.header(str(n_tampil)+" Negara dengan Produksi Terbesar Kumulatif dari Tahun 1971-2015")
fig, ax = plt.subplots()
ax.bar(absis3, ordinat3, color=colors)
ax.set_xlabel("Produksi Minyak Mentah", fontsize=12)
right_col.pyplot(fig)
############### upper right column ###############

############### lower column ###############
############### Tahun T  ###############
dict2 = dict()
namaNegara0 = []
kodeNegara0 = []
reg = []
subreg = []
raw4 = []
for any in raw:
    if any[2]==str(pilihanTahun) and float(any[3])!=0:
        raw4.append((float(any[3]),any[0]))
raw4.sort()

dict2[""] = ["Produksi terbesar","Produksi terkecil"]
dict2["Negara"] = [raw2[0][1],raw4[0][1]]
for kode in kodeNegara:
    if kode["name"]==raw2[0][1]:
        code1 = kode["alpha-3"]
        region1 = kode["region"]
        subregion1 = kode["sub-region"]
        produksi = raw2[0][3]
for kode in kodeNegara:
    for any in raw:
        code2 = str(kode["alpha-3"])
        region2 = kode["region"]
        subregion2 = kode["sub-region"]
        produksi2 = raw2[0][3]
dict2["Kode"]= [code1,code2]
dict2["Region"] = [region1,region2]
dict2["Sub-region"]=[subregion1,subregion2]
dict2["Produksi"]= [produksi,produksi2]

table1 = pd.DataFrame(dict2)

dict4 = dict()
for any in raw2:
    if any[0]==0:
        namaNegara0.append(any[1])
for name in namaNegara0:
    for kode in kodeNegara:
        if kode["name"]==name:
            kodeNegara0.append(kode["alpha-3"])
            reg.append(kode["region"])
            subreg.append(kode["sub-region"])
            
dict4["Negara"] = namaNegara0
dict4["Kode"] = kodeNegara0
dict4["Region"] = reg
dict4["Sub-region"] = subreg
table3 = pd.DataFrame(dict4)

with st.expander("Summary Tahun "+pilihanTahun):
    st.subheader("Tabel Summary Tahun "+str(pilihanTahun))
    st.table(table1)
    st.subheader("Tabel Negara dengan 0 Produksi Tahun "+str(pilihanTahun))
    st.write("Semua negara yang tidak memproduksi minyak mentah pada tahun "+pilihanTahun)
    st.table(table3)
############### Tahun T  ###############

############### Tahun Kumulatif ###############
dict3 = dict()
namaNegara0kum = []
kodeNegara0kum = []
reg2 = []
subreg2 = []
raw5 = []

for name,integer in dict1.items():
    if integer != 0:
        a = integer,name
        raw5.append(a)
raw5.sort()

dict3[""] = ["Produksi terbesar","Produksi terkecil"]
dict3["Negara"] = [str(raw3[0][1]),str(raw5[0][1])]
for kode in kodeNegara:
    if kode["name"]==raw3[0][1]:
        code1 = kode["alpha-3"]
        region1 = kode["region"]
        subregion1 = kode["sub-region"]
for kode in kodeNegara:
    if kode["name"]==raw5[0][1]:
        code2 = str(kode["alpha-3"])
        region2 = kode["region"]
        subregion2 = kode["sub-region"]
dict3["Kode"]= [code1,code2]
dict3["Region"] = [region1,region2]
dict3["Sub-region"]=[subregion1,subregion2]
table2 = pd.DataFrame(dict3)

dict5 = dict()
for any in raw3:
    if any[0]==0:
        namaNegara0kum.append(any[1])
for name in namaNegara0kum:
    for kode in kodeNegara:
        if kode["name"]==name:
            kodeNegara0kum.append(kode["alpha-3"])
            reg2.append(kode["region"])
            subreg2.append(kode["sub-region"])

dict5["Negara"] = namaNegara0kum
dict5["Kode"] = kodeNegara0kum
dict5["Region"] = reg2
dict5["Sub-region"] = subreg2
table4 = pd.DataFrame(dict5)
    
with st.expander("Summary Kumulatif"):
    st.subheader("Tabel Summary Kumulatif")
    st.table(table2)
    st.subheader("Tabel Negara dengan 0 Produksi Kumulatif dari Tahun 1971-2015")
    st.write("Semua negara yang tidak memproduksi minyak mentah untuk keseluruhan tahun")
    st.table(table4)
############### Tahun Kumulatif ###############
############### lower column ###############