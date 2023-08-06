import colored

class ASORA:
    info_background = colored.bg(27)
    err_background = colored.bg(124)
    warning_background = colored.bg(172)
    reset = colored.attr('reset')
    white_text = colored.fg(15)

async def info(text: str) -> str:
    style = ASORA.info_background + ASORA.white_text
    print(colored.stylize("[?]", style), text)

async def error(err: str) -> str:
    style = ASORA.err_background + ASORA.white_text
    print(colored.stylize("[X]", style), err)

async def warning(war: str) -> str:
    style = ASORA.warning_background + ASORA.white_text
    print(colored.stylize("[!]", style), war)
