"""Analyze saved counter samples; never access a device or infer VCPU execution."""
import argparse,json
from pathlib import Path

def integer(x,name,minimum=0):
 if isinstance(x,bool) or not isinstance(x,int) or x<minimum:raise ValueError(name+' must be an integer in range')
 return x

def analyze(data):
 width=integer(data.get('counter_width_bits'),'counter_width_bits',1)
 if width>64:raise ValueError('counter width exceeds64')
 samples=data.get('samples')
 if not isinstance(samples,list) or len(samples)<2:raise ValueError('At least two saved samples required')
 modulus=1<<width;bound=data.get('independent_max_rate_counts_per_second');bound_source=data.get('max_rate_basis','')
 if bound is not None:
  integer(bound,'independent_max_rate_counts_per_second',1)
  if not isinstance(bound_source,str) or not bound_source.strip():raise ValueError('An independent rate-bound basis is required')
 required=['counter_identity','mapping_provenance','timebase_provenance','boot_context','configuration_identity']
 missing=[k for k in required if not isinstance(data.get(k),str) or not data[k].strip()]
 if data.get('counter_model')!='unsigned_modulo_up':missing.append('counter_model unsigned_modulo_up not established')
 rows=[]
 for sample in samples:
  if not isinstance(sample,dict):raise ValueError('Sample must be an object')
  integer(sample.get('t_ns'),'t_ns');integer(sample.get('count'),'count')
  if sample['count']>=modulus:raise ValueError('Counter outside declared width')
  if sample.get('valid') is not True:missing.append('sample validity')
 for a,b in zip(samples,samples[1:]):
  dt=b['t_ns']-a['t_ns']
  if dt<=0:raise ValueError('Timestamps must increase strictly')
  delta=(b['count']-a['count'])%modulus
  row={'elapsed_ns':dt,'modular_delta':delta,'minimum_modular_rate_counts_per_second':delta*1_000_000_000/dt,
       'unique_delta_under_supplied_bound':False,'additional_wraps_possible':None,'rate_counts_per_second':None}
  # Integer arithmetic bounds all possible actual increments without using requested frequency.
  if bound is not None:
   maximum=(bound*dt)//1_000_000_000
   if delta>maximum:row['bound_consistent']=False
   else:
    wraps=(maximum-delta)//modulus;row.update({'bound_consistent':True,'additional_wraps_possible':wraps,'unique_delta_under_supplied_bound':wraps==0})
    if wraps==0:row['rate_counts_per_second']=row['minimum_modular_rate_counts_per_second']
  if a.get('reset_or_reconfigured') or b.get('reset_or_reconfigured'):
   row.update(rate_counts_per_second=None, minimum_modular_rate_counts_per_second=None, bound_consistent=None, additional_wraps_possible=None, unique_delta_under_supplied_bound=False, excluded='Reset/reconfiguration reported; modular_delta is raw arithmetic only')
  if missing:row['rate_counts_per_second']=None
  rows.append(row)
 return {'classification':'PROVEN_STATICALLY','scope':'Arithmetic over supplied saved samples; no authenticity verification','missing_provenance':sorted(set(missing)),
         'counter_width_bits':width,'supplied_counts_change':any(a['count']!=b['count'] for a,b in zip(samples,samples[1:])), 'intervals':rows,'requested_frequency_used_in_calculation':False,
         'rate_unit':'counter increments per second; not automatically clock cycles per second','physical_clock_source_proven':False,'vcpu_execution_proven':False,
         'limits':['The supplied bound must bound actual increments over each interval; a nominal oscillator frequency alone does not establish this (sampling phase, read latency and timestamp uncertainty matter)','A supplied independent bound is not independently verified by this program','Timing uncertainty and read latency are not measured; results use supplied timestamps','A modulo lower bound of zero does not prove a stopped clock','No cross-counter equivalence is inferred']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(json.dumps(analyze(json.loads(a.input.read_text())),indent=2)+'\n')
