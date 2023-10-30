import PyPDF2 as pdf
import pdf2image
import pytesseract as pytesss
import pandas as pd
import openpyxl as xl
import re
import os
import time
import datetime
import unicodedata
import tesserocr as ts
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk



flag = None
path = None

def disable_buttons():
    folder_button.config(state="disabled")
    pdf_button.config(state="disabled")


def check_folder():
    global flag, path
    flag = 2
    disable_buttons()
    folder_button.config(text="Click on Execute please.")

    folder_button.update()


    path = filedialog.askdirectory()
    pdf_button.config(text= "Processing: " + path)

def check_single_pdf():
    global flag, path
    flag = 1
    disable_buttons()
    pdf_button.config(text="Click on Execute now please.")
    pdf_button.update()

    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    folder_button.config(text= "Processing: " + path)

def execution():
	global flag, path
	execute_button.config(state="disabled")
	# print(flag, path)
	
	result_label.config(text=" Please wait until your Excel file appears in folder...")

	pdf_folder = path
	start_time = time.time()

	def clean_string(string):
			cleaned_string = re.sub(r'[^a-zA-Z0-9/,.-\\n]', ' ', string)
			return cleaned_string.strip()

	aux = 0

	df = pd.DataFrame(columns=['PDFs', 'PDF DATA', 'Report number', 'Nº HRE', 'Data', 'Client', "Test", "Standard", "Test Result", "Type", "Tested components"])

	tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'


	api = ts.PyTessBaseAPI(lang='eng')
	api.SetVariable("tessedit_pageseg_mode", "6")
	api.SetVariable("tessedit_ocr_engine_mode", "3")
	datatype = ""
	for folder in os.listdir(pdf_folder):
			folder_path = os.path.join(pdf_folder, folder)
			if os.path.isdir(folder_path):
					for filename in os.listdir(folder_path):
							if filename.endswith(".pdf"):
									pdf_path = os.path.join(folder_path, filename)
									if True:
										reader = pdf.PdfReader(pdf_path)
										first_page = reader.pages[0]
										text = first_page.extract_text()
										if text == "":
												datatype = "Image"
												img = pdf2image.convert_from_path(pdf_path, dpi=400, first_page=1, last_page=1)[0]
												api.SetImage(img)
												text = api.GetUTF8Text()
										second_page = reader.pages[1].extract_text()
										if second_page == "":
												datatype = "Image"
												img2 = pdf2image.convert_from_path(pdf_path, dpi=400, first_page=2, last_page=2)[0]
												api.SetImage(img2)
												second_page = api.GetUTF8Text()
										raw_second_page=second_page.replace(" ","")
										page_matches = re.findall(r"(Page:|Page :|Página|Pagina)", raw_second_page)
										request_matches = re.findall(r"(Request|Solicitud|Application)", raw_second_page)
										hre_matches = re.findall(r"HRE|HOM", raw_second_page)
										if len(hre_matches) < 1:
												hre_matches.append("Request:")
										n_matches = re.findall(r"(Nº|N°|Nr|number|N:|n:)", raw_second_page)
										# print(n_matches, request_matches)
										report_num = raw_second_page[raw_second_page.find(n_matches[0])+len(n_matches[0]):raw_second_page.find(request_matches[0])].translate({ord(y): None for y in ' :'}).strip()
										hre = raw_second_page[raw_second_page.find(hre_matches[0])+len(hre_matches[0]):raw_second_page.find(page_matches[0])].strip().replace(" ", "").replace("\n", "")

										date_match = re.search(r"\d+/\d+/\d+", text[text.find("Reception date:")+15:])

										if date_match:
												date = clean_string(date_match.group())
										else:
												date = -1

										client_matches=re.findall(r"(Client:|Cliente:|Manufacturer:|Fabricante:)", text)
										if len(client_matches) < 2:
											client = "Error"
										else:
											client = text[text.find(client_matches[0])+len(client_matches[0]):text.find(client_matches[1])].strip()
										keywords=["Denomination", "Designation", "Designacion","Date of receipt","Reception date", "Fecha de recepcion","Test standard", "Norma de ensayo","Performed test", "Performed tests","Ensayos realizados","Ensavos realizados","Performed te sts","Tests performed","Testresults","Results of the tests","The report","Resultado de los ensayos","This report","El informe","The report"]
										raw_keywords = []
										for word in keywords:
												raw_keywords.append(r'\s*'.join(word))
										raw_matches = '|'.join(word for word in raw_keywords)
										matches = re.findall(r"("+raw_matches+")", text)
										if "Test standard" not in matches:
												matches.insert(2, matches[3])
										standard = text[text.find(matches[2])+len(matches[2])+1:text.find(matches[3])].strip()
										standards = standard.split("\n")

										standard = ""
										test = ""
										for i, x in enumerate(standards):
												if x.find("test") == -1 and x.find("Test") == -1 and x.find("Durability") == -1:
														if standard=="":
																standard = x
														else:
																standard =  standard + "\n" + x
												else:
														while i < len(standards):
																if test=="":
																		test = standards[i].replace(":","")
																else:
																		test = test + "\n" + standards[i].replace(":","")
																i += 1
														break

										if test=="":
												test = text[text.find(matches[3])+len(matches[3])+1:text.find(matches[4])].replace(":","").strip()
										else:
												test = test + "\n" + text[text.find(matches[3])+len(matches[3])+1:text.find(matches[4])].replace(":","").strip()

										ttype_matches = re.findall(r"(Test object:|Teswopiect:|Objeto de ensayo:|Objeto de ensavo:)", text)
										if len(ttype_matches) == 0:
											ttype = "None"
										else:
											ttype = text[text.find(ttype_matches[0])+len(ttype_matches[0]):text.find(matches[0])].strip()
										lab_matches = re.findall(r"(L\s*a\s*b\s*o\s*r\s*a\s*t\s*o\s*r\s*y)", text[text.find(matches[4]):])
										components = text[text.find(matches[0])+len(matches[0])+1:text.find(matches[1])].strip()
										if components.find("(See") == -1 and (components.find("see") != -1 or components.find("See") != -1):
												page= int(re.findall(r"(1|2|3|4|5|6|7|8|9)", components)[0])
												text_page = reader.pages[page-1].extract_text()
												if text_page == "":
														datatype = "Image"
														img3 = pdf2image(reader.pages[page-1], dpi=400, first_page=page, last_page=page)[0]
														api.SetImage(img3)
														text_page=api.GetUTF8Text()
												components_text = text_page[text_page.find("COMPONENTS:"):text_page.find("2. TEST")].split("\n")
												splited_components = []
												for i in components_text:
														if "COMPONENTS" in i:
																continue
														elif "type" in i:
																continue
														else:
																splited_components.append(i[:i.find("(")])
												components = '\n'.join(i for i in splited_components)
										components = clean_string(components)
										if len(matches) < 6:
												result = text[text.find(matches[4])+len(matches[4])+1:text.find(lab_matches[0], text.find(matches[4]))].strip()
										else:
												result = text[text.find(matches[4])+len(matches[4])+1:text.find(matches[5])].strip()

										result_matches = re.findall(r"(PASS|pass|Pass|FAIL|Fail|fail|TRUNCATED|Truncated|truncated)", result)

										pas = ["PASS","pass","Pass"]

										fail = ["FAIL","Fail","fail"]

										trunc = ["TRUNCATED","Truncated","truncated"]

										if len(result_matches) < 1:
												result = "Measured"
										elif (result_matches[0] in pas):
												result = "Pass"
										elif result_matches[0] in fail:
												result = "Fail"
										elif result_matches[0] in trunc:
												result = "Not aplicable"


										test = test.translate({ord(y): None for y in ';|'}).replace("$","S").strip()
										ttype = ttype.translate({ord(y): None for y in ';|'}).replace("$","S").strip()
										components = components.translate({ord(y): None for y in ';|'}).replace("$","S").strip()
										if datatype == "":
											datatype = "Text"
										# if WSL in ubuntu
										print(pdf_path)
										hyperlink_formula = '=HYPERLINK("' + 'file://wsl.localhost/Ubuntu' + pdf_path + '","' + filename + '")'
										# else:
										# 	hyperlink_formula = '=HYPERLINK("' + pdf_path + '","' + filename + '")'
										df.loc[len(df)] = {'PDFs': hyperlink_formula, 'PDF DATA': datatype, 'Report number': report_num, 'Nº HRE': hre, 'Data': date, 'Client': client, "Test": test, "Standard": standard, "Test Result": result, "Type": ttype, "Tested components": components}
									# except (PermissionError, pdf.utils.PdfReadError) as e:
									# 		print(f"Error processing file {filename}: {e}")

	xls_fileName = f"database_{os.path.basename(path)}.xlsx"
	df.to_excel(xls_fileName, index=False)

	total_time = (time.time() - start_time)
	elapsed_time = str(datetime.timedelta(seconds=total_time))
	print(elapsed_time, " seconds to process this database")
	exit("Open you XLS file now")

def exit_program():
    root.destroy()
    exit("Bye!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Welcome to ParserMe!")
    screen_width = 500
    screen_height = 350
    root.geometry(f"{screen_width}x{screen_height}")


    style = ttk.Style()

    style.configure("Red.TButton",
                    font=("Comfortaa", 12),
                    foreground="white",
                    background="red",
                    padding=10)
    style.configure("TButton",
                    font=("Comfortaa", 12),
                    foreground="white",
                    background="blue",
                    padding=10)
    style.configure("Green.TButton",
                    font=("Comfortaa", 12),
                    foreground="white",
                    background="green",
                    padding=10)

    style.configure("TFrame", background="rgba(255, 0, 0, 0.5)")



    folder_button = ttk.Button(root, text="Process a Folder ", command=check_folder, style="TButton")
    folder_button.pack(pady=2)

    pdf_button = ttk.Button(root, text="Process a Single PDF", command=check_single_pdf, style="TButton")
    pdf_button.pack()

    logo_image = tk.PhotoImage(file="/home/iquecine/Doga/DOGA.png")
    logo_image = logo_image.subsample(3)  # Reduce the size 1/3

    logo_label = tk.Label(root, image=logo_image)
    logo_label.place(x=142, y=213)

    execute_button = ttk.Button(root, text="Execute", command=execution, style="Green.TButton")
    execute_button.pack(pady=13)

    exit_button = ttk.Button(root, text="Exit", command=exit_program, style="Red.TButton")
    exit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()
