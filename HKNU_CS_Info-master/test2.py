import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import json
import re

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("데이터베이스 관리")

        # Notebook 위젯 생성
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        # 필터링 관리 탭 생성
        self.filtering_tab = tk.Frame(self.notebook)
        self.notebook.add(self.filtering_tab, text="필터링 관리")
        self.setup_filtering_management(self.filtering_tab)

        # 공지 관리 탭 생성
        self.notice_tab = tk.Frame(self.notebook)
        self.notebook.add(self.notice_tab, text="공지 관리")
        self.setup_notice_management(self.notice_tab)

    def setup_filtering_management(self, tab):
        # 필터링 관리 탭 안에 새로운 Notebook 생성
        inner_notebook = ttk.Notebook(tab)
        inner_notebook.pack(expand=1, fill='both')
        
        name = ["한경공지", "학사공지", "장학공지", "취창업공지", "채용공지"]
        name_txt = ["hankyong", "haksa", "janghak", "changup", "chaeyong"]

        # 5개의 서브탭 생성
        for i in range(5):
            inner_tab = ttk.Frame(inner_notebook)
            inner_notebook.add(inner_tab, text=name[i])
            self.setup_sub_tab(inner_tab, name_txt[i])

    def setup_sub_tab(self, tab, tab_name):
        def load_words_from_file(file_name, words_list):
            with open(file_name, 'r', encoding='UTF8') as file:
                words = file.read().split()
                words_list.configure(state=tk.NORMAL)
                words_list.delete(0, tk.END)
                for word in words:
                    words_list.insert(tk.END, word)
            return words

        def save_words_to_file(file_name, words):
            with open(file_name, 'w', encoding='UTF8') as file:
                file.write(' '.join(words))

        def delete_selected_word(words_list, words, file_name, label):
            selected_word_index = words_list.curselection()
            if selected_word_index:
                selected_word = words_list.get(selected_word_index)
                words_list.delete(selected_word_index)
                words.remove(selected_word)
                save_words_to_file(file_name, words)
                label.config(text="")

        def add_word_to_list_and_file(entry, words_list, words, file_name):
            new_word = entry.get().strip()
            if new_word and new_word not in words:
                words.append(new_word)
                words_list.insert(tk.END, new_word)
                save_words_to_file(file_name, words)
                entry.delete(0, tk.END)  # 입력란을 비웁니다.

        def on_select(event, label):
            selected_indices = event.widget.curselection()
            if selected_indices:
                selected_word = event.widget.get(selected_indices[0])
                label.config(text=selected_word)

        exclude_label = tk.Label(tab, text="제외 키워드:")
        exclude_label.place(x=5, y=3)

        words_list = tk.Listbox(tab, width=40, height=10, activestyle='none')
        words_list.place(x=5, y=23)
        words_list.bind("<<ListboxSelect>>", lambda event: on_select(event, exclude_selected_label))

        exclude_label2 = tk.Label(tab, text="포함 키워드:")
        exclude_label2.place(x=5, y=200)

        words_list2 = tk.Listbox(tab, width=40, height=10, activestyle='none')
        words_list2.place(x=5, y=220)
        words_list2.bind("<<ListboxSelect>>", lambda event: on_select(event, include_selected_label))

        words1 = load_words_from_file(f"./filter/{tab_name}.txt", words_list)
        words2 = load_words_from_file(f"./keyword/{tab_name}.txt", words_list2)

        entry1 = tk.Entry(tab)
        entry1.place(x=330, y=25, height=25)
        add_button1 = tk.Button(tab, text="제외 키워드 추가", command=lambda: add_word_to_list_and_file(entry1, words_list, words1, f"./filter/{tab_name}.txt"))
        add_button1.place(x=480, y=25)

        entry2 = tk.Entry(tab)
        entry2.place(x=330, y=223, height=25)
        add_button2 = tk.Button(tab, text="포함 키워드 추가", command=lambda: add_word_to_list_and_file(entry2, words_list2, words2, f"./keyword/{tab_name}.txt"))
        add_button2.place(x=480, y=223)

        exclude_selected_label = tk.Label(tab, text="", bg="white", width=20)
        exclude_selected_label.place(x=330, y=100, height=25)
        delete_button1 = tk.Button(tab, text="제외 키워드 삭제", command=lambda: delete_selected_word(words_list, words1, f"./filter/{tab_name}.txt", exclude_selected_label))
        delete_button1.place(x=480, y=100)

        include_selected_label = tk.Label(tab, text="", bg="white", width=20)
        include_selected_label.place(x=330, y=300, height=25)
        delete_button2 = tk.Button(tab, text="포함 키워드 삭제", command=lambda: delete_selected_word(words_list2, words2, f"./keyword/{tab_name}.txt", include_selected_label))
        delete_button2.place(x=480, y=300)

    def setup_notice_management(self, tab):
        inner_notebook = ttk.Notebook(tab)
        inner_notebook.pack(expand=1, fill='both')

        name = ["2,3학년", "4학년"]
        tab_keys = ["g23", "g4"]
        json_file = 'json/classified_data.json'

        for i in range(2):
            inner_tab = ttk.Frame(inner_notebook)
            inner_notebook.add(inner_tab, text=name[i])
            self.setup_notice_sub_tab(inner_tab, json_file, tab_keys[i])

    def setup_notice_management(self, tab):
        inner_notebook = ttk.Notebook(tab)
        inner_notebook.pack(expand=1, fill='both')

        name = ["2,3학년", "4학년"]
        tab_keys = ["g23", "g4"]
        json_file = 'json/classified_data.json'

        for i in range(2):
            inner_tab = ttk.Frame(inner_notebook)
            inner_notebook.add(inner_tab, text=name[i])
            self.setup_notice_sub_tab(inner_tab, json_file, tab_keys[i])

    def setup_notice_sub_tab(self, tab, json_file, tab_key):
        def load_json_data(file_name):
            with open(file_name, 'r', encoding='UTF8') as file:
                return json.load(file)

        def save_json_data(file_name, data):
            with open(file_name, 'w', encoding='UTF8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        def delete_selected_notice(notice_list, data, file_name, label):
            with open('json/data.json', 'r', encoding='utf-8') as f:
                data_json = json.load(f)

            selected_index = notice_list.curselection()
            if selected_index:
                selected_notice = notice_list.get(selected_index)
                notice_list.delete(selected_index)
                for notice in data[tab_key]:
                    if notice['제목'] == selected_notice:
                        data[tab_key].remove(notice)
                        break
                save_json_data(file_name, data)
                label.config(text="")

                data_json['deleted'].append(selected_notice)
                with open('json/data.json', 'w', encoding='utf-8') as file:
                        json.dump(data_json, file, ensure_ascii=False, indent=4)

        def add_notice_to_list_and_file(entry_num, entry_title, entry_date, combo, notice_list, data, file_name):
            new_notice_num = entry_num.get().strip()
            new_notice_title = entry_title.get().strip()
            new_notice_date = entry_date.get().strip()
            selected_board = combo.get()

            board_mapping = {
                "한경공지": "hankyong",
                "학사공지": "haksa",
                "장학공지": "janghak",
                "취창업공지": "changup",
                "채용공지": "chaeyong"
            }
            target_key = board_mapping.get(selected_board)

            # 입력 값 검증
            if not new_notice_num or not new_notice_title or not new_notice_date or not selected_board:
                messagebox.showwarning("입력 오류", "모든 필드를 입력하세요.")
                return

            if not re.match(r"^\d{4}\.\d{2}\.\d{2}$", new_notice_date):
                messagebox.showwarning("날짜 형식 오류", "작성일 형식이 잘못되었습니다. yyyy.mm.dd 형식으로 입력하세요.")
                return

            if target_key and new_notice_num and new_notice_title and new_notice_date:
                new_notice = {"번호": new_notice_num, "작성일": new_notice_date, "제목": new_notice_title}
                data[tab_key].append(new_notice)
                notice_list.insert(tk.END, new_notice_title)
                save_json_data(file_name, data)

                with open('json/data.json', 'r', encoding='utf-8') as f:
                    data_json = json.load(f)

                if target_key in data_json:
                    data_json[target_key].append(new_notice)
                else:
                    data_json[target_key] = [new_notice]
                
                with open('json/data.json', 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=4)

                entry_num.delete(0, tk.END)  # 입력란을 비웁니다.
                entry_title.delete(0, tk.END)  # 입력란을 비웁니다.
                entry_date.delete(0, tk.END)  # 입력란을 비웁니다.
                combo.set('')  # 셀렉트 박스를 초기화합니다.

        def on_select(event, label):
            selected_indices = event.widget.curselection()
            if selected_indices:
                selected_notice = event.widget.get(selected_indices[0])
                label.config(text=selected_notice)

        data = load_json_data(json_file)

        notice_label = tk.Label(tab, text="공지:")
        notice_label.place(x=5, y=3)

        notice_list = tk.Listbox(tab, width=96, height=10, activestyle='none')
        notice_list.place(x=5, y=23)
        notice_list.bind("<<ListboxSelect>>", lambda event: on_select(event, selected_notice_label))

        for notice in data.get(tab_key, []):
            notice_list.insert(tk.END, notice['제목'])

        board_label = tk.Label(tab, text="공지 게시판:")
        board_label.place(x=30, y=190)
        combo = ttk.Combobox(tab, values=["한경공지", "학사공지", "장학공지", "취창업공지", "채용공지"])
        combo.place(x=120, y=190, height=25, width=100)

        num_label = tk.Label(tab, text="번호:")
        num_label.place(x=30, y=220)
        entry_num = tk.Entry(tab)
        entry_num.place(x=80, y=220, height=25)

        title_label = tk.Label(tab, text="제목:")
        title_label.place(x=30, y=250)
        entry_title = tk.Entry(tab)
        entry_title.place(x=80, y=250, height=25, width=480)

        date_label = tk.Label(tab, text="작성일:")
        date_label.place(x=30, y=280)
        entry_date = tk.Entry(tab)
        entry_date.place(x=80, y=280, height=25)

        add_button = tk.Button(tab, text="공지 추가", command=lambda: add_notice_to_list_and_file(entry_num, entry_title, entry_date, combo, notice_list, data, json_file))
        add_button.place(x=160, y=310)

        selected = tk.Label(tab, text="선택된 공지:")
        selected.place(x=5, y=370)
        selected_notice_label = tk.Label(tab, text="", bg="white", width=20)
        selected_notice_label.place(x=80, y=370, height=25, width=540)
        delete_button = tk.Button(tab, text="공지 삭제", command=lambda: delete_selected_notice(notice_list, data, json_file, selected_notice_label))
        delete_button.place(x=560, y=400)

app = Application()
app.mainloop()
