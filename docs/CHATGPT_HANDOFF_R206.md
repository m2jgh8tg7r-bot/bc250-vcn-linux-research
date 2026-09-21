# R206 — 保存Robin1のmetrics producerと8-core形式修正の照合

2026-09-21。R205の条件付きモデルを、保存済み原イメージ・metrics形式修正ソース・Linux変換コードで照合した。実機アクセス、patch適用、firmware生成、boot変更なし。

## 追加で確認できたこと

保存Robin1 SHA256 `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`の関数`0x29AEC`は、literal `0x17F24`が指す`0xCB54`を出力record baseとして扱う。DCLKに対応する書込みは`0x29B71: s16i a15,a2,0x4c`。これは6-core PMFW定義のCurrent.DclkFrequency offset76と一致する。

保存済み[metrics形式修正ソース](https://github.com/rw-r-r-0644/bc250-smu-unlock/blob/f686abcba57c5e4a25f39d4411a2c4b497a2f65d/patches/metrics-8core.s)は、同じ命令の格納offsetを`0x60`＝96へ変更する。ローカルcheckoutはclean、ソースSHA256は`fd82de34257d6353693d0853ea7eecb736f4763f57981855885d825ce4b96d7a`。このファイルはテキストとして読んだだけで、assemble・実行・適用していない。

| 対象 | 保存原命令のoffset | 保存修正ソースのoffset |
|---|---:|---:|
| Current SOC clock | 0x48 | 0x5c |
| Current VCLK | 0x4a | 0x5e |
| Current DCLK | 0x4c | 0x60 |
| Current Memclk | 0x4e | 0x62 |
| Current Power配列 | 0x60 | 0x74 |
| export長の即値 | 0xf4 (244) | 0x11c (284) |

6-core record116 bytes×2+12=244、8-core record136 bytes×2+12=284とも一致する。表の名称は既存PMFW構造体との対応から付けたもので、全field・全patch・export末端の完全検証ではない。

PROVEN_STATICALLY: 保存修正ソースには、R205で仮定したDCLK offset96への変更が具体的に存在する。STRONGLY_SUPPORTED: このソースを適用したproducerを既存6-core driverで読むと、DCLKの下位16bitがLinux v2.2の`average_soc_power` offset44へ入るという説明。外部実験がこのcommit・driverの組合せだったことは未証明のため、外部環境の再現成功には格上げしない。

## DCLK/VCLK値の元は何か

原イメージの命令列を追うと、`0x29B47`が`0xFA00`のfloatを読み、1000.0fを掛け、整数変換後に前述のDCLK欄へ保存する。VCLKは`0xFA1C`から同様に作る。

この二つのアドレスは、R203で調べた`0x23CB4(slot)`のclock計算出力と一致する。

```text
DCLK source: 0xF718 + 0x16 * 0x1C + 0x80 = 0xFA00
VCLK source: 0xF718 + 0x17 * 0x1C + 0x80 = 0xFA1C
```

これにより、この版のLinux欄名に対応するproducer入力はDCLK=slot0x16、VCLK=slot0x17と結び付く。slot番号を他版・別資料のラベルへ無条件に転用しない。

`0x23CB4`はmodeとcached codeを参照し、code0の経路では出力を0にする。それ以外ではdescriptorのclock値や代替mode表から出力を計算する。今回追った経路はVCNの物理周波数カウンター・VCPU heartbeat・ring completionを測るものではない。別writerの不存在や、cached値を作る全経路の物理的正しさは未証明。

平均欄を更新する`0x29848`も同じ`0xFA00/0xFA1C`を読む。helper `0x29824`は整数の`old * count + new`と`count + 1`をfloatに変換して数値helperへ渡し、結果を整数へ戻す。ここにも独立したclock測定はない。整数overflow・浮動小数点丸め・実際の更新間隔を含む完全な平均モデルは未検証。平均と現在の一致を独立した二つの物理観測とは扱えない。

追加で`0x1C9C8`がcached codeから区分的な数値変換を行うhelperであることを命令で確認した。原版のreset `0x29804`は0x7A個の16bit要素、計244 bytesを0にする。この原版の処理を修正適用後の全挙動へ転用せず、今回の照合が形式修正全体の正当性検証ではないことを明示する。

## 方針

R204のABI欄名確認、R205の形式不一致モデル、今回の保存修正ソースを合わせると、外部offset44の1111を単に無関係な電力値と退けるべきではない。一方、DCLK由来である可能性が強まっても、その値だけでVCN電源や停止原因は確定しない。1111が特別なsentinelであることも今回の処理では証明していない。

静的解析を継続し、次はmetrics形式変更後のrecord境界・resetと、外部driver版の対応を保存資料で追う。未知呼出し・レジスター書込み・新規metrics読出しは行わない。ライブ提案6条件は未充足のまま。

[命令抜粋と照合結果](../logs/R206_STATIC_EVIDENCE.txt)。[前段R205](CHATGPT_HANDOFF_R205.md)。

```text
STAGE=R206_SAVED_METRICS_PRODUCER
RESULT=LAYOUT_MODEL_SUPPORTED_BY_SAVED_SOURCE
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=SAVED_DCLK_STORE_OFFSET_CHANGE_AND_COMPUTED_INPUT
REJECTED=CLOCK_FIELD_ALONE_PROVES_VCN_EXECUTION
UNPROVEN=EXTERNAL_EXACT_PATCH_DRIVER_PAIR_AND_PHYSICAL_STATE
NEXT=RECORD_BOUNDARIES_AND_EXTERNAL_DRIVER_PROVENANCE
```
