# R210 — Session15 BAR2報告と保存Linux sourceの限定比較

2026-09-21。計画で任意作業としていた既存BAR/window資料の比較を実施。新規BAR走査・レジスター読出し・CCP操作なし。Domain6 statusの物理意味を直接定義する資料は、今回確認した保存範囲では得られていない。

## BAR番号はPCI functionと組にして読む

固定kernel commit `0bb924b042ab85b8f529aed6e4f3e24750584276`の**committed blob**を読み、作業treeの実験変更と分けて確認した。

| driver側の対象 | sourceでの割当て |
|---|---|
| PSP/CCPのsp-pci device | device dataのBAR2をio_mapへ割当て |
| amdgpuのdoorbell | GPU deviceのBAR2 |
| amdgpuのregister MMIO（Bonaire以降の分岐） | GPU deviceのBAR5 |

従って、過去GPU実験のBAR2/doorbell記録を、そのままSession15のPSP/CCP BAR2の独立再現と数えない。同様に、GPUのMMIO size表示だけからPSP BARやGPU doorbellのsizeは決まらない。sourceの割当て規則はPROVEN_STATICALLYだが、外部scanがどのPCI function/resourceを使用したかの実採取identityは別の証拠を要する。

## Session15の何が対応するか

[外部固定報告](https://github.com/Shalasere/bc250-vcn-research/blob/edb222c65477b6ebc63834ef3562855009179539/research/TOCTOU_ANALYSIS_2026_09_20.md)は、約1MiBのBAR2走査で少数のmailbox/status領域とoffset0xCのTRNGを観測し、queue領域で0xFFFFFFFFだったと記す。

保存Linux CCP v5 sourceでは`TRNG_OUT_REG=0xC`、queue stride=0x1000、各queue controlは`io_regs+stride*(i+1)`、statusはそこから+0x100。外部が調べたqueue offsetの構造はこのdriverモデルと整合する。ただしCyanで各queueが利用可能である保証にはならない。

報告内の「0..0x6000がすべてFFFFFFFF」という広い表現には、同報告が挙げる0xCの例外がある。ここでは「報告されたqueue register範囲で有効なqueue状態を得ていない」という限定された読みにとどめる。TRNG値が変わることだけをPSP firmwareの特定処理やVCN許可処理が動いた証拠にはしない。

FFFFFFFFという読出し値だけでは、write可能性、firmware権限、内部queueの実在・電源、将来の全runtime経路を確定できない。今回の比較では外部のwrite試験を再現していない。特定のhost queue経路を優先しない材料にはなるが、全経路不可能の普遍的証明とは扱わない。

## 外部採取コードの追加監査

同じ外部固定commitの`code/toctou-analysis/ccp_bar_scan.py`を取得しGit blob hashを照合した。AST parseとテキスト検査のみで、import・実行していない。

- 特定のPCI functionを固定し、BAR2はresource2から1MiBをmapする。BAR5はresource情報のsizeを使う。外部実行時のPCI IDとの対応確認は別途必要。
- `live`の集計条件は「0でもFFFFFFFFでもない」。従って15 regions／約100 bytesという数は、このフィルターを通った領域の集計であり、残りがすべてFFFFFFFFだったことを示さない。正当に0を返すregisterも集計外になる。
- region検出・表示・version候補探索は別々のread pass。表示はregionあたり最大256 bytesで、完全な同時snapshotや全値のraw dumpを保存する実装ではない。
- スクリプトは読み取り専用ではない。必要時のdevice enableとPCI command変更、さらに先頭0x200 bytesに条件付きwrite/readback/restore処理を含む。今回こちらでは一切実行していない。
- そのwrite試験範囲は、Linux CCP v5のqueue base（0x1000刻み）を含まない。また候補regionが空なら早期returnしwrite試験まで進まない。したがってこのコードだけから「queue registerの非書込み性を試験済み」とは言えない。他の外部試験があった可能性は残す。

これは外部報告の取得方法を限定する新しい根拠である。コードが存在することと、その版が実際に完走して報告の値を出したことは区別する。保存スクリプトのhash・確認内容は同梱証拠に記録した。

## ローカル資料との独立性

保存project-ariel manualにもmailbox/TRNGが見えqueue maskがFFFFFFFFという記述がある。ただしこれはローカルに保存された**外部資料**であり、この実機で採取した結果ではない。既存root-level研究ログ中の同manual引用も独立測定として重ねて数えない。確認した引き継ぎ・既存テキスト範囲では、Session15と同条件のローカル完全BAR2 captureを特定できなかった。全保存媒体に不存在という主張ではない。

R197/R199のPSP firmware responseやplacement記録は別の観測経路であり、CCP queueのhost可視性を証明・反証する資料として代用しない。

## 方針

Session15はEXTERNAL_REPORTEDのまま、driver配置との整合だけを静的に追加確認した。新しい広域走査やCCP操作へ進む根拠は得ていない。R201〜R209で分離したDomain6、全体電源、de-isolation、PSP受理、VCPU、ring、VA-APIの各境界を維持する。

次の保存資料解析では、外部のPCI function identity・resource size・取得方式・raw値・版を揃えられる資料の有無を優先する。経路を変更して試すのではなく、同じ対象を比較できているかを先に確定する。

[固定source抜粋とhash](../logs/R210_STATIC_EVIDENCE.txt) / [R209](CHATGPT_HANDOFF_R209.md)。

```text
STAGE=R210_BAR_WINDOW_EVIDENCE_COMPARISON
RESULT=SOURCE_MAPPING_CONSISTENT_EXTERNAL_CAPTURE_UNREPRODUCED
STATIC_OR_LIVE=STATIC_AND_EXTERNAL_REPORT
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NOT_TESTED
PROVEN=COMMITTED_DRIVER_BAR_AND_QUEUE_OFFSET_MAPPING
REJECTED=GPU_BAR2_EVIDENCE_EQUALS_PSP_BAR2_REPRODUCTION
UNPROVEN=LOCAL_MATCHING_CAPTURE_AND_GLOBAL_RUNTIME_IMPOSSIBILITY
NEXT=EXTERNAL_RAW_CAPTURE_AND_VERSION_IDENTITY
```
