

import firebase_admin
from firebase_admin import credentials, db
from SoapRecordSupport.models.PostEvaluate.PostEvaluateResponseModel import \
    Guideline


class Firebase():
    def __init__(self, 
                 cred_path:str,
                 databaseURL: str,
                 target_path: str
        ) -> None:
        cred = credentials.Certificate(cred_path)

        firebase_admin.initialize_app(cred, {
            'databaseURL': databaseURL
        })
        self.target_path_prefix = target_path
        self.group_path_prefix = "groups" # ユーザグループDBのprefix

    def add(self, id, content: dict):
        """指定したIDのエリアにデータを追加する

        Args:
            id (_type_): 保存する看護記録ID
            content (dict): データの中身
        """
        db.reference(f"{self.target_path_prefix}/{id}").push().set(content)

    def get(self, id: str):
        return db.reference(f"{self.target_path_prefix}/{id}").get()
    
    def get_all(self):
        return db.reference(f"{self.target_path_prefix}").get()
    
    def get_group_users(self, group_id: str):
        return db.reference(f"{self.group_path_prefix}/{group_id}").get()
    
    def get_guideline(self, keywords: list[str])->list[Guideline]:
        guidelines = db.reference(f"guidelines").get()
        
        target_guidelines: list[Guideline] = []

        for guide in guidelines:
            try:
                print(keywords)
                if guide.get('category') in keywords:
                    target_guidelines.append(
                        Guideline(
                            category=guide.get('category'),
                            url=guide.get('url'),
                        )
                    )
            except:
                pass # エラーが発生したらとりあえずスキップ
                    
        return target_guidelines
    
# if __name__ == "__main__":
    # import logging
    # logging.basicConfig(level=logging.INFO)
    # from dotenv import load_dotenv
    # load_dotenv()
    
    # fb = Firebase(
    #     './keys/hackday-327101-a19313490ec3.json', 
    #     "https://hackday-327101-default-rtdb.firebaseio.com",
    #     "feedback_comments"
    # )
    # fb.add(
    #     id = 'sample',
    #     content = {
    #         "name": "山田",
    #         "comment": "アクションプランの内容が充実していて、感動しました！成長しましたね。",
    #     }
    # )
    
    # fb.add(
    #     id = 'sample',
    #     content = {
    #         "name": "田中",
    #         "comment": "患者さんが寒そうなので血圧も心配です。いつもより血圧を多めに測ってみてください。",
    #     }
    # )
    
    # obj = fb.get_all().get('sample')
    # for i in obj:
    #     print(i)
    #     print(obj.get(i))
    # print(fb.get_group_users("1"))
