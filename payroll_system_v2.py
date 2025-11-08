#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة رواتب المصنع - إصدار 2
Factory Payroll Management System - Version 2

مع المعادلات المحدثة ونظام إضافة الموظفين يدوياً
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

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
        """حساب أجر اليوم - Calculate daily wage"""
        return self.base_salary / 30
    
    def calculate_hourly_wage(self) -> float:
        """حساب أجر الساعة - Calculate hourly wage"""
        daily_wage = self.calculate_daily_wage()
        return daily_wage / self.hours_per_day
    
    def calculate_minute_wage(self) -> float:
        """حساب أجر الدقيقة - Calculate per minute wage"""
        hourly_wage = self.calculate_hourly_wage()
        return hourly_wage / 60
    
    def calculate_absence_deduction(self) -> float:
        """حساب خصم الغياب (يوم بيوم) - Calculate absence deduction"""
        daily_wage = self.calculate_daily_wage()
        return self.absence_days * daily_wage
    
    def calculate_late_deduction(self) -> float:
        """حساب خصم التأخير (الدقيقة بـ 3 دقائق)"""
        minute_wage = self.calculate_minute_wage()
        return self.late_minutes * minute_wage * 3
    
    def calculate_extra_days_pay(self) -> float:
        """حساب أجر الأيام الإضافية (نفس أجر اليوم)"""
        daily_wage = self.calculate_daily_wage()
        return self.extra_days * daily_wage
    
    def calculate_extra_hours_pay(self) -> float:
        """حساب أجر الساعات الإضافية (نفس أجر الساعة)"""
        hourly_wage = self.calculate_hourly_wage()
        return self.extra_hours * hourly_wage
    
    def calculate_net_salary(self) -> float:
        """حساب صافي الراتب - Calculate net salary"""
        # الإضافات
        additions = (
            self.calculate_extra_days_pay() +
            self.calculate_extra_hours_pay()
        )
        
        # الخصومات
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

class PayrollSystem:
    """نظام الرواتب - Payroll System"""
    
    def __init__(self, data_file: str = 'employees.json'):
        self.data_file = data_file
        self.employees: List[Employee] = []
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.employees = [Employee.from_dict(emp) for emp in data]
                print(f"✓ تم تحميل {len(self.employees)} موظف")
            except:
                print("سيتم إنشاء ملف جديد")
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = [emp.to_dict() for emp in self.employees]
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✓ تم حفظ البيانات")
        except Exception as e:
            print(f"✗ خطأ: {e}")
    
    def add_employee(self):
        """إضافة موظف جديد - Add new employee"""
        print("\n" + "="*50)
        print("إضافة موظف جديد")
        print("="*50)
        
        emp_id = input("رقم الموظف: ")
        if self.find_employee(emp_id):
            print("✗ الموظف موجود بالفعل")
            return
        
        name = input("اسم الموظف: ")
        base_salary = float(input("الراتب الأساسي: "))
        hours_per_day = int(input("عدد ساعات العمل يومياً: "))
        insurance = float(input("خصم التأمينات: "))
        
        emp = Employee(emp_id, name, base_salary, hours_per_day, insurance)
        self.employees.append(emp)
        self.save_data()
        print(f"✓ تم إضافة {name} بنجاح")
    
    def find_employee(self, emp_id: str) -> Optional[Employee]:
        for emp in self.employees:
            if emp.emp_id == emp_id:
                return emp
        return None
    
    def update_employee_data(self):
        emp_id = input("رقم الموظف: ")
        emp = self.find_employee(emp_id)
        if not emp:
            print("✗ الموظف غير موجود")
            return
        
        print(f"\nتحديث بيانات: {emp.name}")
        print("1. أيام الغياب")
        print("2. دقائق التأخير")
        print("3. الأيام الإضافية")
        print("4. الساعات الإضافية")
        print("5. الخصم الجزائي")
        
        choice = input("اختر: ")
        
        if choice == '1':
            emp.absence_days = float(input("عدد أيام الغياب: "))
        elif choice == '2':
            emp.late_minutes = float(input("عدد دقائق التأخير: "))
        elif choice == '3':
            emp.extra_days = float(input("عدد الأيام الإضافية: "))
        elif choice == '4':
            emp.extra_hours = float(input("عدد الساعات الإضافية: "))
        elif choice == '5':
            emp.penalty_deduction = float(input("قيمة الخصم الجزائي: "))
        
        self.save_data()
        print("✓ تم التحديث")
    
    def generate_payslip(self):
        emp_id = input("رقم الموظف: ")
        emp = self.find_employee(emp_id)
        if not emp:
            print("✗ الموظف غير موجود")
            return
        
        print("\n" + "="*70)
        print(f"كارت راتب - {emp.name}")
        print("="*70)
        print(f"رقم الموظف: {emp.emp_id}")
        print(f"عدد ساعات العمل: {emp.hours_per_day} ساعة/يوم")
        print("-"*70)
        print(f"الراتب الأساسي: {emp.base_salary:.2f} جنيه")
        print("\nالإضافات:")
        print(f"  + أيام إضافية ({emp.extra_days}): {emp.calculate_extra_days_pay():.2f} جنيه")
        print(f"  + ساعات إضافية ({emp.extra_hours}): {emp.calculate_extra_hours_pay():.2f} جنيه")
        print("\nالخصومات:")
        print(f"  - غياب ({emp.absence_days} يوم): {emp.calculate_absence_deduction():.2f} جنيه")
        print(f"  - تأخير ({emp.late_minutes} دقيقة): {emp.calculate_late_deduction():.2f} جنيه")
        print(f"  - تأمينات: {emp.insurance_deduction:.2f} جنيه")
        print(f"  - خصم جزائي: {emp.penalty_deduction:.2f} جنيه")
        print("-"*70)
        print(f"💰 صافي الراتب: {emp.calculate_net_salary():.2f} جنيه")
        print("="*70 + "\n")
    
    def list_employees(self):
        if not self.employees:
            print("لا يوجد موظفون")
            return
        
        print("\n" + "="*90)
        print(f"{الرقم:<10} {الاسم:<25} {الراتب:<15} {الساعات:<10} {التأمينات:<15}")
        print("="*90)
        for emp in self.employees:
            print(f"{emp.emp_id:<10} {emp.name:<25} {emp.base_salary:<15.2f} {emp.hours_per_day:<10} {emp.insurance_deduction:<15.2f}")
        print("="*90 + "\n")

def main():
    system = PayrollSystem()
    
    while True:
        print("\n" + "="*60)
        print("💼 نظام إدارة رواتب المصنع - إصدار 2")
        print("="*60)
        print("👥 1. إضافة موظف جديد")
        print("📋 2. عرض جميع الموظفين")
        print("✏️  3. تحديث بيانات موظف (غياب/تأخير/إضافي/خصم)")
        print("💰 4. إنشاء كارت راتب")
        print("🚪 5. خروج")
        print("="*60)
        
        choice = input("اختر عملية (1-5): ")
        
        if choice == '1':
            system.add_employee()
        elif choice == '2':
            system.list_employees()
        elif choice == '3':
            system.update_employee_data()
        elif choice == '4':
            system.generate_payslip()
        elif choice == '5':
            print("\n✅ شكراً لاستخدامك النظام!")
            break
        else:
            print("✗ اختيار غير صحيح")

if __name__ == "__main__":
    print("""
    ╭────────────────────────────────────────────────────────╮
    │  💼 نظام إدارة رواتب المصنع - إصدار 2.0          │
    │  Factory Payroll Management System V2.0         │
    ├────────────────────────────────────────────────────────┤
    │  ✅ الغياب: يوم بيوم                                  │
    │  ✅ التأخير: الدقيقة بـ 3 دقائق                      │
    │  ✅ اليوم الإضافي: نفس أجر اليوم                   │
    │  ✅ الساعة الإضافية: نفس أجر الساعة               │
    │  ✅ خصم التأمينات والجزاءات                        │
    ╰────────────────────────────────────────────────────────╯
    """)
    main()
