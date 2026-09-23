# R207 — metrics拡張後のrecord境界と管理領域の静的監査

2026-09-21。保存Robin1と既存metricsパッチの**静的な組合せ**を監査。実機アクセス、パッチ適用、修正パッチの作成は行っていない。

## 結論

R206で確認したDCLK offset76→96の変更は、保存配布HEXにも一致する。しかし、このHEXが触れない旧管理領域を含めると、8-coreの平均recordと時刻・カウンターが重なる。従って、この組合せのmetrics全体を正しい8-core telemetryとして扱う根拠は不足する。実際に外部でこの組合せが動いたか、追加修正があったかは未確認。

## 固定入力と確認方法

- 原イメージSHA256: `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`
- 保存ソースcommit: `f686abcba57c5e4a25f39d4411a2c4b497a2f65d`
- 保存`patches.hex` SHA256: `89a53429c6467c9a20dd00215801a49059633d258c494355a56b41535f21501e`

独立したファイル読取専用parserで60 data recordsのchecksum・重複なし・終端を検証。Intel HEX type3は開始アドレスのmetadataで、書込みrecordに数えない。hardware libraryや元のpatcherはimport・実行しない。原イメージは変更しない。

DCLK current store、平均DCLK/Memclk store、平均Voltage storeについて、既存disassemblyのoperand prefixを原バイトと比較し、配布HEXのscaled immediateを検算した。単なるソース記述との比較より一段強いが、全パッチの機能検証ではない。

## 管理領域との重複

record baseは`0xCB54`。原版は116-byteのCurrentとAverageに、12-byte管理領域を続ける。保存metrics修正は136-byteのCurrent/Average配置を採用するが、以下の旧参照命令・base literalをHEXは変更しない。

| 相対byte範囲 | 原版の管理用途 | 拡張平均recordの用途 |
|---|---|---|
| 0xE8–0xEB | SampleStartTime | Average.DCLK / Memclk |
| 0xEC–0xEF | SampleStopTime | Average.Voltage[0] |
| 0xF0–0xF3 | Accnt | Average.Voltage[1] |

例えば平均DCLK store `0x298CB`は拡張後`base+0xE8`へ書く。一方、exportの`0x29AF8`は同じ場所をstart値として読み、`0x29B11/0x29CCD`はそこへ時刻を書き込む。平均countのread `0x29AD6` / write `0x29AE1`も旧位置のまま。異なるbase registerを使う命令は、`addmi -0x100`等を含めて同じ実効アドレスに正規化した。

PROVEN_STATICALLY: 上記命令をそのまま組み合わせるとアドレスが重なる。CPU byte-array例でも、旧start欄に設定した`0x12345678`が、平均DCLK=1111/Memclk=1750の二つの16bit storeで`0x06D60457`へ変わることを確認した。これは重複の説明であり、実機のscheduler・時刻・平均値のシミュレーションではない。

この重複を現在DCLK offset96の取り出しにそのまま拡張しない。R205/R206の限定的なDCLK由来値の対応は維持するが、平均値・管理値や全recordの健全性とは別問題である。

## resetとLinux読取サイズ

原reset `0x29804`は244 bytesを0にする。今回のHEXはその32-byte命令区間を変更しない。一方、export長の即値は284へ変更される。従って、このresetだけでは拡張領域の末尾40 bytes (`0xF4..0x11B`)を初期化しない。初期化の不足が実際に値へ影響したかは、他のwriter・初期状態・呼出し順が不明なので未証明。

固定Linux sourceのCyan初期化は`sizeof(SmuMetrics_t)`＝244をtable sizeとして設定する。`smu_cmn_update_table`と`smu_cmn_get_metrics_table`はその登録sizeでhost側へコピーする。Linux出力はその後128-byteのv2.2へ変換される。従って128-byte sysfs出力という長さだけでは、内部producerが244/284のどちらだったかを判別できない。今回確認したサイズ差だけからDMA領域外書込みや実機障害を断定しない。

## 保存policyとの追加照合

旧R125Aにはpolicy entry14（slot0x16）のold/targetがともに1111.0と記録される。これは既存記録であり、新しい実機測定ではない。R206でDCLK producer入力をslot0x16へ結び付けたことと合わせると、1111は通常の設定値として現れる値でもある。外部1111の直接の由来や適用完了は証明しないが、値の一致・不変だけで特別な停止sentinelだとは判定できない。

## 研究方針への反映

外部の「1111が移動／不変」は、producer・driverの版とrecord整合性を伴わない限り、VCNの状態変化を区別できる観測値として不十分。これは物理的にVCNを動かせないという証明ではない。既存の時刻・平均値を使う比較も、この版対応を確認してから採用する。

次は保存資料内で、適用済みpatch hash、対応driver定義、raw record/headerが揃うかを整理する。ライブ提案6条件のうち観測値の判別性は未充足。新規telemetry読出し・SMU要求・boot変更へは進まない。

[証拠](../logs/R207_STATIC_EVIDENCE.txt) / [ファイル読取専用検算器](../logs/R207_audit_saved_hex.py) / [前段R206](CHATGPT_HANDOFF_R206.md)。

```text
STAGE=R207_METRICS_RECORD_CONTRACT
RESULT=CONDITIONAL_METADATA_OVERLAP_IDENTIFIED
STATIC_OR_LIVE=STATIC_AND_BYTE_ARRAY_MODEL
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=SAVED_HEX_COVERAGE_AND_RECORD_ALIASING
REJECTED=128_BYTE_OUTPUT_PROVES_INTERNAL_LAYOUT_MATCH
UNPROVEN=EXTERNAL_RUNTIME_PAIR_ADDITIONAL_FIXES_EFFECTS
NEXT=SAVED_PROVENANCE_AND_OBSERVATION_CONTRACT
```
