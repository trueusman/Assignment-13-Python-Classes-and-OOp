"""Task 07: Employee payroll with abstract base class and polymorphism."""

from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calculate_pay(self):
        pass

class SalariedEmployee(Employee):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = float(salary)

    def calculate_pay(self):
        return self.salary

class HourlyEmployee(Employee):
    def __init__(self, name, hourly_rate, hours):
        super().__init__(name)
        if hourly_rate < 0 or hours < 0:
            raise ValueError("Rate and hours cannot be negative")
        self.hourly_rate = float(hourly_rate)
        self.hours = float(hours)

    def calculate_pay(self):
        regular = min(self.hours, 40) * self.hourly_rate
        overtime = max(0, self.hours - 40) * self.hourly_rate * 1.5
        return regular + overtime

class CommissionEmployee(Employee):
    def __init__(self, name, base, sales, rate):
        super().__init__(name)
        if min(base, sales, rate) < 0:
            raise ValueError("Pay inputs cannot be negative")
        self.base = float(base)
        self.sales = float(sales)
        self.rate = float(rate)

    def calculate_pay(self):
        return self.base + self.sales * self.rate

def payroll_summary(employees):
    return [
        {"name": employee.name, "pay": employee.calculate_pay()}
        for employee in employees
    ]


if __name__ == "__main__":
    staff = [
        HourlyEmployee("Hassan", 20, 45),
        CommissionEmployee("Ayesha", 500, 4000, 0.10),
        SalariedEmployee("Usman", 3000),
    ]
    print(payroll_summary(staff))
