#!/usr/bin/env python
import csv
import sys
import re

total = 0
sse2 = 0
multicore = 0
fourcore = 0
core_sum = 0
core_max = 0
windowsxp = 0
amd = 0

def has_sse2(vendor, family, model, stepping):
    if vendor == 'AuthenticAMD' and family >= 15:
        return True
    if vendor == 'GenuineIntel' and family >= 15 or (family == 6 and (model == 9 or model > 11)):
        return True
    if vendor == 'CentaurHauls' and family >= 6 and model >= 10:
        return True
    return False

def has_sse2(vendor, family, model, stepping):
    if vendor == 'AuthenticAMD' and family >= 15:
        return True
    if vendor == 'GenuineIntel' and family >= 15 or (family == 6 and (model == 9 or model > 11)):
        return True
    if vendor == 'CentaurHauls' and family >= 6 and model >= 10:
        return True
    return False

breakdown = {}
reader = csv.reader(sys.stdin, delimiter='\t')
for row in reader:
    if row[6] != "Firefox":
        pass
    if row[7] != "17.0.1" and row[7] != "18.0" and row[7] != "19.0" and row[7] != "20.0" and row[7] != "21.0" and row[7] != "22.0":
        #print row[6], row[7]
        pass
        #continue
    if row[10] == 'Windows NT':
        if row[11].find('5.1') == 0:
            windowsxp += 1
    cpuinfo = [i.strip() for i in row[12].split("|")]
    #print [i.strip() for i in cpuinfo]
    if len(cpuinfo) > 1:
        cpu_type = cpuinfo[0]
        cpu_model = cpuinfo[1]
        cores = cpuinfo[2]
        if cpu_type == 'x86':
            #print cpu_model
            try:
                # AuthenticAMD family 16 model 6 stepping 3
                m = re.match(r"(?P<vendor>\w+) family (?P<family>\w+) model (?P<model>\w+) stepping (?P<stepping>\w+)", cpu_model)
                [vendor, family, model, stepping] = (m.group('vendor'), int(m.group('family')), int(m.group('model')), int(m.group('stepping')))
        
                if vendor == "AuthenticAMD":
                    amd += 1
                if has_sse2(vendor, family, model, stepping):
                    sse2 += 1
                if True:
                    key = (vendor, family, model)
                    if key in breakdown:
                        breakdown[key] += 1
                    else:
                        breakdown[key] = 0
                    pass
                if int(cores) >= 2:
                    multicore += 1
                if int(cores) >= 4:
                    fourcore += 1
                core_sum += int(cores)
                core_max = max(core_max, int(cores))
                total += 1

            except:
                pass

descriptive_names = {'AuthenticAMD': {6:
    {3: 'Athlon Duron',
        4: 'Athlon',
        6: 'Athlon XP',
        7: 'Duron Morgan',
        8: 'Athlon (Palomino) XP/Duron',
        10: 'Athlon MP'},
    5:{8:'K6-2'},
    15:{107:'AMD64 X2'},
    16:{2: 'Athlon II X2',
        3: 'Phenom II X3',
        4: 'Athlon II X4',
        5: 'Athlon II X4',
        6: 'AMD64 Athlon II' },
    20:{1:'AMD64 C-50',
        2:'AMD64 C-60'},
    },
    'CentaurHauls': {6:
        {7:'VIA Ezra/Samuel 2'}},
    'GenuineIntel': {6:
        {
        5:'Pentium II Deschutes 0.25 um',
        6: 'Pentium II Mendocino 0.25 um',
        7:'Pentium III Katmai 0.25 um',
        8:'Pentium III Coppermine 0.18 um',
        11:'Pentium III Tualatin 0.13 um',
        13:'Pentium M',
        14:'Core Duo 65nm',
        15:'Core 2 Duo Allendale/Kentsfield 65nm',
        22:'Core based Celeron 65nm',
        23:'Core 2 Duo 45nm',
        28:'Atom',
        37:'Core i[735] Westmere',
        38:'Atom',
        42:'Core i[735] Sandybridge',
        58:'Core i[735] Ivybridge',
        },
        15: {
            1:'Pentium 4 Willamette 180nm',
            2:'Pentium 4 Northwood 130nm',
            3:'Pentium 4 Prescott 90nm',
            4:'Pentium 4 Prescott 2M 90nm',
            6:'Pentium D',
            }
        }}
def describe(vendor, family, model):
    name = ""
    if vendor in descriptive_names:
        if family in descriptive_names[vendor]:
            if model in descriptive_names[vendor][family]:
                return descriptive_names[vendor][family][model]
    return name

for i in sorted([(i[1], i[0]) for i in breakdown.items()], reverse=True):
    print i[1], 100.*breakdown[i[1]]/(total), describe(i[1][0], i[1][1], i[1][2])
print "sse2", "%s%%" % (sse2*100./total)
print "amd", "%s%%" % (amd*100./total)
print "coreavg", 1.*core_sum/total
print "coremax", core_max
print "mulicore", "%s%%" % (multicore*100./total)
print "windowsxp", "%s%%" % (windowsxp*100./total)
#print "windowsxp",  (windowsxp, total)
print "fourcore", "%s%%" % (fourcore*100./total)
