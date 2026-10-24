#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import statistics
latencies=[10,11,12,13,15,18,21,30,90,150]
latencies.sort()
for pct in (50,95):
 idx=max(0,__import__('math').ceil(len(latencies)*pct/100)-1)
 print(f'p{pct}:',latencies[idx],'ms')
print('failure: long tail can be hidden by mean:',round(statistics.mean(latencies),1),'ms')
print('recovery: inspect slow requests, saturation and dependencies before scaling')
