# Импортируем библиотеку, соответствующую типу нашей базы данных
# В данном случае импортируем все ее содержимое, чтобы при обращении не писать каждый раз имя библиотеки, как мы делали в первой статье
from peewee import Model, SqliteDatabase, AutoField, TextField, IntegerField

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = SqliteDatabase('korobka.db')


# ТУТ БУДЕТ КОД НАШИХ МОДЕЛЕЙ
# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):
    class Meta:
        database = conn  # соединение с базой, из шаблона выше


# Определяем модель юзера
class User(BaseModel):
    name = TextField(column_name='name', null=True)
    strength = IntegerField(column_name='strength', null=True)

    class Meta:
        table_name = 'User'


# Создаем курсор - специальный объект для запросов и получения данных с базы
cursor = conn.cursor()

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ

# Не забываем закрыть соединение с базой данных
conn.close()
