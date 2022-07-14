import pandas as pd
import streamlit as st

class Sommelier:
    def __init__(self, dishDB):
        self.dishDB = dishDB

    def evaluateNotandoPairing(self, dishData, sake):
        """
        濃淡度の相性度を0～1で返す
        """
        dish_notando = dishData['濃淡度']['値']
        # print(dish_notando)

        # 濃淡度の相性度
        notando_match = 1 - abs(sake['濃淡度'] - dish_notando) # 0-1：0が最も合わない、1が最も合う

        return notando_match
    
    def evaluateFlavorPairing(self, dishData, sake):
        """
        各香りの同調度を0～1で返す
        """
        flavor_max = 5 # 酒の香りの強さの最大値

        # フルーティな香りとの同調度
        fruity_match = dishData['フルーティ']['値']*sake['フルーティ']/flavor_max

        # 乳製品の香りとの同調度
        dairy_match = dishData['乳製品']['値']*sake['乳製品']/flavor_max

        # 穀物の香りとの同調度
        grain_match = dishData['穀物']['値']*sake['穀物']/flavor_max

        # メイラードの香りとの同調度
        maillard_match = dishData['メイラード']['値']*sake['メイラード']/flavor_max

        # スパイシーな香りとの同調度
        spicy_match = dishData['刺激']['値']*sake['スパイス']/flavor_max

        # 辞書型で返す
        flavor_dict = {'フルーティ':fruity_match, '乳製品':dairy_match, '穀物':grain_match, 'メイラード':maillard_match, 'スパイシー':spicy_match}

        return flavor_dict

    def evaluateWashEffect(self, dishData, sake):
        """
        ウォッシュ効果の程度を0～1で返す。
        ウォッシュ効果というのは、「樽酒のタンニンが肉類の油脂を洗い流す」「炭酸の持つすっきり感」などがある。
        """
        gas_max = 5 # 炭酸の強さの最大値

        return dishData['脂肪味']*sake['炭酸']/gas_max

    def comment(self, sake_s):
        if sake_s['スコア'] < 30:
            if sake_s['濃淡同調度'] < 0.3:
                st.info(f"　🤢料理とお酒の味の濃淡のバランスが悪い：{sake_s['濃淡同調度']}")
        elif sake_s['スコア'] > 50:
            if sake_s['濃淡同調度'] > 0.7:
                st.info(f"　😋料理とお酒の味の濃淡のバランスが良い：{sake_s['濃淡同調度']}")
            if sake_s['香り同調度'] > 0.7:
                st.info(f"　🌹香りが同調している：{sake_s['香り同調度']}[{sake_s['香り同調要素']}]")
            if sake_s['ウォッシュ同調度'] > 0.7:
                st.info(f"　✨ウォッシュ効果あり：{sake_s['ウォッシュ同調度']}")

    def kikizake(self, dish_name, condiment, sake, preference):
        df_kikizake = sake.copy()

        df_kikizake['スコア'] = 0.0
        df_kikizake['濃淡度スコア'] = 0.0
        df_kikizake['香りスコア'] = 0.0
        df_kikizake['ウォッシュスコア'] = 0.0
        df_kikizake['濃淡同調度'] = 0.0
        df_kikizake['香り同調度'] = 0.0
        df_kikizake['ウォッシュ同調度'] = 0.0
        df_kikizake['香り同調要素'] = ''

        best_index = 0 # ベストな酒のインデックス
        best_point = 0 # 最高の同調度
        best_flavor = "" # 最高に同調したフレーバー

        # 料理データを取得
        dishData = self.dishDB.getDishData(dish_name, condiment)
        print(dishData)

        # 好み
        st.markdown("### あなたの好みの傾向")

        if preference == 'ワイン':
            st.write('ワイン好みのあなたは「香り重視タイプ」')
        elif preference == 'ビール':
            st.write('ビール好みのあなたは「スッキリ感重視タイプ」')
        elif preference == 'サワー':
            st.write('サワー好みのあなたは「スッキリ感重視タイプ」')
        elif preference == '日本酒':
            st.write('日本酒好みのあなたは「バランス重視タイプ」')
        else:
            pass

        # 料理の特徴をコメントする
        st.markdown("### 料理のポイント")

        if dishData['濃淡度']['値'] > 0.7:
            st.markdown("- 味は**濃いめ**。")
        elif dishData['濃淡度']['値'] < 0.3:
            st.markdown("- 味は**さっぱりめ**。")
        else:
            st.markdown("- 味の濃淡は**中間**。")

        if dishData['うま味']['値'] > 0.5:
            st.markdown(f"- **{'、'.join(dishData['うま味']['要素'])}**のうま味多め。")

        if dishData['フルーティ']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['フルーティ']['要素'])}**に由来するフルーティな香りあり。")

        if dishData['乳製品']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['乳製品']['要素'])}**に由来するフクリーミーな香りあり。")
        
        if dishData['麹']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['麹']['要素'])}**に由来する麹の香りあり。")

        if dishData['穀物']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['穀物']['要素'])}**に由来する穀物の香りあり。")

        if dishData['マリーン']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['マリーン']['要素'])}**に由来する磯の香りあり。")

        if dishData['メイラード']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['メイラード']['要素'])}**に由来する焦げたような香りあり。")

        if dishData['テルペン']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['テルペン']['要素'])}**に由来するテルペンの香りあり。")

        if dishData['酸味']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['酸味']['要素'])}**に由来する酸味の香りあり。")

        if dishData['刺激']['値'] == 1:
            st.markdown(f"- **{'、'.join(dishData['刺激']['要素'])}**に由来するスパイシーな香りあり。")


        for index, sake_item in df_kikizake.iterrows():
            # まずは濃淡の判断
            notando_match = self.evaluateNotandoPairing(dishData, sake_item.to_dict())

            # 次に香りの判断
            flavor_dict = self.evaluateFlavorPairing(dishData, sake_item.to_dict())

            # 最後にウォッシュの判断
            wash = self.evaluateWashEffect(dishData, sake_item.to_dict())

            # 重みを考慮して点数化
            # このときpreferenceによって重み付けを変化させる
            if preference == 'ワイン':
                notando_weight = 0.4
                flavor_weight = 0.5
                wash_weight = 0.1
            elif preference == 'ビール':
                notando_weight = 0.5
                flavor_weight = 0.2
                wash_weight = 0.3
            elif preference == 'サワー':
                notando_weight = 0.5
                flavor_weight = 0.2
                wash_weight = 0.3
            else:
                notando_weight = 0.6
                flavor_weight = 0.3
                wash_weight = 0.1

            notando_score = notando_match*notando_weight*100
            flavor_score = max(flavor_dict.values())*flavor_weight*100
            wash_score = wash*wash_weight*100

            score = notando_score + flavor_score + wash_score
            df_kikizake.loc[index,'スコア'] = score
            df_kikizake.loc[index,'濃淡度スコア'] = notando_score
            df_kikizake.loc[index,'香りスコア'] = flavor_score
            df_kikizake.loc[index,'ウォッシュスコア'] = wash_score
            df_kikizake.loc[index,'濃淡同調度'] = notando_match
            df_kikizake.loc[index,'香り同調度'] = max(flavor_dict.values())
            df_kikizake.loc[index,'ウォッシュ同調度'] = wash
            df_kikizake.loc[index,'香り同調要素'] = max(flavor_dict, key=flavor_dict.get)

        
        df_s = df_kikizake.sort_values('スコア', ascending=False)

        st.markdown("### きき酒")

        st.markdown("#### ベストSAKEは")
        best_sake = df_s.iloc[0]
        st.metric(label=best_sake['名前'], value="{}点".format(round(best_sake['スコア'])))
        self.comment(best_sake)

        st.markdown("#### ワーストSAKEは")
        worst_sake = df_s.iloc[-1]
        st.metric(label=worst_sake['名前'], value="{}点".format(round(worst_sake['スコア'])))
        self.comment(worst_sake)

        st.markdown("#### きき酒一覧")
        for index, sake_item in df_s.iterrows():
            st.metric(label=sake_item['名前'], value="{}点".format(round(sake_item['スコア'])))
            # 評価に対するコメント
            self.comment(sake_item)

        st.dataframe(df_s)
