import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict

Point = Tuple[float, float]
Satellite = Tuple[float, float, float, float, float]  # x0, y0, x1, y1, radius
Status = str
FireArea = Tuple[float, float, float, float]  # xmin, ymin, xmax, ymax


def generate_grid(area_size: float, dx: float) -> List[Point]:
    x_vals = np.arange(0, area_size + dx, dx)
    y_vals = np.arange(0, area_size + dx, dx)
    return [(x, y) for x in x_vals for y in y_vals]


def compute_coverage(grid: List[Point], satellites: List[Satellite],
                     fire_area: FireArea) -> Dict[Point, Status]:
    """
        Для каждой точки в сетке определяет её статус:
        - 'seen_fire': точка находится внутри зоны пожара и попадает в радиус действия спутника.
        - 'seen_clear': точка попадает в радиус действия спутника, но не находится в пожаре.
        - 'unseen': точка не покрыта ни одним спутником.

        Параметры:
        - grid: список точек сетки (из generate_grid)
        - satellites: список спутников с их траекториями и радиусами
        - fire_area: координаты прямоугольной области пожара (xmin, ymin, xmax, ymax)

        Возвращает словарь: {точка: статус}
    """
    point_status: Dict[Point, Status] = {point: 'unseen' for point in grid}
    xmin, ymin, xmax, ymax = fire_area

    for sx0, sy0, sx1, sy1, radius in satellites:
        trajectory_x = np.linspace(sx0, sx1, 100)
        trajectory_y = np.linspace(sy0, sy1, 100)

        for px, py in grid:
            for tx, ty in zip(trajectory_x, trajectory_y):
                dist = np.hypot(px - tx, py - ty)
                if dist <= radius:
                    if xmin <= px <= xmax and ymin <= py <= ymax:
                        point_status[(px, py)] = 'seen_fire'
                    elif point_status[(px, py)] != 'seen_fire':
                        point_status[(px, py)] = 'seen_clear'
                    break
    return point_status


def draw_visualization(area_size: float, dx: float,
                       satellites: List[Satellite],
                       point_status: Dict[Point, Status],
                       fire_area: FireArea) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    for (x, y), status in point_status.items():
        color = {'seen_fire': 'red', 'seen_clear': 'green', 'unseen': 'gray'}[status]
        ax.add_patch(plt.Rectangle((x - dx / 2, y - dx / 2), dx, dx, color=color))

    ax.plot([0, area_size, area_size, 0, 0],
            [0, 0, area_size, area_size, 0],
            color='black', linewidth=2)

    for sx0, sy0, sx1, sy1, _ in satellites:
        ax.plot([sx0, sx1], [sy0, sy1], linestyle='--', color='blue')

    xmin, ymin, xmax, ymax = fire_area
    ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                               fill=False, edgecolor='darkred', linewidth=2, linestyle='-'))

    ax.set_xlim(-1, area_size + 1)
    ax.set_ylim(-1, area_size + 1)
    ax.set_aspect('equal')
    ax.set_title('Мониторинг квадрата с помощью спутников')

    plt.legend(handles=[
        plt.Line2D([0], [0], color='red', lw=4, label='Пожар обнаружен'),
        plt.Line2D([0], [0], color='green', lw=4, label='Покрыто, пожара нет'),
        plt.Line2D([0], [0], color='gray', lw=4, label='Не покрыто'),
        plt.Line2D([0], [0], linestyle='--', color='blue', label='Траектория спутника'),
        plt.Line2D([0], [0], color='darkred', lw=2, label='Область пожара')
    ])

    plt.grid(True)
    plt.show()


def main():
    area_size = 10
    dx = 0.1

    # satellites: List[Satellite] = [
    #     (0, 0, 10, 10, 3),
    #     (0, 10, 10, 0, 3),
    #     (0, 5, 10, 5, 3)
    # ]
    #
    # fire_area: FireArea = (4, 4, 6, 6)

    # satellites: List[Satellite] = [
    #     (0, 0, 10, 10, 2),
    #     (0, 10, 10, 0, 2),
    # ]
    #
    # fire_area: FireArea = (4, 4, 10, 7)

    satellites: List[Satellite] = [
        (0, 0, 5, 6, 2),
        (0, 10, 10, 0, 2),
    ]

    fire_area: FireArea = (4, 4, 4, 4)

    grid = generate_grid(area_size, dx)
    point_status = compute_coverage(grid, satellites, fire_area)
    draw_visualization(area_size, dx, satellites, point_status, fire_area)


if __name__ == '__main__':
    main()
