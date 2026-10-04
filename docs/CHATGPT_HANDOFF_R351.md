# R351 preparation handoff — single VCN0 PGFSM_STATUS read

As of 2026-10-04, R350 live evidence has been updated from the user's receiver capture: exact receiver token accepted, AMDGPU initialization progressed, R324 final VCN0 record/base guard matched, both no-write PCI identity reads returned `0x13fe1002`, then the expected R328 checkpoint panic/end was captured. The user reported manual reset. This proves the no-write PCI control path only. It does not prove VCN MMIO, power, firmware execution, or decode.

A local R351 package is prepared at `~/bc250-research/research/r351-vcn-status-read-observation`. It retains the R324 discovery guard and R350 pre/post PCI checks. On passing guards, it issues exactly one 32-bit `PGFSM_STATUS` read (byte offset `0x1f804`), logs the raw value if it returns, then intentionally panics. No PGFSM_CONFIG write, polling/wait, or PSP enrollment was added; the existing R79 guard remains. The same early-init wired receiver gate now proven live by R350 is retained with a new exact token.

Static package audit passed: same-tree paired build with 1003 other AMD objects unchanged; only `.text` differs among six executable sections; module signed with expected key/vermagic; gzip initramfs exact roundtrip of 1,706 paths; Python and init shell syntax parse. Image is 168,063,084 bytes. No protected `/boot` preflight, installation, menu arm, module load, reboot, or hardware access has occurred. Read-only status at preparation close: normal kernel is `7.2.1-ogc4.1.fc44.x86_64`, amdgpu is loaded, EFI pstore policy is `Y`, and `kernel.nmi_watchdog=0`. R351 preflight requires the watchdog at `1`; the unprivileged pstore listing was denied and will be read under sudo during preflight.

After user return, first restore the runtime watchdog setting, then run protected read-only preflight:

```sh
sudo sysctl -w kernel.nmi_watchdog=1
sudo python3 ~/bc250-research/research/r351-vcn-status-read-observation/install.py
```

This is protected read-only preflight (stores result in the HOME package). Stop unless it reports PASS. Installation and manual-menu arming remain separate operator steps documented in the package's `OPERATOR.md`. R351 can leave the machine requiring manual reset; a missing return marker does not identify the exact stopped instruction. VCN usability remains unproven.

## Live boot observations after installation

The first R351 selection produced no receiver capture. The user saw the last visible kernel line `clocksource: Switched to clocksource tsc`; Enter led to a command-input shell, then the user manually reset to the normal entry. The BC-250-side Ethernet LED was reported dark for that attempt. After recovery, the normal kernel was `7.2.1-ogc4.1.fc44.x86_64`, GRUB showed only `boot_success=1`, EFI pstore policy was `Y`, and `/sys/fs/pstore` was empty. This did not identify the R351 failure point.

Normal-boot wired validation subsequently passed: `enp4s0` is PCI `04:00.0` with `r8169`, `carrier=1`, address `192.168.128.130/24`; ping to `192.168.128.189` succeeded and learned MAC `8c:1d:55:1b:af:44`, matching R351's configured target. A normal-boot test's three `BC250 NETCONSOLE TEST 1/3–3/3` messages were received on Windows. Its local tcpdump showed only the explicit pre-netconsole control packet, so the external receiver capture is the positive evidence for the printk markers.

R351 was re-armed once with a fresh-state retry script (`MENU_RETRY_RESULT.json` PASS) and selected again. The user reports the same visible situation and no receiver data, then reports recovery to normal boot. The second attempt's raw capture, whether the exact local R351 token was entered, and post-attempt pstore contents have not been supplied. Therefore it is not established whether the amdgpu gate was reached; no R351 VCN STATUS result is claimed.

Historical R298 NETOBS1 independently received unique early-initramfs network qualification markers with amdgpu absent. R350 also captured the shared NETHOLD receiver gate live. Those controls show the early wired/netconsole path has worked before, while the normal-boot smoke confirms the current receiver path. The failure is thus localized only to the unobserved R351 boot attempt; link-down, netconsole initialization, capture readiness, and user-input state remain competing explanations.

**Decision:** stop further R351 boots until the second attempt is classified. Preserve any receiver capture and pstore records. Do not clear pstore or infer that absence of UDP means amdgpu was not loaded. The next investigation should inspect the current `/sys/fs/pstore`, confirm whether a fresh raw receiver process was active during attempt 2, and determine whether the exact token was entered. If a future boot is justified, collect local shell state (`/proc/cmdline`, interface-to-PCI mapping, carrier, and netconsole state) before reset. Do not repeat the same uninstrumented attempt.
