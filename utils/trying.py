import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time 
import streamlit as st
# Глобальный флаг обновления (можно установить в False для остановки) 
update = True


print("Begins updating")

current_time = time.time()                                                                                                 
local_time = time.localtime(current_time)                                                                                  
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)                                                            
print(formatted_time)


def init_firebase():
    """Инициализировать Firebase приложение."""
    #fb_credentials = st.secrets["firebase"]['my_project_settings']
    fb_credentials = st.secrets["firebase"]['my_project_settings']
    fb_credentials = dict(fb_credentials)
    cred = credentials.Certificate(fb_credentials)
    try:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://imoex2-default-rtdb.europe-west1.firebasedatabase.app/'
        })
    except Exception as e:
        print(f"Ошибка во время инициализации БД {e}")

def kill_firebase():
    """
        Убивает приложение если оно есть

        Returns:
        True, если ПО есть и все ок
        False, если его не было 
    """
    try:
        app = firebase_admin.get_app()
        firebase_admin.delete_app(app=app)
        return True
    except ValueError as e:
        print(f"Ошибка во время удаления экземпляра приложения БД: {e}")
    return False

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
    func_shares_isin = ""
    func_bonds_isin = ""
    try:
        for i in range(length):
            counter += 1

            # Обновление акций
            if i < sharesData.shape[0] and update:
                shares_isin = sharesData.iloc[i]['ISIN']
                shares_ref = ref.child(f'Shares/{shares_isin}')
                func_shares_isin = shares_isin
                payload = {
                        "HIGH": sharesData.iloc[i]['HIGH'],
                        "ISIN": shares_isin,
                        "LAST": sharesData.iloc[i]['LAST'],
                        "LOTSIZE": int(sharesData.iloc[i]['LOTSIZE']),
                        "LOW": sharesData.iloc[i]['LOW'],
                        "NAME": sharesData.iloc[i]['SECNAME'],
                        "OPEN": sharesData.iloc[i]['OPEN']
                }
                payload = {
                        key: value
                        for key, value in payload.items()
                        if value is not None
                }
                if shares_ref.get() is not None:

                    shares_ref.update(payload)
                else:
                    shares_ref.set(payload)

            # Обновление облигаций
            if i < bondsData.shape[0] and update:
                bonds_isin = bondsData.iloc[i]['ISIN']
                bonds_ref = ref.child(f'Bonds/{bonds_isin}')
                func_bonds_isin = bonds_isin
                payload = {
                    "HIGH": bondsData.iloc[i]['HIGH'],
                    "ISIN": bonds_isin,
                    "LAST": bondsData.iloc[i]['LAST'],
                    "LOTVALUE": int(bondsData.iloc[i]['FACEVALUE']),
                    "LOW": bondsData.iloc[i]['LOW'],
                    "NAME": bondsData.iloc[i]['SECNAME'],
                    "OPEN": bondsData.iloc[i]['OPEN'],
                    "YIELD": bondsData.iloc[i]['YIELD'],
                    "COUPONVALUE": bondsData.iloc[i]['COUPONVALUE']
                }
                payload = {
                        key: value
                        for key, value in payload.items()
                        if value is not None
                }
                if bonds_ref.get() is not None:
                    bonds_ref.update(payload)
                else:
                    bonds_ref.set(payload)

    except Exception as e:
        print(f"Error occured while updating db: {e}\nОбновлено {counter} из {length}")
        print(f"Больше данных bonds_isin: {func_bonds_isin} shares_isin: {func_shares_isin}")
        print(f"Облигация: {func_bonds_isin}\n{bondsData.iloc[i]}")
        print(f"Акция: {func_shares_isin}\n{sharesData.iloc[i]}")  
        kill_firebase()
        return False

    kill_firebase()
    return True

current_time = time.time()                                                                                                 
local_time = time.localtime(current_time)                                                                                  
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)                                                            
print(formatted_time)
