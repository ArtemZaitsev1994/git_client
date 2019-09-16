import os, subprocess


class GitClient:
	
	def __init__(self, path: str, git_exist: bool):
		"""Создание экземпляра класса
		флаг self.running используется для выхода из цикла
		"""
		self.path = path
		self.git_exist = git_exist
		self.running = True

	def init_repo(self):
		"""
		Ме тод создания пустого репозитория с первым коммитом
		и подключением к удаленному репозиторию		
		"""
		self.exec_com('touch hi.txt')
		self.exec_com('git init')
		self.exec_com('git add -A')
		self.exec_com('git commit -m "first_commit"')
		remote_repo = input('Введите ссылку на удаленный репозиторий: ')
		self.exec_com(f'git remote add origin {remote_repo}')
		self.exec_com('git push -u origin master')
		self.git_exist = True

	def get_cur_branch(self) -> str:
		"""
		Возвращает название текущей ветки
		"""
		br = self.exec_com('git branch').split('*')[1]
		br = br.split('\n')[0][1:]
		return br

	def clone(self):
		"""
		Клонирует удаленный репозиторий в текущую папку self.path
		"""
		print('_____________________________________________')
		print('|+ Введите ссылку на репозиторий           +|')
		print('|* назад - back                            *|')
		print('---------------------------------------------')
		link = input()
		if link == 'back':
			return
		result = self.exec_com(f'git clone {link}')
		if result:
			self.git_exist = True

	def exec_com(self, com: str) -> str:
		"""
		Метод исполнения команды в Bash
		"""
		pr = subprocess.Popen(com.split(), stdout=subprocess.PIPE)
		output, err = pr.communicate()
		if err is not None:
			print('Something went wrong... I\'m dying..')
			self.running = False
		return output.decode('utf-8')

	def create_branch(self):
		"""
		Метод создания новой ветки от текущей		
		"""
		print('_____________________________________________')
		print('|+ Введите имя ветки                       +|')
		print('|* Назад - back                            *|')
		print('---------------------------------------------')
		name = input().replace(' ', '_')
		if name == 'back':
			return
		self.exec_com(f'git checkout -b {name}')

	def change_branch(self):
		"""
		Метод перехода на другую ветку
		"""
		# Выводит на печать все ветки
		self.exec_com('git branch')
		print('_____________________________________________')
		print('|+ Введите имя ветки                       +|')
		print('|* Назад - back                            *|')
		print('---------------------------------------------')
		name = input().replace(' ', '_')
		if name == 'back':
			return
		self.exec_com(f'git checkout {name}')

	def commit(self):
		"""
		Метод коммитит все результаты в текущей ветке и отправляет в удаленный репозиторий
		"""
		print('_____________________________________________')
		print('|+ Коммит и пуш - yes                      +|')
		print('|* Назад        - back                     *|')
		print('---------------------------------------------')
		com = input()
		if com == 'yes':
			self.exec_com('git add -A')
			commit_mess = input('Введите сообщение коммита: ').replace(' ', '_')
			self.exec_com(f'git commit -m {commit_mess}')
			# Пытаемся запушить изменения,
			# Если это первый пуш для данной ветки,
			# То выполняем команду, чтобы указать ветку,
			# на которую будет ссылаться наша локальная
			if subprocess.run('git push'.split()).returncode == 128:
				branch = self.get_cur_branch()
				self.exec_com(f'git push --set-upstream origin {branch}')
				return

	def run(self):
		"""
		Запуск цикла работы основной программы
		"""
		while self.running:
			# Если репозиторий инициализирован в выбранной папке
			if self.git_exist:
				print('_____________________________________________')
				print('|+ Введите команду(цирфа):                 +|')
				print('|+ Создать новую ветку в репозитории   - 1 +|')
				print('|+ Переключится между ветками          - 2 +|')
				print('|+ Закомитить все изменения и запушить - 3 +|')
				print('|* Выход - exit                            *|')
				print('---------------------------------------------')
				com = input()
				if com == 'exit':
					return
				elif com == '1':
					self.create_branch()
				elif com == '2':
					self.change_branch()
				elif com == '3':
					self.commit()
			
			# Если репозиторий не инициализирован в выбранной папке
			else:
				print('_____________________________________________')
				print('|+ Введите команду(цирфа):                 +|')
				print('|+ Инициализировать пустой репозиторий - 1 +|')
				print('|+ Клонировать репозиторий             - 2 +|')
				print('|* Выход - exit                            *|')
				print('---------------------------------------------')
				com = input()
				if com == 'exit':
					return
				elif com == '1':
					self.init_repo()
				elif com == '2':
					self.clone()


if __name__ == '__main__':
	# Выбираем папку в которой будем работать с репозиторием
	path = input('Введите локальную папку: ')
	git_exist = False
	os.chdir(path)
	if '.git' in os.listdir():
		git_exist = True
	app = GitClient(path, git_exist)
	
	app.run()

