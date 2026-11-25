"""Завдання 2. Обчислення визначеного інтеграла методом Монте-Карло."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


def f(x):
    return x ** 2


a = 0  # Нижня межа
b = 2  # Верхня межа


def monte_carlo_integral(func, a, b, n_points, rng):
    """Метод «влучань»: кидаємо випадкові точки в прямокутник [a, b] x [0, y_max]
    і рахуємо частку точок під кривою. Інтеграл = площа прямокутника * частка.
    """
    y_max = func(np.linspace(a, b, 1000)).max()
    x = rng.uniform(a, b, n_points)
    y = rng.uniform(0, y_max, n_points)
    under_curve = y <= func(x)
    integral = (b - a) * y_max * under_curve.mean()
    return integral, x, y, under_curve


def plot(func, a, b, x_pts, y_pts, under_curve, filename="monte_carlo.png"):
    x = np.linspace(-0.5, 2.5, 400)
    y = func(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, "r", linewidth=2)

    ix = np.linspace(a, b)
    ax.fill_between(ix, func(ix), color="gray", alpha=0.3)

    shown = slice(0, 2000)  # показуємо лише частину точок, щоб графік був читабельним
    ax.scatter(x_pts[shown][under_curve[shown]], y_pts[shown][under_curve[shown]], s=2, color="green", label="під кривою")
    ax.scatter(x_pts[shown][~under_curve[shown]], y_pts[shown][~under_curve[shown]], s=2, color="blue", label="над кривою")

    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")
    ax.set_title("Графік інтегрування f(x) = x^2 від " + str(a) + " до " + str(b))
    ax.legend(loc="upper left")
    plt.grid()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    return filename


def main():
    rng = np.random.default_rng(42)

    analytic = (b ** 3 - a ** 3) / 3
    quad_result, quad_error = spi.quad(f, a, b)

    print(f"Аналітично:  {analytic:.6f}")
    print(f"SciPy quad:  {quad_result:.6f} (оцінка похибки {quad_error:.1e})")
    print()
    print(f"{'Точок':>10} | {'Монте-Карло':>12} | {'Абс. похибка':>12} | {'Відн. похибка':>13}")
    print("-" * 56)

    for n in (100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000):
        mc, x_pts, y_pts, under = monte_carlo_integral(f, a, b, n, rng)
        abs_err = abs(mc - quad_result)
        print(f"{n:>10} | {mc:>12.6f} | {abs_err:>12.6f} | {abs_err / quad_result:>12.3%}")
        if n == 10_000:
            filename = plot(f, a, b, x_pts, y_pts, under)

    print(f"\nГрафік збережено у {filename}")


if __name__ == "__main__":
    main()
