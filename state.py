import pandas as pd

# Глобальное хранилище данных акций и облигаций
# Инициализируется пустыми DataFrame, заполняется при первом запуске
sharesData: pd.DataFrame = pd.DataFrame()
bondsData: pd.DataFrame = pd.DataFrame()


def set_data(shares: pd.DataFrame, bonds: pd.DataFrame):
    """Установить данные акций и облигаций в глобальное хранилище."""
    global sharesData, bondsData
    sharesData = shares
    bondsData = bonds


def get_data():
    """Получить текущие данные из глобального хранилища."""
    return sharesData, bondsData
