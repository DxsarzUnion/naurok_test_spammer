from naurok import Client
from threading import Thread
import colorama
colorama.init(autoreset=True)

print( f"""
[!!]Автор не несет ответственность за ваши действия {colorama.Fore.RED}
[!!]Айпи банятся, используйте прокси
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮
╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
╭━╮╭━━┳╮╭┳━┳━━┫┃╭╮╭━━┳━━┳━━┳╮╭┳╮╭┳━━┳━╮
┃╭╮┫╭╮┃┃┃┃╭┫╭╮┃╰╯╯┃━━┫╭╮┃╭╮┃╰╯┃╰╯┃┃━┫╭╯
┃┃┃┃╭╮┃╰╯┃┃┃╰╯┃╭╮╮┣━━┃╰╯┃╭╮┃┃┃┃┃┃┃┃━┫┃
╰╯╰┻╯╰┻━━┻╯╰━━┻╯╰╯╰━━┫╭━┻╯╰┻┻┻┻┻┻┻━━┻╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯
{colorama.Fore.YELLOW}MADE BY XSARZ [https://linktr.ee/xsarz]

"""
)


nick = input(f"{colorama.Fore.LIGHTBLUE_EX}Введите имя для ботов (по умолчанию рандом) #~ ")
nick = nick if nick else None
try:
	threads_count = int(input(f"{colorama.Fore.LIGHTBLUE_EX}Коло-во потоков (1 по умолчанию) #~ "))
except ValueError:
	threads_count = 1

prox = input("Введите прокси (не обязательно)[ip:port] #~ ")
if not prox:prox=None

while True:
	test_link = input(f"{colorama.Fore.LIGHTBLUE_EX}Ссылка на тест или его id #~")
	if test_link:
		testId = test_link.split("/")[-1].split("=")[-1]
		print(f"{colorama.Fore.GREEN}Айди теста:{colorama.Fore.LIGHTGREEN_EX}", testId)
		break
	print(f"{colorama.Fore.RED}Вы не указали ссылку на тест")

def check():
	c = Client(proxy=prox)
	try:
		uuid = c.start_test(testId=testId, nick=nick)
		try:session_id = c.get_session_id(uuid)
		except Exception as e:
			print(f"{colorama.Fore.RED}Не удалось достать session_id")
			exit()
		c.end_test(session_id)
		print(f"{colorama.Fore.YELLOW}Тест проверен. запуск спама...")
	except Exception as e:
		print(f"{colorama.Fore.RED}Не удалось запустить текст")
		exit()
	finally:
		del c


def main(num: int):
	print(f"\n{colorama.Fore.GREEN}Запущен поток [{colorama.Fore.LIGHTBLUE_EX}{num}{colorama.Fore.GREEN}]")
	client = Client(proxy=prox)
	while True:
		uuid = client.start_test(testId=testId, nick=nick)
		print(f"{colorama.Fore.GREEN}[{colorama.Fore.LIGHTBLUE_EX}{num}{colorama.Fore.GREEN}]Тест запущен [{uuid}]")
		try:session_id = client.get_session_id(uuid)
		except Exception:
			print(f"{colorama.Fore.RED}[{colorama.Fore.LIGHTBLUE_EX}{num}{colorama.Fore.GREEN}]Не удалось достать session_id")
		client.end_test(session_id)
		print(f"{colorama.Fore.GREEN}[{colorama.Fore.LIGHTBLUE_EX}{num}{colorama.Fore.GREEN}]Тест завершен [{colorama.Fore.LIGHTBLUE_EX}https://naurok.com.ua/test/complete/{uuid}{colorama.Fore.GREEN}]")





if __name__ == "__main__":
	check()
	for num in range(threads_count):
		Thread(target=main, args=(num+1,)).start()