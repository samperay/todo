#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
total=10000;bad=17;target=99.9
sli=(total-bad)/total*100;budget=total*(1-target/100)
print('SLI availability:',round(sli,3),'%')
print('allowed bad requests:',round(budget,1),'observed:',bad)
print('failure: budget exceeded:',bad>budget)
print('recovery: prioritize reliability and reduce risky releases')
