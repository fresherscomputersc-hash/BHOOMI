grep -o "DOC-[A-F0-9]*" /home/ubuntu/realror-run.log | sort -u
grep -o "stress_0[0-9][^ ]*\|DOC-[A-F0-9]*" /home/ubuntu/stress-run.log | sort -u | head -20
