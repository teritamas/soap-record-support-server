

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
        self.guidelines_path_prefix = "guidelines" # ユーザグループDBのprefix
        self.records_path_prefix = "nursing_records" # ユーザグループDBのprefix

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
        guidelines = db.reference(self.guidelines_path_prefix).get()
        
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
    
    def set_record(self, record_id: str, content: dict):
        """看護記録を保存する。同じIDのデータが存在していたら上書きする。

        Args:
            record_id (str): 更新対象のレコードID
            content (dict): データの中身
        """
        db.reference(f"{self.records_path_prefix}/{record_id}").set(content)

    def get_record(self, record_id: str) -> dict:
        return db.reference(f"{self.records_path_prefix}/{record_id}").get()
    