# R232から外部研究へ確認したい一次根拠

外部のChatGPTや研究者から既存資料を共有できる場合、次の情報がR233以降の判別に役立つ。これは未送信の質問票であり、返信受領や別ChatGPTとの同期を示すものではない。バイナリの追加取得・逆解析を求める質問ではない。

1. t02/t28/op-id-8の説明に対応するBIOS名、各本文SHA-256、解析base、関数のbody offsetを示せるか。外部の「31 entries」は実メモリーの占有数なのか、通常descriptor割当可能数なのか。
2. 同じTOS版で、row+0x18のselectorからoperation array id8へつながる、すでに共有可能なcall/data-flow記録はあるか。host command8=SAVE_RESTORE、service1 request0x1024、内部operation id8を区別したい。
3. `0x115b6 → 0xfc50` は直接call、同期を介する間接経路、または別版の対応か。こちらの保存版では直接callerはinitializer `0x1174c`、非zero mode byte `0x2060f5` が条件。modeのwriter・値の意味について既存の一次テキストがあれば必要。
4. 保存本文hash `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d` と対応するSVC67 worker `body+0xcb4` の既存テキストまたは一次仕様はあるか。SVC64はR218の保存証拠で解決しており、再探索は不要。
5. service1 bootstrap imageについて、boot-context+0x23c、source mapping、実image範囲の対応を説明する既存manifestはあるか。bootloaderの表示versionだけではTOS/service imageの一致を確認できない。

VCN成功報告については、標準PSP条件か変更された条件か、同じbootに帰属するfirmware受理status・配置、VCN/JPEG ring実行、VA-API、hardware decodeの順で根拠を区別する。CPU decodeやVulkan computeによる動画処理は有用だが、VCN実行の証拠には数えない。
