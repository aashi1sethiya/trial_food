## PATHS 
from pathlib import Path

ROOT_DIR = Path(__file__).parent
PATH_TO_NUTRITION_RDI = ROOT_DIR / "data/nutrition_rdi.csv"
PATH_TO_APP_USER_DATA = ROOT_DIR / "data/app_user_data.db"
PATH_TO_CSS = ROOT_DIR / "styles/style.css"
PATH_TO_LOTTIE = ROOT_DIR / "lottiefiles"
PATH_TO_IMAGES = ROOT_DIR / "images"
PATH_TO_HTML = ROOT_DIR / "apps/html"
PATH_TO_HTML_CSS = ROOT_DIR / "apps/css"
PATH_TO_FIREBASE_CONFIG = ROOT_DIR / "firebase"

# Firebase
FIREBASE_APP_NAME = "streamlit-ourfood"

## Menu
MENU_BREAKFAST = ["粟米魚茸粥",
                  "白粥",
                  "fried bread sticks",
                  "火腿雜菌燜伊麵",
                  "chinese dim sum"]

MENU_SALAD_BAR = ["烚蛋",
                  "seasonal vegetable",
                  "oatmeal porridge",
                  "baked beans",
                  "scrambled egg",
                  "pancake",
                  "roasted cocktail potato",
                  "bacon",
                  "粟米粒",
                  "青瓜",
                  "雜錦生菜",
                  "紅菜頭",
                  "車厘茄",
                  "吞拿魚",
                  "紅及黃甜椒",
                  "亞之竹芯",
                  "蘋果",
                  "橙子",
                  "梨子",
                  ]

MENU_ASIAN = ['四川擔擔鷄湯粉麵',
              '南乳粉葛燜鴨',
              '火腿雜菌燜伊麵',
              '花旗參蒸鰈魚柳',
              '芥菜',
              '紹菜',
              '發菜眉豆花生鷄脚湯',
              '白花蛇舌草']

MENU_INTERNATIONAL = ['thai green curry brisket',
                      'seafood casserole',
                      'penne with crustaceans sauce',
                      'brown rice',
                      'cauliflower with cheese',
                      'caldo verde']

MENU_DESSERT = ["乳酪",
                "士多啤梨蛋糕",
                "豆腐花",
                "龜苓膏"]