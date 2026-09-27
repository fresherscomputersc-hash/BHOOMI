import win32com.client
import os

ppt_path = os.path.abspath("BHOOMI_SIH_2026_Final.pptx")
pdf_path = os.path.abspath("BHOOMI_SIH_2026_Final.pdf")

app = win32com.client.Dispatch("PowerPoint.Application")
app.Visible = 1
app.DisplayAlerts = 0

prs = app.Presentations.Open(ppt_path)
prs.SaveAs(pdf_path, 32)  # 32 = ppSaveAsPDF
prs.Close()
app.Quit()
print(f"PDF saved: {pdf_path}")
