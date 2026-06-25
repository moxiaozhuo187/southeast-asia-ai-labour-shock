import csv

inp='tool_index_2015_2024.csv'
outp='04e_hbase_puts.hbase'

out=open(outp,'w')

with open(inp,'r') as f:
reader=csv.DictReader(f)
for r in reader:
if r['year']!='2024':
continue

```
    key=r['country_code']+'#'+r['year']

    out.write("put 'labour_profile','%s','meta:country_name','%s'\n" % (key,r['country_name']))
    out.write("put 'labour_profile','%s','meta:is_benchmark','%s'\n" % (key,r['is_benchmark']))
    out.write("put 'labour_profile','%s','meta:year','%s'\n" % (key,r['year']))
    out.write("put 'labour_profile','%s','vulnerability:evi_main','%s'\n" % (key,r['evi_main']))
    out.write("put 'labour_profile','%s','readiness:dri','%s'\n" % (key,r['dri']))
    out.write("put 'labour_profile','%s','result:risk_gap','%s'\n" % (key,r['risk_gap']))
```

out.write("count 'labour_profile'\n")
out.close()

print('created '+outp)
