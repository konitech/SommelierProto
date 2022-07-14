import pandas as pd

class FoodDB:

    def __init__(self):
        # データベースの初期化
        # 基礎料理知識ベースの読み込み
        # relationの説明
        # - IsA:
        # - Synonym:同義語
        # - SubAttribute:副属性
        # - Ingredient:材料
        # - RIngredient:代表材料
        # - Attribute:属性
        # - RAttribute:代表属性
        # - Method:調理法
        # - RMethod:代表調理法
        # 独自に追加したrelation
        # - Class:食材の分類
        # - Taste:食材の味わい
        # - Flavor:食材の香り（「フレーバー・マトリクス」に基づく）

        self.synonym = pd.read_csv('./data/synonym.tsv', sep='\t')
        self.synonym['synonym'] = self.synonym['synonym'].str.replace(" ", "", regex=True)
        self.synonym['synonym'] = self.synonym['synonym'].str.replace("'", "", regex=True)
        self.synonym['synonym'] = self.synonym['synonym'].str.replace("[", "", regex=True)
        self.synonym['synonym'] = self.synonym['synonym'].str.replace("]", "", regex=True)

        self.dish = pd.read_csv('./data/dish.tsv', sep='\t')
        self.dish['ingredient'] = self.dish['ingredient'].str.replace(" ", "", regex=True)
        self.dish['ingredient'] = self.dish['ingredient'].str.replace("'", "", regex=True)
        self.dish['ingredient'] = self.dish['ingredient'].str.replace("[", "", regex=True)
        self.dish['ingredient'] = self.dish['ingredient'].str.replace("]", "", regex=True)

        self.ingredient = pd.read_csv('./data/ingredient.tsv', sep='\t')

        self.condiment = pd.read_csv('./data/condiment.tsv', sep='\t')