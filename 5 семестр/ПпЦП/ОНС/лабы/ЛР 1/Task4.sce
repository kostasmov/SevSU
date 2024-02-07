d = grand(15, 500, "exp", 5);
histplot(20, d);    // отображение гистограммы
clf; histplot(20, d, normalization=%f)
clf; histplot(20, d, leg='exp(15, 500, ''exp λ=5'')', style=5);
clf; histplot(20, d, leg='exp(15, 500, ''exp λ=5'')', style=16, rect=[-3, 0, 3, 0.5]);
xgrid

mean(d)     // среднее
variance(d) // дисперсия
stdev(d)    // стандартное отклонение
median(d)   // медиана

