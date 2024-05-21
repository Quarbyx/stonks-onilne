import yfinance as yf
import flet as ft
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import unittest
def load_favorites(file_path="favorites.txt"):
    try:
        with open(file_path, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []
def save_favorites(favorites, file_path="favorites.txt"):
    with open(file_path, "w") as f:
        for ticker in favorites:
            f.write(ticker + "\n")
def get_stock_data(page, symbol, price_text, delta_text, chart_container):
    data = yf.download(symbol, period="1mo")
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        previous_close = data['Close'].iloc[-2]
        delta = current_price - previous_close
        price_text.value = f"Цена: ${current_price:.2f}"
        delta_text.value = f"Изменение: ${delta:.2f}"
        delta_text.color = ft.colors.GREEN if delta >= 0 else ft.colors.RED
        fig = px.line(data.reset_index(), x='Date', y='Close', title=f"Цена акций {symbol} за последний месяц")
        chart_container.content = PlotlyChart(fig, expand=True)
        page.update()
    else:
        price_text.value = "Цена: (недоступно)"
        delta_text.value = "Изменение: (недоступно)"
        delta_text.color = ft.colors.BLACK
        chart_container.content = ft.Text("График недоступен")
        page.update()
def main(page: ft.Page):
    favorites = load_favorites()
    ticker_input = ft.TextField(label="Введите тикер")
    current_price_display = ft.Text("Текущая цена: ")
    delta_display = ft.Text("Изменение: ")
    chart_container = ft.Container(width=600, height=300)
    favorites_dropdown = ft.Dropdown(width=200,options=[ft.dropdown.Option(t) for t in favorites])
    def on_favorites_dropdown_change(e):
        ticker_input.value = e.control.value
        page.update()
    favorites_dropdown.on_change = on_favorites_dropdown_change
    loading_overlay = ft.Container(width=page.width, height=page.height, bgcolor=ft.colors.BLACK,opacity=0.5, visible=False)
    loading_animation = ft.ProgressRing(visible=False)
    loading_row = ft.Row([loading_animation], alignment=ft.MainAxisAlignment.CENTER)
    loading_column = ft.Column([loading_row], alignment=ft.CrossAxisAlignment.CENTER)
    page.overlay.append(loading_column)
    def get_data_button_clicked(e):
        ticker = ticker_input.value
        get_stock_data(page, ticker, current_price_display, delta_display, chart_container)
        loading_overlay.visible = True
        loading_animation.visible = True
        page.update()
        loading_overlay.visible = False
        loading_animation.visible = False
        page.update()
    def add_to_favorites(e):
        ticker = ticker_input.value
        if ticker not in favorites:
            favorites.append(ticker)
            favorites_dropdown.options.append(ft.dropdown.Option(ticker))
            save_favorites(favorites)
            page.show_snack_bar(ft.SnackBar(ft.Text(f"{ticker} добавлен в избранное")))
        page.update()
    get_data_button = ft.ElevatedButton("Получить данные", on_click=get_data_button_clicked)
    add_to_favorites_button = ft.ElevatedButton("Добавить в избранное", on_click=add_to_favorites)
    page.overlay.append(loading_overlay)
    page.overlay.append(loading_animation)
    page.add(
        ft.Row([ticker_input, favorites_dropdown]),current_price_display,delta_display,get_data_button,add_to_favorites_button,chart_container,)
class TestFavorites(unittest.TestCase):
    def test_load_favorites(self):
        with open("favorites_test.txt", "w") as f:
            f.write("AAPL\nMSFT\nGOOG")
        favorites = load_favorites("favorites_test.txt")
        self.assertEqual(favorites, ["AAPL", "MSFT", "GOOG"])
    def test_save_favorites(self):
        favorites = ["TSLA", "AMZN", "NVDA"]
        save_favorites(favorites, "favorites_test.txt")
        loaded_favorites = load_favorites("favorites_test.txt")
        self.assertEqual(loaded_favorites, favorites)
if __name__ == "__main__":
    ft.app(target=main)
    unittest.main(argv=['first-arg-is-ignored'], exit=False)