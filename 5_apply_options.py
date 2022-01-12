from tkinter import*
from tkinter import filedialog #submodule이기 때문에 따로 임포트
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
from PIL import Image
import os

root = Tk()
root.title("Mich Photo")
# root.geometry("640x480+300+100")

def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", \
        filetypes=(("PNG 파일", "*.png"), ("모든 파일", "*")), \
        initialdir=r"C:\Users\miche\OneDrive\Document\Personal\Python\intermediate\gui_basic") #최초에 지정된 경로를 열음

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
    
#이미지 통합
def merge_image():
    print("가로넓이: ", cmb_width.get())
    print("간격: ", cmb_space.get())
    print("포맷: ", cmb_format.get())
    
    try:
        #가로넓이
        img_width = cmb_width.get()
        if img_width == '원본유지':
            img_width = -1 #원본 기준으로
        else:
            img_width = int(img_width)
            
        #간격
        img_space = cmb_space.get()
        if img_space == '좁게':
            img_space = 30
        elif img_space == '보통':
            img_space = 60
        elif img_space == '넓게':
            img_space = 90
        else: #없음
            img_space = 0
            
        #포맷
        img_format = cmb_format.get().lower()
        
        ###########################################################   
        
        # print(list_file.get(0, END)) #모든 파일 목록을 가지고 오기
        images = [Image.open(x) for x in list_file.get(0, END)]
        
        #이미지 사이즈 리스트에 넣어서 하나씩 처리
        img_sizes = [] #(width1, height1), (width2, height2)
        if img_width > -1:
            #width 값 변경
            img_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            #원본 사이즈 사용
            img_sizes = [(x.size[0], x.size[1]) for x in images]
            
        #계산식
        #100 * 60 이미지가 있음 -> width를 80 으로 줄이면 height=?
        #(original width) : (original height) = (modified width) : (modified height)
        #       100                 60                80                  ?
        #modified height = 48
        
        #original width = width = size[0]
        #original height = height = size[1]
        #modified width = img_width 이 값으로 변경해야함
        #modified height = img_width * size[1] / size[0]
        
        #size -> size[0]: width, size[1]: height
        # widths = [x.size[0] for x in images]
        # heights = [x.size[1] for x in images]

        widths, heights = zip(*(img_sizes))

        max_width, total_height = max(widths), sum(heights)

        #스케치북 준비
        if img_space > 0: #이미지 간격 옵션 적용
            total_height += (img_space * (len(images) -1))
        
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0 #y 위치 
        # for img in images:
        #     result_img.paste(img, (0, y_offset))
        #     y_offset += img.size[1] #height 값 만큼 더해줌
        
        for idx, img in enumerate(images):
            #width 가 원본유지이 아닐때에는 이미지 크기 조정
            if img_width > -1:
                img = img.resize(img_sizes[idx])
            
            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space) #height값 + 사용자가 지정한 간격
            
            progress = (idx+1) / len(images) * 100 #실제 percent 정보를 계산
            p_var.set(progress)
            progressbar.update()
            
        #포맷 옵션 처리
        file_name = "Mich Photo." + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림", "작업이 완료되었습니다")
        
    except Exception as err:
        msgbox.showerror("Error", err)
    
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

    #이미지 통합 작업
    merge_image()

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