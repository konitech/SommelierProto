class Recipe:
    def __init__(self, name, fooddb):
        self.name = self.getSynonym(name, fooddb) # 料理名

        if len(self.name) == 0:
            self.ingredients = [] # 食材・調味料
            self.method = [] # 調理法
            self.ingredientsdb = None
        else:
            self.ingredients = fooddb.dish[fooddb.dish['name'] == self.name].iloc[0]['ingredient'].split(',')# 食材・調味料
            self.method = fooddb.dish[fooddb.dish['name'] == self.name].iloc[0]['method'] # 調理法
            self.ingredientsdb = fooddb.ingredient.query("node1 in @self.ingredients")

    def getName(self):
        return self.name

    def getIngredients(self):
        return self.ingredients

    def getMethod(self):
        return self.method

    def getgetIngredientsDB(self):
        return self.ingredientsdb

    # 料理名の同義語を検索
    def getSynonym(self, dish, fooddb):
        # 料理名を抽出
        dishs = set(fooddb.dish['name'].unique())
        if dish in dishs:
            return dish
        else:
            # 同義語を検索
            for index, row in fooddb.synonym.iterrows():
                if dish in row['synonym'].split(','):
                    return row['name']

            return '' # 見つからない場合

    # 標準の食材名に直す
    def getStdName(self, name, fooddb):
        # 食材名を抽出
        ingredient_names = fooddb.ingredient['node1'].unique()
        if name in ingredient_names:
            return name
        else:
            # 同義語を検索
            for index, row in fooddb.synonym.iterrows():
                if name in row['synonym'].split(','):
                    return row['name']

            return '' # 見つからない場合

    def getNotando(self):
        # 食材、調味料、調理法のそれぞれで、さっぱり系：+0、中関係：+1、濃厚系：+2
        
        # 濃い食材をカウント
        df_tmp = self.ingredientsdb.query("relation == 'Taste' & node2 == '濃い'")
        scale = len(df_tmp)*2 # 濃厚系は+2
        elements = df_tmp['node1'].unique()

        # 調理法
        method_notan_lv1 = ['蒸す', 'おろす', '炊く', '和える', '浸す', '巻く', '包む']
        method_notan_lv2 = ['蒸して焼く', '焼く', 'ホイル焼き', '漬ける']
        method_notan_lv3 = ['煮る', '炒める', '煮込む', '揚げる', '煮て浸す', '炒めて煮る', '揚げて浸す', 'ローストする', 'ソテーする']

        if self.method in method_notan_lv2:
            scale += 1
        elif self.method in method_notan_lv3:
            scale += 2
        else:
            pass

        return scale, elements

    def getUmami(self):
        df_tmp = self.ingredientsdb.query("relation == 'Taste' & node2.str.contains('うま味')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()
        return scale, elements

    def isOily(self):
        if self.method == "揚げる":
            return True
        else:
            return False

    def getFruity(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('フルーティ')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements


    def getDairy(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('乳製品')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements
    
    def getKouji(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('麹')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

    def getGrain(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('穀物')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

    def getMarine(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('マリーン')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

    def getMaillard(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('メイラード')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

    def getTerpenes(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('テルペン')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

    def getSour(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('酸味')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

    def getSpicy(self):
        df_tmp = self.ingredientsdb.query("relation == 'Flavor' & node2.str.contains('刺激')", engine='python')
        scale = len(df_tmp)
        elements = df_tmp['node1'].unique()

        isFlavor = True if scale > 0 else False

        return isFlavor, elements

# デバッグ用のShow関数
def showRecipe(recipe):
    print(recipe.getName())
    print(recipe.getIngredients())
    print(recipe.getMethod())
    print(recipe.getgetIngredientsDB())

    notando, notando_elms = recipe.getNotando()
    umami, umami_elms = recipe.getUmami()
    fruity, fruity_elms = recipe.getFruity()
    dairy, dairy_elms = recipe.getDairy()
    kouji, kouji_elms = recipe.getKouji()
    grain, grain_elms = recipe.getGrain()
    marine, marine_elms = recipe.getMarine()
    maillard, maillard_elms = recipe.getMaillard()
    terpenes, terpenes_elms = recipe.getTerpenes()
    sour, sour_elms = recipe.getSour()
    spicy, spicy_elms = recipe.getSpicy()

    print("濃淡度：", notando, notando_elms)
    print("うま味：", umami, umami_elms)
    print("脂味：", recipe.isOily())
    print("フルーティ：", fruity, fruity_elms)
    print("乳製品：", dairy, dairy_elms)
    print("麹：", kouji, kouji_elms)
    print("穀物：", grain, grain_elms)
    print("マリーン：", marine, marine_elms)
    print("メイラード：", maillard, maillard_elms)
    print("テルペン：", terpenes, terpenes_elms)
    print("酸味：", sour, sour_elms)
    print("刺激：", spicy, spicy_elms)