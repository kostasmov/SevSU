function z=f(x,y)
    z = exp((y + 5) / x^2) - sqrt(y + x);
endfunction

x = linspace(0, 3, 3);
y = linspace(0, 3, 3);
z = feval(x, y, f);      // определить z
plot3d1(x, y, z');       // печать 3D-графика
xtitle("Задание 3. f(x, y) = e^((y+5)/x^2)-√(y+x)")
