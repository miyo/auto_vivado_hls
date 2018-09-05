import sys
from xml.etree.ElementTree import *

import generator

class CSynthReport:
    def __init__(self, version):
        self.version = version
        self.data = {}

    def name(self):
        return self.version + "("+ self.data['period']['target'] +")"


def parse_result(file):
    tree = parse(file)
    elem = tree.getroot()

    #for e in list(elem):
    #    print(e.tag)

    version = elem.find('./ReportVersion/Version')
    if version is None:
        return None
    
    report = CSynthReport(version.text)

    target = elem.find('./UserAssignments/TargetClockPeriod').text
    estimated = elem.find('./PerformanceEstimates/SummaryOfTimingAnalysis/EstimatedClockPeriod').text
    report.data['period'] = {
        'target': target,
        'estimated': estimated,
        'margin': str(float(target)-float(estimated)),
        }

    e = elem.find('./PerformanceEstimates/SummaryOfOverallLatency')
    report.data['latency'] = {
        'best':        e.find('./Best-caseLatency').text,
        'average':     e.find('./Average-caseLatency').text,
        'worst':       e.find('./Worst-caseLatency').text,
        'throughput':  e.find('./DataflowPipelineThroughput').text,
        'interval-min':e.find('./Interval-min').text,
        'interval-max':e.find('./Interval-max').text,
        }

    e = elem.find('./AreaEstimates/Resources')
    report.data['resources'] = {
        'bram18k': e.find('./BRAM_18K').text,
        'dsp48e':  e.find('./DSP48E').text,
        'ff':      e.find('./FF').text,
        'lut':     e.find('./LUT').text,
        }

    return report

if __name__ == '__main__':
    args = sys.argv
    if not (len(args) > 1):
	print('Usage python %s filename' % args[0])
	quit()

    reports = []
    for arg in args[1:]:
        r = parse_result(arg)
        if not (r is None):
            reports.append(r)

    for r in reports:
        print(r.version)
        print(r.data['period'])
        print(r.data['latency'])
        print(r.data['resources'])

    generator.write_csv('analysis_result.csv', reports)
    generator.write_graph('analysis_result.html', reports)
