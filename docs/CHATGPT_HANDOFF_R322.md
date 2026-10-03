# R322 — Retained discovery evidence and export limitations

STAGE=R322
RESULT=No relevant full discovery capture identified in scoped inventory; sysfs export cannot exclude duplicate records
STATIC_OR_LIVE=Saved-file inventory and PROVEN_STATICALLY export implementation
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Separate sysfs copies, per-die instance naming, unchecked instance-add result, debugfs heap-blob binding
REJECTED=One sysfs instance necessarily means one source record; debugfs blob necessarily preserves raw acquisition bytes
UNPROVEN=Actual duplicate records, final helper bases, full relevant-boot discovery availability outside searched scope, VCN execution
NEXT=Bounded offline discovery inspection when a provenance-matched capture exists; no unchanged hanging-read trial

## Inventory and limits

The scoped filename inventory examined 54,974 names beneath the research root, excluding retained kernel trees, packaged root filesystems, firmware trees and selected build/source directories. Candidate names included discovery, receiver, transcript and jsonl. raw/ is empty and saved is a zero-length regular file. Named candidates were source/object evidence, metadata summaries, receiver scripts or unrelated session ledgers. The R273 discovery-203.txt candidate is a source-search transcript, not binary discovery data.
No full R318 or failed CP06/07 discovery capture was identified by this search. This is a scoped negative, not proof that no differently named file, archive member, excluded directory or external receiver capture exists. LOCAL_INVENTORY.json remains private; it is not a raw-log publication.
R319 records that the supplied receiver command printed UDP data without saving raw datagrams. Its transcript establishes the named intended panic; it cannot reconstruct a full discovery record inventory.

## Why sysfs cannot settle duplicates

In the retained source, amdgpu_discovery_sysfs_ips builds a separate heap object and copies record bases (1250–1267). It registers instance names under hardware-ID and die parents (1269–1272). Same-instance records on different dies have different parents, whereas same-die duplicates attempt the same name. The return from instance kobject_add is assigned to res but not checked before advancing; this function ultimately returns 0 (1285). This alone is not proof of a registration collision on the machine, but a single visible entry cannot certify source-record uniqueness or final reg_offset identity. The register parser separately retains the last matching pointer as established in R320/R321.

## Existing memory-backed export

amdgpu_discovery.c:349–350 binds debugfs_blob.data/size to the device-owned discovery allocation. amdgpu_debugfs.c:2228–2230 registers amdgpu_discovery with debugfs_create_blob if the size is nonzero. The reviewed registration points to the already-loaded heap buffer, rather than a fresh register or VRAM acquisition callback. No current debugfs file was opened in this stage; the running driver's exact implementation and export availability are not attested.
The parser changes revision bits and converts base addresses in place (R320/R321). Therefore a later exported blob is post-parser memory evidence: do not call it untouched firmware data or assume original checksums remain valid. With 64-bit bases, 32-bit converted entries coexist in the original record allocation; a raw wire-layout parser alone may misinterpret them.
Any future offline reader must explicitly distinguish original acquisition format from post-parser memory format, validate all table/record bounds and retain boot/source provenance. A normal-boot export could constrain normal metadata, but would not prove historical CP06/07 state or the helper's final pointer. No export acquisition, build, installation or reboot is requested or performed here.
