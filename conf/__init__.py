import conf.defaults as defaults
import conf.mysql as mysql


class settings(defaults.settings):
    apikey = "xoxb-6345640501-uETlx0hmxEwkG4kIkfTQq3Fc"
    channel = "mmibots"
    username = "MMI-Bot"
    callSign = "mmibot"
    manOpList = ["levi"]
    commandPrefix = "!"                         #Leave as "" to disallow
    filterBotMessages = True
    # textReplacements = [("\b","\x02"),("\\b","\x02")]
    textReplacements = []
    version = 1