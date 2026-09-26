import json, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "supervisor", "password": "supervisor123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
d = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/dashboard",
    headers={"Authorization": "Bearer " + tok})))
print("measured:", d["extraction"]["measured_accuracy_pct"])
print("bands:", d["extraction"]["confidence_bands"])
print("top_corrected:", d["extraction"]["top_corrected_fields"])
print("error_fields:", d["validation"]["top_error_fields"][:4])
print("resolved:", d["validation"]["discrepancies_resolved"])
print("by_state:", d["progress"]["by_state"][:4])
print("district_verified:", d["progress"]["district_verified"][:4])
