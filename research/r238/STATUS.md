# R238 — platform PSP identity interfaces

Pinned Linux source has supported `ccp` sysfs `bootloader_version` and `tee_version` attributes. They are register-backed values formatted as four hexadecimal bytes. Documentation identifies the former as AGESA bootloader firmware and the latter as AMD TEE firmware. This is a real counterexample to any blanket assertion that every Linux PSP version interface is merely a cached firmware-file field.

Visibility requires an initialized PSP object, an applicable nonzero register offset, and a readable value other than all-ones. TEE additionally requires the TEE capability bit. Zero itself is not hidden by this function. Missing attributes therefore do not uniquely identify missing firmware, a disabled device or a particular silicon state.

`ccp` binds a table of 13 AMD vendor **1022** device IDs; the Cyan GPU driver binds vendor **1002**, device **13FE/143F**. These are different driver endpoints. No bridge from the inspected platform interface to GPU service1, selected KDB or live VCN image identity was demonstrated. This is not proof that the physical PSPs or firmware environments must be separate, nor proof that such a bridge cannot exist elsewhere. No platform endpoint was queried on this machine.

`TEE_IOC_VERSION` through amdtee returns implementation ID and capability constants, not a TEE firmware version, image hash or KDB inventory. An API named version must not be treated as an image identity measurement without checking its producer.

Q36 local GPU assistance: the first tool-enabled review lost the task during compaction and was discarded. A bounded no-tools review completed in 60 seconds with 2010 generated tokens and no context truncation. Its classifications were checked independently; scalar-offset wording, omitted PSP-null gate and overly strong separation wording were corrected. Model output is advisory, never a primary source.

Sources: pinned source hashes and excerpts in `results.json`; [AMD-TEE documentation](https://docs.kernel.org/tee/amd-tee.html), [TEE userspace API](https://kernel.org/doc/html/latest/userspace-api/tee.html), [ABI reference](https://www.kernel.org/doc/html/v7.0/admin-guide/abi-testing.html). No research device access or mutation occurred; local AI used GPU_COMPUTE.

Publication cross-check: at official Linux commit `fd179f8a05be3ccae366b9b96e176b51fbe54aab`, five of six inspected platform source/ABI files are wholly byte-identical to the local snapshot. pci_ids.h differs elsewhere, but AMD1022/ATI1002 definitions were independently verified with current line links. `upstream-comparison.json` records this and the exact source hashes.
