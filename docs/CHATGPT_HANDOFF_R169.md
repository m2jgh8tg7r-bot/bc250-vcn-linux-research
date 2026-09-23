# ChatGPT向け研究差分：R125〜R169（2026-09-14）

**STOPPED_AWAITING_USER_INSTRUCTION。今回は共有のみ。研究は続行していない。続きは次回起動時のユーザー指示から。**

公開済みのR124系記録を補う、保存済み成果の要約。GitHub公開は別ChatGPTの閲覧・記憶同期を保証しない。この文書のURLを参照入口として使う。

最新完了段階はR169（研究終了：2026-09-14 00:01 JST）。VCN実機動作はUNPROVEN。最後の実機成果はR141の保護付きsoftware初期化と通常復帰（PROVEN_LIVE）。R157観測controlは準備済みだが未設置・未起動。R158〜R169は静的解析・限定CPUモデルの成果。

旧READMEの「firmwareをaccept」はドライバー側の取得・header認識の範囲であり、PSP受理やVCPU起動を意味しない。旧資料のCurrent/Nextより本書の到達点を優先する。段階番号は実機成功回数ではない。

## 研究の流れと古い成果

初期stage1〜30系と、その後のstage30an-R1〜R157は別系列。firmware名のR1/R5と研究段階番号も別物。資料のmtimeだけでは実験日時や連続稼働時間を証明できない。

- 初期〜R36付近: 保存SMU firmwareの公開入口、callback、clock descriptor、電源経路、Linuxとの対応や読取り観測の整理。旧claimは索引に残しているが、今回すべてを再認定していない。
- R37〜R80付近: VCN/JPEG 2.0.3の登録、初期化の保護、firmware取得とPSP転送の境界、個別boot成果物と復帰手順を調査。登録・取得とhardware動作を分離する土台になった。
- R123〜R130付近: 保存R1/R5の内部policy・callback・clock経路と過去観測の対応を解析。内部setterの静的存在は、公開Linux制御から安全に呼べることの証明ではない。R124Pでは単純な線形Q2解釈を棄却。R125B観測の非同期性は後のR147で再検討した。
- 保存R129ではradeonsiをロードできてもvaInitializeがerror 2で失敗。FFmpegのsoftware変換成功も保存されているが、hardware decodeではない。これは当時の記録であり、本日の再試験ではない。
- R131〜R140: source/build/ABI、boot設定、root filesystem、GPUとLANを切り分け。設定・ビルドの失敗とVCN故障を区別した。R140でGPU初期化と有線LANを確認し、R141の比較基準にした。

古い全段階の所在はRESEARCH_INDEX.mdとaudit-20260913/stage-evidence-index.json。欠番・抽出対象外・未審査はUNKNOWNのまま保持し、「R157まで全部実機成功」と解釈しない。

## 外出中に放置していた研究（R142〜R156）

保存資料から確認できる主な作業帯は2026-09-09 11:22〜12:31 JST。数日間連続して研究が動いていた証拠はない。依頼された別ChatGPTチャットへの初回・2時間ごとの報告は、投稿・予約手段がなく**未送信・未設定**。ローカルのreports/001-initial.mdは存在する。

| 段階 | 得られたこと | 残る限界 |
|---|---|---|
| R142 | PSP処理の準備・submit・応答・fence等を区別する観測コード。CPU 3,072条件で既存動作との等価比較 | source/object段階、実機転送未確認 |
| R143 | Cyanのpower callback欠落/no-op経路、software電源状態と物理電源の違い、firmware配置を整理 | ret=0やclockを電源投入証明にできない |
| R144〜146 | R5公開11操作、R1 callback登録・queue・walker・applicator経路を静的追跡。OS報告SMC版0x00580600は保存R1と一致、R5の0x580701とは異なる | 実行中firmware全バイト同一性、callback稼働周期、公開hostから内部setterへの経路は未証明 |
| R147 | 過去R125Bの値を非同期更新の競合で説明でき、CPU 572条件と整合 | 原因確定ではない。過去に停止した書込みを再試行する根拠にならない |
| R148 | software scheduler readyとguardによるIB -95の関係を整理 | readyはhardware ring実行ではない |
| R149 | 同一bootのロード済みmodule GNU Build IDで成果物とログを対応づけるcollector | kernel名7.2.3+だけでは段階を特定できない |
| R150 | 当時保存した公開プロジェクト一次資料を審査 | VCN成功を確立できず。compute encoderをVCN成功としない |
| R151 | PSP応答の数値・名前・返り値の区別、parser 15テスト | 未知statusを署名失敗、ret=0を受理成功と断定しない |
| R152〜153 | firmware scan・VCN slot・skip観測を追加。観測control後に別段階で登録を検討する実験設計 | この時点では起動していない。登録操作のPSP内部効果は単なるコピーと仮定できない |
| R154 | 保存R140ではGPU初期化より後にLAN接続 | early netconsole未確認。ログ欠落だけで停止箇所を断定できない |
| R155 | VCN instance0、version2.0.3、hwid12、harvest表示0。enc1はinstance0内のqueue | metadataは稼働証明ではない |
| R156 | 保存kernelのcodec queryで2.0.3が既定の-EINVALへ進むこと、保存Mesa 26.2.1のqueue条件を監査 | 実installed binaryとの対応やVA-API失敗の真因は未確定 |

R156は9月9日12:29〜12:31の成果物がSTATUS/canonical未整理で残っていた。9月13日に整理し、CPU 8条件を再検証した。放置中の成果が失われたわけではなく、引き継ぎへの反映が不足していた。

## 帰宅後の実機成果（9月13日）

R141をユーザーが手動起動し、同一bootのロード済みamdgpu Build IDと期待値の一致を確認。診断20マーカーが所定の順序で完了しret=0、amdgpu初期化とLAN接続を記録した（PROVEN_LIVE）。PSP VCN登録、VCN/JPEG hw_init、JPEG sw_initは抑止され、VCN dec/enc0/enc1のIB -95はguardの期待結果だった。

その後ユーザーが通常entryへ戻り、別採取で通常kernel、異なるamdgpu Build ID、GPU初期化、LAN 1Gbps/fullを確認。通常復帰はPROVEN_LIVE。cold recoveryや長期安定性は未証明。

同日比較で11種類のDRMエラーは通常/R141に共通し、R141だけの3種類はVCN guardのIB -95。すべてをR141による新規故障とはしない。通常環境ではCU管理serviceのumr未検出とTDP serviceのryzenadj --force拒否が記録されており、85W設定が適用済みとはみなせない。Unsupported clock typeも以前からの記録があり、実際の呼出し元・clock種別までは確定していない。

## 直近の約1時間で完成したもの（R157）

2026-09-13の約60.6分の作業では、R152の既存source treeを使い、R157の専用initramfs、boot entry、installer、collectorと検証記録を作成した。新しい28GB sourceコピーは作らなかった。/boot変更、moduleロード、再起動、新規device register/SMU/firmware書込みは行っていない。

- R141との94,895 tracked path比較で差分はamdgpu_psp.cのみ。image内の変更もamdgpu.koのみ。保護関連9ファイル・config・symvers等を照合した。
- module署名を暗号学的に検証し、改変データの拒否も確認。実kernelの署名受理は未試験。
- 実ソース抽出CPU比較はscan 15,360条件、execute 108条件、既存submit 3,072条件。実機timing・並行実行の同等性を証明するものではない。
- control parserと帰属判定を検証。通常bootをR157成功と誤認しないことを記録。collector初回のjournalctl引数形式エラーは修正し、部分記録を残した。
- 想定するcontrol観測はscan max_ucodes=73 → 空VCN slot index57 → skip=1。VCN acquire/prepare/submitには進まない。VCN/JPEG hardware guardを維持。

**R157は未設置・未起動。** installerも未実行。成果物の完成を実験の成功としない。将来ユーザーが再開を指示した場合の候補はR157の設置・在席手動control起動・帰属確認・通常復帰であり、その後のVCN登録試験は別段階。現時点では実行しない。

最後の約14分間の受動的な30サンプルは同じ通常boot/kernel、LAN carrierあり、1Gbps/fullだった。GPU負荷試験でもVCN試験でもない。


## R158〜R162：VA初期化・公開queue・firmware表示の境界

| 段階 | 新しく確認できたこと | 限界 |
|---|---|---|
| R158 | kernel queue公開→Mesa capability→video callback→VA initの経路。codec queryが片方でも失敗すると事前capabilityを保持する | 初期CPUテストは簡略型・helper stub。実型での確認はR160 |
| R159 | installed Mesa ELFのSHA256はRPM記録と一致。保存headerのcallback位置0x688/0x6c8がELFのNULL検査と一致し、共通return 2へ進む | 過去R129がどの分岐で失敗したかは未証明。error 2だけでメモリ枯渇を断定できない |
| R160 | 無変更の保存capability helperと実codec enumで18,432条件、実IP数/queue型のcallbackで7,168条件通過。valid bitだけで非対応codecを有効化できない | 仮想queue入力。VCN 2.0.3のsoftware候補にAV1はないが、他codecの実機成功を意味しない |
| R161 | 保存kernel query関数・entity上限で55,296条件通過。VCN ENCを含め公開entity上限1。内部ring複数でも公開mask1のケースがある | 実機のavailable_rings値は未測定。公開queue数は内部ring本数や実行証明ではない |
| R162 | 保存firmware header 0x0811800dがR141のENC1.24/DEC8/VEP0/rev13表示と一致。同じログにPSP登録skipあり | Found行やfirmware version queryはheader/cached fieldの情報。PSP受理・VCPU起動の証明ではない |

これにより「codec queryのcase欠落がVA初期化失敗の原因」「allocation failedだからメモリ不足」「queue数は内部ring数」「firmware版が出たからVCNが起動した」という飛躍を避けられる。将来の候補は保護を残したR157 controlの手動試験だが、この資料は実施指示ではない。


## R163〜R169：起動待機とqueue/workerの静的証拠

今回の到達点:
- R163: 起動待機fragmentの12,012 CPU条件を確認。Cyanはこの手前のguardで戻るため、実機のreset実行や起動成功とは解釈しない。
- R164: 保存R1のpriority探索を元命令・Ghidra pcode・Cadence公式ISAで照合し、限定CPU interpreterの3,584条件通過。loop終端への明示jumpと通常反復を区別し、逆コンパイル警告を実callbackと扱わない。実queueの容量/実行状態は未証明。
- R165: R1 queue投入の限定CPU interpreterと独立sort referenceで12,224条件通過。通常投入の容量拒否、別分類の受理/警告、queue順序を区別した。割込みやcontext switchの実行はモデル外で、実機の非適用原因は未証明。
- R166: R1/R5既存命令を読み取り専用で走査。各348 loop中、明示的な非setup分岐が終端へ入る54箇所をレビュー候補として保存。54不具合の証明ではない。両project各9ファイルはhash不変。
- R167: queue本体118命令323 bytesと直接literal3語は保存R1/R5で完全一致。callee・初期化・実機RAMまでの等価性ではなく、R145で確認済みの他領域の差も維持する。大きな入力コピーは増やしていない。
- R168: queue即時切替の条件wordを加算/減算する保存命令とcontext復元への接続を確認。実callxとloop由来の生成BRANCHINDを区別した。timer実行時のword値や割込み全体は未証明で、実機のpending固着原因とは断定しない。
- R169: 保存命令からqueue取り出し→workerの実callx8→完了後の次loopまで接続。131,072連続操作、48,640出力bit/threshold条件、5,120末尾link操作がCPU上で通過。slotはcallback開始前に解放されるのでqueueゼロは完了証拠ではない。実機callbackとVCN実行は未証明。


## 保存資料と検証の範囲

上記のテスト件数は以前の研究で保存された結果の引用。今回テストや実機操作を再実行していない。割込み・実機RAM・task選択・callback完了・VCN実行はCPUモデルの通過から導けない。

要約元のローカル相対パスとSHA-256を以下に残す。これらの原資料自体はこの公開文書への添付ではなく、hashのみで内容の独立再検証はできない。必要な詳細の追加共有は別途可能。生ログ、firmware、machine ID、UUID、個人homeパス、実行用スクリプトは今回の公開対象に含めていない。

| 保存資料 | SHA-256 |
|---|---|
| `CHATGPT_RESEARCH_SUMMARY.md` | `9fc9226b828e8d7cd093069e81375d41cfd749c4bb2a090709c8b18ec5d6016c` |
| `CHATGPT_LATEST.md` | `fe1d2abb495c26ce866aa0a6a67b8a4bc71f579423c921d56e704698ea7d19d1` |
| `handoffs/BC250_VCN_handoff_CANONICAL_R141_POSTBOOT.md` | `7a7175a6024b28f72216c73e2abaf89a05244f442b52a8df0db88a15671581bb` |
| `handoffs/BC250_VCN_handoff_CANONICAL_R141_ROLLBACK.md` | `cb00ac5414005a47931e9a617d7bc41c644128b781f133cffa9184c83290ed1b` |
| `r157-psp-observation-control/STATUS.md` | `1459f8879e6c5c48bc7c4c54707d6290d62c584ba9fd16b81aecb95bc424e1d8` |
| `r158-video-capability-chain/STATUS.md` | `3fc276d81121452e904904a321d1799c53cf594c97b9f55c72f44e3b68a29236` |
| `r159-installed-va-init-audit/STATUS.md` | `e20c3bce4eee6bdf65b0638431bf62705e7680fbf0988eb29884501a82b26c19` |
| `r160-mesa-capability-model/STATUS.md` | `5ca315fdd621e3e5ce5fe9ff59be9e0e68f7cc80ace12884b744a953e9018482` |
| `r161-kernel-queue-accounting/STATUS.md` | `26cf31282d457e30513439647fcb68473b87457ec822459c6926d1f69bf29b15` |
| `r162-firmware-version-evidence/STATUS.md` | `30346c9380b407831110b44168415df0a5676b8704b4cd03c40b11bbdd2cf936` |
| `r163-vcn-startup-wait-model/STATUS.md` | `e268875479500917c0ce84fadf13e22356a221cd4b72fb207a1eac2a56d61ddc` |
| `r164-r1-queue-flow/STATUS.md` | `3f76f5d780f3ede477d37e34215b2f8cea9c9e9e7af16e653cfdba482ce2efdc` |
| `r165-r1-queue-model/STATUS.md` | `755c074b1ca8fed1bfed3f32f7dae254283752553b70ee8dc0013bf10e93844a` |
| `r166-xtensa-loop-audit/STATUS.md` | `8f39141adae571ea770f35986f71c723fb9d18f0101a32cf4d34bcc2256a4d14` |
| `r167-queue-image-comparison/STATUS.md` | `240ec8ef6fded0928303824c13085fa9bf853b4a93e876724c5d372172a8db41` |
| `r168-scheduler-context-boundary/STATUS.md` | `4d40f15e17f9d81601305fb0bed22766c9c035914f7de168c15db9d177f4714f` |
| `r169-queue-consumer/STATUS.md` | `15151127575675fc2cbe79f9a71d59493af4a28a63ad264025f287ee8e1a593b` |

未証明：PSP VCN firmware受理、VCPU起動、VCN/JPEG hardware ring実行、VA-API成功、FFmpeg hardware decode、ブラウザ動画の安定動作。将来候補の記載は今回の実行指示ではない。
