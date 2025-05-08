import os

# 顏色設定
BLUE_COLOR = "#2633BC"
GREY_COLOR = "#747678"
GREY_COLOR2 = "#838383"
BLACK_COLOR = "#000000"
TRANSFER_GREY_COLOR = "#D7D5D5"
WHITE_BACKGROUND_COLOR = "#FFFFFF"
BORDER_DEBUG = "" #"border: 2px solid #ccc;"

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

STATION_STATE_APPROACH = 0         # 車即將到達下一站
STATION_STATE_ARRIVED = 1          # 車在車站
STATION_STATE_NEXT = 2             # 車開往下一站
STATION_STATE_READY_TO_DEPART = 3  # 車準備在起站發車
STATION_STATE_IN_TERMINAL = 4      # 車在終點站

DEST_STATION_INFO = ["　ゆき", "　ゆき", "For　", "開往　"]
MIDOSUJI_LINE_NAME = ["御堂筋線", "みどうすじせん", "Midosuji Line", "御堂筋線"]

NOW_STATE_MAP = {
    "0": ["まもなく", "まもなく", "Arriving at", "即將到達"],
    "2": ["次は", "つぎは", "Next", "下一站"],
    "1": ["ただいま", "ただいま", "Now stopping at", "這一站"],
    "3": ["", "", "For", "開往"],
    "4": ["終点", "しゅうてん", "Arrived at", "已到達"],
}

CAR_INST_TOP = ["", "", "Car No.", ""]
CAR_INST_BOT = ["号車", "号車", "", "號車廂"]

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

LINE_COLOR_MAP = {
  "Chuo": "#019a66",
  "Imazatosuji": "#f8b500",
  "Midosuji": "#e5171f",
  "Nagahori Tsurumi-ryokuchi": "#a9cc51",
  "New Tram": "#00b2e5",
  "Sakaisuji": "#804000",
  "Tanimachi": "#8f76d6",
  "Yotsubashi": "#0078ba",
  "Sennichimae": "#f08fc0",
  "Kintetsu": "#000000",
  "Nankai": "#000000",
  "Hankyu": "#000000",
  "Keihan": "#000000",
  "Hanshin": "#000000",
  "Hankai": "#000000",
  "JR": "#000000",
  "Kita-Osaka Kyuko": "#000000",
  "Imazato Liner": "#000000"
}


# Line 
MIDOSUJI_RED_COLOR = LINE_COLOR_MAP['Midosuji']