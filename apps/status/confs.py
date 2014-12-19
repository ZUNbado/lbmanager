
class GraphConf():
    GRAPH={
            'CPU': """DEF:idle=RRDFILE/cpu-0/cpu-idle.rrd:value:AVERAGE
DEF:nice=RRDFILE/cpu-0/cpu-nice.rrd:value:AVERAGE
DEF:user=RRDFILE/cpu-0/cpu-user.rrd:value:AVERAGE
DEF:waitio=RRDFILE/cpu-0/cpu-wait.rrd:value:AVERAGE
DEF:system=RRDFILE/cpu-0/cpu-system.rrd:value:AVERAGE
DEF:softirq=RRDFILE/cpu-0/cpu-softirq.rrd:value:AVERAGE
DEF:interrupt=RRDFILE/cpu-0/cpu-interrupt.rrd:value:AVERAGE
DEF:steal=RRDFILE/cpu-0/cpu-steal.rrd:value:AVERAGE
AREA:steal#000000:"Steal"
AREA:system#fd0000:"System":STACK
AREA:waitio#fdaf00:"Wait-IO":STACK
AREA:nice#00df00:"Nice":STACK
AREA:user#0000fd:"User":STACK
AREA:softirq#fd00fd:"Soft-IRQ\c":STACK
AREA:interrupt#9f009f:"IRQ":STACK
AREA:idle#e7e7e7:"Idle\c":STACK
""",

        'MEM': """DEF:bavg=RRDFILE/memory/memory-buffered.rrd:value:AVERAGE
DEF:bmin=RRDFILE/memory/memory-buffered.rrd:value:MIN
DEF:bmax=RRDFILE/memory/memory-buffered.rrd:value:MAX
DEF:cavg=RRDFILE/memory/memory-cached.rrd:value:AVERAGE
DEF:cmin=RRDFILE/memory/memory-cached.rrd:value:MIN
DEF:cmax=RRDFILE/memory/memory-cached.rrd:value:MAX
DEF:favg=RRDFILE/memory/memory-free.rrd:value:AVERAGE
DEF:fmin=RRDFILE/memory/memory-free.rrd:value:MIN
DEF:fmax=RRDFILE/memory/memory-free.rrd:value:MAX
DEF:uavg=RRDFILE/memory/memory-used.rrd:value:AVERAGE
DEF:umin=RRDFILE/memory/memory-used.rrd:value:MIN
DEF:umax=RRDFILE/memory/memory-used.rrd:value:MAX
AREA:uavg#ff0000:"Used        "
GPRINT:umin:MIN:"%5.1lf%sB Min"
GPRINT:uavg:AVERAGE:"%5.1lf%sB Avg"
GPRINT:umax:MAX:"%5.1lf%sB Max"
GPRINT:uavg:LAST:"%5.1lf%sB Last\l"
AREA:bavg#f0a000:"Buffer cache":STACK
GPRINT:bmin:MIN:"%5.1lf%sB Min"
GPRINT:bavg:AVERAGE:"%5.1lf%sB Avg"
GPRINT:bmax:MAX:"%5.1lf%sB Max"
GPRINT:bavg:LAST:"%5.1lf%sB Last\l"
AREA:cavg#0000fd:"Page cache  ":STACK
GPRINT:cmin:MIN:"%5.1lf%sB Min"
GPRINT:cavg:AVERAGE:"%5.1lf%sB Avg"
GPRINT:cmax:MAX:"%5.1lf%sB Max"
GPRINT:cavg:LAST:"%5.1lf%sB Last\l"
AREA:favg#00cc00:"Free        ":STACK
GPRINT:fmin:MIN:"%5.1lf%sB Min"
GPRINT:favg:AVERAGE:"%5.1lf%sB Avg"
GPRINT:fmax:MAX:"%5.1lf%sB Max"
GPRINT:favg:LAST:"%5.1lf%sB Last\l"
""",

        'LOAD': """DEF:savg=RRDFILE/load/load.rrd:shortterm:AVERAGE
DEF:smin=RRDFILE/load/load.rrd:shortterm:MIN
DEF:smax=RRDFILE/load/load.rrd:shortterm:MAX
DEF:mavg=RRDFILE/load/load.rrd:midterm:AVERAGE
DEF:mmin=RRDFILE/load/load.rrd:midterm:MIN
DEF:mmax=RRDFILE/load/load.rrd:midterm:MAX
DEF:lavg=RRDFILE/load/load.rrd:longterm:AVERAGE
DEF:lmin=RRDFILE/load/load.rrd:longterm:MIN
DEF:lmax=RRDFILE/load/load.rrd:longterm:MAX
LINE1:savg#00cc00:" 1 min"
GPRINT:smin:MIN:"%4.2lf Min"
GPRINT:savg:AVERAGE:"%4.2lf Avg"
GPRINT:smax:MAX:"%4.2lf Max"
GPRINT:savg:LAST:"%4.2lf Last\l"
LINE1:mavg#0000fd:" 5 min"
GPRINT:mmin:MIN:"%4.2lf Min"
GPRINT:mavg:AVERAGE:"%4.2lf Avg"
GPRINT:mmax:MAX:"%4.2lf Max"
GPRINT:mavg:LAST:"%4.2lf Last\l"
LINE1:lavg#ff0000:"15 min"
GPRINT:lmin:MIN:"%4.2lf Min"
GPRINT:lavg:AVERAGE:"%4.2lf Avg"
GPRINT:lmax:MAX:"%4.2lf Max"
GPRINT:lavg:LAST:"%4.2lf Last\l"
"""
    }


    def getallconf(self, base_path):
        confs={}
        for (graph, conf) in self.GRAPH.items():
            confs[graph]=conf.replace('RRDFILE',base_path)
        return confs

    def getconf(self, graph_type, base_path):
        return self.GRAPH[graph_type].replace('RRDFILE', base_path)
