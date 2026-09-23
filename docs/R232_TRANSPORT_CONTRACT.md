# R232 — platform mailboxとVCN経路の区別

2026-09-23。公開patchの文章と固定Linux sourceを照合。driverの導入、PCI binding、mailbox送信、MMIOアクセスは実施していない。

## sourceの範囲

Linux sourceはcommit `704340f1cd0dcef829eb62f5b48ae95a2ce17bdf` に固定した。取得URL・SHA-256は `../logs/R232/kernel-source-manifest.json`。ccp関連7ファイルと`psp_gfx_if.h`は保存R152 source treeとbyte一致した。`amdgpu_psp.c`と`psp_v11_0.c`は同一ではないため、以下の上流契約は取得した固定commitを根拠にする。ローカルtreeのtagや外部試験kernel 7.2.6へ無条件には転用しない。

## transport比較

| 層 | source上のtransport / selector | 確認できること | それだけでは確認できないこと |
|---|---|---|---|
| ccp platform access | `pa_v1`: C2PMSG **28/29/30**。mapped BAR内byte offset `0x10570/0x10574/0x10578` | host request bufferの物理アドレスを渡し、platform commandを送る契約 | amdgpu firmware受理、PSP内部SVC実行、VCN ring実行 |
| ccp TEE init | pspv3系のC2PMSG **17/18/19**、offset `0x10544/0x10548/0x1054c`。TEE_RING_INIT enum=1 | TEE ring作成を別mailboxで要求 | platform access成功とTEE ring成功の同一性 |
| amdgpu PSP KM ring制御 | PSP v11.0.8の非VF分岐: C2PMSG **64**、base **69/70**、size **71**、wptr **67** | GPCOM/KM ringの設定・frame投入 | VCN自身のhardware ring実行 |
| amdgpu PSP ring payload | `GFX_CMD_ID_LOAD_IP_FW=6`, `GFX_FW_TYPE_VCN=13` | firmware種類を伴うhost request | BIOS directory type13との同一性、受理・VCPU実行 |
| 保存TOSの内部service呼出し | SVC **0xf2**、r0=service selector0..15、r1=request pointer等 | `0x8430` map経由の内部destination選択 | C2PMSG番号やhost fw_typeとの同一性 |
| 保存TOS descriptor割当 | SVC **0x64**、classとslot出力pointer | R218/R232で確認したallocator契約 | platform command0x64との同一性 |

C2PMSG末尾の番号はregisterのindexであり、SVC immediateやmailbox command値ではない。BAR内byte offsetとamdgpuのSOC15 register indexも単位・基準が違うため、そのまま数値比較しない。

版選択も確認した。固定上流の`amdgpu_psp.c`はMP0 11.0.8かつCYAN_SKILLFISH2 flagで専用のv11.0.8 callbackを選び、`autoload_supported=false`を設定する。[専用callback](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/psp_v11_0_8.c)でも表の非VF register契約を確認した。通常v11の名前だけからCyanへ転用した結論ではない。専用fileはweb textで確認し、ローカルfileとの全byte一致は主張しない（`../logs/R232/kernel-variant-review.json`）。`autoload_supported=false`はこのLinux driverの選択であり、PSP内部の全autoload機構の不存在を証明しない。

根拠: [sp-pci.c](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/crypto/ccp/sp-pci.c)、[psp-dev.c](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/crypto/ccp/psp-dev.c)、[tee-dev.c](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/crypto/ccp/tee-dev.c)、[psp_v11_0.c](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/psp_v11_0.c)、[psp_gfx_if.h](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/psp_gfx_if.h)。

## platform accessのcommand/status契約

`psp_send_platform_access_msg()` はrecovery bit30が0かを確認し、response bit31を待つ。request bufferの物理アドレスをlow/highへ書き、commandをbits23:16に置いて送信する。完了待ちの後、low/highが自分のbufferアドレスのままかを確かめ、mailbox status bits15:0とrequest header.statusを評価する。header.statusが非zeroなら`-EIO`になる。ready bitだけではpayload成功を証明できない。[platform-access.c](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/crypto/ccp/platform-access.c)、[psp.h](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/include/linux/psp.h)

platform enumの `0x64` はI2C bus request、次の `0x65` はdynamic boostのnonce取得。この `0x65` を保存TOSのSVC65（descriptor cleanup側）と結び付けない。[psp-platform-access.h](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/include/linux/psp-platform-access.h)

## 9月19日投稿の採用範囲

[patch 3/3](https://lists.openwall.net/linux-kernel/2026/09/19/922)はPCI `1022:143e` 向けに、platform accessのみを持つvdataを追加する提案。著者はTEE ring timeoutと、platform command0x65に対するstatus4も報告している。[cover letter](https://lists.openwall.net/linux-kernel/2026/09/19/969)は試験kernel 7.2.6、bootloader表示 `00.1c.01.02` を記載する。

sourceとの対応はplatform mailboxがTEE ringとは別という説明を支持する。ただし著者実機の結果をローカルPROVEN_LIVEへ移さない。`bootloader_version` sysfs属性は専用registerの4 byteを表示する契約であり、保存TOS本文hashやservice image hashではない。数字の一部が保存TOS versionに似ていても同一性の証拠にはならない。

また`platform access enabled`の表示点は、固定sourceの`platform_access_dev_init()`が構造体・vdata・mutexを設定した後にある。この関数自身はmailbox requestを送らないため、その表示だけを通信往復の成功証拠にはしない。投稿にあるDBC commandのstatus4は別の観測であり、platform commandが成功したという意味でもない。

このpatchからR232のPSP-private row/descriptor/mapを読む観測口は確認できない。従って今回の未証明リンクを調べるためだけにccp driverを追加・bindingする実機試験は準備しない。platform accessを独立した研究目的で検証する場合は、VCN受理・実行とは別の成功条件を設ける必要がある。
