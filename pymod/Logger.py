import logging
import logging.handlers
import sys
import os.path


class Logger(object):
    """
       Logger objects with initialized File and Syslog logger.
    """
    _logger = None
    _logname = None

    def _init_stdout(self):
        lfs = '%(levelname)s - %(message)s'
        lf = logging.Formatter(lfs)
        lv = logging.INFO

        logging.basicConfig(format=lfs, level=lv, stream=sys.stdout)
        self._logger = logging.getLogger(self._logname)

    def _init_syslog(self):
        lfs = '%(name)s[%(process)s]: %(levelname)s - %(message)s'
        lf = logging.Formatter(lfs)
        lv = logging.INFO

        sh = logging.handlers.SysLogHandler('/dev/log', logging.handlers.SysLogHandler.LOG_USER)
        sh.setFormatter(lf)
        sh.setLevel(lv)
        self._logger.addHandler(sh)

    def _init_filelog(self, logfile):
        lfs = '%(asctime)s %(name)s[%(process)s]: %(levelname)s - %(message)s'
        lf = logging.Formatter(fmt=lfs, datefmt='%Y-%m-%d %H:%M:%S')
        lv = logging.INFO

        sf = logging.handlers.RotatingFileHandler(logfile, maxBytes=512*1024, backupCount=4)
        self._logger.fileloghandle = sf.stream
        sf.setFormatter(lf)
        sf.setLevel(lv)
        self._logger.addHandler(sf)

    def __init__(self, logname, logdir):
        self._logname = logname
        try:
            if not os.path.isdir(logdir):
                os.makedirs(logdir)
            self._init_stdout()
            self._init_filelog(logdir + self._logname + '.log')
            self._init_syslog()
        except (OSError, IOError) as e:
            sys.stderr.write('ERROR - ' + str(e) + '\n')
            raise SystemExit(1)

    def get(self):
        return self._logger
