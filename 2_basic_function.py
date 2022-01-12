from tkinter import*
from tkinter import filedialog #submodule이기 때문에 따로 임포트
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import os

root = Tk()
root.title("Mich Photo")
# root.geometry("640x480+300+100")

def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", \
        filetypes=(("PNG 파일", "*.png"), ("모든 파일", "*")), \
        initialdir=r"C:\Users\miche\OneDrive\Document\Personal\Python") #최초에 지정된 경로를 열음

    #사용자가 선택한 파일 목록
    for file in files:
        list_file.insert(END, file)

def del_file():
    print(list_file.curselection())
    
    for index in reversed(list_file.curselection()): #꺼꾸로 선택됌
        list_file.delete(index)

#저장 경로 (폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '': #사용자가 취소를 누를때
        return
    # print(folder_selected)
    txt_dest_path.delete(0, END) #무언가가 벌써 있을때
    txt_dest_path.insert(0, folder_selected)
    
# 시작
def start():
    #각 옵션들 값을 확인
    print("가로넓이: ", cmb_width.get())
    print("간격: ", cmb_space.get())
    print("포맷: ", cmb_format.get())
    
    #파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return
    
    #저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return


#파일 프레임
file_frame = Frame(root)
file_frame.pack(fill='x', padx=5, pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일추가", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택삭제", command=del_file)
btn_del_file.pack(side="right")

#List frame
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview) #Listbox도 scrollbar을 wrapping하고 vice versa

#저장경로

#저장경로 title
path_frame = LabelFrame(root, text="저장경로") #제목이 있는 프레임
path_frame.pack(fill="both", expand=True, padx=5, pady=5, ipady=5)

#저장경로 text field
txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) #innerpad

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

#옵션 프레임
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(fill="x", padx=5, pady=5, ipady=5)

# 1. 가로 넓이 옵션
lbl_width = Label(frame_option, text="가로넓이", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

opt_width= ['원본유지', '1024', '800', '640']
cmb_width = ttk.Combobox(frame_option, width=10, values=opt_width, state="readonly")
cmb_width.current(0)
cmb_width.pack(side='left', padx=5, pady=5)

# 2. 간격 옵션
lbl_space = Label(frame_option, text="가로넓이", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

opt_space= ['없음', '좁게', '보통', '넓게']
cmb_space = ttk.Combobox(frame_option, width=10, values=opt_space, state="readonly")
cmb_space.current(0)
cmb_space.pack(side='left', padx=5, pady=5)

# 3. 파일 포맷 옵션
lbl_format = Label(frame_option, text="포맷", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

opt_format= ['PNG', 'JPG', 'BMP']
cmb_format = ttk.Combobox(frame_option, width=10, values=opt_format, state="readonly")
cmb_format.current(0)
cmb_format.pack(side='left', padx=5, pady=5)

#진행상황 progress bar
frame_progress = LabelFrame(root, text='진행상황')
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
# progressbar.start(10)
progressbar.pack(fill='x', padx=5, pady=5)

frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()