
import os
import sys
import glob

import radical.utils as ru


# ------------------------------------------------------------------------------
#
def stack():
    '''
    returns a dict with information about the currently active python
    interpreter and all rc (and radical) modules (incl. version details)
    '''

    ret = {
              'sys': {
                  'python'     : sys.version.split()[0],
                  'pythonpath' : os.environ.get('PYTHONPATH',       ''),
                  'virtualenv' : os.environ.get('VIRTUAL_ENV',      '') or
                                 os.environ.get('CONDA_DEFAULT_ENV','')
              }
          }

    for ns in ['rc', 'radical']:
        ret[ns] = stack_ns(ns)

    return ret


# ------------------------------------------------------------------------------
#
def stack_ns(ns):
    '''
    same as `stack()`, but for any specified name space
    '''

    ret   = dict()
    nsmod = ru.import_module(ns)
    rpath = nsmod.__path__

    if hasattr(rpath, '_path'):
        rpath = getattr(rpath, '_path')

    if isinstance(rpath, list):
        rpath = rpath[0]

    for mpath in glob.glob('%s/*' % rpath):

        if os.path.isdir(mpath):

            mname = '%s.%s' % (ns, os.path.basename(mpath))
            try:
                ret[mname] = ru.import_module(mname).version_detail
            except Exception as e:
                ret[mname] = str(e)

    return ret


# ------------------------------------------------------------------------------

