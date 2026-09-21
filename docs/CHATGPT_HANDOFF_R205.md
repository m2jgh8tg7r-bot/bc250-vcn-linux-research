# R205 — offset44へのDCLK混入仮説とR204の解釈補足

2026-09-21。外部固定commit `edb222c65477b6ebc63834ef3562855009179539`の完全treeと関連29テキストを取得し、各Git blob hashを照合。ダウンロードしたコードは実行していない。実機アクセスなし。

## R204から進んだ点

**offset44のABIフィールド名が電力であることは、そこにDCLK由来の値が入らない証明ではない。** R204のlayout計算と保存サンプル復号は正しいが、内部PMFW形式とドライバー形式の不一致をさらに分ける必要がある。

[外部の前日報告](https://github.com/Shalasere/bc250-vcn-research/blob/edb222c65477b6ebc63834ef3562855009179539/research/SMU_EXPLOIT_CHAIN_RESULT_2026_09_13.md)には、パッチ前の1111はoffset74/86、8-core metricsパッチ後はoffset44と記される。内部形式の変更を報告しているので、単純なv2.2欄名の誤認だけでこの履歴を否定できない。一方、同報告は平均／現在の呼称をローカルv2.2と逆にしており、Linux ABIそのものが移動したという説明も確認できていない。

## CPU上の条件付き再現

既存CyanのPMFW構造体は6-core配列。**仮説として**4種類の`[6]`配列だけを`[8]`へ拡張した構造体を作り、C compilerでoffsetを比較した。実パッチの全変更を再現したものではない。

| PMFW record | size | VCLK | DCLK | Memclk | Power[0] |
|---|---:|---:|---:|---:|---:|
| 既存6-core定義 | 116 | 74 | 76 | 78 | 96 |
| 仮説8-core定義 | 136 | 94 | 96 | 98 | 116 |

little-endianで仮説8-core recordのDCLK=1111、Memclk=1750としたバッファを6-core定義で解釈すると、`Power[0]`の下位16bitは1111になる。既存Cyanコードはこれを16bitの`gpu_metrics_v2_2.average_soc_power`、つまりoffset44へ代入する。

```text
hypothetical PMFW8 Current.DCLK @96
  -> stale PMFW6 Current.Power[0] @96 (low 16 bits)
  -> gpu_metrics_v2_2.average_soc_power @44
```

PROVEN_CPU_MODEL: 上記条件なら、**Linux側のABI offsetを一切変えずに**DCLK由来値がoffset44へ入る。これは外部報告の1111移動とCONSISTENT_WITH。

UNPROVEN: 外部の実際の8-core patch、raw PMFW record、kernel decoder、overlay状態がこの仮説と完全に一致すること。ローカルR72の1111も同じ原因かは未証明。実際のclock動作・VCN活性も未証明。値1111を探すだけでは、意味のあるsentinelや物理clockを同定したことにならない。

## 方針への影響

R204の「ローカルv2.2でoffset44というフィールドはDCLKではない」は維持する。一方、それだけで外部の1111を無関係な電力値と決めつけることはできない。必要な証拠は外部の既存header/raw record/patch版とdriver mappingの組合せである。

現状の公開treeにはgpu_metrics専用raw capture・header・decoderを独立した成果物として確認できなかった。29ファイルの限定内容検索であり、全コード・別repository・非公開記録に不存在とは言わない。操作成功、SMU側lock全般の否定、VCN電源や実行成功のいずれにも格上げしない。

R201のSSC解釈、R202のfeature lifecycle、R203のpower bookkeepingと併せ、実機への新規操作を必要とする根拠はまだ得ていない。次は保存資料だけで内部metrics producerと既存driver変換の対応を追い、仮説に留まる部分を絞る。外部のexploit実装や適用には進まない。

[条件付きCPUモデルとoffset結果](../logs/R205_STATIC_EVIDENCE.txt)。[R204](CHATGPT_HANDOFF_R204.md)。

```text
STAGE=R205_METRICS_LAYOUT_MISMATCH_MODEL
RESULT=R204_INTERPRETATION_QUALIFIED
STATIC_OR_LIVE=STATIC_AND_CPU_MODEL
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=CONDITIONAL_DCLK_TO_OFFSET44_MAPPING
REJECTED=ABI_FIELD_NAME_ALONE_EXCLUDES_DCLK_ORIGIN
UNPROVEN=ACTUAL_EXTERNAL_LAYOUT_AND_PHYSICAL_CLOCK
NEXT=SAVED_METRICS_PRODUCER_MAPPING
```
