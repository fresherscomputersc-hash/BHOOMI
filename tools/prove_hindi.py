import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from app.services.extraction import detect_profile, extract_fields, required_fields_for

texts = {
    "UP": "उत्तर प्रदेश खतौनी\nजिला सीतापुर\nतहसील महमूदाबाद\nग्राम रामपुर\nखाता संख्या 45\nगाटा संख्या 118\nखातेदार का नाम श्री रमेश कुमार\nक्षेत्रफल 1.25 हेक्टेयर",
    "MP": "मध्य प्रदेश खसरा पंचशाला\nपटवारी हल्का 12\nग्राम बिलकिसगंज\nखसरा संख्या 227/1\nखातेदार सुनीता प्रधान\nपति का नाम रमेश प्रधान",
    "BIHAR": "बिहार जमाबंदी\nजिला नालंदा\nअंचल बिहारशरीफ\nग्राम सोहसराय\nखाता संख्या 12\nखेसरा संख्या 340",
}
for name, t in texts.items():
    prof = detect_profile(t)
    out = extract_fields(t, [], profile=prof)
    f = out.fields
    print(name, "profile:", prof)
    print("  owner:", f["owner_name"].normalized_value, "| guardian:", f["guardian_name"].normalized_value)
    print("  village:", f["village"].normalized_value, "| tehsil:", f["tehsil"].normalized_value)
    print("  khata:", f["khata_no"].normalized_value, "| khasra:", f["khasra_no"].normalized_value,
          "| plot:", f["plot_no"].normalized_value)
    print("  required:", required_fields_for(prof))
