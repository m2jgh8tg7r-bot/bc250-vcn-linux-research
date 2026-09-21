# R204 — 外部DCLK proxyのABI監査

2026-09-21。保存済みソースとR72サンプルのみ使用。新規gpu_metrics読出し・SMU要求・実機操作なし。

## 結果

外部報告はgpu_metricsのoffset44で1111が不変だったことをDCLK proxyとして扱う。一方、版を固定したローカルCyanドライバーの出力形式は`gpu_metrics_v2_2`であり、**offset44はDCLKではなく`average_soc_power`**である。

| フィールド | byte offset | 保存R72の値 |
|---|---:|---:|
| average_soc_power | 44 | 1111 |
| average_vclk_frequency | 72 | 1128 |
| average_dclk_frequency | 74 | 1114 |
| current_vclk | 84 | 34 |
| current_dclk | 86 | 15 |

表はフィールドの復号値であり、実際の電力や動作周波数の正しさを検証したものではない。平均値と現在値の差だけから停止・動作を判定しない。

## 再現根拠と既存研究との差

ローカルkernel source基準commit `0bb924b042ab85b8f529aed6e4f3e24750584276`の`kgd_pp_interface.h`から実際の二つの構造体を抽出し、C compilerの`sizeof`/`offsetof`で検算した。size128、DCLK offsets74/86は既存R69Fの結果と一致し、構造体定義SHA256も`39619060b8a7a2af413bc0f88baabf27ddecf1a45eba536152816b2ae5494719`で一致する。ABI自体は新発見ではなく、外部proxyとの照合が今回の追加点。

`cyan_skillfish_get_gpu_metrics`は形式2.2を明示し、`average_soc_power`に`metrics.Current.Power[0]`、DCLKの平均・現在欄に対応するPMFW欄を代入する。保存R72ファイルは128 bytes、header `(128,2,2)`、SHA256 `3c1a775982d3666d07a06afcf622145529ef1879974a25d2215e1666f8c49c1d`。既存R72採取記録に同じhashとnative sysfs underlayの確認がある。今回は保存ファイルを再復号しただけである。

[外部報告の固定版](https://github.com/Shalasere/bc250-vcn-research/blob/4499a7c9fc4fd340c1fda82631b9a0b5f34d611e/research/SMU_AUTHORITY_WRITE_TESTS_2026_09_14.md)はR200で取得・blob照合済み。外部側のraw header、driver版、decoder、overlay有無が揃わないため、外部の値をこちらのABIへ無条件に割り当てない。1111の一致だけでは同じ誤読だったとも断定しない。

## 証拠の扱い

PROVEN_STATICALLY: ローカルv2.2でoffset44をDCLKと読むことは誤り。

UNRESOLVED: 外部側の形式と読み取り実装。別形式・独自加工の可能性は残る。

NOT_ESTABLISHED: 外部の1111不変からDCLK不変、VCN全体の電源状態、SMU側lock全般の否定を導くこと。正しいDCLK欄でも、周波数欄だけではfirmware placementやVCPU/ring動作は証明できない。

次に必要なのは新たな操作実験ではなく、外部の既存raw header・decoder・driver版の対応資料。既存公開資料で追跡し、なければ未確認として維持する。保存Robin1の制御フロー解析を優先する方針は継続。

[復号・layout証拠](../logs/R204_STATIC_EVIDENCE.txt)。[Domain6 bookkeeping](CHATGPT_HANDOFF_R203.md)。R197を再実行する根拠は得ていない。

```text
STAGE=R204_SAVED_METRICS_ABI_AUDIT
RESULT=EXTERNAL_DCLK_PROXY_NOT_VALIDATED
STATIC_OR_LIVE=STATIC_AND_SAVED_CAPTURE
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=LOCAL_V2_2_OFFSET44_IS_AVERAGE_SOC_POWER
REJECTED=OFFSET44_IS_DCLK_IN_LOCAL_V2_2
UNPROVEN=EXTERNAL_ABI_AND_PHYSICAL_CLOCK_STATE
NEXT=EXTERNAL_SAVED_DECODER_PROVENANCE
```
