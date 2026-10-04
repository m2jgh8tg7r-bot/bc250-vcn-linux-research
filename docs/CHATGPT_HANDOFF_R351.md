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

The user set a 90-minute maximum for this session and asked to shut down on early completion or timeout. A noninteractive shutdown reservation failed because sudo requires a password. Do not claim shutdown is scheduled; after user return, run `sudo shutdown --poweroff +90 "BC250 research session time limit"` if still within the authorized session, or `sudo systemctl poweroff` when ending early.
