#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة رواتب المصنع - واجهة رسومية
Factory Payroll Management System - GUI Version
بواجهة رسومية احترافية لنظام ويندوز
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import shutil


class Employee:
    """فئة الموظف - Employee Class"""
    
    def __init__(self, emp_id: str, name: str, base_salary: float, 
                 hours_per_day: int, insurance_deduction: float):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary
        self.hours_per_day = hours_per_day
        self.insurance_deduction = insurance_deduction
        
        # الغياب والتأخير | Absence & Late
        self.absence_days = 0
        self.late_minutes = 0
        
        # العمل الإضافي | Overtime
        self.extra_days = 0
        self.extra_hours = 0
        
        # الخصومات | Deductions
        self.penalty_deduction = 0
    
    def calculate_daily_wage(self) -> float:
        """حساب أجر اليوم"""
        return self.base_salary / 30
    
    def calculate_hourly_wage(self) -> float:
        """حساب أجر الساعة"""
        daily_wage = self.calculate_daily_wage()
        return daily_wage / self.hours_per_day
    
    def calculate_minute_wage(self) -> float:
        """حساب أجر الدقيقة"""
        hourly_wage = self.calculate_hourly_wage()
        return hourly_wage / 60
    
    def calculate_absence_deduction(self) -> float:
        """حساب خصم الغياب (يوم بيوم)"""
        daily_wage = self.calculate_daily_wage()
        return self.absence_days * daily_wage
    
    def calculate_late_deduction(self) -> float:
        """حساب خصم التأخير (الدقيقة بـ 3 دقائق)"""
        minute_wage = self.calculate_minute_wage()
        return self.late_minutes * minute_wage * 3
    
    def calculate_extra_days_pay(self) -> float:
        """حساب أجر الأيام الإضافية"""
        daily_wage = self.calculate_daily_wage()
        return self.extra_days * daily_wage
    
    def calculate_extra_hours_pay(self) -> float:
        """حساب أجر الساعات الإضافية"""
        hourly_wage = self.calculate_hourly_wage()
        return self.extra_hours * hourly_wage
    
    def calculate_net_salary(self) -> float:
        """حساب صافي الراتب"""
        additions = (
            self.calculate_extra_days_pay() +
            self.calculate_extra_hours_pay()
        )
        
        deductions = (
            self.calculate_absence_deduction() +
            self.calculate_late_deduction() +
            self.insurance_deduction +
            self.penalty_deduction
        )
        
        net_salary = self.base_salary + additions - deductions
        return round(net_salary, 2)
    
    def to_dict(self) -> Dict:
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'base_salary': self.base_salary,
            'hours_per_day': self.hours_per_day,
            'insurance_deduction': self.insurance_deduction,
            'absence_days': self.absence_days,
            'late_minutes': self.late_minutes,
            'extra_days': self.extra_days,
            'extra_hours': self.extra_hours,
            'penalty_deduction': self.penalty_deduction
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        emp = cls(
            data['emp_id'],
            data['name'],
            data['base_salary'],
            data['hours_per_day'],
            data['insurance_deduction']
        )
        emp.absence_days = data.get('absence_days', 0)
        emp.late_minutes = data.get('late_minutes', 0)
        emp.extra_days = data.get('extra_days', 0)
        emp.extra_hours = data.get('extra_hours', 0)
        emp.penalty_deduction = data.get('penalty_deduction', 0)
        return emp


class PayrollGUI:
    """واجهة نظام الرواتب - Payroll GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("💼 نظام إدارة رواتب المصنع - Factory Payroll System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        self.data_file = 'employees.json'
        self.backup_folder = 'payroll_backups'
        self.employees: List[Employee] = []
        
        self.load_data()
        self.setup_ui()
        
    def load_data(self):
        """\u062a\u062d\u0645\u064a\u0644 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.employees = [Employee.from_dict(emp) for emp in data]
            except:
                self.employees = []
    
    def save_data(self):
        """\u062d\u0641\u0638 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = [emp.to_dict() for emp in self.employees]
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("نجاح", "✓ تم حفظ البيانات بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"✗ حدث خطأ: {e}")
    
    def backup_data(self):
        """\u0646\u0633\u062e \u0627\u062d\u062a\u064a\u0627\u0637\u064a"""
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_folder, f"employees_{timestamp}.json")
        
        try:
            shutil.copy2(self.data_file, backup_file)
            messagebox.showinfo("نجاح", f"✓ تم حفظ نسخة احتياطية\n{backup_file}")
        except Exception as e:
            messagebox.showerror("خطأ", f"✗ حدث خطأ: {e}")
    
    def setup_ui(self):
        """\u0625\u0639\u062f\u0627\u062f \u0627\u0644\u0648\u0627\u062c\u0647\u0629"""
        # ش\u0631\u064a\u0637 \u0627\u0644\u0639\u0646\u0648\u0627\u0646
        title_frame = tk.Frame(self.root, bg='#34495e', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="💼 نظام إدارة رواتب المصنع",
            font=('Arial', 24, 'bold'),
            bg='#34495e',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # \u0634\u0631\u064a\u0637 \u0627\u0644\u0623\u0632\u0631\u0627\u0631
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        buttons = [
            ("➕ إضافة موظف", self.add_employee, '#27ae60'),
            ("📋 عرض الموظفين", self.show_employees, '#3498db'),
            ("✏️ تحديث بيانات", self.update_employee, '#f39c12'),
            ("💰 كارت راتب", self.generate_payslip, '#9b59b6'),
            ("💾 حفظ", self.save_data, '#16a085'),
            ("💾 نسخة احتياطية", self.backup_data, '#d35400'),
            ("🖨️ طباعة", self.print_report, '#c0392b'),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                width=15,
                height=2,
                relief='raised',
                cursor='hand2'
            )
            btn.pack(side='left', padx=5)
        
        # \u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0639\u0631\u0636
        display_frame = tk.Frame(self.root, bg='#2c3e50')
        display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.display_area = scrolledtext.ScrolledText(
            display_frame,
            font=('Courier New', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wrap='word'
        )
        self.display_area.pack(fill='both', expand=True)
        
        # \u0631\u0633\u0627\u0644\u0629 \u062a\u0631\u062d\u064a\u0628ي\u0629
        welcome_msg = """
\u256d\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256e
\u2502   💼 \u0645\u0631\u062d\u0628\u0627\u064b \u0628\u0643 \u0641\u064a \u0646\u0638\u0627\u0645 \u0625\u062f\u0627\u0631\u0629 \u0631\u0648\u0627\u062a\u0628 \u0627\u0644\u0645\u0635\u0646\u0639           \u2502
\u2502   Factory Payroll Management System v3.0      \u2502
\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524
\u2502   \u2713 \u0648\u0627\u062c\u0647\u0629 \u0631\u0633\u0648\u0645\u064a\u0629 \u0627\u062d\u062a\u0631\u0627\u0641\u064a\u0629 \u0644\u0646\u0638\u0627\u0645 \u0648\u064a\u0646\u062f\u0648\u0632      \u2502
\u2502   \u2713 \u062d\u0641\u0638 \u062a\u0644\u0642\u0627\u0626\u064a \u0644\u0644\u0628\u064a\u0627\u0646\u0627\u062a                        \u2502
\u2502   \u2713 \u0646\u0633\u062e \u0627\u062d\u062a\u064a\u0627\u0637\u064a\u0629 \u0622\u0645\u0646\u0629                          \u2502
\u2502   \u2713 \u0637\u0628\u0627\u0639\u0629 \u0643\u0634\u0648\u0641\u0627\u062a \u0627\u0644\u0631\u0648\u0627\u062a\u0628                    \u2502
\u2570\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256f

\u0627\u0633\u062a\u062e\u062f\u0645 \u0627\u0644\u0623\u0632\u0631\u0627\u0631 \u0641\u064a \u0627\u0644\u0623\u0639\u0644\u0649 \u0644\u0644\u0628\u062f\u0621...
        """
        self.display_area.insert('1.0', welcome_msg)
    
    def add_employee(self):
        """\u0625\u0636\u0627\u0641\u0629 \u0645\u0648\u0638\u0641 \u062c\u062f\u064a\u062f"""
        add_window = tk.Toplevel(self.root)
        add_window.title("➕ إضافة موظف جديد")
        add_window.geometry("500x450")
        add_window.configure(bg='#34495e')
        
        # \u0627\u0644\u062d\u0642\u0648\u0644
        fields = [
            ("رقم الموظف:", "emp_id"),
            ("الاسم:", "name"),
            ("الراتب الأساسي:", "base_salary"),
            ("ساعات العمل يومياً:", "hours_per_day"),
            ("خصم التأمينات:", "insurance")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            lbl = tk.Label(
                add_window,
                text=label,
                font=('Arial', 12),
                bg='#34495e',
                fg='white'
            )
            lbl.grid(row=i, column=0, padx=20, pady=15, sticky='e')
            
            entry = tk.Entry(add_window, font=('Arial', 12), width=25)
            entry.grid(row=i, column=1, padx=20, pady=15)
            entries[key] = entry
        
        def save_employee():
            try:
                emp_id = entries['emp_id'].get()
                name = entries['name'].get()
                base_salary = float(entries['base_salary'].get())
                hours = int(entries['hours_per_day'].get())
                insurance = float(entries['insurance'].get())
                
                if any(e.emp_id == emp_id for e in self.employees):
                    messagebox.showerror("خطأ", "✗ الموظف موجود بالفعل")
                    return
                
                emp = Employee(emp_id, name, base_salary, hours, insurance)
                self.employees.append(emp)
                self.save_data()
                
                add_window.destroy()
                self.display_area.delete('1.0', 'end')
                self.display_area.insert('1.0', f"✓ تم إضافة الموظف {name} بنجاح!")
            except ValueError:
                messagebox.showerror("خطأ", "✗ يرجى إدخال قيم صحيحة")
        
        btn = tk.Button(
            add_window,
            text="✓ حفظ",
            command=save_employee,
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            width=20,
            height=2
        )
        btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    def show_employees(self):
        """\u0639\u0631\u0636 \u062c\u0645\u064a\u0639 \u0627\u0644\u0645\u0648\u0638\u0641\u064a\u0646"""
        self.display_area.delete('1.0', 'end')
        if not self.employees:
            self.display_area.insert('1.0', "✗ \u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0648\u0638\u0641\u0648\u0646")
            return
        
        output = "\n" + "="*100 + "\n"
        output += f"{'\u0627\u0644\u0631\u0642\u0645':<10} {'\u0627\u0644\u0627\u0633\u0645':<25} {'\u0627\u0644\u0631\u0627\u062a\u0628 \u0627\u0644\u0623\u0633\u0627\u0633\u064a':<15} {'\u0627\u0644\u0633\u0627\u0639\u0627\u062a':<10} {'\u0627\u0644\u062a\u0623\u0645\u064a\u0646\u0627\u062a':<15}\n"
        output += "="*100 + "\n"
        
        for emp in self.employees:
            output += f"{emp.emp_id:<10} {emp.name:<25} {emp.base_salary:<15.2f} {emp.hours_per_day:<10} {emp.insurance_deduction:<15.2f}\n"
        
        output += "="*100 + "\n"
        output += f"\n\u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0645\u0648\u0638\u0641\u064a\u0646: {len(self.employees)}\n"
        
        self.display_area.insert('1.0', output)
    
    def update_employee(self):
        """\u062a\u062d\u062f\u064a\u062b \u0628\u064a\u0627\u0646\u0627\u062a \u0645\u0648\u0638\u0641"""
        if not self.employees:
            messagebox.showwarning("ت\u0646\u0628\u064a\u0647", "✗ \u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0648\u0638\u0641\u0648\u0646")
            return
        
        update_window = tk.Toplevel(self.root)
        update_window.title("✏\ufe0f \u062a\u062d\u062f\u064a\u062b \u0628\u064a\u0627\u0646\u0627\u062a \u0645\u0648\u0638\u0641")
        update_window.geometry("500x500")
        update_window.configure(bg='#34495e')
        
        # \u0627\u062e\u062a\u064a\u0627\u0631 \u0627\u0644\u0645\u0648\u0638\u0641
        tk.Label(
            update_window,
            text="\u0627\u062e\u062a\u0631 \u0627\u0644\u0645\u0648\u0638\u0641:",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=10)
        
        emp_names = [f"{e.emp_id} - {e.name}" for e in self.employees]
        emp_var = tk.StringVar()
        emp_combo = ttk.Combobox(
            update_window,
            textvariable=emp_var,
            values=emp_names,
            font=('Arial', 11),
            width=40,
            state='readonly'
        )
        emp_combo.pack(pady=10)
        
        # \u0627\u062e\u062a\u064a\u0627\u0631 \u0646\u0648\u0639 \u0627\u0644\u062a\u062d\u062f\u064a\u062b
        tk.Label(
            update_window,
            text="\u0646\u0648\u0639 \u0627\u0644\u062a\u062d\u062f\u064a\u062b:",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=10)
        
        update_types = [
            "\u0623\u064a\u0627\u0645 \u0627\u0644\u063a\u064a\u0627\u0628",
            "\u062f\u0642\u0627\u0626\u0642 \u0627\u0644\u062a\u0623\u062e\u064a\u0631",
            "\u0627\u0644\u0623\u064a\u0627\u0645 \u0627\u0644\u0625\u0636\u0627\u0641\u064a\u0629",
            "\u0627\u0644\u0633\u0627\u0639\u0627\u062a \u0627\u0644\u0625\u0636\u0627\u0641\u064a\u0629",
            "\u0627\u0644\u062e\u0635\u0645 \u0627\u0644\u062c\u0632\u0627\u0626\u064a"
        ]
        
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(
            update_window,
            textvariable=type_var,
            values=update_types,
            font=('Arial', 11),
            width=40,
            state='readonly'
        )
        type_combo.pack(pady=10)
        
        # \u062d\u0642\u0644 \u0627\u0644\u0642\u064a\u0645\u0629
        tk.Label(
            update_window,
            text="\u0627\u0644\u0642\u064a\u0645\u0629:",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=10)
        
        value_entry = tk.Entry(update_window, font=('Arial', 12), width=30)
        value_entry.pack(pady=10)
        
        def save_update():
            try:
                selected = emp_var.get()
                if not selected:
                    messagebox.showerror("\u062e\u0637\u0623", "\u2717 \u064a\u0631\u062c\u0649 \u0627\u062e\u062a\u064a\u0627\u0631 \u0645\u0648\u0638\u0641")
                    return
                
                emp_id = selected.split(' - ')[0]
                emp = next((e for e in self.employees if e.emp_id == emp_id), None)
                
                if not emp:
                    return
                
                value = float(value_entry.get())
                update_type = type_var.get()
                
                if update_type == "\u0623\u064a\u0627\u0645 \u0627\u0644\u063a\u064a\u0627\u0628":
                    emp.absence_days = value
                elif update_type == "\u062f\u0642\u0627\u0626\u0642 \u0627\u0644\u062a\u0623\u062e\u064a\u0631":
                    emp.late_minutes = value
                elif update_type == "\u0627\u0644\u0623\u064a\u0627\u0645 \u0627\u0644\u0625\u0636\u0627\u0641\u064a\u0629":
                    emp.extra_days = value
                elif update_type == "\u0627\u0644\u0633\u0627\u0639\u0627\u062a \u0627\u0644\u0625\u0636\u0627\u0641\u064a\u0629":
                    emp.extra_hours = value
                elif update_type == "\u0627\u0644\u062e\u0635\u0645 \u0627\u0644\u062c\u0632\u0627\u0626\u064a":
                    emp.penalty_deduction = value
                
                self.save_data()
                update_window.destroy()
                self.display_area.delete('1.0', 'end')
                self.display_area.insert('1.0', f"\u2713 \u062a\u0645 \u062a\u062d\u062f\u064a\u062b \u0628\u064a\u0627\u0646\u0627\u062a {emp.name} \u0628\u0646\u062c\u0627\u062d!")
            except ValueError:
                messagebox.showerror("\u062e\u0637\u0623", "\u2717 \u064a\u0631\u062c\u0649 \u0625\u062f\u062e\u0627\u0644 \u0642\u064a\u0645\u0629 \u0635\u062d\u064a\u062d\u0629")
        
        btn = tk.Button(
            update_window,
            text="\u2713 \u062d\u0641\u0638 \u0627\u0644\u062a\u062d\u062f\u064a\u062b",
            command=save_update,
            font=('Arial', 14, 'bold'),
            bg='#f39c12',
            fg='white',
            width=20,
            height=2
        )
        btn.pack(pady=20)
    
    def generate_payslip(self):
        """\u0625\u0646\u0634\u0627\u0621 \u0643\u0627\u0631\u062a \u0631\u0627\u062a\u0628"""
        if not self.employees:
            messagebox.showwarning("\u062a\u0646\u0628\u064a\u0647", "\u2717 \u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0648\u0638\u0641\u0648\u0646")
            return
        
        payslip_window = tk.Toplevel(self.root)
        payslip_window.title("💰 \u0643\u0627\u0631\u062a \u0631\u0627\u062a\u0628")
        payslip_window.geometry("500x300")
        payslip_window.configure(bg='#34495e')
        
        tk.Label(
            payslip_window,
            text="\u0627\u062e\u062a\u0631 \u0627\u0644\u0645\u0648\u0638\u0641:",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=20)
        
        emp_names = [f"{e.emp_id} - {e.name}" for e in self.employees]
        emp_var = tk.StringVar()
        emp_combo = ttk.Combobox(
            payslip_window,
            textvariable=emp_var,
            values=emp_names,
            font=('Arial', 11),
            width=40,
            state='readonly'
        )
        emp_combo.pack(pady=10)
        
        def show_payslip():
            selected = emp_var.get()
            if not selected:
                messagebox.showerror("\u062e\u0637\u0623", "\u2717 \u064a\u0631\u062c\u0649 \u0627\u062e\u062a\u064a\u0627\u0631 \u0645\u0648\u0638\u0641")
                return
            
            emp_id = selected.split(' - ')[0]
            emp = next((e for e in self.employees if e.emp_id == emp_id), None)
            
            if not emp:
                return
            
            payslip = f"""
\n{'='*70}
\u0643\u0627\u0631\u062a \u0631\u0627\u062a\u0628 - {emp.name}
{'='*70}
\u0631\u0642\u0645 \u0627\u0644\u0645\u0648\u0638\u0641: {emp.emp_id}
\u0639\u062f\u062f \u0633\u0627\u0639\u0627\u062a \u0627\u0644\u0639\u0645\u0644: {emp.hours_per_day} \u0633\u0627\u0639\u0629/\u064a\u0648\u0645
{'-'*70}
\u0627\u0644\u0631\u0627\u062a\u0628 \u0627\u0644\u0623\u0633\u0627\u0633\u064a: {emp.base_salary:.2f} \u062c\u0646\u064a\u0647

\u0627\u0644\u0625\u0636\u0627\u0641\u0627\u062a:
 + \u0623\u064a\u0627\u0645 \u0625\u0636\u0627\u0641\u064a\u0629 ({emp.extra_days}): {emp.calculate_extra_days_pay():.2f} \u062c\u0646\u064a\u0647
 + \u0633\u0627\u0639\u0627\u062a \u0625\u0636\u0627\u0641\u064a\u0629 ({emp.extra_hours}): {emp.calculate_extra_hours_pay():.2f} \u062c\u0646\u064a\u0647

\u0627\u0644\u062e\u0635\u0648\u0645\u0627\u062a:
 - \u063a\u064a\u0627\u0628 ({emp.absence_days} \u064a\u0648\u0645): {emp.calculate_absence_deduction():.2f} \u062c\u0646\u064a\u0647
 - \u062a\u0623\u062e\u064a\u0631 ({emp.late_minutes} \u062f\u0642\u064a\u0642\u0629): {emp.calculate_late_deduction():.2f} \u062c\u0646\u064a\u0647
 - \u062a\u0623\u0645\u064a\u0646\u0627\u062a: {emp.insurance_deduction:.2f} \u062c\u0646\u064a\u0647
 - \u062e\u0635\u0645 \u062c\u0632\u0627\u0626\u064a: {emp.penalty_deduction:.2f} \u062c\u0646\u064a\u0647
{'-'*70}
💰 \u0635\u0627\u0641\u064a \u0627\u0644\u0631\u0627\u062a\u0628: {emp.calculate_net_salary():.2f} \u062c\u0646\u064a\u0647
{'='*70}

\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0637\u0628\u0627\u0639\u0629: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            payslip_window.destroy()
            self.display_area.delete('1.0', 'end')
            self.display_area.insert('1.0', payslip)
        
        btn = tk.Button(
            payslip_window,
            text="\u2713 \u0625\u0646\u0634\u0627\u0621 \u0627\u0644\u0643\u0627\u0631\u062a",
            command=show_payslip,
            font=('Arial', 14, 'bold'),
            bg='#9b59b6',
            fg='white',
            width=20,
            height=2
        )
        btn.pack(pady=20)
    
    def print_report(self):
        """\u0637\u0628\u0627\u0639\u0629 \u0627\u0644\u062a\u0642\u0631\u064a\u0631"""
        content = self.display_area.get('1.0', 'end')
        if not content.strip():
            messagebox.showwarning("\u062a\u0646\u0628\u064a\u0647", "\u2717 \u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u062d\u062a\u0648\u0649 \u0644\u0644\u0637\u0628\u0627\u0639\u0629")
            return
        
        # \u062d\u0641\u0638 \u0641\u064a \u0645\u0644\u0641 \u0646\u0635\u064a
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"report_{timestamp}.txt"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("\u0646\u062c\u0627\u062d", f"\u2713 \u062a\u0645 \u062d\u0641\u0638 \u0627\u0644\u062a\u0642\u0631\u064a\u0631 \u0641\u064a:\n{report_file}\n\n\u064a\u0645\u0643\u0646\u0643 \u0637\u0628\u0627\u0639\u062a\u0647 \u0645\u0646 \u0627\u0644\u0645\u0644\u0641")
        except Exception as e:
            messagebox.showerror("\u062e\u0637\u0623", f"\u2717 \u062d\u062f\u062b \u062e\u0637\u0623: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollGUI(root)
    root.mainloop()
