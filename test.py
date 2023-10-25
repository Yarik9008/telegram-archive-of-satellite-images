import yadisk

# y = yadisk.YaDisk(token="<токен>")
# или
y = yadisk.YaDisk("55e51759dd214657a39b8f7b6d07c040", "0193d99275ef4450a96f677f9c083ff8", "y0_AgAAAAA5moDRAAqyiQAAAADvzebH-Cc3Azz2SL-rkANpwzA9o4olw5M")

# Проверяет, валиден ли токен
print(y.check_token())

print(y.get_disk_info())