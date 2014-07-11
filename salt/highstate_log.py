import time
import os
import json
import bz2


highstate_log_suffix = '_highstate.log.bz2'
result_log_suffix = '_result.log.bz2'
ts_format = '%Y-%m-%dT%H:%M:%S'


class HighStateLog(object):
    '''Represent state log'''
    def __init__(self, log_dir):
        self.log_dir = log_dir
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

    def new_entry(self):
        '''Create new state log entry'''
        return HighStateLogEntry(
            self, time.strftime(ts_format, time.localtime()))

    def _get_highstate_path(self, ts):
        return os.path.join(self.log_dir, ts + highstate_log_suffix)

    def _get_result_path(self, ts):
        return os.path.join(self.log_dir, ts + result_log_suffix)

    def __contains__(self, ts):
        return os.path.isfile(self._get_highstate_path(ts))

    def __len__(self):
        return sum(1 for ts in self)

    def __getitem__(self, ts):
        if ts not in self:
            raise KeyError('No log entry available for specified timestamp')
        return HighStateLogEntry(self, ts)

    def __iter__(self):
        seen = set()
        for name in os.listdir(self.log_dir):
            if name.endswith(highstate_log_suffix):
                ts = name[:-len(highstate_log_suffix)]
                if ts not in seen:
                    seen.add(ts)
                    yield ts


class HighStateLogEntry(object):
    '''Represent the log entry for a single highstate run'''
    def __init__(self, highstate_log, ts):
        self.highstate_log = highstate_log
        self.ts = ts

    def write_highstate(self, data):
        '''Write highstate data'''
        path = self.highstate_log._get_highstate_path(self.ts)
        if os.path.isfile(path):
            raise RuntimeError('Log file for highstate data already exists')
        try: # can't use with here on Python 2.7
            f = bz2.BZ2File(path, 'w')
            json.dump(data, f)
        finally:
            f.close()

    def write_result(self, result):
        '''Write highstate result'''
        path = self.highstate_log._get_result_path(self.ts)
        if os.path.isfile(path):
            raise RuntimeError('Log file for highstate result already exists')
        try: # can't use with here on Python 2.7
            f = bz2.BZ2File(path, 'w')
            json.dump(result, f)
        finally:
            f.close()

    def read_highstate(self):
        '''Return highstate data'''
        path = self.highstate_log._get_highstate_path(self.ts)
        if not os.path.isfile(path):
            return None
        try: # can't use with here on Python 2.7
            f = bz2.BZ2File(path)
            return json.load(f)
        finally:
            f.close()

    def read_result(self):
        '''Return highstate result'''
        path = self.highstate_log._get_result_path(self.ts)
        if not os.path.isfile(path):
            return None
        try: # can't use with here on Python 2.7
            f = bz2.BZ2File(path)
            return json.load(f)
        finally:
            f.close()
