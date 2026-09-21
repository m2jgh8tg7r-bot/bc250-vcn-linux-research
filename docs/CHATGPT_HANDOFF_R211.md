# R211 — 0xCEE1 / SSC候補のcaller lifecycle

2026-09-21。R201の固定Robin1イメージで、既知xrefから四つのcallerを復元し、R208のfeature5 callbackへ接続した。複製Ghidra projectのreadOnly解析のみ。実機アクセスなし。

## callbackからの接続

R208で確認したfeature5 enable `0x1DED8`は、callback slot23へ`0x1DF74`を登録する。今回このcallbackのentryを命令で確認した。

```text
feature5 enable -> callback slot23 = 0x1DF74
0x1DF74: resource mask 0x48000を取得
         state byte [0xCEC8+0x0E]を読む
         0x1DF4C(state)を呼ぶ
         同resourceを解放
```

feature5のheader名FCLK_DPM、callback slot23、SSC判定のfeature11、clock slot番号は別物である。callbackが登録済み・実行済みという実機証拠は今回追加していない。

`0x1DF4C`は要求stateが現在stateと異なり、state数未満で、別config byteが0のとき、次の順で呼ぶ。

```text
0x1EDB0    SSC様設定の解除側（R201）
0x1E268    state変更処理
0x1EDD4    SSC様設定の適用側（R201）
```

state変更条件が成立しない場合も最後の`0x1EDD4`へ進む。したがって適用側関数の呼出し自体は、新たなstate変更を行った証拠ではない。適用側内部では引き続きfeature11と`0xCEE1`を検査する。

## 他のcallerとの比較

| caller | 今回確認した直接call順 |
|---|---|
| 0x1DF4C | 条件付き解除→state変更、その後適用 |
| 0x1E470 | 有効indexの正常経路で解除→state変更 |
| 0x1E4D0 | 有効な保存indexで解除→state変更、iterator更新 |
| 0x1E540 | 正常経路で解除→state変更→適用 |

`0x1E470/0x1E4D0`のcaller本体には、正常return前の直接`0x1EDD4`呼出しがない。後続callbackや間接calleeの全挙動までは追っていないので、実機でflagがどの期間0だったかは未証明。

この順序は、R201のdescriptor3/4への設定と重複実行回避flagという解釈を補強する。`0xCEE1=0`を「VCN解除前」、`=1`を「VCNが閉鎖された状態」と単純に割り当てることはできない。設定解除・state変更・再適用という通常の制御手順の中にも同じflagが現れる。

## 証拠の範囲

PROVEN_STATICALLY: 固定imageのcaller、分岐、選択した直接call順、callback entryとの接続。

STRONGLY_SUPPORTED: `0x1EDD4/0x1EDB0`はFCLK側state遷移に伴うSSC様設定の適用／解除として使われる。R201のG6 SSC header、descriptor3/4操作と整合する。

UNPROVEN: indirect/bulk writerの完全性、runtime登録状態、実際のstate遷移、VCN全体電源との因果。FCLK側制御との接続を、VCN電源の経路だと読み替えない。外部の異なるbyte列に同じアドレス対応を適用しない。

## 方針への反映

当初の`0xCEE1`を直接変える候補は引き続き採用しない。今回のcaller解析は新しい解除操作を示すものではなく、候補の役割を限定する成果である。次の静的課題は、未追跡のindirect writerを限定的に調べるか、独立したCyan固有電源経路の証拠へ戻ること。ライブ提案6条件は未充足。

[命令証拠](../logs/R211_STATIC_EVIDENCE.txt) / [R201](CHATGPT_HANDOFF_R201.md) / [R208](CHATGPT_HANDOFF_R208.md)。

```text
STAGE=R211_SSC_CALLER_LIFECYCLE
RESULT=SSC_CANDIDATE_CONNECTED_TO_STATE_TRANSITION_CALLBACK
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=FIXED_DIRECT_CALL_ORDER_AND_CALLBACK_ENTRY
REJECTED=CEE1_ALONE_IDENTIFIES_VCN_CLOSED_GATE
UNPROVEN=INDIRECT_WRITERS_RUNTIME_STATE_AND_PHYSICAL_VCN_EFFECTS
NEXT=BOUNDED_STATE_WRITER_OR_INDEPENDENT_POWER_ROUTE_EVIDENCE
```
