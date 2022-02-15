# Импортируем библиотеку, соответствующую типу нашей базы данных В данном случае импортируем все ее содержимое,
# чтобы при обращении не писать каждый раз имя библиотеки, как мы делали в первой статье
from peewee import Model, SqliteDatabase, TextField, IntegerField, ForeignKeyField, FloatField, DateTimeField

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы

conn = SqliteDatabase('korobka.db')


# ТУТ БУДЕТ КОД НАШИХ МОДЕЛЕЙ.
# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):
    class Meta:
        database = conn  # соединение с базой, из шаблона выше


class NameSynonims(BaseModel):
    names = TextField(column_name='names', null=True)


'''егорка, свит, крок, соня, димка, витя, валера, москвич, пюрешка, кряк, кроцк, витёк, витек, егор'''


# Определяем модель юзера
class User(BaseModel):
    username = TextField(column_name='username', null=True)
    first_name = TextField(column_name='first_name', null=True)
    strength = FloatField(column_name='strength', null=True)
    telegram_id = IntegerField(column_name='telegram_id', unique=True)
    wins = IntegerField(column_name='wins', default=0)
    loses = IntegerField(column_name='loses', default=0)
    last_efficient_duel = DateTimeField(null=True, formats='%Y-%m-%d %H:%M:%S.%f')
    efficient_duels_count = IntegerField(default=0)

    class Meta:
        table_name = 'User'


class NameSynonim(BaseModel):
    user = ForeignKeyField(User, on_delete='NO ACTION', backref='synonims')
    name_synonims = TextField(column_name='name_synonims', null=True)


class Insult(BaseModel):
    user = ForeignKeyField(User)
    insults = TextField()

    class Meta:
        table_name = 'Insult'


class TextVariants(BaseModel):
    name = TextField(column_name='name')
    text = TextField(column_name='text')

class Info(BaseModel):
    text = TextField(column_name='text', null=True)
    percentage = FloatField()
