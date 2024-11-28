import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from math import pi
import random

# Читання даних із CSV файлу
file_name = "exports_2015_2019.csv"

try:
    data = pd.read_csv(file_name, encoding='cp1251') 

    # Вибір кількості країн для лінійного графіка
    if input("Бажаєте створити лінійний графік? (так/ні): ").strip().lower() == "так":
        num_countries = int(input("Введіть кількість країн для побудови лінійного графіка: "))
        countries = []
        for i in range(num_countries):
            country = input(f"Введіть назву країни {i+1}: ")
            if country in data["Country"].values:
                countries.append(country)
            else:
                print(f"Країну '{country}' не знайдено в даних. Пропустимо її.")

        if not countries:
            print("Не було вибрано жодної країни для побудови графіка.")
        else:
            years = list(range(2015, 2020))

            # Побудова лінійного графіка для вибраних країн
            output_file("visualization.html")
            line_plot = figure(title="Динаміка показника Exports of goods and services (% of GDP)", 
                               x_axis_label="Рік", y_axis_label="Показник (% of GDP)", 
                               width=800, height=400)

            # Генерація випадкових кольорів для кожної країни
            colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in countries]

            for i, country in enumerate(countries):
                country_data = data[data["Country"] == country].iloc[0, 1:].values
                line_plot.line(years, country_data, line_width=2, legend_label=country, color=colors[i])
                line_plot.circle(years, country_data, size=8, color=colors[i], legend_label=country)

            line_plot.legend.location = "top_left"
            show(line_plot)

    # Кругова діаграма
    if input("Бажаєте створити кругову діаграму? (так/ні): ").strip().lower() == "так":
        selected_country = input("Введіть країну для побудови кругової діаграми: ")
        if selected_country in data["Country"].values:
            country_data = data[data["Country"] == selected_country].iloc[0, 1:].values
            pie_data = pd.DataFrame({
                'year': list(range(2015, 2020)),
                'value': country_data
            })
            pie_data['angle'] = pie_data['value'] / pie_data['value'].sum() * 2 * pi
            pie_data['color'] = Category20c[len(pie_data)]

            pie_chart = figure(title=f"Розподіл показників для {selected_country} (2015-2019)", 
                               width=400, height=400, 
                               tools="hover", tooltips="@year: @value", x_range=(-0.5, 1.0))

            pie_chart.wedge(x=0, y=1, radius=0.4, 
                            start_angle=cumsum('angle', include_zero=True), 
                            end_angle=cumsum('angle'), 
                            line_color="white", fill_color='color', 
                            legend_field='year', source=ColumnDataSource(pie_data))

            pie_chart.legend.title = "Рік"
            pie_chart.axis.visible = False
            pie_chart.grid.grid_line_color = None
            show(pie_chart)
        else:
            print(f"Країну '{selected_country}' не знайдено в даних. Кругова діаграма не побудована.")

except FileNotFoundError:
    print(f"Файл '{file_name}' не знайдено. Переконайтеся, що він знаходиться в тій самій папці, що й програма.")
except Exception as e:
    print(f"Виникла помилка: {e}")
