import os

# 顏色設定
MIDOSUJI_RED_COLOR = "#E5171F"
BLUE_COLOR = "#2633BC"
GREY_COLOR = "#747678"
GREY_COLOR2 = "#838383"
BLACK_COLOR = "#000000"
MIDOSUJI_BACKGROUND_COLOR = "#FFFFFF"

# 動畫時間設定
ANIMATION_INTERVAL_MS = 1000

# 大小設定
ARROW_WIDGET_WIDTH = 65
ARROW_WIDGET_HEIGHT = 40

if (os.name == "posix"):
    ICON_PATH = "osaka_metro/transfer_icons/"
    MIDOSUJI_LINE_INFO = "osaka_metro/midosuji_line.yaml"
    FONT_NAME = "Noto Sans JP"
else:
    ICON_PATH = "osaka_metro\\transfer_icons\\"
    MIDOSUJI_LINE_INFO = "osaka_metro\\midosuji_line.yaml"
    FONT_NAME = "Noto Sans JP SemiBold"

# icon map
ICON_MAP = {
    "Chou": "line_chuo",
    "Imazatosuji": "line_imazatosuji.png",
    "Midosuji": "line_midosuji.png",
    "NHTRMRKC": "line_nagahoritsurumiryokuchi.png",
    "New_Tram": "line_new_tram.png",
    "Sakaisuji": "line_sakaisuji.png",
    "Tanimachi": "line_tanimachi.png",
    "Yotsubashi": "line_yotsubashi.png",
    "Sennichimae": "line_sennichimae.png",
    "Kintetsu": "line_other.png",
    "Nankai": "line_other.png",
    "Hanshin": "line_other.png",
    "JR": "line_other.png",
}