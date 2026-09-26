import hashlib, subprocess
files = subprocess.check_output(
    ["git", "ls-files", "app", "tests", "static", "requirements.txt",
     "requirements-ec2.txt", "render.yaml"],
    text=True).split()
manifest = []
for f in files:
    raw = open(f, "rb").read().replace(b"\r\n", b"\n")
    manifest.append(f"{hashlib.md5(raw).hexdigest()}  {f}")
open("tools/ec2_manifest.txt", "w", newline="\n").write("\n".join(manifest) + "\n")
print(len(manifest), "files fingerprinted (LF-normalized)")
