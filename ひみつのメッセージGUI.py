from tkinter import messagebox, Tk
import tkinter
from random import choice
import csv
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def 偶数チェック(数):
    return 数 % 2 == 0

def 偶数番目の文字取得(メッセージ):
    偶数番目文字 = []
    for カウンター in range(0, len(メッセージ)):
        if 偶数チェック(カウンター):
            偶数番目文字.append(メッセージ[カウンター])
    return 偶数番目文字

def 奇数番目の文字取得(メッセージ):
    奇数番目文字 = []
    for カウンター in range(0, len(メッセージ)):
        if not 偶数チェック(カウンター):
            奇数番目文字.append(メッセージ[カウンター])
    return 奇数番目文字

def 文字入れかえ(メッセージ):
    文字リスト = []
    if not 偶数チェック(len(メッセージ)):
        メッセージ = メッセージ + "x"
    偶数番目文字 = 偶数番目の文字取得(メッセージ)
    奇数番目文字 = 奇数番目の文字取得(メッセージ)
    for カウンター in range(0, int(len(メッセージ)/2)):
        文字リスト.append(奇数番目文字[カウンター])
        文字リスト.append(偶数番目文字[カウンター])
    処理後メッセージ = "".join(文字リスト)
    return 処理後メッセージ

def 暗号化(メッセージ, 共通鍵):
    逆順メッセージ = 文字入れかえ(メッセージ)
    暗号化メッセージ = "".join(reversed(逆順メッセージ))
    捨字メッセージ = 捨字入れ(暗号化メッセージ)
    return 共通鍵暗号化(捨字メッセージ, 共通鍵)

def 復号(メッセージ, 共通鍵):
    共通鍵復号メッセージ = 共通鍵復号(メッセージ, 共通鍵)
    捨字抜きメッセージ = 捨字抜き(共通鍵復号メッセージ)
    順序戻しメッセージ = "".join(reversed(捨字抜きメッセージ))
    復号メッセージ = 文字入れかえ(順序戻しメッセージ)
    return 復号メッセージ

def 捨字入れ(メッセージ):
    暗号化_リスト = []
    捨字リスト = []
    
    # CSVファイルから捨字リストを読み込む
    with open('ひみつの鍵.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "捨字リスト":
                捨字リスト = row[1:]
                break
    
    for カウンター in range(0, len(メッセージ)):
        暗号化_リスト.append(メッセージ[カウンター])
        暗号化_リスト.append(choice(捨字リスト))
    
    新メッセージ = "".join(暗号化_リスト)
    return 新メッセージ

def 捨字抜き(メッセージ):
    偶数番目文字 = 偶数番目の文字取得(メッセージ)
    新メッセージ = "".join(偶数番目文字)
    return 新メッセージ

def 共通鍵暗号化(メッセージ, 共通鍵):
    cipher = AES.new(bytes.fromhex(共通鍵), AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, _ = cipher.encrypt_and_digest(メッセージ.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def 共通鍵復号(メッセージ, 共通鍵):
    data = base64.b64decode(メッセージ)
    nonce = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(bytes.fromhex(共通鍵), AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('utf-8')

def e():
    メッセージ = txt1.get()
    共通鍵 = txt4.get()
    if メッセージ != "" and 共通鍵 != "":
        暗号化_メッセージ = 暗号化(メッセージ, 共通鍵)
        txt2.delete(0, tkinter.END)
        txt2.insert(tkinter.END, 暗号化_メッセージ)
    else:
        messagebox.showerror("エラー:", "空文字は指定できません。")
        
def d():
    メッセージ = txt1.get()
    共通鍵 = txt4.get()
    if メッセージ != "" and 共通鍵 != "":
        復号_メッセージ = 復号(メッセージ, 共通鍵)
        txt2.delete(0, tkinter.END)
        txt2.insert(tkinter.END, 復号_メッセージ)
    else:
        messagebox.showerror("エラー:", "空文字は指定できません。")

def cl1():
    txt1.delete(0, tkinter.END)
def cl2():
    txt2.delete(0, tkinter.END)

def save_dummy_keys():
    捨字リスト = [item for item in txt3.get().split(',') if item]
    updated_rows = []
    捨字リスト_found = False

    # Read existing data from the CSV file
    try:
        with open('ひみつの鍵.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) > 0 and row[0] == "捨字リスト":
                    updated_rows.append(["捨字リスト"] + 捨字リスト)
                    捨字リスト_found = True
                else:
                    updated_rows.append(row)
    except FileNotFoundError:
        pass

    if not 捨字リスト_found:
        updated_rows.append(["捨字リスト"] + 捨字リスト)

    # Write updated data back to the CSV file
    with open('ひみつの鍵.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in updated_rows:
            writer.writerow(row)

    messagebox.showinfo("情報", "捨字リストが更新されました。")

def save_common_key():
    共通鍵 = txt4.get()
    捨字リスト = [item for item in txt3.get().split(',') if item]
    updated_rows = []
    共通鍵_found = False
    捨字リスト_found = False

    # Read existing data from the CSV file
    try:
        with open('ひみつの鍵.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) > 0 and row[0] == "共通鍵":
                    updated_rows.append(["共通鍵", 共通鍵])
                    共通鍵_found = True
                elif len(row) > 0 and row[0] == "捨字リスト":
                    updated_rows.append(["捨字リスト"] + 捨字リスト)
                    捨字リスト_found = True
                else:
                    updated_rows.append(row)
    except FileNotFoundError:
        pass

    if not 共通鍵_found:
        updated_rows.append(["共通鍵", 共通鍵])
    if not 捨字リスト_found:
        updated_rows.append(["捨字リスト"] + 捨字リスト)

    # Write updated data back to the CSV file
    with open('ひみつの鍵.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in updated_rows:
            writer.writerow(row)

    messagebox.showinfo("情報", "共通鍵が更新されました。")

def generate_key():
    key = get_random_bytes(16)
    txt4.delete(0, tkinter.END)
    txt4.insert(tkinter.END, key.hex())

def load_keys():
    try:
        with open('ひみつの鍵.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) > 0 and row[0] == "捨字リスト":
                    txt3.insert(tkinter.END, ",".join(row[1:]))
                elif len(row) > 0 and row[0] == "共通鍵":
                    txt4.delete(0, tkinter.END)
                    txt4.insert(tkinter.END, row[1])
    except FileNotFoundError:
        pass
        with open('ひみつの鍵.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

root = Tk()
root.geometry('740x120')
root.title("ひみつのメッセージ v0.1.0")
root.resizable(width=False, height=False)

# 暗号化/復号セクション
lbl_title1 = tkinter.Label(text="暗号化/復号")
lbl_title1.place(x=10, y=10)

lbl1 = tkinter.Label(text="処理前の文")
lbl1.place(x=10, y=40)

lbl2 = tkinter.Label(text="処理後の文")
lbl2.place(x=10, y=90)

txt1 = tkinter.Entry(width=34)
txt1.place(x=100, y=40)

txt2 = tkinter.Entry(width=34)
txt2.place(x=100, y=90)

btn1 = tkinter.Button(text='暗号化', command=e)
btn1.place(x=10, y=62)

btn2 = tkinter.Button(text='復号', command=d)
btn2.place(x=65, y=62)

btn3 = tkinter.Button(text='X', command=cl1)
btn3.place(x=310, y=40)

btn4 = tkinter.Button(text='X', command=cl2)
btn4.place(x=310, y=90)

# パスワード編集セクション
lbl_title2 = tkinter.Label(text="パスワード編集")
lbl_title2.place(x=350, y=10)

lbl3 = tkinter.Label(text="捨字リスト")
lbl3.place(x=350, y=40)

txt3 = tkinter.Entry(width=34)
txt3.place(x=420, y=40)

btn5 = tkinter.Button(text='保存', command=save_dummy_keys)
btn5.place(x=630, y=38)

lbl4 = tkinter.Label(text="共通鍵")
lbl4.place(x=350, y=90)
txt4 = tkinter.Entry(width=34, show='*')
txt4.place(x=420, y=90)

btn7 = tkinter.Button(text='保存', command=save_common_key)
btn7.place(x=630, y=88)

btn6 = tkinter.Button(text='生成', command=generate_key)
btn6.place(x=680, y=88)

# Ensure txt4 is defined before calling load_keys
txt4 = tkinter.Entry(width=34, show='*')
txt4.place(x=420, y=90)

load_keys()

root.mainloop()
