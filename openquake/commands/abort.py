#  -*- coding: utf-8 -*-
#  vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright (c) 2017, GEM Foundation

#  OpenQuake is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  OpenQuake is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import signal
import psutil
from openquake.baselib import sap, config, workerpool
from openquake.commonlib import logs


@sap.Script
def abort(job_id):
    """
    Abort the given job
    """
    job = logs.dbcmd('get_job', job_id)
    if job is None:
        sys.exit('There is no job %d' % job_id)
    elif job.status not in ('executing', 'running'):
        sys.exit('Job %d is %s' % (job_id, job.status))
    logs.dbcmd('set_status', job_id, 'aborted')
    name = 'oq-job-%d' % job_id
    for p in psutil.process_iter():
        if p.name() == name:
            os.kill(p.pid, signal.SIGABRT)
    workerpool.WorkerMaster(**config.zworkers).stop('abort')
    print('%d aborted' % job_id)

abort.arg('job_id', 'job ID', type=int)