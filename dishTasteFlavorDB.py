# DishDataBase：料理の味香りデータベースを作成するクラス
import pandas as pd

class DishTasteFlavorDB:
    def __init__(self, fooddb):
        self.fooddb = fooddb
        self.database = pd.read_pickle('./data/dishDB.pkl')

    def getDishData(self, dish, condiment=None):
        std_name = self.getSynonym(dish)
        if len(std_name) > 0:
            s = self.database[self.database['名前'] == std_name].iloc[0]
            dict_dish = {'名前':s['名前'],
                        '材料':s['材料'],
                        '調理法':s['調理法'],
                        '濃淡度':{'値':s['濃淡度'],'要素':s['濃淡度要素'].tolist()},
                        'うま味':{'値':s['うま味'],'要素':s['うま味要素'].tolist()},
                        '脂肪味':s['脂肪味'],
                        'フルーティ':{'値':s['フルーティ'],'要素':s['フルーティ要素'].tolist()},
                        '乳製品':{'値':s['乳製品'],'要素':s['乳製品要素'].tolist()},
                        '麹':{'値':s['麹'],'要素':s['麹要素'].tolist()},
                        '穀物':{'値':s['穀物'],'要素':s['穀物要素'].tolist()},
                        'マリーン':{'値':s['マリーン'],'要素':s['マリーン要素'].tolist()},
                        'メイラード':{'値':s['メイラード'],'要素':s['メイラード要素'].tolist()},
                        'テルペン':{'値':s['テルペン'],'要素':s['テルペン要素'].tolist()},
                        '酸味':{'値':s['酸味'],'要素':s['酸味要素'].tolist()},
                        '刺激':{'値':s['刺激'],'要素':s['刺激要素'].tolist()}}

            if condiment: # 調味料をかける場合
                # 調味料による調整
                dict_dish['名前'] = dict_dish['名前'] + "+" + condiment

                tmp_condiment = self.fooddb.condiment[self.fooddb.condiment['name']==condiment]
                if len(tmp_condiment) > 0:
                    add_notando = tmp_condiment.iloc[0]['notando']
                    dict_dish['濃淡度']['値'] = dict_dish['濃淡度']['値'] + add_notando
                    if dict_dish['濃淡度']['値'] > 1.0: # 最大値は1.0なので
                        dict_dish['濃淡度']['値'] = 1.0
                    if add_notando >0:
                        dict_dish['濃淡度']['要素'].append(condiment)


            return dict_dish
        else:
            return None

    # 料理名の同義語を検索
    def getSynonym(self, dish):
        # 料理名を抽出
        dishs = set(self.fooddb.dish['name'].unique())
        if dish in dishs:
            return dish
        else:
            # 同義語を検索
            for index, row in self.fooddb.synonym.iterrows():
                if dish in row['synonym'].split(','):
                    return row['name']

            return '' # 見つからない場合