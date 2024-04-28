import yfinance as yf
import flet as ft
import time
def get_stock_data(symbol, price_text, delta_text):
    data = yf.download(symbol)
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        previous_close = data['Close'].iloc[-2]
        delta = current_price - previous_close
        price_text.value = f"Цена: ${current_price:.2f}"
        delta_text.value = f"Изменение: ${delta:.2f}"
    else:
        price_text.value = "Цена: (недоступно)"
        delta_text.value = "Изменение: (недоступно)"

def main(page: ft.Page):
    ticker_input = ft.TextField(label="Введите тикер")
    current_price_display = ft.Text("Текущая цена: ")
    delta_display = ft.Text("Изменение: ") 
    loading_overlay = ft.Container(
        width=page.width, 
        height=page.height,
        bgcolor=ft.colors.BLACK,
        opacity=0.5,
        visible=False
    )
    loading_animation = ft.ProgressRing(visible=False) 
    loading_row = ft.Row(
        [loading_animation],
        alignment=ft.MainAxisAlignment.CENTER
    )
    loading_column = ft.Column(
        [loading_row],
        alignment=ft.CrossAxisAlignment.CENTER 
    )
    page.overlay.append(loading_column)
    def get_data_button_clicked(e):
        ticker = ticker_input.value
        get_stock_data(ticker, current_price_display, delta_display)
        loading_overlay.visible = True
        loading_animation.visible = True
        page.update()
        time.sleep(1)
        loading_overlay.visible = False
        loading_animation.visible = False
        page.update()
    get_data_button = ft.ElevatedButton("Получить данные", on_click=get_data_button_clicked)
    page.overlay.append(loading_overlay)
    page.overlay.append(loading_animation)
    page.add(ticker_input, current_price_display, delta_display, get_data_button)

ft.app(target=main)