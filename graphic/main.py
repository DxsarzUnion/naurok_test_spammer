from naurok import Client
from threading import Thread
import customtkinter
from tkinter.ttk import Spinbox
from tkinter import messagebox
from datetime import datetime
from webbrowser import open as wopen

def date_now(): return str(datetime.now()).split(" ")[0].replace("-", ".")
def time_now(): return str(datetime.now()).split(" ")[1].split(".")[0]
def create_time(): return f'{date_now()} - {time_now()}'

class UI:
	customtkinter.set_appearance_mode("System")
	customtkinter.set_default_color_theme("blue")
	app = customtkinter.CTk()
	app.title("TRaider")
	app.geometry("200x240")
	app.resizable(False, False)

	buffer = []

	nicks: str = None
	testId: str = None
	threads_count: int = 1
	console: customtkinter.CTkTextbox = None


	def get_obj(self, name: str):
		for obj in self.buffer:
			if obj["name"] == name:return obj["obj"]


	def start_click(self):
		try:self.threads_count = int(self.get_obj("th_count").get())
		except ValueError:
			messagebox.showerror("Ошибка", "Укажите число потоков.")
			return
		self.nicks = self.get_obj("name_entry").get() if self.get_obj("name_entry").get() else None
		if self.get_obj("link_entry").get():
			testId= testId = self.get_obj("link_entry").get().split("/")[-1].split("=")[-1]
			if self.check(testId):
				self.testId=testId
				self.clear()
				self.buildV2()
				for i in range(self.threads_count):
					Thread(target=self.main, args=(i+1,)).start()
		else:
			messagebox.showerror("Ошибка", "Укажите ссылку на тест.")
			return 


	def check(self, testId: str):
		c = Client()
		try:
			uuid = c.start_test(testId=testId, nick=self.nicks)
			try:session_id = c.get_session_id(uuid)
			except Exception as e:
				messagebox.showerror("Ошибка", "Не удалось достать session_id")
				del c
				return False
			c.end_test(session_id)
			messagebox.showinfo("Ошибка", "Тест проверен.")
		except Exception as e:
			messagebox.showerror("Ошибка", "Не удалось запустить текст")
			del c
			return False
		del c
		return True



	def clear(self):
		for obj in self.buffer:
			obj["obj"].destroy()
		self.buffer=list()


	def out(self, text):
		self.console.configure(state='normal')
		self.console.insert('end', f"\n[{create_time()}] {text}")
		self.console.configure(state='disabled')



	def buildV1(self):
		name_entry = customtkinter.CTkEntry(master=self.app, placeholder_text="Ник (не обязательно)")
		link_entry = customtkinter.CTkEntry(master=self.app, placeholder_text="Ссылка на тест")
		th_count = Spinbox(master=self.app, from_=1, to=100, width=5)
		th_lbl = customtkinter.CTkLabel(master=self.app, text="Коло-во потоков:")
		button = customtkinter.CTkButton(master=self.app, text="Запустить", command=self.start_click)
		name_entry.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
		link_entry.place(relx=0.5, rely=0.35, anchor=customtkinter.CENTER)
		th_lbl.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
		th_count.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
		button.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)

		for obj in [name_entry, link_entry, th_count, button, th_lbl]:
			for name, value in locals().items():
				if value is obj:
					self.buffer.append({"obj": obj, "name": name})
	
	def buildV2(self):
		self.app.geometry("800x600")
		self.app.title("TRaider : Naurok test spammer")
		self.console = customtkinter.CTkTextbox(master=self.app, width=750, height=500)
		self.console.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)
		self.console.configure(state='disabled')
		customtkinter.CTkButton(master=self.app, text="github", command=lambda: wopen("https://github.com/xXxCLOTIxXx")).place(relx=0.2, rely=0.95, anchor=customtkinter.CENTER)
		customtkinter.CTkButton(master=self.app, text="telegram", command=lambda: wopen("https://t.me/DxsarzUnion")).place(relx=0.4, rely=0.95, anchor=customtkinter.CENTER)
		customtkinter.CTkButton(master=self.app, text="discord", command=lambda: wopen("https://discord.gg/GtpUnsHHT4")).place(relx=0.6, rely=0.95, anchor=customtkinter.CENTER)
		customtkinter.CTkButton(master=self.app, text="youtube", command=lambda: wopen("https://www.youtube.com/@Xsarzy")).place(relx=0.8, rely=0.95, anchor=customtkinter.CENTER)



	
	def main(self, num: int):
		self.out(f"Запущен поток [{num}]")
		client = Client()
		while True:
			uuid = client.start_test(testId=self.testId, nick=self.nicks)
			self.out(f"[{num}]Тест запущен [{uuid}]")
			try:session_id = client.get_session_id(uuid)
			except Exception:
				self.out(f"[{num}]Не удалось достать session_id")
				continue
			client.end_test(session_id)
			self.out(f"[{num}]Тест завершен [https://naurok.com.ua/test/complete/{uuid}]")




if __name__ == "__main__":
	ui = UI()
	ui.buildV1()
	UI().app.mainloop()