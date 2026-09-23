# R202 — feature 13 / Domain6 policy lifecycle

2026-09-21。R201の固定Robin1イメージ（SHA256 `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`）で静的解析を継続。実機アクセスなし。

## 新しい解析範囲と既存証拠

R125U/W・R146・R147が既に示した「selector A!=Bでのみ20項目を適用し最後にA=Bとする」「setterはtargetを変えるがselectorを更新しない」「callback slot24登録」を再発見として数えない。今回はfeature状態遷移との接続、未解読入口、無効化・resetとの順序を追加した。

既存Ghidraには`0x1DA78..0x1DAC3`の命令がなく、`0x1D940`への参照にenable側が欠けていた。二つの保存handler pointer（`0x730C`、`0x7644`）と`0x1DA78`のentry bytesを根拠にこの76-byte区間だけを複製project上で解読。`readOnly`セッション終了時に変更を破棄し、新しい関数境界は作成していない。結果は次の通り。

```text
0x1DA78: obtain argument buffer
         OR its two 32-bit words into requested bitmap at 0xCC98
0x1DAA6: call8 0x1D940
         copy the two result words back to the argument buffer
         report handler status 1; return at 0x1DAC2
```

これはバイナリー中の処理の記述であり、hostから呼び出していない。status1だけで全要求featureがactiveになったとは読まない。要求bitmap、active bitmap、返却bitmapは別である。既存解析に命令・xrefがないことをコード不在の根拠にできない具体例になった。

## feature 13の登録と状態更新の順序

feature構造はrequested `0xCC98..0xCC9F`、active `0xCCA0..0xCCA7`、enable table `+0x10`、disable table `+0x110`。index13はenable `0x2E3E8`、disable `0x2E43C`。

`0x1D940`はrequested=1 / active=0でenable callbackを呼び、**callbackが1を返した後**にactive bitを立てる（callsite `0x1D9A4`、return比較`0x1D9AE`、active store `0x1D9C0`）。feature13 callbackの内部順序は以下。

1. `0x2E69C(0)`がprofile Bを0にして20件のtargetを読み込む。
2. `0x1B1E4(24, 0x2E448)`が`0xC760`へapplicatorを登録する。
3. config byte `0x7F9C/0x7F9D/0x7F9E`をdescriptor 0/1/6の`+0x15`へ移す。各`+0x18`には0.5fを設定する。
4. `0x247E8(0/1/6, 0.5f)`を順に呼ぶ。このhelperはdescriptor `+0x15 != 0 && +0x16 == 0`の場合だけ`0x241AC`へ進む。呼出しから戻ると`+0x16=1`にする。
5. feature callbackが1を返す。その後frameworkがactive bit13を更新する。

descriptor6を含むが、これはSSC様設定の経路であり、その存在や完了だけでVCN全体電源・isolation解除・VCPU実行を証明しない。config値0なら該当descriptor処理を飛ばしてもfeature callbackは1を返す。

従って「登録slotがあるからactive bitも1」「active bitが1ならDomain6を操作済み」「active bitが1ならVCN電源ON」はいずれも成立しない。登録とactive更新の間の実際のscheduler割込み可否は未確定であり、命令の順序だけから実機raceを断定しない。

## 解除・reset経路

`0x2E43C`はslot24を`0x1B1F4`でno-op callbackへ置き換えて1を返す。feature frameworkはその後active bitを消す。

全体reset `0x1DB30`は`0x1B204`による40-slot callback表のno-op化を先に行い、その後requested/activeの2-word bitmapを消去する。保存コードにはreset系callerがあるが、R125B時点でその経路が走った証拠はない。callbackとfeature bitを別々の時刻に読んだsnapshotを、同時状態や不整合の証拠として扱わない。

## 過去R125Bの不適用をどう読むか

保存記録は、gate readback A=1/B=0、setter成功、後のA=B=0、target=1250、old=0、slot17 code=0を含む。setter `0x2E6C8`はtargetを書いた後、applicator `0x2E448`を**直接呼ぶ**。

そのため、callback未登録だけでは、実際のapplicator entryでもA!=Bだったという条件下での不適用を説明できない。一方、保存されたgate readbackはそのentryでの値ではない。

この順序仮説とCPUモデルは既存R147の572ケース監査で確認済みであり、新発見ではない。今回の単純化した再検算でも、readback後・setterのtarget store前に一回のbackground applyが完了すると、旧target0を適用してA=Bとし、後のdirect applyがskipする、という履歴が保存されたsoftware fieldsと一致することを確認した。background applyなしのモデルではdirect applyが1250を処理するので一致しない。

これは**CONSISTENT_WITH**の反例モデル。実際にそのcallbackが動いた証明、ハードウェアcode変換のシミュレーション、排他・割込みモデルではない。別firmware、別writer、reset、観測時刻の違い等を排除しない。旧実験の再実施には進まない。

## 次の静的作業

Domain6 descriptorのpower bookkeeping (`+0x14`)、今回のSSC要求/適用 (`+0x15/+0x16`) を分け、初期化と書込み元を追う。特に`0x2362C`の条件付きpower helper呼出しが、bookkeepingの値でskipされる構造を既存証拠と照合する。これが物理powerの未証明境界をどう残すかを調べる。

[命令証拠とCPU順序モデル](../logs/R202_STATIC_EVIDENCE.txt)。現行の静的限定・ライブ提案6条件を維持。新規BAR scan、firmware/boot変更、未知呼出し、レジスター書込み、ring/VCPU実行なし。

```text
STAGE=R202_FEATURE_POLICY_LIFECYCLE
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=STATIC saved image and CPU abstraction
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=bounded enable-entry decode; feature requested/active/callback order; reset/unregister paths; abstract ordering witness
REJECTED=missing Ghidra xref proves missing enable path; callback absence alone explains direct setter with unequal entry selectors
UNPROVEN=runtime bitmap/callback state; actual R125B ordering; physical effects; VCN execution
NEXT=trace Domain6 descriptor bookkeeping separately from SSC and physical power
```
