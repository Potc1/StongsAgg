import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time 
import streamlit as st
import json
# Глобальный флаг обновления (можно установить в False для остановки)
update = True


print("Begins updating")

current_time = time.time()                                                                                                 
local_time = time.localtime(current_time)                                                                                  
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)                                                            
print(formatted_time)


def init_firebase():
    """Инициализировать Firebase приложение."""
    fb_credentials = st.secrets["firebase"]['my_project_settings']
    fb_credentials = dict(fb_credentials)
    cred = credentials.Certificate(fb_credentials)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://imoex2-default-rtdb.europe-west1.firebasedatabase.app/'
    })


def updateDB():
    """
    Обновить данные в Firebase.

    Returns:
        bool: True если обновление прошло успешно, False иначе.
    """
    from state import sharesData, bondsData
    print(f"Акции {sharesData.shape}")
    print(f"Облиги: {bondsData.shape}")
    init_firebase()
    ref = db.reference('/')

    # Определяем количество итераций как максимум из двух наборов данных
    length = max(bondsData.shape[0], sharesData.shape[0])
    counter = 0

    try:
        for i in range(length):
            counter += 1

            # Обновление акций
            if i < sharesData.shape[0] and update:
                shares_isin = sharesData.iloc[i]['ISIN']
                shares_ref = ref.child('Shares/' + shares_isin)

                if shares_ref.get() is not None:
                    shares_ref.update({
                        "HIGH": sharesData.iloc[i]['HIGH'],
                        "ISIN": shares_isin,
                        "LAST": sharesData.iloc[i]['LAST'],
                        "LOTSIZE": int(sharesData.iloc[i]['LOTSIZE']),
                        "LOW": sharesData.iloc[i]['LOW'],
                        "NAME": sharesData.iloc[i]['SECNAME'],
                        "OPEN": sharesData.iloc[i]['OPEN']
                    })
                else:
                    shares_ref.set({
                        "HIGH": sharesData.iloc[i]['HIGH'],
                        "ISIN": shares_isin,
                        "LAST": sharesData.iloc[i]['LAST'],
                        "LOTSIZE": int(sharesData.iloc[i]['LOTSIZE']),
                        "LOW": sharesData.iloc[i]['LOW'],
                        "NAME": sharesData.iloc[i]['SECNAME'],
                        "OPEN": sharesData.iloc[i]['OPEN']
                    })

            # Обновление облигаций
            if i < bondsData.shape[0] and update:
                bonds_isin = bondsData.iloc[i]['ISIN']
                bonds_ref = ref.child('Bonds/' + bonds_isin)

                if bonds_ref.get() is not None:
                    bonds_ref.update({
                        "HIGH": bondsData.iloc[i]['HIGH'],
                        "ISIN": bonds_isin,
                        "LAST": bondsData.iloc[i]['LAST'],
                        "LOTVALUE": int(bondsData.iloc[i]['FACEVALUE']),
                        "LOW": bondsData.iloc[i]['LOW'],
                        "NAME": bondsData.iloc[i]['SECNAME'],
                        "OPEN": bondsData.iloc[i]['OPEN'],
                        "YIELD": bondsData.iloc[i]['YIELD'],
                        "COUPONVALUE": bondsData.iloc[i]['COUPONVALUE']
                    })
                else:
                    bonds_ref.set({
                        "HIGH": bondsData.iloc[i]['HIGH'],
                        "ISIN": bondsData.iloc[i]['ISIN'],
                        "LAST": bondsData.iloc[i]['LAST'],
                        "LOTVALUE": int(bondsData.iloc[i]['FACEVALUE']),
                        "LOW": bondsData.iloc[i]['LOW'],
                        "NAME": bondsData.iloc[i]['SECNAME'],
                        "OPEN": bondsData.iloc[i]['OPEN'],
                        "YIELD": bondsData.iloc[i]['YIELD'],
                        "COUPONVALUE": bondsData.iloc[i]['COUPONVALUE']
                    })

    except Exception as e:
        print(f"Error occured while updating db: {e}\nОбновлено {counter} из {length}")
        print(f"Больше данных bonds_isin: {bonds_isin} shares_isin: {shares_isin}")
        print(f"Облигация: {bonds_isin}\n{bondsData.iloc[i]}")
        print(f"Акция: {shares_isin}\n{sharesData.iloc[i]}")  
        firebase_admin.delete_app(firebase_admin.get_app())
        return False

    firebase_admin.delete_app(firebase_admin.get_app())
    return True

current_time = time.time()                                                                                                 
local_time = time.localtime(current_time)                                                                                  
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)                                                            
print(formatted_time)
