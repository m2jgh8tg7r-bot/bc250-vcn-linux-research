# R222 — Saved BIOS type-0x13 candidate

STAGE=R222
RESULT=PROVEN_STATICALLY_CANDIDATE
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=The saved P3 BIOS PSP directory has a type `0x13` entry whose signed PS1 body checksum matches
REJECTED=Assuming the directory type is already proven identical to external PSP `fw_type 13`
UNPROVEN=Type semantic mapping, runtime selection, AUTOLOAD registration, VCN clamp release, VCN execution
NEXT=Decode this candidate and compare it with external t02/t28 / fw_type-13 descriptions

## Saved-image observation

The complete saved PSP directory at ROM `0x8e0000` has 19 entries. In addition to the previously documented type `0x8` SMU body and type `0x12` zero-template, entry index 5 is:

```text
directory type = 0x13
ROM offset     = 0x97f900
container size = 0x2000
PS1 header     = present at container+0x10
signed         = 1
encrypted      = 0
compressed     = 0
version       = 0x291c0001
body size      = 0x1e00
body SHA-256   = 413fcd1f3e87a7afc3c6ce28f4be550d79d04d182d3fd376e9726382de876654
header digest  = matches body SHA-256
```

The body begins with ARM code bytes (`20 d0 9f e5 ...`) rather than the Xtensa SMU body. This is a strong candidate for a PSP firmware/service payload, but its exact type meaning and runtime loading are not proven.

## Relation to external research

R220 external reports describe a PSP `fw_type 13` VCN path whose rejection prevents a cold-reset/clamp-release write. The numeric match to the saved directory type is a high-value lead. It is not yet an identity proof: directory type numbering and PSP command `fw_type` numbering must be checked against primary headers, loader tables, or decoded records. The earlier R218 TOS service-1 path remains a transport finding and does not establish that this type-0x13 container is selected.

No BIOS, PSP, SMU, or kernel mutation was made. No live read was performed.

## Sources

- [R220 external audit](../handoffs/BC250_VCN_handoff_CANONICAL_R220.md)
- [R214 saved PSP directory evidence](../r214-boot-image-selection/public/R214_DIRECTORY_EVIDENCE.json)
- [R218 saved TOS/load analysis](../handoffs/BC250_VCN_handoff_CANONICAL_R218.md)
