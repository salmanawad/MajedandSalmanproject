# URLTrap 🔍

مشروع لفحص الروابط وتحليلها والتأكد من أمانها وتتبع التحويلات.

## 🧠 فكرة المشروع

يقوم URLTrap بتحليل الرابط المُدخل من المستخدم ويقوم بـ:
- التحقق من صحة الرابط
- تتبع التحويلات (Redirects)
- تحليل الصفحة النهائية واستخراج الروابط منها
- الإشارة إلى أي روابط مشبوهة تحتوي على كلمات مثل `track`, `ads`, `click`, إلخ.

## 🛠️ مكونات المشروع

- `app.py`: الكود الرئيسي لتشغيل الأداة باستخدام Flask
- `requirements.txt`: يحتوي على المكتبات المطلوبة
- `Procfile`: ملف لتحديد طريقة التشغيل (مهم لاستضافة مثل Render)

## ⚙️ طريقة التشغيل محلياً

```bash
git clone https://github.com/salmanawad/Majed-and-Salman-project.git
cd Majed-and-Salman-project
pip install -r requirements.txt
python app.py
