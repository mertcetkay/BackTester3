import logging


class Logger:
    def __init__(self, name, level=logging.INFO):
        """
        Logger sınıfı, uygulamanın loglama işlemlerini yönetmek için yapılandırılmıştır.

        Args:
            name (str): Logger ismi.
            level (int): Loglama seviyesi (varsayılan olarak INFO).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Henüz handler eklenmediyse ekle
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)
