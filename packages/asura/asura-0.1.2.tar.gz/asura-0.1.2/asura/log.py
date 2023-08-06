import colored

class ASORA:
    info_background = colored.bg256(27)
    err_background = colored.bg256(124)
    warning_background = colored.bg256(172)
    reset = colored.reset(0)
    white_text = colored.fg256(15)

async def info(text: str):
    print(ASORA.white_text+ASORA.info_background+"[?]"+ASORA.reset+"    "+text)

async def error(err: str):
    print(ASORA.white_text+ASORA.err_background+"[X]"+ASORA.reset+"    "+err)

async def warning(war: str) -> str:
    print(ASORA.white_text+ASORA.warning_background+"[!]"+ASORA.reset+"    "+war)
