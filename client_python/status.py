class Status:
    def __init__(self, status, filename, timestamp, explanation,uid):
        self.uid = uid
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation

    def is_done(self):
        return self.status == 'done'

    def __str__(self):
        return f"uid: {self.uid}\n"\
               f"Status: {self.status}\n" \
               f"Filename: {self.filename}\n" \
               f"Timestamp: {self.timestamp}\n" \
               f"Explanation: {self.explanation}\n"