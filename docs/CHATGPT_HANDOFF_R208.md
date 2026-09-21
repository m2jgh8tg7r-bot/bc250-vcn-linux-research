# R208 — profile観測の判別性とfeature番号の版照合

2026-09-21。保存データのみ。R207のrecord整合性監査に続き、外部の観測対象とfeature解釈を固定Robin1へ照合した。実機操作なし。

## 1111不変だけではprofile適用の成否を区別できない

R125Aの保存profile値と、原イメージのpolicy→slot表を独立に対応させた。表base `0x13EDC`の32bit entry14は`0x16`、entry15は`0x17`。R206のproducer解析では、それぞれDCLK/VCLK欄の入力となる計算値のslotに対応する。

| 保存profile index | entry14 / slot0x16 / DCLK側target | entry15 / slot0x17 / VCLK側target |
|---|---:|---:|
| 0 | 1111 | 0 |
| 1〜6 | 1111 | 1250 |
| 7 | 0 | 0 |

この表は保存configurationであり、全indexをhostが選択できた、実際に適用された、実clockがこの値になった、という意味ではない。targetそのものはR125Aの既存結果で、今回追加したのは固定producerとの接続である。

少なくともこの保存configurationでprofile0→3の**target差**を見ると、DCLK側の目標は変わらずVCLK側だけが変わる。従ってDCLK=1111不変だけから、profile適用の失敗・VCLK不変・VCN停止を判定することはできない。これは外部profile試験の再現でも成功証明でもない。外部のVCLK観測そのものは、そのdriver/producer形式と取得時刻を別途確認する必要がある。

## feature bit4/5の名前をCyanで照合

[外部の固定報告](https://github.com/Shalasere/bc250-vcn-research/blob/edb222c65477b6ebc63834ef3562855009179539/research/LIVE_SMU_PROBE_2026_09_13.md)はbitmap `0xDD602C7D`のbit4/5をDPM_VCLK/DPM_DCLKとして扱う。しかし、保存Cyan系header `smu_v11_8_pmfw.h`は次の定義である。

| bit | 保存headerの名前 | 固定Robin1のenable callback |
|---|---|---|
| 4 | PLL_POWER_DOWN | 0x23C24 |
| 5 | FCLK_DPM | 0x1DED8 |
| 13 | SOC_DPM | 0x2E3E8 |

header SHA256 `8893329478e28c2f36b0298b2aeb0fc4b5902a77e76e82db57e2884fe0a82966`。同系列headerだけでopaque firmwareを命名したのではなく、原イメージ内table `0xCC98+0x10+4*index`とcallback内容を照合した。

bit4 callbackは既にR203で確認した自動PLL電源policyをcallback slot25へ登録する。bit5 callbackは状態を初期化し`0x1DF74`をcallback slot23へ登録する。bit13はR202のDomain6を含むSOC policyである。feature番号、callback slot番号、clock slot番号は別の名前空間であり、同じ整数でも同じ機能を指さない。

R201で復元したfeature読出しhandler `0x1DB14`はactive bitmapの下位word `0xCCA0`を返す。報告bitmapのbit4/5/13が1という算術自体は正しいが、その値を外部実測としてここで再確認したわけではない。外部側が異なるfirmware/ABIだった可能性は残す。

結論: 固定Robin1の意味付けとして「bit4/5はVCLK/DCLK機能」を採用しない。「それらがONだからenable不足は否定済み」という一般的結論も未確立。ただし、別のbitを新たに変更すれば解決するとも言っていない。登録状態・active bit・hardware操作・実行成功の証明境界はR202のまま。

## 現在の方針と不足している証拠

| 論点 | 採用できる証拠 | 未確認 |
|---|---|---|
| SSC候補 | 固定Robin1の呼出先・分岐・descriptor3/4操作 | 外部と同じbyte列か、VCN全体との因果 |
| Domain6 | policy/callback/bookkeeping条件 | 同時点の物理電源・de-isolation |
| metrics | 原producer・保存patch・driver変換の静的対応 | 外部で適用されたhashとdriver、raw header/record |
| profile | 保存target差とslot対応 | 実際のapplicator entry状態・完了 |
| PSP | 既存R199までの応答・placement | VCN firmware受理、VCPU/ring/VA-API成功 |

ライブ提案6条件のうち、とくにversion一致と判別可能な観測値が揃わない。今回の成果は、新しいlive操作を選ぶ根拠ではなく、過去・外部の観測を適切な範囲で使うためのもの。次の静的優先順は、(1) 外部適用hash/driverの既存記録、(2) Domain6 bookkeepingと実statusの対応資料、(3) Session15の既存ログとの限定比較。保存R197の再実行・新規BAR scanは対象外。

[照合証拠](../logs/R208_STATIC_EVIDENCE.txt) / [R207 record監査](CHATGPT_HANDOFF_R207.md) / [R206 producer](CHATGPT_HANDOFF_R206.md)。

```text
STAGE=R208_OBSERVATION_AND_FEATURE_CONTRACT
RESULT=PROXY_DISCRIMINATION_AND_BIT_NAMES_QUALIFIED
STATIC_OR_LIVE=STATIC_AND_SAVED_CAPTURE
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=SAVED_TARGET_DIFFERENCES_AND_FIXED_BIT_TABLE
REJECTED=DCLK_UNCHANGED_ALONE_DECIDES_VCLK_PROFILE_OUTCOME
UNPROVEN=EXTERNAL_EXACT_ABI_AND_EXECUTION
NEXT=EXISTING_PROVENANCE_AND_DOMAIN6_STATUS_MAPPING
```
