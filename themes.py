from npyscreen import Themes, ThemeManager


class DefaultTheme(ThemeManager):
    pass


class CriticalTheme(ThemeManager):
    default_colors = {
        "DEFAULT": "GREEN_BLACK",
        "FORMDEFAULT": "WHITE_BLACK",
        "NO_EDIT": "BLUE_BLACK",
        "STANDOUT": "CYAN_BLACK",
        "CURSOR": "GRAY_BLACK",
        "CURSOR_INVERSE": "BLACK_WHITE",
        "LABEL": "GREEN_BLACK",
        "LABELBOLD": "WHITE_GRAY",
        "CONTROL": "YELLOW_BLACK",
        "WARNING": "RED_BLACK",
        "CRITICAL": "BLACK_RED",
        "GOOD": "GREEN_BLACK",
        "GOODHL": "GREEN_BLACK",
        "VERYGOOD": "BLACK_GREEN",
        "CAUTION": "YELLOW_BLACK",
        "CAUTIONHL": "BLACK_YELLOW",
    }


themes = [DefaultTheme, CriticalTheme, Themes.ColorfulTheme, Themes.ElegantTheme]
