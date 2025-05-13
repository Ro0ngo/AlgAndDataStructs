import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, sqrt


def draw_circle(ax, center, radius, color='blue', label=None):
    circle = plt.Circle(center, radius, color=color, fill=False, linewidth=2, label=label)
    ax.add_artist(circle)
    if label:
        ax.text(center[0], center[1], label, fontsize=10, ha='center', va='center')


C1 = (0, 0, 1)
C2 = (4, 0, 1)
C3 = (2, 4, 1)

# C1 = (0, 0, 1)
# C2 = (4, 0, 1)
# C3 = (2, 3, 1)

# C1 = (0, 0, 1)
# C2 = (5, 0, 2)
# C3 = (2, 4, 0.5)

# C1 = (0, 0, 3)
# C2 = (1, 0, 1)
# C3 = (-1, 0, 1)

# C1 = (0, 0, 0)
# C2 = (4, 0, 2)
# C3 = (2, 2, 1)

# C1 = (0, 0, 1)
# C2 = (1.99, 0, 1)
# C3 = (1, 1.73, 1)

# C1 = (0, 0, 2)
# C2 = (1, 1, 2)
# C3 = (-1, 1, 2)


def apollonius_circles(c1, c2, c3):
    x, y, r = symbols('x y r')
    (x1, y1, r1) = c1
    (x2, y2, r2) = c2
    (x3, y3, r3) = c3

    results = []

    for s1 in [1, -1]:
        for s2 in [1, -1]:
            for s3 in [1, -1]:
                eq1 = Eq(sqrt((x - x1) ** 2 + (y - y1) ** 2), r + s1 * r1)
                eq2 = Eq(sqrt((x - x2) ** 2 + (y - y2) ** 2), r + s2 * r2)
                eq3 = Eq(sqrt((x - x3) ** 2 + (y - y3) ** 2), r + s3 * r3)

                try:
                    sol = solve((eq1, eq2, eq3), (x, y, r), dict=True)
                    for s in sol:
                        if s[r] > 0:
                            results.append((float(s[x]), float(s[y]), float(s[r])))
                except Exception:
                    continue

    return results


apollony_solutions = apollonius_circles(C1, C2, C3)

if not apollony_solutions:
    print("Нет окружности, которая касается всех трёх заданных окружностей.")
else:
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.grid(True)

    draw_circle(ax, C1[:2], C1[2], color='black', label='C1')
    draw_circle(ax, C2[:2], C2[2], color='black', label='C2')
    draw_circle(ax, C3[:2], C3[2], color='black', label='C3')

    colors = ['red', 'green', 'orange', 'purple', 'cyan', 'magenta', 'brown', 'grey']

    for i, (xc, yc, rc) in enumerate(apollony_solutions[:8]):
        draw_circle(ax, (xc, yc), rc, color=colors[i], label=f'A{i + 1}')

    ax.legend()
    plt.xlim(-5, 10)
    plt.ylim(-5, 10)
    plt.title('Окружности Аполлония для трёх заданных окружностей')
    plt.show()
