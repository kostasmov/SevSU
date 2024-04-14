function y = f(x)
    y = x .* (sin(x) + cos(x)) .* (x - cotg(2*x)) ./ (1 + sin(x)^2);
endfunction

x = linspace(0, %pi/2, 10); // вектор значений x
plot2d(x, f(x));            // построение графика y=f(x)
xgrid;                      // сетка
xtitle("f(x)=x(sinx+cosx)(x-cot2x)/(1+(sinx)^2)", 'x', 'y');
