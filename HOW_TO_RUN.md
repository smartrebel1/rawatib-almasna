# 🚀 كيفية تشغيل البرنامج - How to Run the Program

## 💻 متطلبات التشغيل | Requirements

### لتشغيل البرنامج بصيغة Python:
1. **تثبيت Python 3.7+**
   - قم بتحميل Python من: https://www.python.org/downloads/
   - تأكد من تفعيل خيار "Add Python to PATH" أثناء التثبيت

2. **تحميل الملفات**
   ```bash
   git clone https://github.com/smartrebel1/rawatib-almasna.git
   cd rawatib-almasna
   ```

3. **تشغيل البرنامج**
   ```bash
   python payroll_gui.py
   ```

---

## 📦 تحويل البرنامج إلى ملف EXE | Convert to EXE

### لإنشاء ملف exe يعمل على أي جهاز ويندوز دون تثبيت Python:

1. **تثبيت PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **إنشاء ملف EXE**
   ```bash
   pyinstaller --onefile --windowed --name="PayrollSystem" payroll_gui.py
   ```

3. **موقع الملف الناتج**
   - سيتم إنشاء مجلد `dist/`
   - الملف التنفيذي: `dist/PayrollSystem.exe`

4. **نسخ وتشغيل**
   - انسخ `PayrollSystem.exe` إلى أي مكان
   - شغله بنقرة مزدوجة
   - لا حاجة لتثبيت Python!

---

## 💾 إدارة البيانات | Data Management

### ملفات البيانات:
- `employees.json` - ملف بيانات الموظفين الرئيسي
- `payroll_backups/` - مجلد النسخ الاحتياطية

### استعادة البيانات بعد إعادة تثبيت ويندوز:
1. ابحث عن ملف `employees.json` في المجلد القديم
2. انسخه إلى نفس مجلد البرنامج الجديد
3. شغل البرنامج - ستظهر بياناتك القديمة!

---

## ⚙️ خيارات PyInstaller متقدمة | Advanced Options

### لإضافة أيقونة مخصصة:
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="PayrollSystem" payroll_gui.py
```

### لتضمين ملفات إضافية:
```bash
pyinstaller --onefile --windowed --add-data "employees.json;." payroll_gui.py
```

---

## ❓ مشاكل شائعة | Common Issues

### 1. خطأ "Python not found"
- تأكد من تثبيت Python وإضافته للـ PATH

### 2. خطأ "tkinter not found"
- tkinter متضمنة مع Python - أعد تثبيت Python

### 3. البرنامج لا يظهر العربي بشكل صحيح
- استخدم فونت Arial أو Tahoma

---

## 📞 دعم | Support
للدعم الفني أو الاستفسارات، افتح Issue على GitHub
