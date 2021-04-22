
class ExperienceWriter():
    DATA_DIR = path.join(path.dirname(path.realpath(__file__)), "_data")
    
    def __init__(self, data_dir = None):
        self._data = dict()
        self._path = dict()

        self._data_dir = data_dir if data_dir else ExperienceWriter.DATA_DIR
        if not path.exists(self._data_dir):
            makedirs(self._data_dir)

    def run(self):

if __name__ == "__main__":
    fetcher = ExperienceWriter()
    fetcher.run()
