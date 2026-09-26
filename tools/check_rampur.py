import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from app.services.extraction import _is_header_leak, extract_fields
print("leak रामपुर:", _is_header_leak("रामपुर"))
print("leak महमूदाबाद:", _is_header_leak("महमूदाबाद"))
out = extract_fields("ग्राम रामपुर\nतहसील महमूदाबाद\nजिला सीतापुर", [], profile="up_khatauni")
print("village:", out.fields["village"].normalized_value)
print("tehsil:", out.fields["tehsil"].normalized_value)
