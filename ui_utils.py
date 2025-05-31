# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: ui_utils.py
# Version: 0.2.0
# Date: 2024-03-21
# Author: [Your Name/Nickname]
# Description: UI helper functions, including cell styling.
# FILE_VERSION_END

def apply_cell_styles_for_display(val, column_name_displayed=""):
    """
    Determines CSS color and font-weight attributes for a cell.
    column_name_displayed refers to column names AFTER renaming for display.
    """
    color_css = ""
    font_weight_css = ""

    if isinstance(val, (int, float)) and "%" in column_name_displayed:
        if val > 0: color_css = 'color: green'
        elif val < 0: color_css = 'color: red'
        else: color_css = 'color: gray'
    elif isinstance(val, str):
        val_upper = val.upper()
        current_col_name_upper = column_name_displayed.upper()

        if current_col_name_upper == 'AI SIGNAL':
            if 'STRONG BUY' in val_upper: color_css = 'color: darkgreen'; font_weight_css = 'font-weight: bold'
            elif 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'STRONG SELL' in val_upper: color_css = 'color: darkred'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'NEUTRAL' in val_upper: color_css = 'color: gray'
        elif current_col_name_upper == 'ADX':
            if 'STRONG' in val_upper or 'TREND' in val_upper: color_css = 'color: green'
            elif 'WEAK' in val_upper or 'NO TREND' in val_upper: color_css = 'color: gray'
            else: color_css = 'color: gray'
        elif current_col_name_upper == 'BB POS.':
            if 'UPPER' in val_upper: color_css = 'color: red'
            elif 'LOWER' in val_upper: color_css = 'color: green'
            elif 'MID' in val_upper: color_css = 'color: gray'
        elif current_col_name_upper in ['OBV', 'ATR', 'RSI (14)', 'SRSI %K', 'MACD', 'STOCH K', 'AO', 
                                        'EMA20/P', 'SMA50/200', 'VWAP/P', 
                                        'MA CROSS', 'RSI DIV', 'MACD DIV', 'VOL BREAK']:
            if 'BUY' in val_upper or 'BULLISH' in val_upper or 'GOLDEN' in val_upper:
                color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper or 'BEARISH' in val_upper or 'DEATH' in val_upper:
                color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'WAIT' in val_upper or 'NEUTRAL' in val_upper or 'NONE' in val_upper or 'NO BREAK' in val_upper or 'MID' in val_upper or 'N/A' in val_upper or 'ERROR' in val_upper:
                color_css = 'color: gray'
    
    final_style = []
    if color_css: final_style.append(color_css)
    if font_weight_css: final_style.append(font_weight_css)
    return '; '.join(final_style) if final_style else None

# FILE_FOOTER_START
# End of file: ui_utils.py
# Version: 0.2.0
# Last Modified: 2024-03-21
# FILE_FOOTER_END
