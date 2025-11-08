#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة رواتب المصنع
Factory Payroll Management System

برنامج شامل لإدارة رواتب الموظفين في المصنع
Complete program for managing employee payroll in factory
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Employee:
    """فئة الموظف - Employee Class"""
    
    def __init__(self, emp_id: str, name: str, position: str, 
                 base_salary: float, hire_date: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.base_salary = base_salary
        self.hire_date = hire_date
        self.overtime_hours = 0
        self.bonuses = 0
        self.deductions = 0
    
    def calculate_salary(self, overtime_rate: float = 1.5) -> float:
        """حساب الراتب الإجمالي - Calculate total salary"""
        overtime_pay = self.overtime_hours * (self.base_salary / 160) * overtime_rate
        total = self.base_salary + overtime_pay + self.bonuses - self.deductions
        return round(total, 2)
    
    def to_dict(self) -> Dict:
        """تحويل بيانات الموظف إلى قاموس - Convert employee data to dictionary"""
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'position': self.position,
            'base_salary': self.base_salary,
            'hire_date': self.hire_date,
            'overtime_hours': self.overtime_hours,
            'bonuses': self.bonuses,
            'deductions': self.deductions
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """إنشاء موظف من قاموس - Create employee from dictionary"""
        emp = cls(
            data['emp_id'],
            data['name'],
            data['position'],
            data['base_salary'],
            data['hire_date']
        )
        emp.overtime_hours = data.get('overtime_hours', 0)
        emp.bonuses = data.get('bonuses', 0)
        emp.deductions = data.get('deductions', 0)
        return emp

class PayrollSystem:
    """نظام الرواتب - Payroll System"""
    
    def __init__(self, data_file: str = 'employees.json'):
        self.data_file = data_file
        self.employees: List[Employee] = []
        self.load_data()
    
    def load_data(self):
        """تحميل البيانات من الملف - Load data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.employees = [Employee.from_dict(emp) for emp in data]
                print(f"✓ تم تحميل {len(self.employees)} موظف")
            except Exception as e:
                print(f"✗ خطأ في تحميل البيانات: {e}")
        else:
            print("! ملف البيانات غير موجود. سيتم إنشاء ملف جديد.")
    
    def save_data(self):
        """حفظ البيانات إلى الملف - Save data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = [emp.to_dict() for emp in self.employees]
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✓ تم حفظ البيانات بنجاح")
        except Exception as e:
            print(f"✗ خطأ في حفظ البيانات: {e}")
    
    def add_employee(self, emp_id: str, name: str, position: str,
                     base_salary: float, hire_date: str = None):
        """إضافة موظف جديد - Add new employee"""
        if self.find_employee(emp_id):
            print(f"✗ الموظف برقم {emp_id} موجود بالفعل")
            return False
        
        if hire_date is None:
            hire_date = datetime.now().strftime("%Y-%m-%d")
        
        emp = Employee(emp_id, name, position, base_salary, hire_date)
        self.employees.append(emp)
        self.save_data()
        print(f"✓ تم إضافة الموظف {name} بنجاح")
        return True
    
    def find_employee(self, emp_id: str) -> Optional[Employee]:
        """البحث عن موظف - Find employee"""
        for emp in self.employees:
            if emp.emp_id == emp_id:
                return emp
        return None
    
    def update_employee(self, emp_id: str, **kwargs):
        """تحديث بيانات موظف - Update employee data"""
        emp = self.find_employee(emp_id)
        if not emp:
            print(f"✗ الموظف برقم {emp_id} غير موجود")
            return False
        
        for key, value in kwargs.items():
            if hasattr(emp, key):
                setattr(emp, key, value)
        
        self.save_data()
        print(f"✓ تم تحديث بيانات الموظف {emp.name}")
        return True
    
    def delete_employee(self, emp_id: str):
        """حذف موظف - Delete employee"""
        emp = self.find_employee(emp_id)
        if not emp:
            print(f"✗ الموظف برقم {emp_id} غير موجود")
            return False
        
        self.employees.remove(emp)
        self.save_data()
        print(f"✓ تم حذف الموظف {emp.name}")
        return True
    
    def generate_payslip(self, emp_id: str):
        """إنشاء كشف راتب - Generate payslip"""
        emp = self.find_employee(emp_id)
        if not emp:
            print(f"✗ الموظف برقم {emp_id} غير موجود")
            return
        
        print("\n" + "="*50)
        print("كشف راتب - PAYSLIP")
        print("="*50)
        print(f"رقم الموظف: {emp.emp_id}")
        print(f"الاسم: {emp.name}")
        print(f"الوظيفة: {emp.position}")
        print(f"تاريخ التوظيف: {emp.hire_date}")
        print("-"*50)
        print(f"الراتب الأساسي: {emp.base_salary:.2f}")
        
        overtime_pay = emp.overtime_hours * (emp.base_salary / 160) * 1.5
        print(f"ساعات إضافية ({emp.overtime_hours}h): {overtime_pay:.2f}")
        print(f"المكافآت: {emp.bonuses:.2f}")
        print(f"الخصومات: -{emp.deductions:.2f}")
        print("-"*50)
        print(f"إجمالي الراتب: {emp.calculate_salary():.2f}")
        print("="*50 + "\n")
    
    def list_employees(self):
        """عرض قائمة الموظفين - List all employees"""
        if not self.employees:
            print("! لا يوجد موظفون في النظام")
            return
        
        print("\n" + "="*80)
        print(f"{'الرقم':<10} {'الاسم':<20} {'الوظيفة':<20} {'الراتب':<15}")
        print("="*80)
        for emp in self.employees:
            print(f"{emp.emp_id:<10} {emp.name:<20} {emp.position:<20} "
                  f"{emp.base_salary:<15.2f}")
        print("="*80 + "\n")
    
    def generate_monthly_report(self):
        """تقرير شهري للرواتب - Monthly payroll report"""
        if not self.employees:
            print("! لا يوجد موظفون في النظام")
            return
        
        total_payroll = sum(emp.calculate_salary() for emp in self.employees)
        
        print("\n" + "="*60)
        print(f"تقرير الرواتب الشهري - {datetime.now().strftime('%B %Y')}")
        print("="*60)
        print(f"عدد الموظفين: {len(self.employees)}")
        print(f"إجمالي الرواتب: {total_payroll:.2f}")
        print(f"متوسط الراتب: {total_payroll/len(self.employees):.2f}")
        print("="*60 + "\n")

def main():
    """الوظيفة الرئيسية - Main function"""
    system = PayrollSystem()
    
    while True:
        print("\n" + "="*50)
        print("نظام إدارة رواتب المصنع")
        print("Factory Payroll Management System")
        print("="*50)
        print("1. إضافة موظف جديد (Add Employee)")
        print("2. عرض جميع الموظفين (List Employees)")
        print("3. تحديث بيانات موظف (Update Employee)")
        print("4. حذف موظف (Delete Employee)")
        print("5. إنشاء كشف راتب (Generate Payslip)")
        print("6. تقرير شهري (Monthly Report)")
        print("7. خروج (Exit)")
        print("="*50)
        
        choice = input("اختر عملية (Enter choice): ")
        
        if choice == '1':
            emp_id = input("رقم الموظف (Employee ID): ")
            name = input("الاسم (Name): ")
            position = input("الوظيفة (Position): ")
            base_salary = float(input("الراتب الأساسي (Base Salary): "))
            system.add_employee(emp_id, name, position, base_salary)
        
        elif choice == '2':
            system.list_employees()
        
        elif choice == '3':
            emp_id = input("رقم الموظف (Employee ID): ")
            print("ما تريد تحديثه:")
            print("1. الراتب الأساسي (Base Salary)")
            print("2. ساعات إضافية (Overtime Hours)")
            print("3. مكافآت (Bonuses)")
            print("4. خصومات (Deductions)")
            update_choice = input("اختر: ")
            
            if update_choice == '1':
                value = float(input("الراتب الجديد: "))
                system.update_employee(emp_id, base_salary=value)
            elif update_choice == '2':
                value = float(input("عدد الساعات: "))
                system.update_employee(emp_id, overtime_hours=value)
            elif update_choice == '3':
                value = float(input("المبلغ: "))
                system.update_employee(emp_id, bonuses=value)
            elif update_choice == '4':
                value = float(input("المبلغ: "))
                system.update_employee(emp_id, deductions=value)
        
        elif choice == '4':
            emp_id = input("رقم الموظف (Employee ID): ")
            confirm = input("هل أنت متأكد؟ (yes/no): ")
            if confirm.lower() in ['yes', 'y', 'نعم']:
                system.delete_employee(emp_id)
        
        elif choice == '5':
            emp_id = input("رقم الموظف (Employee ID): ")
            system.generate_payslip(emp_id)
        
        elif choice == '6':
            system.generate_monthly_report()
        
        elif choice == '7':
            print("\nشكراً لاستخدامك النظام!")
            print("Thank you for using the system!")
            break
        
        else:
            print("✗ اختيار غير صحيح")

if __name__ == "__main__":
    main()
