> **R232 correction — 2026-09-23:** R232 research is complete. SVC64 was found in existing R218 exports; the plan's allocator-unknown statement is superseded. See the completed evidence and corrections. [Evidence](CHATGPT_HANDOFF_R232.md). The original text below is historical.

# 外部研究照合とR232方針 — 2026-09-23

ユーザー指定の外部情報収集・既存証拠照合・方針決定を完了。R232の解析本体は未実施。実機アクセス・変更・外部コード実行なし。別ChatGPTからの回答ではなく、公開一次資料を直接取得した結果。

## 結論

R232は「公開テキストと保存済み解析記録によるPSP登録・dispatch契約の照合」を行う。SVC 0x64の探索だけに固定せず、row+0x18の生成元とF2への引数対応を主対象にする。版一致するSVC 0x64/0x67資料が得られれば接続する。今回確認した範囲では、R231の未証明事項を解消する新しいVCN実動作の証拠は得られなかった。

## 調査範囲と更新差分

2026-09-23 11:15–11:20 UTC頃に7リポジトリの既定branch最新5 commits、更新順issues/PR最大10件、releases最大3件を取得。関連READMEは固定commitで取得。既存issueのコメント、関連PR本文とmerge情報、Linux mailing-listの原投稿も確認。対象範囲の結果であり、Discord、非公開情報、全branch/fork、全履歴の不存在証明ではない。

| 対象 | 確認したHEAD / 更新 | 既存記録との関係 |
|---|---|---|
| daveconde/bc250-vcn-enable | 7c511b725b13 / 8月24日 | 9月21日保存HEADと一致。最新issue更新9月11日、2件ともコメントなし |
| thelamer/bc250-vcn | e53aa40d8a51 / 8月18日 | 9月21日保存HEADと一致。既存PR更新9月3日、issueコメントなし |
| thelamer/bc250-lab-image | 200cce14e2b1 / 8月19日 | 9月21日保存HEADと一致。最新release v0.3.0 |
| Shalasere/bc250-vcn-research | edb222c65477 / 9月20日UTC | R210で監査済みSession15と同一HEAD |
| katzzero/bc250-unofficial-community-guide | b6014e44087e / 9月14日 | R225以降の既知のt02/t28報告。二次資料のため新しい実測根拠にしない |
| rw-r-r-0644/bc250-smu-unlock | f5886d015af9 / 9月18日 | 最新変更はpackaging。9月22日以降の更新をこの範囲では確認せず |
| simpmix/bc250-encoding-decoding-fix | 26464955f569 / 9月23日 | 9月21日保存106ea01910e7から更新。decodeとVideoProcの進展あり |

日付は特記以外UTC。取得時刻・URL・SHA-256はローカルmanifest.json/text-manifest.jsonに記録。

## 一次資料の評価

### 1. 動画処理の新成果はVCN解除とは別

[PR23](https://github.com/simpmix/bc250-encoding-decoding-fix/pull/23)は9月22日merge。著者はH.264/HEVC decodeがCPU、encodeがVulkan computeと明記している。VA-API経由の実機結果は著者報告であり、こちらでは再現していない。

[PR24](https://github.com/simpmix/bc250-encoding-decoding-fix/pull/24)はMain10/P010対応、[PR26](https://github.com/simpmix/bc250-encoding-decoding-fix/pull/26)はcomputeのVideoProc対応。[PR31](https://github.com/simpmix/bc250-encoding-decoding-fix/pull/31)は9月23日mergeで、JCT-VC一致数111/147と報告。READMEの旧302件とこの147本は異なる試験集合なので混同しない。v0.5.0リリースと9月23日のmainも区別する。

[固定README](https://github.com/simpmix/bc250-encoding-decoding-fix/blob/26464955f569303f311a849135c3935a6aeaf3c9/README.md)の永久eFuse無効化という断定は、decode成功からは導けないため採用しない。逆に他資料の「fuseではない」という断定もこの調査では立証しない。

版照合: 実装はcommitで固定できるが、PRの実測に対応するBIOS・PSP/VCN firmware hash・kernelの完全な組合せは、確認した本文では揃っていない。標準PSPでのVCN受理やVCN ring実行ログもこのdecode成果の根拠ではない。

### 2. 新たに把握したPSP platform mailbox対応（投稿自体は9月19日）

[Linux投稿 patch 3/3](https://lists.openwall.net/linux-kernel/2026/09/19/922)はPCI 1022:143eにplatform access用設定を追加する提案。投稿者はTEE ringの初期化失敗も記載している。[cover letter](https://lists.openwall.net/linux-kernel/2026/09/19/969)の試験kernelは7.2.6、bootloader表示は00.1c.01.02。BIOS/PSP image hashは本文にない。

これはPSP用PCI functionのplatform mailbox観測であり、amdgpuのVCN firmware command、内部SVC、VCN hardware ringとの同一視はできない。採用済み上流機能とも断定しない。R210のmailboxとqueue apertureの区別と整合するが、同じ対象版の独立したローカル再現ではない。SVC 0x64の解答にもならない。

### 3. 既存VCN報告の版と証拠

[daveconde固定README](https://github.com/daveconde/bc250-vcn-enable/blob/7c511b725b135766c52a3e13776c1cd187e5015d/README.md)はP3/Robin1・PMFW 0.58.6.0対象。P5へのoffset転用は支持しない。SMU状態の変更とVCN MMIOアクセス可能化は区別されている。今回の更新確認で新しいring成功証拠は得られない。

[Shalasere固定HEAD](https://github.com/Shalasere/bc250-vcn-research/tree/edb222c65477b6ebc63834ef3562855009179539)は既にR210で監査した資料。外部の変更されたPSP条件や広い不可能性の主張を、ローカル標準PSP経路の実測へ転用しない。完全な版一致は未証明。

## ローカルR231までとの照合

- 基準TOS body SHA-256: 19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d。
- R228/R229: 保存コード上でbase 0x280000 + 0x6000 = 0x286000、stride 0x54、tag 0x5244のwriter/readerが対応する。これはPROVEN_STATICALLYでありlive tableではない。古いR225/R226のbase未解決表記より新しい結果を優先。
- R230: 32 slotの重複検索でmiss時0xff。新規row書込みの前にSVC 0x64からindex出力を受け取る。0xffをそのまま行番号として使う仮説はREJECTED。allocatorの実装・範囲はUNPROVEN。
- row+0x18はF2 dispatchに使われ、値3は別分岐。31 occupied slots、t28登録、clamp解除はUNPROVEN。
- 最終ローカル実験R199_R173ではPSP応答0xffff0008、返却配置0。新しいCPU decode成果やplatform mailbox応答でこれを成功へ更新しない。
- Linux command fw_type=13とBIOS directory type 0x13は別namespace。番号一致だけで関連付けない。

## 決定したR232の作業と終了条件

1. 公開一次テキストに版/hash・関数offset・SVC引数/戻り値の対応があるか照合する。Cezanne/Vangoghの番号だけの一致やPOST code一覧はCyanのSVC仕様に採用しない。短い探索で版一致根拠が得られなければSVC64/67はUNPROVENのままにし、同じ探索を反復しない。
2. 保存済みテキスト解析を使い、row+0x18の書込み元→loader入力→値3/その他の分岐→SVC F2引数を対応表にする。外部t02/t28/op-id-8報告の各接続を、対応済み・版不明・未証明に分ける。AMD公開blobの追加取得・逆解析は行わない。
3. 新たなccp投稿はソース上のplatform mailbox契約として補足し、amdgpu command経路との差を表にする。driver導入やmailbox送信を今回の方針から自動的に実施しない。
4. 成果物は根拠offset/出典付きdispatch表、未証明リンク一覧、次に必要な観測項目。型/版を特定できない項目は推測で埋めない。
5. 次回実機試験へ進める条件は、対象版と操作点が定まり、成功/失敗を区別できる観測・復帰手順が書けること。現時点で新規実機試験は未準備。

compute/CPUによる動画処理は実用上の別候補として記録するが、BC-250 VCN 2.0.3の有効化という研究目標は維持する。
