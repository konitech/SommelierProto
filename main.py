import streamlit as st
import pandas as pd
from foodDB import FoodDB
from recipe import Recipe
from dishTasteFlavorDB import DishTasteFlavorDB
from sommelier import Sommelier

# 日本酒データベース（仮）
sake =  pd.read_csv('./data/sake.tsv', sep='\t')

# 濃淡度とうま味を正規化
def minmax_norm(s):
    return (s - s.min()) / (s.max() - s.min())

sake['濃淡度'] = minmax_norm(sake['濃淡度'])
sake['うま味'] = minmax_norm(sake['うま味'])

# 料理の味と香りのデータベースを構築
fooddb = FoodDB()
dishDB = DishTasteFlavorDB(fooddb)

# ソムリエ
yui = Sommelier(dishDB)


st.title('🍶AIソムリエ 内部検証版🍱')

st.markdown("好きな料理の名前を入力すると、その料理に最適な日本酒銘柄をコメントともに**AIソムリエ**が提案してくれます")
st.warning("これはAIソムリエの「ペアリングの確からしさ」を検証するための内部検証版です。そのため素っ気ない見た目になっていることをご了承ください🙇‍♀️")

choice_drink = st.radio('あなたが普段よく飲むお酒は？',['ビール','サワー','ワイン','日本酒'])

dish_name = st.text_input('料理名を入力してください')

condiment_name = st.selectbox('かける調味料を選択してください',
                        ['なし','醤油','塩','コショウ','ウスターソース','マヨネーズ','ケチャップ','タルタルソース','唐辛子','ポン酢','マスタード','味噌'])

start = st.button('ペアリング')

if start:
    if dish_name == None:
        st.error('料理名を入力してください')
    else:
        if condiment_name == 'なし':
            yui.kikizake(dish_name, None, sake, choice_drink)
        else:
            yui.kikizake(dish_name, condiment_name, sake, choice_drink)