def generate_price_monitor_response(
    previous_prices, current_prices, threshold, time_interval
):
    out_str = ""
    for name_asset in previous_prices.keys():
        price_return = current_prices[name_asset] / previous_prices[name_asset] - 1
        if price_return > threshold / 100:
            out_str += f"{name_asset} IS GOING UP!\n"
        elif price_return < -threshold / 100:
            out_str += f"{name_asset} IS GOING DOWN!\n"

    out_str += '\n\nSummary prices\n##################\n'
    for name_asset in previous_prices.keys():
        price_return = current_prices[name_asset] / previous_prices[name_asset] - 1
        out_str += f"{name_asset} return over {time_interval} minutes is {threshold} %\n"
        out_str += f"{name_asset} current price is {current_prices[name_asset]:.2f} \n"
        out_str += f"{name_asset} price {time_interval} minutes ago is {previous_prices[name_asset]:.2f} \n"
        out_str += "##################\n"

    return out_str
