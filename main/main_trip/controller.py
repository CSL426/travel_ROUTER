from typing import Dict, List, Tuple, Union
from feature.line import line_handler
from feature.llm import llm_processor
from feature.sql import sql_query
from feature.retrieval import retrieval
from feature.trip import TripPlanningSystem


class TripController:
    """行程規劃系統控制器"""

    def process_message(self, input_text: str) -> str:
        """
        處理輸入訊息並返回結果

        輸入:
            input_text (str): 使用者輸入文字，例如"想去台北文青的地方"

        輸出:
            str: 規劃好的行程或錯誤訊息
        """
        try:
            # 1. LLM意圖分析
            period_describe, unique_requirement, base_requirement = self._analyze_intent(
                input_text
            )

            # 2. 向量檢索
            placeIDs = self._vector_retrieval(period_describe)

            # 3. 取得景點詳細資料
            location_details = self._get_places(placeIDs, unique_requirement)

            # 3. 規劃行程
            trip = self._plan_trip(location_details, base_requirement)

            # 4. 格式化輸出
            return self._linebot(trip)

        except Exception as e:
            return f"抱歉，系統發生錯誤: {str(e)}"

    def _analyze_intent(self, text: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        From Abby:
        分析使用者意圖

        輸入:
            text (str): 使用者輸入

        輸出:
            Tuple[List[Dict], List[Dict], List[Dict[str, Union[int, str, None]]]]:
                - List[Dict]: 旅遊各時段形容詞 (對應圖中的 'a')
                - List[Dict]: 特殊需求 (對應圖中的 'b')
                - List[Dict[str, Union[int, str, None]]]: 客戶基本要求 (對應圖中的 'c')
        """
        # 假設 llm_processor.analyze 會回傳三個結果
        return llm_processor.analyze(text)

    def _vector_retrieval(self, period_describe: Dict) -> List[Dict]:
        """
        由形容客戶行程的一(五)句話，找出相關景點ID

        輸入:
            period_describe (Dict): 形容客戶行程的一(五)句話

        輸出:
            List[Dict]: 一系列的PlaceID
        """
        # 向量檢索
        return retrieval.filter_places(period_describe)

    def _get_places(self, placeIDs: List, unique_requirement: List[Dict]) -> List[Dict]:
        """
        根據意圖PlaceID和特殊需求，從資料庫中找出景點詳細資料

        輸入:
            placeIDs (List): 初步篩選出的PlaceID
            unique_requirement (List[Dict]): 用戶的特殊需求

        輸出:
            List[Dict]: 景點詳細資料
        """
        # 從資料庫取得景點資料
        return sql_query.get_places(placeIDs, unique_requirement)

    def _plan_trip(self, location_details: List[Dict], base_requirement: List[Dict]) -> List[Dict]:
        """
        規劃行程

        輸入:
            location_details (List[Dict]): 景點詳細資料
            base_requirement (List[Dict]): 客戶基本要求

        輸出:
            Dict: 完整行程規劃
        """
        return TripPlanningSystem().plan_trip(location_details, base_requirement)

    def _linebot(self, trip: List[Dict]):
        """
        Line Bot輸出

        輸入:
            trip (List[Dict]): 旅遊行程

        輸出:
            Line用戶端
        """

        return line_handler.line_output(trip)
