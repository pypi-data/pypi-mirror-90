class NoNextTaskSituation(Exception):
    def __init__(self, message: str):
        Exception(message)
