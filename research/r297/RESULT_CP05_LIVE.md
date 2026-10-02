# R297 CP05 LIVE Result

## 判定

**R297 CP05 = LIVE PASS**

BC-250 実機上で、最初の意図した VCN MMIO write 経路を実行し、
WREG 呼び出しから CPU 側へ return して、
write 直後の checkpoint まで到達した。

## LIVE で観測した決定的シーケンス

```text
[    7.410959] amdgpu 0000:01:00.0: BC250 R291P1 pre_reset: begin
[    7.410961] amdgpu 0000:01:00.0: BC250 R297 CP05: helper_entry before guards
[    7.410963] amdgpu 0000:01:00.0: BC250 R297 CP05: guards_pass before PGFSM_CONFIG
[    7.410966] amdgpu 0000:01:00.0: BC250 R297 CP05: after PGFSM_CONFIG write before status wait
[    7.410969] Kernel panic - not syncing: BC250 R297 CP05 after PGFSM_CONFIG write before status wait
```

## LIVE で証明できたこと

- R291P1 pre-reset path に到達
- CP05 helper に到達
- pg_flags / cg_flags guard を通過
- SR-IOV VF guard を通過
- PGFSM_CONFIG に 0x55555 を書く WREG 経路を実行
- WREG 呼び出しから return
- write 直後の checkpoint に到達
- 意図した kernel panic に到達

installed machine-code audit と組み合わせることで、
first intended VCN MMIO write path の LIVE 実行を証明した。

## 同一 boot の前段

R274B firmware direct-copy も成功している。

```text
BC250 R274B direct_copy: bytes=405696 src_off=256 dst_off=0 bo=1069056 equal=1
```

## Evidence

Decisive EFI pstore:

```text
dmesg-efi_pstore-179094055003001
SHA-256: 90cfaa270a661fce3132d3083a0b7dc3502b1f05856e864173c0a5576c50a91a
```

LIVE collection log:

```text
bc250-r297-cp05-attempt2-live-collect.log
SHA-256: 38e4c79434a01c003dedb9f947ef3f9d6642ed58b28a5871c39453e9da4f1cda
```

## まだ証明していないこと

CP05 は最初の write の直後で意図的に停止しているため、
以下はまだ未証明。

- PGFSM_CONFIG readback
- PGFSM_STATUS の応答
- UVD_POWER_STATUS
- VCN power island の実際の状態変化
- VCPU execution
- firmware ready
- VCN rings
- decode / encode
- VA-API

## 次の段階

次の checkpoint では、CP05 で LIVE 安全性を確認した
PGFSM_CONFIG write の直後から、最小限の status 観測へ進む。
