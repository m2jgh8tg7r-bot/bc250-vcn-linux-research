# R203 — Domain6 bookkeeping と自動PLL電源policy

2026-09-21。保存Robin1/SMU 88.6.0（SHA256 `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`）だけを解析。実機アクセスなし。R201/R202と同じアドレス対応を使用。

## power要求の省略条件

PROVEN_STATICALLY: descriptor6は`0xF700`、baseは`0x6D000`。`+0x14`はpower helperのソフトウェア記録、`+0x15/+0x16`はSSC要求/適用記録として別々に扱われる。保存ファイルでは順に1/0/0だが、実行中の値を示さない。

`0x23B14(index, request)`は`descriptor+0x14 == request`ならレジスターの読出しも書込みも行わず戻る。異なる場合はrequest/status/sequenceを操作・pollしてから記録を更新する。descriptor6の対象はstatus `0x6D190`、request `0x6D17C`、sequence `0x6D184`。確認したpoll loopにはtimeoutがない。これは静的な処理記述であり、実行手順・実行許可ではない。

`0x2362C`にも`+0x14 == 0`の場合のみpower helperを呼ぶ条件がある。従って、要求を送った／関数が戻った／記録が1という事実だけでは、その回に物理状態を確認・変更した証拠にならない。全VCN電源やde-isolationとの対応も未証明。

初期化`0x234A0`はdescriptorのclock設定とslot値を取り込むが、本体に`+0x14`を物理powerから再計測する処理はない。他の間接・bulk writerの不存在までは主張しない。

## callback slot25の自動policy

PROVEN_STATICALLY: feature表index4はenable `0x23C24` / disable `0x23C34`。enableはcallback slot25へ`0x23BB8`を登録し、disableはno-opへ置き換える。feature13のslot24とは独立である。既存walkerの昇順走査では、両方登録されている場合、slot24のpolicy applyの次にslot25を処理する。実際の登録状態・呼出し時刻は未観測。

`0x23BB8`の既存命令を検査した結果、resource mask `0x40000`の区間で次を行う。

1. 8 descriptor分のローカルusedフラグを消す。
2. 27 clock slotを走査する。canonical base `0xF710`、stride `0x1C`に対し、slotの`+0x98 == 0`かつcached code `+0x82 != 0`なら、`+0x80`が示すdescriptorをusedにする。
3. usedでないdescriptorだけに`0x23B14(index, 0)`を呼ぶ。

命令中のbaseは`0xF71C`なので、そこでのoffset `0x8C/0x76/0x74`をcanonical baseへ正規化した。usedならpower-onする処理ではなく、power-off要求を抑制する処理である。VCNのjobやVCPU実行状態を直接pollする判定ではない。

Domain6に対応するslotは`0x16/0x17/0x18`。旧R125Bに保存されたslot codeは`0x12/0x00/0x14`（十進18/0/20）だが、同時点のmode `+0x98`は揃っていない。mode0の非zero codeがあればusedになるという条件は示せても、旧実機で実際にどちらへ分岐したかは断定しない。

## modeと周波数値の由来

`0x2387C`はslot設定レジスターからmodeを読み`+0x98/+0x99`へ保存する。`0x2375C`はmode設定を変更し、そのソフトウェアコピーも更新する。`0x2362C`は必要ならmodeを切り替えてからcodeを扱う。`0x23CB4`が作る周波数欄はcached code等からの計算であり、この関数自体は物理周波数カウンター測定ではない。

これらは「Domain6 policy」「clock設定・ソフトウェア記録」「ブロック電源」「de-isolation」「firmware placement」「VCPU」「ring」「VA-API」を一段ずつ分ける必要性を補強する。ライブ提案6条件は未充足のまま。

[静的証拠](../logs/R203_STATIC_EVIDENCE.txt)。次は外部のDCLK proxyを既存Linux ABIと保存サンプルで監査する。

```text
STAGE=R203_DOMAIN6_BOOKKEEPING
RESULT=STATIC_PATHS_RECONSTRUCTED
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=BOOKKEEPING_SKIP_AND_CACHED_SLOT_POLICY
REJECTED=FUNCTION_RETURN_ALONE_PROVES_PHYSICAL_POWER
UNPROVEN=RUNTIME_FLAGS_WHOLE_VCN_POWER_EXECUTION
NEXT=SAVED_METRICS_ABI_AUDIT
```

2026-09-21 R207監査時訂正: 上記codeの16進表記を明示。以前の12/0/14表記は基数が不明瞭だった。保存レジスターcodeとSMU cached fieldの同時一致は別の証拠を要する。
