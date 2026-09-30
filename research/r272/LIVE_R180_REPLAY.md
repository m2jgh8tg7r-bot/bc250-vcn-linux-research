# R272 live R180 replay evidence

## Same-boot analyzer summary

```json
{
  "result": "PROVEN_LIVE",
  "module_and_boot_attributed": true,
  "capture_hashes_verified": 14,
  "identity_note_correspondence": true,
  "response_consistency": "CONSISTENT_WITH",
  "enrollment_log_conditions_met": false,
  "observation_complete": "PROVEN_LIVE",
  "selective_response_pattern": "PROVEN_LIVE",
  "trace_issues": []
}
```

## Loaded module identity

```text
loaded_module_build_id=9e4870cde4dfbec0c4dab01a3a7667bd1c153223
expected_module_build_id=9e4870cde4dfbec0c4dab01a3a7667bd1c153223
kernel_release=7.2.3+
r180_metadata_correspondence=true
```

## VCN request

```text
id=57
command=6
fw_type=13
size=405696
source_aligned=1
source_matches=1
bo_present=1
map_present=1
iomem=0
map_matches=1
bounds_ok=1
header_ok=1
payload_checked=1
payload_equal=1
```

## R180 LOAD_IP_FW comparison

```text
1/9/33536      -> status=0x0,        fw_addr_nonzero=0
2/10/33536     -> status=0x0,        fw_addr_nonzero=0
12/3/263040    -> status=0x0,        fw_addr_nonzero=1
13/2/263168    -> status=0x0,        fw_addr_nonzero=1
14/1/263168    -> status=0x0,        fw_addr_nonzero=1
26/4/267440    -> status=0x0,        fw_addr_nonzero=1
27/5/896       -> status=0x0,        fw_addr_nonzero=0
28/4/267440    -> status=0x0,        fw_addr_nonzero=1
29/6/896       -> status=0x0,        fw_addr_nonzero=0
50/8/25088     -> status=0x0,        fw_addr_nonzero=0
57/13/405696   -> status=0xffff0008, fw_addr_nonzero=0
```

All had ret=0, submitted=1, response_valid=1, matching fence, timeout remaining, ras_intr=0.

## Analyzer classification

```text
trace_pair_count=11
trace_structure_valid=true
accepted_control_count=5
accepted_control_ids=[12,13,14,26,28]
selective_response_conditions_met=true
selective_response_pattern=PROVEN_LIVE
observation_complete=PROVEN_LIVE
root_cause=UNPROVEN
host_request_result=PROVEN_LIVE
```

## Normal recovery

After manual boot back to Bazzite:

```text
kernel=7.2.1-ogc4.1.fc44.x86_64
enp4s0=UP
wlp0s16f0u2i2=UP
failed_units:
  bc250-tdp.service
```

No causal claim is made about the service failure.
