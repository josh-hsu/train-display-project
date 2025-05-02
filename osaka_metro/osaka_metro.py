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
    "Chuo": "line_chuo.png",
    "Imazatosuji": "line_imazatosuji.png",
    "Midosuji": "line_midosuji.png",
    "Nagahori Tsurumi-ryokuchi": "line_nagahoritsurumiryokuchi.png",
    "New Tram": "line_new_tram.png",
    "Sakaisuji": "line_sakaisuji.png",
    "Tanimachi": "line_tanimachi.png",
    "Yotsubashi": "line_yotsubashi.png",
    "Sennichimae": "line_sennichimae.png",
    "Kintetsu": "line_other.png",
    "Nankai": "line_other.png",
    "Hankyu": "line_other.png",
    "Keihan": "line_other.png",
    "Hanshin": "line_other.png",
    "Hankai": "line_other.png",
    "JR": "line_other.png",
    "Kita-Osaka Kyuko": "line_other.png",
    "Imazato Liner": "line_other.png",
}

TRANSFER_MAP = {
    "Chuo": "中央線",
    "Imazatosuji": "今里筋線",
    "Midosuji": "御堂筋線",
    "Nagahori Tsurumi-ryokuchi": "長堀鶴見緑地線",
    "New Tram": "ニュートラム",
    "Sakaisuji": "堺筋線",
    "Tanimachi": "谷町線",
    "Yotsubashi": "四つ橋線",
    "Sennichimae": "千日前線",
    "Kintetsu": "近鉄線",
    "Nankai": "南海線",
    "Hankyu": "阪急線",
    "Keihan": "京阪線",
    "Hanshin": "阪神線",
    "Hankai": "阪堺線",
    "JR": "JR線",
    "Kita-Osaka Kyuko": "北大阪急行線",
    "Imazato Liner": "今里ライナー線",
}