"""Independent small-width increment enumeration and scientific negative controls."""
from analyze_counter import analyze
from pathlib import Path
import copy,json
base={'counter_model':'unsigned_modulo_up','counter_width_bits':4,'counter_identity':'synthetic','mapping_provenance':'synthetic','timebase_provenance':'synthetic monotonic ns','boot_context':'synthetic','configuration_identity':'synthetic','independent_max_rate_counts_per_second':10,'max_rate_basis':'synthetic independent cap','samples':[{'t_ns':0,'count':1,'valid':True},{'t_ns':1_000_000_000,'count':4,'valid':True}]}
cases=0
for width in range(1,5):
 modulus=1<<width
 for a in range(modulus):
  for b in range(modulus):
   for cap in sorted({1,modulus-1,modulus,modulus+3,2*modulus+1}):
    d=copy.deepcopy(base);d.update(counter_width_bits=width,independent_max_rate_counts_per_second=cap);d['samples'][0]['count']=a;d['samples'][1]['count']=b
    candidates=[n for n in range(cap+1) if (a+n)%modulus==b]
    row=analyze(d)['intervals'][0];assert row['bound_consistent']==bool(candidates)
    assert row['unique_delta_under_supplied_bound']==(len(candidates)==1)
    assert row['rate_counts_per_second']==(candidates[0] if len(candidates)==1 else None);cases+=1
controls=[]
def control(name,mutate,predicate):
 d=copy.deepcopy(base);mutate(d);assert predicate(analyze(d)),name;controls.append(name)
control('no cap leaves wrap ambiguous',lambda d:d.pop('independent_max_rate_counts_per_second'),lambda r:r['intervals'][0]['rate_counts_per_second'] is None)
control('missing provenance withholds rate',lambda d:d.pop('timebase_provenance'),lambda r:r['intervals'][0]['rate_counts_per_second'] is None)
control('invalid sample withholds rate',lambda d:d['samples'][1].update(valid=False),lambda r:r['intervals'][0]['rate_counts_per_second'] is None)
control('reset excludes interval',lambda d:d['samples'][1].update(reset_or_reconfigured=True),lambda r:all(r['intervals'][0][k] is None for k in ['rate_counts_per_second','minimum_modular_rate_counts_per_second','bound_consistent','additional_wraps_possible']))
control('unknown counter model withholds rate',lambda d:d.pop('counter_model'),lambda r:r['intervals'][0]['rate_counts_per_second'] is None)
control('requested rate does not affect arithmetic',lambda d:d.update(requested_rate_hz=1250000000),lambda r:r['intervals'][0]['rate_counts_per_second']==3)
for rate in [800000000,1250000000]:
 d=copy.deepcopy(base);d.update(counter_width_bits=32,independent_max_rate_counts_per_second=2000000000);d['samples']=[{'t_ns':0,'count':0,'valid':True},{'t_ns':1000000,'count':rate//1000,'valid':True}]
 assert analyze(d)['intervals'][0]['rate_counts_per_second']==rate;controls.append('synthetic '+str(rate)+' counts/s')
for mutation in [lambda d:d.update(counter_width_bits=True),lambda d:d['samples'][1].update(t_ns=0),lambda d:d['samples'][1].update(count=16),lambda d:d.update(max_rate_basis='')]:
 d=copy.deepcopy(base);mutation(d)
 try:analyze(d)
 except ValueError:pass
 else:raise AssertionError('Invalid input accepted')
result={'result':'PASS','exhaustive_small_width_cases':cases,'named_controls':controls,'invalid_input_controls':4,'hardware_measurement':False,'external_gpcnt_data_replayed':False}
Path(__file__).with_name('counter-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',cases,'independent enumeration cases;',len(controls),'named controls;4 invalid inputs')
