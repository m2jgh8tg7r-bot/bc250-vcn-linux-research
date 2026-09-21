# R209 — 保存Domain6 statusとhelper待機条件の照合

2026-09-21。R203で復元した固定Robin1 `0x23B14`の条件を、保存R125A/Bの読出し値へ当てはめた。旧採取スクリプトは実行せず、新規実機アクセス・要求・書込みなし。

## 対応関係

固定イメージのdescriptor6はstatus `0x6D190`、sequence `0x6D184`を使う。旧採取スクリプトの`DOM6_STATUS`と`DOM6_RAIL`がこのアドレスへ対応することをソースで確認した。旧ラベルRAILだけで電源railの物理意味を確定せず、ここではsequenceとして扱う。

`0x23B14`のrequest1経路はstatus bit8が立つまで、続いてsequence bit16が消えるまでpollする。request0経路のstatus条件は別のbit12である。requestとbookkeepingが一致すると全処理をskipする条件はR203の通り。

| 保存採取 | phase | status | sequence | request1側の各poll述語 |
|---|---|---|---|---|
| R125A | PRE / POST | 0x01010101 | 0 | ともに成立 |
| R125B | PRE / MID / POST | 0x01010101 | 0 | ともに成立 |

5組をCPU上で再計算し、status `&0x100 != 0`、sequence `&0x10000 == 0`を確認した。同じstatusに対し`&0x1000 != 0`は偽。bit8とbit12を同じ「ready」判定にまとめない。

PROVEN_SAVED_EVIDENCE: 上記値は既存ログに記録されている。PROVEN_STATICALLY: 保存値は原helperのrequest1側述語に一致する。保存中の各readは同時・atomic snapshotではなく、実際のhelper実行途中に読み取った値でもない。

## この照合で言えること

「helperが戻った」「poll条件を満たす値が読めた」だけでは、その要求によって新たな変化が起きたことを示さない。今回の保存基準値はすでにその述語を満たしているため、成功・不変という結果には新規遷移のない説明が残る。

これは当時helperが確実にskipしたという証明でも、statusが固定値・無効値だという証明でもない。runtime bookkeepingの同時値、実際の呼出し経路、要求直後の挙動は揃っていない。また、このstatusの物理意味がVCN全体電源・de-isolation・VCPU生存に対応することも未証明。

R208のDCLK target不変と同様に、判別できる観測には「何が変わればどの仮説を区別できるか」が必要になる。今回は条件を既存データで吟味しただけで、状態を変えるための追加実験を提案・許可していない。

## 引き継ぎ

R207: metrics拡張recordと管理領域の重複を保存HEXで確認。R208: DCLK proxyの判別性とCyan feature名の対応を整理。R209: Domain6 helperの成功条件が既存基準値で成立することを確認した。

この3点はいずれもVCN動作可否そのものを決定しない。現方針は静的解析のまま。外部の実適用版・同時状態・物理対応資料が不足しており、ライブ提案6条件は未充足。保存R197の再実行、新規BAR scan、未知呼出し、ring/VCPU実行なし。

[述語検算と原命令証拠](../logs/R209_STATIC_EVIDENCE.txt) / [R208](CHATGPT_HANDOFF_R208.md) / [R203](CHATGPT_HANDOFF_R203.md)。

```text
STAGE=R209_SAVED_DOMAIN6_PREDICATES
RESULT=BASELINE_ALREADY_SATISFIES_REQUEST1_PREDICATES
STATIC_OR_LIVE=STATIC_AND_SAVED_CAPTURE
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=SAVED_STATUS_MATCHES_FIXED_HELPER_PREDICATES
REJECTED=SUCCESS_PREDICATE_ALONE_PROVES_NEW_TRANSITION
UNPROVEN=SIMULTANEOUS_RUNTIME_STATE_AND_WHOLE_VCN_POWER
NEXT=VERSION_MATCHED_EXTERNAL_STATE_PROVENANCE
```
