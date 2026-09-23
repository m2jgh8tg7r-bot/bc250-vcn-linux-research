# R217 — Saved PSP Trusted OS load response and mutable service routing

STAGE=R217
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=Command 6 invokes service 1 through SVC F2; returned status is copied into the response; SVC 74 can populate its destination map
REJECTED=An initially zero service map alone proves the service is permanently disabled
UNPROVEN=Runtime TOS identity, actual service-1 destination, origin/meaning of 0xffff0008, VCN execution
NEXT=Trace service registration inputs and destination task image

保存BIOSのTrusted OSで、LOAD_IP_FW要求からサービス呼び出し、応答statusへの転記まで接続した。サービス宛先表には登録用の書込み処理があるため、保存時のゼロ表だけを根拠に「サービス無効」とする説明は採用しない。拒否コードの生成元はまだ特定していない。実機操作なし。

## Identity and coordinates

The saved ROM's PSP type-2 container starts at ROM offset `0x8eac00`, length `0x14350`. Its 256-byte header describes an uncompressed, unencrypted body of `0x14150` bytes and version `0x1c0002`; the final 256 bytes are outside that body. Body SHA-256 is `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`, matching the header digest. The full container matches the saved Robin1.00 and Robin3.00 distribution members. This checks content, not signature validity or running-firmware identity.

All offsets below are **body offsets**. Exported Ghidra addresses add an artificial analysis base of `0x200000`. Kernel literals use low addresses while user-side literals use `0x20xxxx`; a single linear runtime mapping is not established. Literal address `0x8430` is kept distinct from a proven live memory observation.

## Command and status path

1. Dispatcher `0x1043c` copies the command buffer and obtains command ID from buffer+8. The TBB at `0x1057e` uses table `0x10582`; entry 6 is `0x4a`, giving `0x10616`.
2. This branch calls wrapper `0xf3ca` with the request union at copied-buffer+`0x1c` and response pointer at buffer+`0x360`. These offsets agree with the local Linux `psp_gfx_if.h` command layout (source commit `0bb924b042ab85b8f529aed6e4f3e24750584276`).
3. Wrapper builds a message beginning `0x1007, 2`, selects pointer representation using helper `0x1002c`, and invokes `SVC 0xf2` at `0xf404` with `r0=1`, `r1=message`. Helper `0x1002c` itself may query service 1 using message `0x103b` and caches a mode value. The decompiler does not model SVC return-register changes: its apparent constant return must not be used as evidence.
4. On wrapper return, `0x10628` copies r0 to r7. Common code `0x10734` passes r7 as the third stack argument to response helper `0x10070`.
5. That helper's stack adjustment is 56 bytes; load `[sp+0x40]` obtains entry-SP+8 into r6. Stores at `0x1009e` and `0x100f8` write r6 unchanged into response status, on the respective response-buffer paths. Failure to obtain a usable response buffer is a separate path, not proof a response was written.

This locates a transport boundary for the historical `0xffff0008`; it does not decode that status or identify its producer.

## Service dispatch and registration

Extended SVC dispatcher `0x4f48` uses table `0x4f62`. SVC F2 (index 2, byte 9) reaches `0x4f74`, which loads saved r1 and tail-branches to `0x1ab8`.

That handler bounds service selector r0 to 0..15 and reads a destination byte from the table whose literal is `0x8430`. Zero destination returns `0x2f`. For a nonzero destination it validates context/stack constraints and reserves a slot in a task record of stride `0x5c`. It installs the destination record's entry address (record+4) in the saved context. Thus this is task/service dispatch, not a direct IP firmware verifier at this boundary.

Ordinary SVC dispatcher `0x45a0` routes SVC `0x74` to `0x4c82`, then helper `0x37ec`. That helper checks destination ID via `0x1724` (ID<32 and bit31 set in its descriptor at literal base `0x69b0`), checks selector<16, and executes `strb r3,[r1,r2]` at `0x3806` with the same table literal `0x8430`. The check preserves r2/r3. A user-side instruction sequence invokes SVC 74 at `0x121f6`, using r5 as selector and a byte from its stack as destination. The full containing function and the origins of those two inputs are not established here. Another raw SVC 74 candidate at `0x130cc` is a follow-up lead, not a proven startup route.

The existence of this writer rejects an inference of permanent disablement from an initial zero table. It does **not** prove service 1 is registered in the historical boot, nor that its implementation is in this same container.

## Verification and limits

`R217_verify_route.py` verifies the exact body hash, each exported instruction's raw bytes, both TBB calculations, the SVC 74 relative table entry, selected call/store instructions, and shared table literals. It is an offline evidence check, not a hardware emulator or an independent semantic proof. Raw firmware is not included.

TBB offset arithmetic follows [Arm's branch instruction explanation](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/branch-and-call-sequences-explained). Ghidra function names assigned to switch cases/snippets are analysis conveniences and must not be interpreted as original function boundaries.

No new live experiment is ready: a discriminating observation of the registered service and its implementation has not yet been prepared. Continue static registration and image-provenance work; no firmware replacement, speculative SVC invocation or memory write is proposed.
