import streamlit as st
import pandas as pd
from foodDB import FoodDB
from recipe import Recipe
from dishTasteFlavorDB import DishTasteFlavorDB
from sommelier import Sommelier

# テストパラメータ
choice_drinks = ['日本酒','ビール','ワイン']

# 料理と調味料は「test_target.csv」から取得する

def all_evaluate(sommelier, sake):
    # 評価対象の取得
    df = pd.read_csv('./test/test_target.csv')
    df['料理のコメント'] = ''
    
    for choice_drink in choice_drinks:
        df[choice_drink] = ''

    for index, row in df.iterrows():
        print(index, row['料理'])
        for choice_drink in choice_drinks:
            dish_name = row['料理']
            condiment_name = str(row['調味料']) # 調味料が空の場合、型がfloatになってしまうため、強制的にstrに型変換する

            if len(condiment_name) == 0:
                preference_comment, dish_comment, sake_score = sommelier.kikizake(dish_name, None, sake, choice_drink)
            else:
                preference_comment, dish_comment, sake_score = sommelier.kikizake(dish_name, condiment_name, sake, choice_drink)

            if preference_comment:
                df.loc[index, '料理のコメント'] = dish_comment
                best_sake = sake_score.iloc[0]
                df.loc[index, choice_drink] = f"{best_sake['名前']}[{best_sake['スコア']}]"

    st.dataframe(df)