# R218 — Service-1 bootstrap and mapped-memory provenance

STAGE=R218
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=Bootstrap passes special-load flag 1; loader selects service 1; source base comes from SVC 73 and a kernel mapping initializer
REJECTED=Interpreting user absolute pointers with the kernel's file-offset mapping
UNPROVEN=Execution of this path in the historical boot, loaded service image bytes, rejection producer, VCN operation
NEXT=Trace boot-context field +0x23c and initial mapping register provenance; match service image to saved artifacts if possible

実機試験を待たず静的研究を継続。R217で見つけた宛先登録を、起動側の特殊ロード経路とメモリー変換処理まで追跡した。サービス1の実体をTOS内の固定関数と決め付けず、別途ロードされるイメージの由来を次の調査対象とする。拒否コード `0xffff0008` の生成元は依然未特定。

## Coordinate correction before following absolute pointers

Same body SHA-256 as R217: `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`. All code locations below are body offsets; exports still use the artificial base `0x200000`.

Two independent pointer-to-code pairs strongly support a user-section mapping of body `0xe000` to address `0x200000`:

- ARM entry at body `0xe000` loads SP through literal `0x206060`, then loads branch target `0x203609` and executes BX. Removing the Thumb bit and applying this section mapping yields body `0x11608`, a coherent initializer.
- That initializer passes literal `0x2042c5` to SVC 51 at body `0x11740`; the same mapping yields body `0x122c4`, a coherent bootstrap/task sequence.

This is STRONGLY_SUPPORTED static layout, not a live relocation measurement. For user pointers, body `0x60c8` is therefore not the right counterpart of address `0x2060c8`; the proposed counterpart is `0x140c8`. R217 deliberately left runtime mapping unresolved and used relative branches/body offsets for its main conclusions; those conclusions do not require a single linear mapping.

## Bootstrap and loader inputs

At body `0x122e6`, the bootstrap loads user address `0x2060e8`. At `0x122fc` it takes a low/high source pair from +0x30/+0x34, passes length `0x20000`, and sets the first stack argument to 1 at `0x1230a` before calling loader `0x11a04`.

The loader saves 52 bytes of registers and reserves `0x13c` bytes, so its entry-SP first stack argument is current-SP+`0x170`. Its nonzero test at `0x11a78` selects an alternate input from `*[0x2060c8]`. This means the special path uses the SVC-derived mapped base; the bootstrap's original low/high pair is not simply treated as an on-ROM file offset.

The loader maps the input at user address `0x20a000` through SVC 62, and checks the image structure at `0x20a100`. It accepts markers `0x4154` or `0x5244`. In the special path `0x11b6a` explicitly sets r5=1 and the task class to 2. In the ordinary driver path helper `0xfe64` obtains the service selector using property string `amd.dr.driverID` at body `0xfe8c`; ordinary TA handling selects zero separately.

Task creation at `0x11cc0` invokes SVC 64 with output pointer SP+`0x60`. Its kernel case calls `0x180c`, which finds an available descriptor among IDs 1..31, marks bit31 and the class, and writes the ID to the output byte. This same byte is passed as destination to SVC 74 at `0x121f6`; selector comes from r5. On the driver-marked success path, later TA-specific r5 reassignment is skipped by the branch at `0x120ca` to `0x121be`.

This proves an encoded conditional bootstrap route for service 1, not that every validation/mapping succeeds at runtime. Called helpers and SVCs are not emulated, and SVC-blind decompiler output cannot establish reachability or a constant return.

## Source-base chain

- User initializer `0x11652` invokes SVC 73, storing its returned r0 at user `0x206068+0x60 = 0x2060c8`.
- SVC 73 case `0x4c7e` returns `*[0x601c]`.
- Kernel initializer `0x50a8` reads a context pointer from `0x6030`, then its field +`0x23c`. It masks that value to 26 bits and writes `0x04000000 + masked_offset` into `0x601c` at `0x50de`.
- The same initializer constructs translation slot 0 at literal `0x8730`, using a value read from literal address `0x03230000`, and stores a 64-bit translated source pair at kernel `0x60e8+0x10`.
- User initializer calls SVC 80 with r0 equal to the SVC-73 base and r1=`0x206118` (`0x206068+0xb0`). SVC 80 dispatches to `0x1f70`, which translates a mapped input using 64-MiB slots from tables `0x8730` or `0x8440`, storing two words through r1. This connects to the pair later read by the bootstrap at `0x2060e8+0x30`.

Thus the unresolved image-provenance boundary is now concrete: context field +`0x23c`, mapping state and the bytes at the resulting base. None of these values is established by a zero-filled static data region. No exact service-image ROM range or historical live address is claimed.

## Verification and next work

`R218_verify.py` pins the full body hash, compares exported instruction bytes, checks the SVC-case relative-table arithmetic, pointer literals, coordinate calculations and key instructions. Raw BL candidates in the local scan were used only to find caller leads; the recovered instruction stream confirms the relevant call at `0x1230c`. The scan is not an exhaustive control-flow proof.

No new hardware test is ready. A safe observation path to this PSP-private mapped region has not been identified, so speculative reads/writes are not a prepared experiment. Continue with the saved kernel/boot-loader context producer and image inventory. Do not infer PSP acceptance or VCN execution from this static route.
