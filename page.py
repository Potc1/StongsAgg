import streamlit as st
import pandas as pd
from utils.parser import startParse
from utils.trying import updateDB
from state import set_data




def show_stonks():
    from state import sharesData, bondsData
    # Отображение данных
    st.markdown("### Акции")
    st.dataframe(sharesData)

    st.markdown("### Облигации")
    st.dataframe(bondsData)


# Инициализация данных при первом запуске
if 'initialized' not in st.session_state:
    shares, bonds = startParse()
    set_data(shares, bonds)
    show_stonks()
    st.session_state['initialized'] = True

# Обновление БД по триггеру (вызывается один раз за сессию)
if 'updated' not in st.session_state or not st.session_state['updated']:
    success = updateDB()
    st.session_state['updated'] = success

if st.session_state['updated'] == True:
    st.markdown("**Готово**")

