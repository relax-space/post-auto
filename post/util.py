
async def getValueByText(text: str, select_tag: str, page):
    # extract all options value
    option_texts = []
    for option_ele in await page.querySelectorAll(f'{select_tag} > option'):
        tag_text = await page.evaluate('(element) => ({"value":element.value,"text":element.textContent})', option_ele)
        option_texts.append(tag_text)

    value = ''
    for v in option_texts:
        if v.get('text') == text:
            value = v.get('value')
            break
    return value
