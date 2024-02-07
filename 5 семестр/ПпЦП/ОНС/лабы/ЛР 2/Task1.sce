// Диапазон значений x
x = [-10:0.05:10];

// Значения функции tansig и её производной
y1 = ann_tansig_activ(x);
y2 = ann_d_tansig_activ(y1);

// График функции tansig и её производной
subplot(1, 2, 1);
plot(x, y1, 'r', x, y2, 'b');
title('График функции tansig и её производной');
xlabel('x');
ylabel('y');
legend('tansig', 'tansig''');

// Значения функции purelin и её производной
y1 = ann_purelin_activ(x);
y2 = ann_d_purelin_activ(y1);

// График функции purelin и её производной
subplot(1, 2, 2);
plot(x, y1, 'r', x, y2, 'b');
title('График функции purelin и её производной');
xlabel('x');
ylabel('y');
legend('purelin', 'purelin''');
