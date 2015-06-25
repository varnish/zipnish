import varnishapi,time,os,sys,syslog,traceback


class LogDataManager:

    def __init__(self):
        self.sessionVxId = 0;
        self.logSessions = {}
        return '__init__'

    def beginSession(self, vxid):
        self.sessionVxId = vxid

    def closeSession(self, vxid):
        self.sessionVxId = 0

    def addLogItem(self, tag, data):
        return 'added log item'


class LogReader:
    def execute(self,vap):
        #connect varnishapi
        self.vap = vap
        while 1:
            ret = self.vap.Dispatch(self.vapCallBack)
            if 0 == ret:
                time.sleep(0.5)

    def vapCallBack(self,vap,cbd,priv):
        level       = cbd['level']
        vxid        = cbd['vxid']
        vxid_parent = cbd['vxid_parent']
        type        = cbd['type']
        tag         = cbd['tag']
        data        = cbd['data']
        isbin       = cbd['isbin']
        length      = cbd['length']
        t_tag = vap.VSL_tags[tag]
        var   = vap.vut.tag2VarName(t_tag,data)

        #print "level:%d vxid:%d vxid_parent:%d tag:%s var:%s type:%s data:%s (isbin=%d,len=%d)" % (level,vxid,vxid_parent,t_tag,var,type,data,isbin,length)
        print "vxid:%d, tag:%s, data:%s" % (vxid, t_tag, data)

        #print "data "
        #print str(data)

        #if data.rsplit(':', 1)[0] == 'X-Varnish':
        #   print str(data)

def main(smp):
    try:
        #vap = varnishapi.VarnishLog(['-i', ''])
        vap = varnishapi.VarnishLog()
        smp.execute(vap)
    except KeyboardInterrupt:
        vap.Fini()
    except Exception as e:
        syslog.openlog(sys.argv[0], syslog.LOG_PID|syslog.LOG_PERROR, syslog.LOG_LOCAL0)
        syslog.syslog(syslog.LOG_ERR, traceback.format_exc())

if __name__ == '__main__':
    shmLog = LogReader()
    main(shmLog)
