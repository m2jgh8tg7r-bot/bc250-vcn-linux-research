# R350 — live no-PGFSM-write PCI-read control

STAGE=R350_ATTEMPT_2_CONTROL_CHECKPOINT_CAPTURED_AND_MANUAL_RESET_CONFIRMED
RESULT=Exact input gate, AMDGPU init, matching pre/post PCI identity reads, no CONFIG write, and intended checkpoint panic/end were received
STATIC/LIVE=PACKAGE_STATIC_CHECKS_PASS; R350_CONTROL_PATH_CONFIRMED_LIVE
HARDWARE_ACCESS=AMDGPU initialization and PCI configuration reads observed
TARGETED_WRITE=PGFSM_CONFIG write omitted and explicit no-write marker received
VCN_STATUS_READ=NONE
VCN_EXECUTION=UNPROVEN
NORMAL_RECOVERY_AFTER_ATTEMPT_2=USER_REPORTED_MANUAL_RESET

## Preparation and boot control

R350 uses the paired R328 control module. It includes two PCI identity reads and omits the PGFSM_CONFIG MMIO write. The package passed signed executable-section comparison, depmod, exact initramfs roundtrip, and the existing no-write CPU harness. The image was installed after protected preflight; the exact R329 image and BLS entry were retained in a local backup. The normal BLS default stayed unchanged.

The first R350 boot attempt had no usable receiver capture. After a normal-boot UDP smoke test reached the receiver over the same wired source path and the resolved target MAC matched R350's configured target, the same R350 entry was re-armed. A fresh raw capture then received the retry boot. Private IP and MAC values are intentionally omitted.

## Attempt 2 — captured result

The pasted receiver excerpt begins with qualification 5/10. It contains qualification 5/10 through 10/10 and `QUALIFICATION_COMPLETE`; entries 1/10–4/10 are outside the excerpt. It also records `stdin_tty=YES`, the exact 18-byte token as `read_rc=0`, and `AMDGPU_MODPROBE_BEGIN`.

AMDGPU initialization proceeded through VCN IP discovery, software initialization, firmware version reporting and hardware phase 2. PSP VCN firmware enrollment was skipped by the existing R79 guard. The log then shows two display IRQ warning traces in `dal_irq_service_ack` and `dal_irq_service_set`; execution continued to the checkpoint. In the retained source, these functions assert when the selected callbacks are dummy handlers. The warning cause or broader display impact has not been investigated.

The VCN checkpoint reports the final discovery record matched (`die=0`, `count=3`, one VCN0 record, `base1=0x7e00`). The pre-read returned `ret=0` with PCI identity `0x13fe1002`, matching the expected identity. The control then explicitly logged that it performed no CONFIG write. The post-read also returned `ret=0` with the same identity and `match=1`.

The intended panic, `BC250 R328 PCI config completion checkpoint; no VCN STATUS read`, and the panic end marker were received. Thus the observed PCI identity reads returned on both sides of the deliberately omitted write, and the bounded control reached its planned endpoint. No VCN STATUS read or first helper VCN MMIO operation was performed. The run does not prove VCN power, firmware execution, ring execution, or hardware video decode/encode.


## Comparison with the earlier write candidate

The earlier R329 capture showed a successful pre-read, a returned CONFIG write, then a post-read begin marker without a captured return. In this R350 no-write control, both PCI identity reads returned successfully. This contrast raises the write-associated state change as a priority explanation for the earlier boundary, but does not prove causality: the R329 tail was incomplete, and the two live runs are not a repeated paired measurement under identical post-write state.

The entry uses `panic=0`; the user reports manually resetting after the planned panic. Whether the display returned normally was not reported. Preserve the original private JSONL capture. The pasted excerpt does not include qualification 1/10–4/10.
