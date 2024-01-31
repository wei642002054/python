import logging,uuid,time,re
def init_log_config():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式化输出
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"  # 日期格式
    filename = "D:/details_error.log"
    fp = logging.FileHandler(filename, encoding='utf-8')
    fs = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])

def generate_unique_id() -> str:
    """
    生成唯一的12位纯数字ID
    :return: 生成的ID
    """
    timestamp = str(int(time.time()))
    while True:
        unique_id = str(uuid.uuid4().int)[:9]
        # print(unique_id)
        if len(unique_id) == 9 and unique_id.isnumeric():
            return str(unique_id+str(timestamp)[-3::])