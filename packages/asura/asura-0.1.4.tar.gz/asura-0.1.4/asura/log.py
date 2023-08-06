import colored

class ASORA:
    info_background = colored.bg(27)
    err_background = colored.bg(124)
    warning_background = colored.bg(172)
    reset = colored.attr('reset')
    white_text = colored.fg(15)

async def info(text: str):
    print(ASORA.white_text+ASORA.info_background+"[?]"+ASORA.reset+"    "+text)

async def error(err: str):
    print(ASORA.white_text+ASORA.err_background+"[X]"+ASORA.reset+"    "+err)

async def warning(war: str) -> str:
    print(ASORA.white_text+ASORA.warning_background+"[!]"+ASORA.reset+"    "+war)
