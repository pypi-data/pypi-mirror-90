import os
import pymongo
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class DBConnect():
    def __init__(self, db: str, collection: str, home_kye='MONGODB_HOST', port_kye='MONGODB_PORT'):
        self.mongo_home = os.environ.get(home_kye, None)
        self.mongo_port = os.environ.get(port_kye, 27017)

        if not self.mongo_home or not self.mongo_port:
            logging.error('MongoDB(组件)的组件连接信息是不完整的')

        self.mongo_client = pymongo.MongoClient(
            host=self.mongo_home,
            port=int(self.mongo_port)
        )
        self.mongo_db = self.mongo_client[db]
        self.mongo_collection = self.mongo_db[collection]

    def write_one_docu(self, docu: dict) -> bool:
        try:
            self.mongo_collection.insert_one(docu)
            return True
        except Exception as err:
            logging.warning('MongoDB(组件)出现写入错误: {0}'.format(err))
            return False

    def does_it_exist(self, docu: dict) -> bool:
        count = self.mongo_collection.count_documents(docu)
        if count != 0:
            return True
        else:
            return False

    def update_docu(self, find_docu: dict, modify_docu: dict, many=False) -> bool:
        try:
            if many:
                self.mongo_collection.update_many(find_docu, modify_docu)
            else:
                self.mongo_collection.update_one(find_docu, modify_docu)
            return True
        except Exception as err:
            logging.warning('MongoDB(组件)出现更新错误: {0}'.format(err))
            return False
