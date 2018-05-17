import random, re

def EncrypKey(str,key):
    KeyPos = 0
    Range = 256
    KeyLen = len(key)
    if KeyLen == 0:
        key = 'ADDBYHGFFOVER'
    else:
        key = '0'+key

    offset = random.randint(0,Range-1)
    # print offset
    dest =  hex(offset)[2:].zfill(2)
    # print dest


    for index in str:
        SrcAsc = (ord(index) + offset) % 255
        if KeyPos < KeyLen:
            KeyPos = KeyPos + 1
        else:
            KeyPos = 1

        SrcAsc = SrcAsc^(ord(key[KeyPos]))
        dest  = dest + hex(SrcAsc)[2:].zfill(2)
        offset = SrcAsc
    return dest

def UncrypKey(str,key):
    keypos = 0
    dest   = ''

    if len(str)==2:
        return ''
    keylen = len(key)
    if keylen == 0:
        key = 'ADDBYHGFFOVER'
    else:
        key = '0'+key

    try:
        offset = int('0x'+str[0:2],16)
    except:
        offset = 0

    str_for = re.findall(r'(.{2})', str[2:])
    for dou in str_for:
        try:
            SrcAsc = int('0x'+dou,16)
        except:
            SrcAsc = 0

        if keypos < keylen :
            keypos = keypos + 1
        else:
            keypos = 1

        TmpSrcAsc = SrcAsc^(ord(key[keypos]))
        if TmpSrcAsc <= offset:
            TmpSrcAsc = 255 + TmpSrcAsc - offset
        else:
            TmpSrcAsc = TmpSrcAsc - offset
        dest = dest + chr(TmpSrcAsc)
        offset = SrcAsc

    return dest