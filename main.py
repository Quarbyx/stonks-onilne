import yfinance as yf
print("Введите тикер акции (например, AAPL, GOOG): ")
symbol = input()
data = yf.download(symbol)
if data.empty:
    print("Не удалось получить данные для указанного тикера.")
else:
    current_price = data['Close'][-1]
    previous_close = data['Close'][-2]
    delta = current_price - previous_close
    print(f"Текущая цена: ${current_price:.2f}")
    print(f"Изменение за день: ${delta:.2f}")