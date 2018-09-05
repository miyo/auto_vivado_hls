import random

def write_csv(dest, reports):
    
    with open(dest, 'w') as file:
        file.write('timing met' + '\n')
        for r in reports:
            file.write(','.join([r.name(),
                                 str(float(r.data['period']['target']) > float(r.data['period']['estimated']))
            ]) + '\n')
        file.write('\n')

        file.write('period' + '\n')
        file.write(',target,estimated,margin' + '\n')
        for r in reports:
            file.write(','.join([r.name(),
                                 r.data['period']['target'],
                                 r.data['period']['estimated'],
                                 r.data['period']['margin'],
            ]) + '\n')
        file.write('\n')

        file.write('latency summary' + '\n')
        file.write(',best,average,worst,througput,interval-min,interval-max' + '\n')
        for r in reports:
            file.write(','.join([r.name(),
                                 r.data['latency']['best'],
                                 r.data['latency']['average'],
                                 r.data['latency']['worst'],
                                 r.data['latency']['throughput'],
                                 r.data['latency']['interval-min'],
                                 r.data['latency']['interval-max'],
            ]) + '\n')
        file.write('\n')

        file.write('resources' + '\n')
        file.write(',BRAM_18K,DSP48E,FF,LUT' + '\n')
        for r in reports:
            file.write(','.join([r.name(),
                                 r.data['resources']['bram18k'],
                                 r.data['resources']['dsp48e'],
                                 r.data['resources']['ff'],
                                 r.data['resources']['lut']
            ]) + '\n')
        file.write('\n')

def gen_chart(id, key, labels, reports, colortbl):
    
    chartname = 'chart{}'.format(id)
    str = ""
    str += '<canvas id="{}" style="width: 100%; height: 300px;"></canvas>\n'.format(chartname)
    str += '<script>\n'
    str += 'var {0} = new Chart(document.getElementById("{0}"),\n'.format(chartname)
    str += '''
{
  title: 'fefe',
  type: 'bar',
  data: {
'''
    str += "labels: [{0}],\n".format(','.join(['"{}"'.format(l) for l in labels]))
    str += '''
  datasets: [
'''
    datasets = []
    for i, r in enumerate(reports):
        s = '{'
        s += "label: '{}',".format(r.name())
        s += "data: [{}],".format(','.join([r.data[key][l] for l in labels]))
        s += "backgroundColor: 'rgba({0}, {1}, {2}, 0.2)',".format(colortbl[i][0], colortbl[i][1], colortbl[i][2])
        s += "borderWidth: 1"
        s += "}"
        datasets.append(s)
    str += ','.join(datasets)
    str += '''
    ]
  },
  options: {
    scales: { yAxes: [{ ticks: { beginAtZero:true } }] }
  }
}
'''
    str += ");\n"
    str += "</script>\n"
    return str

def gen_color(i, num):
    return [random.randint(0, 255) for _ in range(3)]

def write_graph(dest, reports):
    colortbl = [gen_color(i, len(reports)) for i in range(len(reports))]
    
    with open(dest, 'w') as file:
        file.write('''
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
    </head>
    <body>

        <!-- load Chart.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js"></script>
'''
        )
    
        file.write(gen_chart(0, 'period', ['target', 'estimated', 'margin'], reports, colortbl) + '\n')
        file.write(gen_chart(1, 'latency', ['best', 'average', 'worst', 'throughput', 'interval-min', 'interval-max'], reports, colortbl) + '\n')
        file.write(gen_chart(2, 'resources', ['bram18k', 'dsp48e', 'ff', 'lut'], reports, colortbl) + '\n')

        file.write('''
    </body>
</html>
'''
        )

