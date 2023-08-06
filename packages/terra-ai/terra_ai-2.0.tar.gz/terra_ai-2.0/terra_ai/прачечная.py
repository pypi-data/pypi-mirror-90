#Библиотеки
import random as random # Импортируем библиотку генерации случайных значений
import numpy as np # Импортируем библиотеку numpy
import matplotlib.pyplot as plt # Импортируем модуль pyplot библиотеки matplotlib
import matplotlib.colors as colors # Импортируем модуль colors библиотеки matplotlib
import pandas as pd
import random
from tabulate import tabulate
import seaborn as sns
from IPython.display import display, HTML
sns.set_style('darkgrid')


'''
    Функция получения выжившей популяции
        Входные параметры:
        - popul - наша популяция
        - val - текущие значения
        - nsurv - количество выживших
        - reverse - указываем требуемую операцию поиска результата: максимизация или минимизация
'''
def getSurvPopul(
        popul,
        val,
        nsurv,
        reverse
        ):
    newpopul = [] # Двумерный массив для новой популяции
    sval = sorted(val, reverse=reverse) # Сортируем зачения в val в зависимости от параметра reverse    
    for i in range(nsurv): # Проходимся по циклу nsurv-раз (в итоге в newpopul запишется nsurv-лучших показателей)
        index = val.index(sval[i]) # Получаем индекс i-того элемента sval в исходном массиве val
        newpopul.append(popul[index]) # В новую папуляцию добавляем элемент из текущей популяции с найденным индексом
    return newpopul, sval # Возвращаем новую популяцию (из nsurv элементов) и сортированный список

'''
    Функция получения родителей
        Входные параметры:
        - curr_popul - текущая популяция
        - nsurv - количество выживших
'''
def getParents(
        curr_popul,
        nsurv
        ):   
    indexp1 = random.randint(0, nsurv - 1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
    indexp2 = random.randint(0, nsurv - 1) # Случайный индекс второго родителя в диапазоне от 0 до nsurv - 1    
    botp1 = curr_popul[indexp1] # Получаем первого бота-родителя по indexp1
    botp2 = curr_popul[indexp2] # Получаем второго бота-родителя по indexp2    
    return botp1, botp2 # Возвращаем обоих полученных ботов

'''
    Функция смешивания (кроссинговера) двух родителей
        Входные параметры:
        - botp1 - первый бот-родитель
        - botp2 - второй бот-родитель
        - j - номер компонента бота
'''
def crossPointFrom2Parents(
        botp1,
        botp2, 
        j
        ):
    pindex = random.random() # Получаем случайное число в диапазоне от 0 до 1
    
    # Если pindex меньше 0.5, то берем значения от первого бота, иначе от второго
    if pindex < 0.5:
        x = botp1[j]
    else:
        x = botp2[j]
    return x # Возвращаем значние бота

    #доп функции
def pprint_df(dframe):
    print(tabulate(dframe, headers='keys', tablefmt='psql', showindex=False))

# Custom function to color the desired cell
def закрасить_ячейку(дата_фрейм, номер_строки, номер_столбца, цвет_ячейки,  цвет_текста):
    color = 'background-color: green; color: white'
    df_styler = pd.DataFrame('', index=дата_фрейм.index, columns=дата_фрейм.columns)
    df_styler.iloc[номер_строки, номер_столбца] = color
    return df_styler
    
def ввод_данных():
  global стиральные_машины
  global вместимость_машин
  global время_на_стирку
  global количество_мешков
  global вес_мешков

  global новые_мешки
  global количество_новых_мешков
  global вес_новых_мешков

  global cycle_time
  global data_frame
  global data_frame_m

  global вектор_вместимости_на_день

  cycle_time = ['8:00','8:30',	'9:00',	'9:30',	'10:00',	'10:30',	'11:00',	'11:30',	
              '12:00',	'12:30',	'13:00',	'13:30',	'14:00',	'14:30',	'15:00',	
              '15:30',	'16:00', '16:30',	'17:00',	'17:30',	'18:00',	'18:30',	
              '19:00',	'19:30',	'20:00']

  rand_or_request = input('Ввести данные "случайно" или "вручную" ? ')
  rand_or_request = rand_or_request.lower()

  if all(i in 'случайно' for i in rand_or_request):
    стиральные_машины = np.arange(1, 3 + 1 )

    вместимость_машин = [] 
    for m in стиральные_машины:
      sr = random.SystemRandom()
      c = sr.randrange(8, 16, 2)
      вместимость_машин.append(c)
    
    время_на_стирку = []
    for m in стиральные_машины:
      rr = random.SystemRandom()
      cycle = sr.randrange(60, 120, 30)
      время_на_стирку.append(cycle)
    
    time = []
    m = 65
    for i in range(m):
      time.append(cycle_time[0])
    количество_мешков = np.arange(1, m + 1 ) #Количество мешков   
    вес_мешков = np.random.randint(2, 8, len(количество_мешков)) #Масса каждого мешка
    
    новые_мешки = ['10:00', '15:00', '18:00']
    количество_новых_мешков = np.arange(1, 10 + 1 ) #Количество мешков   
    вес_новых_мешков =  np.random.randint(2, 8, len(количество_новых_мешков))

    #добавляем в конец новые мешки
    for i in range(len(количество_новых_мешков)):
      id_maker = m + количество_новых_мешков[i]
      количество_мешков = np.append(количество_мешков, id_maker)
    
    #добавляем в конец новые веса
    for i in range(len(вес_новых_мешков)):
      вес_мешков = np.append(вес_мешков, вес_новых_мешков[i])

    
    m = 65
    for i in range(len(количество_мешков)):
      time.append(cycle_time[0])

    firs_bags_new = количество_новых_мешков[3]
    second_bags_new = количество_новых_мешков[2]
    fird_bags_new = количество_новых_мешков[2]

    time_new_bags = []
    for i in range(len(количество_новых_мешков)):
      if i == 1:
        for t in range(fird_bags_new):
          time_new_bags.append(новые_мешки[0])
      elif i == 2:
        for t in range(second_bags_new):
          time_new_bags.append(новые_мешки[1])
      elif i == 3:
        for t in range(firs_bags_new):
          time_new_bags.append(новые_мешки[2])
    time[m:] = time_new_bags

    print('__________________________________________________________')
    print('Количество стиральных машинок:', len(стиральные_машины))
    print('Время цикла на стирку:', время_на_стирку)
    print('Вместимость:', вместимость_машин, '\n')
    print('Количество мешков в начале смены:', m)
    print('Количество новых мешков:', len(количество_мешков[m:]))
    print('Количество мешков на весь день:', len(количество_мешков))

    data_frame = pd.DataFrame({'Машинки': стиральные_машины, 'Макс. загрузка': вместимость_машин, 'Время цикла': время_на_стирку})
    for t in cycle_time:
      data_frame[t] = 0

    for m in range(len(стиральные_машины)):
      for t in range(len(cycle_time)):
        if t == 0:
          data_frame.loc[(data_frame['Машинки'] == стиральные_машины[m]), '8:00'] = вместимость_машин[m]
        
        else:
          df_mach = data_frame[(data_frame['Машинки'] == стиральные_машины[m])]
          time_max = df_mach.values[:,2][0]
          cycle = time_max / 30 
          avalible_time = np.arange(int(cycle), len(cycle_time), int(cycle))

          for av in avalible_time:
            data_frame.loc[(data_frame['Машинки'] == стиральные_машины[m]), cycle_time[av]] = вместимость_машин[m]
    '''
    Блок принтов
    '''
    machines = pd.DataFrame({'Машинки': стиральные_машины, 'Вместимость(кг)': вместимость_машин, 'Время на один цикл': время_на_стирку})
    data_frame_m = pd.DataFrame(data = [вес_мешков, time], columns=количество_мешков, index=['вес мешка', 'время доступа'])
    machines = machines.set_index('Машинки').dropna()
    data_frame = data_frame.set_index('Машинки')
    print()
    print('Информация о стиральных машинах')
    display(machines.head())
    print()
    print('Информация о мешках и врмени когда мешок будет готов к стирке')
    display(data_frame_m.head())

    #Вектор временных индексов
    numpy_df = data_frame.to_numpy()
    вместимость_на_день = numpy_df[:, 2:30]
    вектор_вместимости_на_день = вместимость_на_день.reshape(len(стиральные_машины)*25,)

    #Ввод от пользователя
  elif all(i in 'вручную' for i in rand_or_request):
    #Создаем массив с номерами стиральных машин
    time = []
    n_m = int(input('Введите количество стиральных машин: '))
    print()
    стиральные_машины = np.arange(1, n_m + 1 )

    вместимость_машин = [] #Список для максимальной загрузки
    for m in стиральные_машины:
      print('Максимальная загрузка в "кг" для стиральной машинки под номером:', m)
      n_temp = int(input('Введите вместимость в "кг": '))
      print()
      вместимость_машин.append(n_temp)

    #Вводим максимальное время цикла стирки для каждой машины
    время_на_стирку = []
    for m in стиральные_машины:
      print('Максимальное время цикла интервал "30 минут"стирки для машинки под номером:', m)
      cycle = int(input('Максимальное время на стирку: '))
      print()
      время_на_стирку.append(cycle)

    #Количесвто мешков, количество которое известно в начале смены
    мешки = int(input('Введите количество мешков для стирки: '))
    print()
    количество_мешков = np.arange(1, мешки + 1 )

    вес_мешков = np.random.randint(2, 8, len(количество_мешков))#Масса каждого мешка
    
    for i in range(мешки):
      time.append(cycle_time[0])

    #Новые мешки
    новые_мешки = input('В какое время приедут новые мешки, введите время в диапазоне с 8:00 - 20:00, интервал 30 минут: ').split()

    количество_новых_мешков = []
    for i in range(len(новые_мешки)):
      print('Какое количесвто мешков приедет в: ', новые_мешки[i])
      temp = int(input(''))
      массив_мешков = np.arange(1, temp + 1)
      количество_новых_мешков.append(массив_мешков)

    time_new_bags = []
    for i in range(len(количество_новых_мешков)):
      t = max(количество_новых_мешков[i])
      for j in range(t):
        time_new_bags.append(новые_мешки[i])
    time[мешки:] = time_new_bags

    вес_новых_мешков = []
    for nm in range(len(количество_новых_мешков)):
      n = количество_новых_мешков[nm][-1]
      вес_мешков_temp = np.random.randint(2, 8, n)
      вес_новых_мешков.append(вес_мешков_temp)

    #добавляем в конец новые мешки
    for i in range(len(количество_новых_мешков)):
      id_maker = количество_мешков[-1] + количество_новых_мешков[i]
      количество_мешков = np.concatenate([количество_мешков, id_maker])

    #добавляем в конец новые веса
    for i in range(len(вес_новых_мешков)):
      вес_мешков = np.concatenate([вес_мешков, вес_новых_мешков[i]])

    print('__________________________________________________________')
    print('Количество стиральных машинок:', len(стиральные_машины))
    print('Время цикла на стирку:', время_на_стирку)
    print('Вместимость:', вместимость_машин, '\n')
    print('Количество мешков в начале смены:', мешки)
    print('Количество новых мешков:', len(количество_мешков[мешки:]))
    print('Количество мешков на весь день:', len(количество_мешков))

    data_frame = pd.DataFrame({'Машинки': стиральные_машины, 'Макс. загрузка': вместимость_машин, 'Время цикла': время_на_стирку})
    for t in cycle_time:
      data_frame[t] = 0

    for m in range(len(стиральные_машины)):
      for t in range(len(cycle_time)):
        if t == 0:
          data_frame.loc[(data_frame['Машинки'] == стиральные_машины[m]), '8:00'] = вместимость_машин[m]
        
        else:
          df_mach = data_frame[(data_frame['Машинки'] == стиральные_машины[m])]
          time_max = df_mach.values[:,2][0]
          cycle = time_max / 30 
          avalible_time = np.arange(int(cycle), len(cycle_time), int(cycle))

          for av in avalible_time:
            data_frame.loc[(data_frame['Машинки'] == стиральные_машины[m]), cycle_time[av]] = вместимость_машин[m]
    '''
    Блок принтов
    '''
    machines = pd.DataFrame({'Машинки': стиральные_машины, 'Вместимость(кг)': вместимость_машин, 'Время на один цикл': время_на_стирку})
    data_frame_m = pd.DataFrame(data = [вес_мешков, time], columns=количество_мешков, index=['вес мешка', 'время доступа'])
    machines = machines.set_index('Машинки').dropna()
    data_frame = data_frame.set_index('Машинки')
    print()
    print('Информация о стиральных машинах')
    display(machines.head())
    print()
    print('Информация о мешках и врмени когда мешок будет готов к стирке')
    display(data_frame_m.head())

    #Вектор временных индексов
    numpy_df = data_frame.to_numpy()
    вместимость_на_день = numpy_df[:, 2:30]
    вектор_вместимости_на_день = вместимость_на_день.reshape(len(стиральные_машины)*25,)
def рассчитать_план_на_день(общее_число_ботов, количество_выживших, количество_эпох, коэфициент_мутаций):
  global data_frame
  n = общее_число_ботов # Общее число ботов
  nsurv = количество_выживших # Количество выживших (столько лучших переходит в новую популяцию)
  nnew = общее_число_ботов - количество_выживших  # Количество новых (столько новых ботов создается)
  epohs = количество_эпох # количество эпох
  mut = коэфициент_мутаций # коэфициент мутаций

  # Длина бота(количество мешков)
  l = вес_мешков.shape[0] 
  trains = вектор_вместимости_на_день.shape[0] # Количество меток на каждый цикл

  popul = [] # Двумерный массив популяции, размерностью [n, l].
  val = [] # Одномерный массив значений этих ботов

  plotmeanval = [] # сюда будут заносится значения для графика по среднему значению
  plotminval = [] # сюда будут заносится значения для графика по минимальному значению
  
  for i in range(n): # Проходим по всей длине популяции
      popul.append([]) # Создаем пустого бота
      for j in range(l): # Проходим по всей длине бота
          
          # В каждый компонент бота записываем рандомное значение в диапазоне от 0 до количества циклов на день
          popul[i].append(random.randint(0, trains - 1)) 

  for it in range(epohs): # Проходим по всем эпохам

      if (it == 500): # Меняем коэфициент мутации после 500-ой эпохи
          mut = 0.1   
      if (it == 1000): # Меняем коэфициет мутации после 1000-ой эпохи
          mut = 0.05  

      val = [] # Создаем пустой список для значений ботов
      for i in range(n): # Проходим по всей популяции
          bot = popul[i] # Берем очередного бота
          trainfill = np.zeros(shape=trains) # Массив, хранящий заполняемость каждой машинки во время цикла
          for j in range(l): # Проходим по всей длине бота
              trainfill[bot[j]] += вес_мешков[j] # Увеличиваем заполненность bot[j] на вес_мешков[j]          
          
          f = 0 # Обнуляем ошибку i-го бота 
          for t in range(trains): # Проходим по всем меткам циклов стирки
              # Увеличиваем ошибку i-го бота на модуль разницы между реальной вместимостью во время цикла 
              # и вместимостью, который посчитал бот
              f += abs(вектор_вместимости_на_день[t] - trainfill[t])
          val.append(f) # Добавляем в val значение ошибки для i-го бота    
      
      newpopul, sval = getSurvPopul(popul, val, nsurv, 0) # Получаем новую популяцию и сортированный список значнией
      print(it, " ", sum(val) / len(val), " ", sval[0:20])  # Выводим среднее значение и 20 лучших ботов  
      plotmeanval.append(sum(val) / len(val)) # Добавляем среднее значение в список
      plotminval.append(sval[0]) # Добавляем минимальное значение в список
      
      for i in range(nnew): # Проходимся в цикле nnew-раз
          botp1, botp2 = getParents(newpopul, nsurv) # Из newpopul(новой популяции) получаем двух случайных родителей-ботов
          newbot = [] # Массив для нового бота
      
          for j in range(l): # Проходим по всей длине бота
              x = crossPointFrom2Parents(botp1, botp2, j) # Получаем значение для j-ого компонента бота
          
              # С вероятностью mut сбрасываем значение j-ого компонента бота на случайное
              if (random.random() < mut):
                  x = random.randint(0, trains - 1)        
              newbot.append(x) # Добавляем новое значение в бота      
          newpopul.append(newbot) # Добавляем бота в новую популяцию    
      popul = newpopul # Записываем в popul новую посчитанную популяцию

  # построение графиков 
  plt.plot(plotmeanval, 
          label='Среднее по популяции')
  plt.plot(plotminval, 
          label='Лучший бот')
  plt.xlabel('Эпоха обучения')
  plt.ylabel('Значение функции')
  plt.legend()
  plt.show()

  bot = popul[0] # Берем лучшее значение в популяции
  print('Значения лучшего бота:', bot, '\n') # Выводим значения бота

  trainfill = np.zeros(trains, dtype = 'int32') # Массив заполненности машинок
  for j in range(l): # Проходим по всей длине бота
      trainfill[bot[j]] += вес_мешков[j] # Увеличиваем заполненность bot[j]-ого поезда на size[j]вес_мешков

  print('Максимальная возможная загрузка на день:', вектор_вместимости_на_день.sum(),'кг', '\n')
  print('Плановое количество:', вес_мешков.sum(), 'кг')
  print('Постирано:', trainfill.sum(), 'кг')
  

  trainfill = np.full(len(вектор_вместимости_на_день), '', dtype='<U150') # Массив заполненности машинок

  for j in range(l): # Проходим по всей длине бота
    trainfill[bot[j]] += str(j) + '(' + str(вес_мешков[j]) + ') '
  trainfill_resh = trainfill.reshape(3, 25)

  for m in range(len(trainfill_resh)):
    for t in range(len(cycle_time)):
      data_frame.loc[(data_frame.index == стиральные_машины[m]), cycle_time[t]] = trainfill_resh[m][t]
      
def план_на_день():
  display(data_frame.head())
  
def информация_о_мешке():
  n = int(input('Ввдите номер мешка: '))
  план = data_frame.iloc[:, 2:].to_numpy().reshape(-1)

  for i in range(len(план)):
    if str(n) + '(' in план[i]:
      if план[i].index('(') == len(str(n)):
        result = i
        break
  idx = result // 25
  col = ((result + время_на_стирку[idx] // 30) %25) + 2  
  

  print('Номер машинки: ', idx + 1)
  print('Время начала стирки:', cycle_time[result %25])
  print('Время готовности: ', cycle_time[result %25 + время_на_стирку[idx] // 30])
  print('Зеленым цветом выделено время готовности стирки для мешка под номером:',n, '\n')

  display(data_frame.style.apply(
            закрасить_ячейку,    
            номер_строки = idx,
            номер_столбца = col,
            цвет_ячейки = 'green',
            цвет_текста = 'white',
            axis = None))