import logging
import logging.handlers
import sys
import os.path
import gzip


class AIRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, **kws):
        backupCount = kws.get('backupCount', 0)
        self.backup_count = backupCount
        logging.handlers.RotatingFileHandler.__init__(self, filename, **kws)

    def doArchive(self, old_log):
        with open(old_log) as log:
            with gzip.open(old_log + '.gz', 'wb') as comp_log:
                comp_log.writelines(log)
        os.remove(old_log)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backup_count > 0:
            for i in range(self.backup_count - 1, 0, -1):
                sfn = "%s.%d.gz" % (self.baseFilename, i)
                dfn = "%s.%d.gz" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
        dfn = self.baseFilename + ".1"
        if os.path.exists(dfn):
            os.remove(dfn)
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            self.doArchive(dfn)
        self.stream = self._open()


class LogConfig(object):
    instance = None

    LOG_FOLDER = './logs'

    def __init__(self):
        if not os.path.exists(self.LOG_FOLDER):
            os.makedirs(self.LOG_FOLDER, mode=0o755)
        self.log_path = os.path.join(self.LOG_FOLDER, 'aiautomation.log')
        self.log_level = logging.DEBUG
        self.log_to_console = True

    def set_log_to_console(self, to_console):
        self.log_to_console = to_console

    def get_log_path(self):
        return self.log_path

    def set_log_path(self, path):
        self.log_path = path

    def set_log_level(self, level):
        self.log_level = level

    def configure(self):
        dirname = os.path.dirname(self.log_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname, 0o755)
        logging.basicConfig(filename=self.log_path, level=self.log_level)

    def get_logger(self, name, logfd=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        max_rotate_handler = AIRotatingFileHandler(self.log_path, maxBytes=10 * 1024 * 1024, backupCount=30)
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
        max_rotate_handler.setFormatter(formatter)
        max_rotate_handler.setLevel(logging.DEBUG)
        logger.addHandler(max_rotate_handler)
        if self.log_to_console:
            formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
            if not logfd:
                logfd = sys.stdout
            ch = logging.StreamHandler(logfd)
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger

    @staticmethod
    def get_log_config():
        if not LogConfig.instance:
            LogConfig.instance = LogConfig()
        return LogConfig.instance


def get_logfile_path():
    return LogConfig.get_log_config().get_log_path()


def set_logfile_path(path):
    LogConfig.get_log_config().set_log_path(path)


def configure_log(log_path, level=logging.DEBUG, log_to_console=False):
    cfg = LogConfig.get_log_config()
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    cfg.set_log_path(log_path)
    cfg.set_log_level(level)
    cfg.set_log_to_console(log_to_console)
    cfg.configure()


def get_logger(name, logfd=None):
    return LogConfig.get_log_config().get_logger(name, logfd)
