#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
requests=[('GET',200,.05),('GET',200,.07),('POST',500,.20)]
print('counter completed:',len(requests))
print('server errors:',sum(500<=s<600 for _,s,_ in requests))
print('histogram_count:',len(requests),'histogram_sum:',round(sum(t for _,_,t in requests),3))
print('Failure: missing scrape target means missing data, not necessarily zero requests')
print('Recovery: inspect /metrics, scrape target health, labels and time window')
