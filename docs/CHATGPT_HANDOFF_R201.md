# R201 — Robin1制御フローの独立照合 / static control-flow correction

2026-09-21。ユーザー指定の静的・読み取り専用方針で、保存Robin1イメージを解析した。**指定された経路は、この保存版ではVCN電源解除経路と認定できない。GDDR6 UCLK/UCLK_DIVのSSC（スペクトラム拡散）設定・解除と強く整合する。** 外部報告の関数入口は一致するが、status呼出先と退出先に訂正が必要だった。

実機アクセス、firmware/boot変更、新しいBAR走査、SMU/PSP呼出し、ring/VCPU実行は一切行っていない。ハードウェア動作の新しい成功・失敗は報告しない。

## 固定入力と再現性

- Robin1 image: 262400 bytes、先頭version word `0x00580600`。
- SHA256: `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`。
- 保存firmware、過去stage12コピー、Ghidra入力の3ファイルは全バイト一致。
- 公開配布元: [amd_smu_reverse_engineering固定版](https://github.com/bc250-collective/amd_smu_reverse_engineering/tree/3f47768eace8ad8ad86c480a55637d14467cffcd)。配布READMEは256-byte header除去済みと記載。今回さらに256 bytesを除去していない。
- 既存Ghidra projectを別領域へ複製し、`readOnly / noanalysis`で既存命令・関数・xrefを抽出。新しい関数境界を推測で作っていない。
- Ghidraは `Xtensa:LE:32:default`。登録された実行ファイルhashに加え、プログラムメモリー全262400 bytesを入力と比較して一致。mapは`0x00000000..0x000400ff`、**file offset = firmware address**。
- call8と分岐の即値を別のPythonコードで生バイトから計算し、Ghidraの対象5命令と一致。命令定義は上記配布元のXtensa SLEIGH定義と照合した。別の独立ISA実装による検証とは区別する。
- 現在稼働firmwareとの全バイト同一性、外部研究者の256KiB SRAM dumpとの同一性は **UNPROVEN**。R145で確認したOS報告版一致だけで全バイト一致としない。

## 外部報告との相違

比較対象: [入口訂正 e68af4a](https://github.com/Shalasere/bc250-vcn-research/commit/e68af4ae63456074f0cae46f315f13a9bb4888c0)、[分岐説明 820297d](https://github.com/Shalasere/bc250-vcn-research/commit/820297d2f292fcbd7f6b51ce11798dfc9c361f28)。外部イメージ差・転記・decoder問題のどれが相違原因かは未確定。

| 項目 | 外部記述 | この固定イメージで確認 |
|---|---|---|
| 入口 | `0x1EDD4` | 一致、`entry a1,0x30` |
| 引数11のstatus呼出先 | `0x1CB58` | **`0x1DB54`**。callsite `0x1EDD9`、bytes `a5 d7 fe` |
| status=0の退出 | `0x1EEB8` | **`0x1EEB4`**。`0x1EDDC`、bytes `16 4a 0d` |
| 状態byte非zeroの退出 | `0x1EEB8` | **`0x1EEB4`**。`0x1EDE5`、bytes `56 b8 0c` |
| 退出の実体 | entryを含む共通退出routine | `0x1EEB4: retw.n`。`0x1EEB8`は別関数 |
| `0x1EE90`の位置 | 入口から0x28 bytes | 実際は**0xBC bytes**。この版では`0x1EE8F`の2-byte命令の途中 |
| `0x241AC`への引数 | 3/4 | 第1引数3/4は一致。ただし**第2・第3引数も使用** |

ここでREJECTEDなのは「これら外部アドレス・解釈をこの固定版にそのまま適用できる」という主張である。他者のdumpを同一と確認せず、その全観測を否定するものではない。

## predicateと0xCEE1のreader/writer

`0x1DB54(n)`の命令列は以下の式に対応する。

```text
return (u32[0xCC98 + 8 + 4*(n >> 5)] >> (n & 31)) & 1
```

したがってn=11は`0xCCA0`のbit11。ソフトウェアfeature bitmapを検査しており、VCNハードウェアのready応答を直接読んでいない。feature状態更新処理`0x1D940`、状態reset処理`0x1DB30`、状態出力処理`0x1DB14`も静的に抽出した。複雑なloopの逆コンパイルには警告があるため、完全なC意味等価性は主張しない。

保存kernel header `smu_v11_8_pmfw.h`はbit11を`FEATURE_G6_SSC_BIT`、コメントをG6 memory UCLK and UCLK_DIV SSと定義する。header SHA256は同梱evidence参照。これは同系列ABIの補助根拠であり、単独でopaque firmwareの意味を確定しない。

`0x171D4`のliteral値は`0xCEC8`、offset `0x19`から対象byteは`0xCEE1`となる。既存Ghidra xrefで確認した直接アクセスは次の4箇所。

| 関数 | reader | writer | 動作 |
|---|---|---|---|
| `0x1EDD4` | `0x1EDE2` | `0x1EEB1` | bit11=1かつbyte=0ならdescriptor 3/4を設定し、復帰後byte=1 |
| `0x1EDB0` | `0x1EDBD` | `0x1EDCF` | bit11=1かつbyte=1なら`0x241F8(3)`、`0x241F8(4)`を呼び、復帰後byte=0 |

従って、`0xCEE1=1`を単に「VCNの閉じたgate」と呼ぶのは不適切。このコードでは設定済み状態の重複実行を避けるflagという解釈が強い。各呼出しが実機で完了するかは別問題。保存ファイルのbyte値0もruntime初期値・観測値の証明ではない。

xrefの結果は既存解析が解決した直接参照の範囲。alias、bulk clear、間接書込み、起動時初期化を網羅した不存在証明ではない。

上位caller `0x1DF4C`は条件付きで`0x1EDB0 → 0x1E268`を通った後`0x1EDD4`を呼ぶ。`0x1E540`にも同じ解除・設定を挟む構造がある。単独の未知関数呼出しを試す根拠にはしない。

## 0x241ACの具体的作用

`D = 0xF550 + index*0x48`でdescriptorを選ぶ。第2引数を設定値として使い、第3引数の下位16bitをhelperへ渡す。以下はバイナリーに含まれる操作の説明であり、今回実行した操作ではない。

1. `base+D[0x28]`の値に`0x2000`をORして書く。
2. `0x23DBC(index, arg3_low16)`を呼ぶ。このhelperはdescriptor offsets `0x20 / 0x24 / 0x30`で、OR `0x10`、mask `0xFFC000FF`とOR `0x100`、下位16bit更新を行う。
3. `base+D[0x2C]`へ第2引数を書く。
4. `base+D[0x1C]`へdescriptorのword0を書く。
5. descriptor `+4`へ第2引数を保存する。

ここでD[offset]はそのoffsetの32-bit field、baseはD[8]。write helper `0x233E8`も抽出済み。index 3/4の対象は特別扱い範囲`0x5B000..0x5B7FF`外で、SMU-local aperture `0x01100000 + (address & 0xFFFFF)`のstore経路となる。このaddress空間をhost MMIOの操作先と混同しない。

| descriptor | base | main control (`+0x28`) | arg2 (`+0x2C`) | arg3 (`+0x30`) |
|---|---|---|---|---|
| 3 | `0x5C800` | `0x5C89C` | `0x5C870` | `0x5C874` |
| 4 | `0x6C000` | `0x6C09C` | `0x6C070` | `0x6C074` |
| 6（比較） | `0x6D000` | `0x6D0A0` | `0x6D074` | `0x6D078` |

`0x1EDD4`はslot15経由のdescriptor 3情報と設定byte `0x7F35`を使い、浮動小数点計算から第2・第3引数を作る。復元Cに浮動小数点変換の不自然な表現があるため、そのCを数式の正しさの証明には使わない。引数配置・算術命令の存在・descriptor選択は命令列で確認した。

G6_SSC bit、対になる設定/解除、clock descriptor、引数生成、上位の状態切替構造を合わせ、**メモリーclock SSC設定経路という分類はSTRONGLY_SUPPORTED**。`power_gate_tile`または`PowerUpVcn`という意味は採用しない。VCNへの間接的影響が一切ないという証明でもない。

## Domain6 policy/callbackとの比較

- この経路のfeature indexは11。保存feature tableのenable/disable両方が`0x1D938`（return 1だけ）を指す。
- 既存Domain6を含むclock policy側のfeature index 13は、enable `0x2E3E8`、disable `0x2E43C`。header名は`SOC_DPM`。
- `0x2E3E8`周辺の既存命令は`0x1B1E4(24, 0x2E448)`によるcallback登録を確認でき、R146と一致する。
- `0x2E448`はpolicy対象slotから要求値を取り、必要時`0x2362C`へ渡す。slot `0x16/0x17/0x18`のdescriptor mappingは6。
- 今回の`0x1EDD4`はdescriptor 3/4を明示しており、descriptor 6を選ぶ同じ処理ではない。
- 共通のdescriptor表やwrite helperを使うことは、同じ電源・isolation制御を証明しない。

このため、今回の候補をVCN解除の第一候補とする優先順位は下げる。既存Domain6 policy/callback研究自体を反証したものではない。

## ローカル実測履歴の訂正

公開R197 handoffは準備時点の履歴で、その後のローカル記録が新しい。9月14日にR197を実施し、VCNは`ret=0 / response_valid=1 / status=0xffff0008 / placement=0`で受理条件未達。公式直前版へ変えても比較対象の応答は変わらなかった。R197後の通常復帰、R198 control、R199 R173再試験と通常復帰が保存されている。これは既存記録の公開要約で、今回の新しい実機結果ではない。R197を未実施の候補として再起動しない。

## 次の方針とライブ移行条件

静的解析を継続し、優先候補を「0xCEE1の解除」から、未解決のCyan固有Domain6/電源/isolation経路の証拠へ戻す。次はfeature 13とDomain6を含むpolicy側の初期化・callback到達条件を既存R124/R145/R146と照合し、未証明の辺だけを追う。外部dumpのhash・該当命令bytesが公開された場合は今回の相違を比較する。

BAR2/CCPは保存ログ比較のみ任意、新規scanなし。APCBは低優先度。compute encoderは別の実用候補でありVCN成功判定に混ぜない。

ライブ実験の提案には、版一致したVCN関連経路、前提条件、正確な操作対象、判別可能な観測値、復旧方法、R197より高い情報価値の6点を必要とする。今回この条件は満たしていない。firmware/initramfs/boot変更、未知のSMU/PSP/SVC呼出し、0xCEE1/VCN/Domain6/NBIO書込み、CCP/APCB操作、ring/VCPU実行へ進まない。

## Evidence / handoff

- [命令・生バイト・descriptor・header証拠](../logs/R201_STATIC_EVIDENCE.txt)
- [CPU-only再検算スクリプト](../logs/R201_audit_image.py)
- 入力binary全体、個人ログ、host識別情報は公開しない。原資料はローカルに保持する。
- GitHub公開は別ChatGPTから参照できる引き継ぎを提供するもの。別会話への直接送信や閲覧・記憶同期を確認したものではない。

```text
STAGE=R201_SMU_CONTROL_FLOW
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=STATIC saved firmware only
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=fixed image identity/map; corrected call/branch targets; direct flag reader/writer pairs; descriptor operations; feature callback distinction
REJECTED=external exact targets apply to this image; this path established as VCN PowerUp; R197 still unbooted locally
UNPROVEN=runtime/external dump full identity; exhaustive indirect writers; physical effects; VCN power/isolation/acceptance/VCPU/rings/VAAPI
NEXT=deprioritize this candidate as direct VCN gate; inspect unresolved Domain6 policy initialization/reachability statically
```
