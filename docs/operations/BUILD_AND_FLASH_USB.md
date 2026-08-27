# Build, Validate, Flash, and Test a Vincent Installer

This procedure covers the safety and evidence requirements for Vincent installer testing. Exact artifact names and helper arguments must come from the source commit being tested; do not reuse filenames or build numbers from an older report.

## 1. Establish the source

Before building:

1. Fetch current repository state and inspect active installer pull requests/branches.
2. Read `docs/DECISIONS.md` and reconcile decisions newer than the build workstream's recorded checkpoint.
3. Select one exact source commit.
4. Confirm the working tree is clean and the source is pushed/recoverable.
5. Read the installer build number from the selected source and confirm it is unique for the test image.

## 2. Validate the repository

Run the repository validation entry point and any installer-specific tests required by the selected source.

Long-running commands must display progress and save complete timestamped output with `tee`, preserve pipeline status, and print an explicit final exit status.

A build must not proceed from failed repository validation.

## 3. Verify Debian source material

Use `installer/debian13/source.env` and the repository's source-fetch/verification tooling. Debian installer media must be verified against Debian's signed checksum metadata before it is used as a Vincent build input.

Do not silently change the Debian source version during a test series.

## 4. Build and inspect the image

Use the build tooling from the exact selected source commit. Record at minimum:

- Vincent source commit;
- installer build number;
- Debian source identity and checksum;
- output image name and checksum;
- generated manifest/checksum artifacts;
- build exit status.

Run the matching image inspection/validation tooling. Validation must cover, as applicable:

- embedded source/build identity;
- manifest/checksum consistency;
- absence of private keys, credentials, reusable enrollment material, and fixed worker identities;
- active obsolete-name checks;
- expected boot/installer configuration;
- installer-build identity consistency.

A successful build is not sufficient if inspection fails.

## 5. Identify removable media

Before flashing, identify the exact intended removable USB device using stable hardware identity, not `/dev/sdX` alone.

Useful inspection commands include:

```text
lsblk -o NAME,PATH,TYPE,TRAN,RM,SIZE,MODEL,SERIAL,MOUNTPOINTS
ls -l /dev/disk/by-id/usb-*
```

Do not proceed if the target is ambiguous, unexpected, non-removable, or mounted. Destructive authorization applies only to the exact verified device.

## 6. Flash and verify

Use the repository's flashing tool with the exact validated image and stable removable-device identity. Preserve the flashing log and explicit final status.

The procedure/tool must verify the target properties and verify written image content after flashing. Record the installer build number associated with the physical media.

## 7. Install on disposable hardware

During installation verify the accepted operator-interaction boundary:

- network interface selection remains interactive;
- Wi-Fi SSID/passphrase entry remains operator-controlled when applicable;
- the active installer medium is not offered as an installation target;
- the operator chooses the target disk;
- the operator chooses partitioning method/layout;
- final disk-write confirmation remains interactive;
- Vincent does not require creation of a conventional human runtime account.

Do not impose a particular partitioning recipe as an acceptance criterion unless a newer accepted decision explicitly requires one.

## 8. First-boot proof

After installation, verify through Vincent's appliance status/self-test/diagnostic interfaces:

- immutable installer build provenance;
- current Vincent software version/build as a separate value;
- dedicated `vincent` service identity;
- networking and required endpoint/package reachability;
- absence of embedded private project authority;
- local installation identity generation;
- unassigned READY state.

Physical testing should not require routine shell repair. If a shell is needed to diagnose a failure, capture that as defect evidence rather than treating the manual repair as part of a successful installation.

## 9. Acceptance

Follow `V1_WORKER_ACCEPTANCE.md` for release-level proof. Preserve concise evidence tied to the exact source commit and installer build; do not create a permanent report for every failed exploratory attempt unless it contains durable information not captured by an issue or pull request.
