'''
Access entries from highstate log
'''

import salt.highstate_log


__outputter__ = {
    'last_result': 'highstate',
    'get_result': 'highstate',
}



def ls():
    '''
    Return list of timestamps for which state logs are available

    CLI Example::

        salt '*' highstate_log.ls
    '''
    return sorted(
        salt.highstate_log.HighStateLog(__opts__['highstate_log_dir']))

def get_highstate(ts):
    '''
    Return data used for highstate run at specified timestamp

    CLI Example::

        salt '*' highstate_log.get_highstate 2013-08-20T14:03:23
    '''
    entry = salt.highstate_log.HighStateLog(__opts__['highstate_log_dir'])[ts]
    return entry.read_highstate()

def get_result(ts):
    '''
    Return result for highstate run at specified timestamp

    CLI Example::

        salt '*' highstate_log.get_result 2013-08-20T14:03:23
    '''
    entry = salt.highstate_log.HighStateLog(__opts__['highstate_log_dir'])[ts]
    return entry.read_result()

def get(ts):
    '''
    Return data used and result for highstate run at specified timestamp

    CLI Example::

        salt '*' highstate_log.get 2013-08-20T14:03:23
    '''
    entry = salt.highstate_log.HighStateLog(__opts__['highstate_log_dir'])[ts]
    return {'highstate': entry.read_highstate(), 'result': entry.read_result()}


def last_highstate(n=None):
    '''
    Return SLS data used for last highstate run if n is None; otherwise return
    data for last n runs as a dict mapping timestamps to entries.

    CLI Example::

        salt '*' highstate_log.last_highstate
        salt '*' highstate_log.last_highstate n=2
    '''
    highstate_log = salt.highstate_log.HighStateLog(
        __opts__['highstate_log_dir'])
    if n is None:
        for ts in sorted(highstate_log, reverse=True):  # return only last entry
            return highstate_log[ts].read_highstate()
    else:
        sorted_ts = sorted(highstate_log, reverse=True)
        return dict((sorted_ts[i], highstate_log[sorted_ts[i]].read_highstate())
            for i in range(min(n, len(sorted_ts))))

def last_result(n=None):
    '''
    Return result for last highstate run if n is None; otherwise return
    last n entries as a list.

    CLI Example::

        salt '*' highstate_log.last_result
        salt '*' highstate_log.last_result n=2
    '''
    highstate_log = salt.highstate_log.HighStateLog(
        __opts__['highstate_log_dir'])
    if n is None:
        for ts in sorted(highstate_log, reverse=True):  # return only last entry
            return highstate_log[ts].read_result()
    else:
        sorted_ts = sorted(highstate_log, reverse=True)
        return dict((sorted_ts[i], highstate_log[sorted_ts[i]].read_result())
            for i in range(min(n, len(sorted_ts))))

def last(n=None):
    '''
    Return SLS data and highstate result for last highstate run if n is None;
    otherwise return last n entries as a list.

    CLI Example::

        salt '*' highstate_log.last
        salt '*' highstate_log.last n=2
    '''
    highstate_log = salt.highstate_log.HighStateLog(
        __opts__['highstate_log_dir'])
    if n is None:
        for ts in sorted(highstate_log, reverse=True):  # return only last entry
            return {
                'highstate': highstate_log[ts].read_highstate(),
                'result': highstate_log[ts].read_result()
            }
    else:
        sorted_ts = sorted(highstate_log, reverse=True)
        return dict((sorted_ts[i], {
                'highstate': highstate_log[sorted_ts[i]].read_highstate(),
                'result': highstate_log[sorted_ts[i]].read_result()
            }) for i in range(min(n, len(sorted_ts))))
