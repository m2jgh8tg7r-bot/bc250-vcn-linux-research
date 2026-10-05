# R353 operator sequence

R353 replaces only the already-installed R351 status-read image and BLS entry after a protected preflight. The scripts do not set the boot entry, load `amdgpu`, or reboot. The operator separately chooses R353 from the visible GRUB menu.

## Prepare and install

Run these commands from the normal Bazzite boot. Stop if any script reports `FAIL`, an assertion, or a nonzero exit.

```sh
sudo sysctl -w kernel.nmi_watchdog=1
sudo python3 /var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard/install.py
```

Review `contract: PASS`, the unchanged normal BLS prefix/default, the R351 retirement hashes, and the reported free-space margin. Only then install the replacement:

```sh
sudo python3 /var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard/install.py --install
sudo python3 /var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard/verify_installed.py
sudo python3 /var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard/arm-menu.py
```

Each command requires sudo because it checks or writes protected `/boot` and GRUB state. The armer changes only `menu_show_once_timeout=30`; it does not choose R353 or reboot.

## Boot and collect

Start a fresh Windows UDP listener on port 6666 before rebooting. At GRUB, manually select `BC-250 R353 guarded R351 VCN STATUS observation`. If the local screen does not say R353, do not enter a token.

R353 must print the local `R353 TARGET ...` line. Confirm the Windows listener also receives the R353 `TARGET` marker and ten qualification messages, followed by `QUALIFICATION_COMPLETE` and `INPUT_READY`. If any expected target setting differs, or these messages are absent, do not type the token; use `reboot -f` and choose the normal Bazzite entry.

Only after both local and receiver evidence agrees, type exactly `R353-STATUS-READ` and press Enter. Save the whole Windows log, including `INPUT_RESULT`, `AMDGPU_MODPROBE_BEGIN`, and any R351 guard/read markers. The test intentionally panics after the guarded read path; use the reset button if needed, then boot normal Bazzite and inspect pstore before changing its contents.

An empty pstore does not prove that no panic happened. A panic line by itself does not prove the STATUS read. `STATUS_READ_RETURN raw=...` is the direct returned-value observation; `ABORT` means the guarded STATUS read was not reached.
