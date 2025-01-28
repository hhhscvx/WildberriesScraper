

def get_basket_version_by_short_id(short_id: int) -> str | None:
    basket = None

    if 0 <= short_id <= 143:
        basket = '01'
    elif 144 <= short_id <= 287:
        basket = '02'
    elif 288 <= short_id <= 431:
        basket = '03'
    elif 432 <= short_id <= 719:
        basket = '04'
    elif 720 <= short_id <= 1007:
        basket = '05'
    elif 1008 <= short_id <= 1061:
        basket = '06'
    elif 1062 <= short_id <= 1115:
        basket = '07'
    elif 1116 <= short_id <= 1169:
        basket = '08'
    elif 1170 <= short_id <= 1313:
        basket = '09'
    elif 1314 <= short_id <= 1601:
        basket = '10'
    elif 1602 <= short_id <= 1655:
        basket = '11'
    elif 1656 <= short_id <= 1919:
        basket = '12'
    elif 1920 <= short_id <= 2045:
        basket = '13'
    elif 2046 <= short_id <= 2189:
        basket = '14'
    elif 2190 <= short_id <= 2405:
        basket = '15'
    elif 2406 <= short_id <= 2621:
        basket = '16'
    elif 2622 <= short_id <= 2837:
        basket = '17'
    elif 2838 <= short_id <= 3053:
        basket = '18'
    else:
        basket = '19'
    
    return basket
