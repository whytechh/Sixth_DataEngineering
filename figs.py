import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('/root/lab6 Viktor/VariantV_p2.csv')

income = data['income']
plt.figure(figsize=(5, 5))
plt.boxplot(income, vert=False)
plt.title('Годовой доход заявителя в квантилях')
plt.xlabel('Доход')
plt.tight_layout()
plt.savefig('/root/lab6 Viktor/fig_income.png')

age = data['customer_age']
plt.figure(figsize=(5, 5))
plt.hist(age, bins=20)
plt.title('Распределение возрастов')
plt.xlabel('Возраст')
plt.ylabel('Количество')
plt.tight_layout()
plt.savefig('/root/lab6 Viktor/fig_age.png')

p_type = data['payment_type'].value_counts()
plt.figure(figsize=(5, 5))
plt.pie(p_type, labels=p_type.index, autopct='%1.1f%%', startangle=90)
plt.title('Распределение типов плана кредитных платежей')
plt.tight_layout()
plt.savefig('/root/lab6 Viktor/fig_ptype.png')

status = data.groupby('housing_status').size().sort_values(ascending=False)
plt.figure(figsize=(5, 5))
plt.barh(status.index, status.values)
plt.title('Текущий статус проживания заявителя')
plt.xlabel('Количество')
plt.ylabel('Статус')
plt.tight_layout()
plt.savefig('/root/lab6 Viktor/fig_status.png')

age_payment = data.groupby(['customer_age', 'payment_type']).size().reset_index(name='count')
pivot_table = age_payment.pivot(index='customer_age', columns='payment_type', values='count').fillna(0)
plt.figure(figsize=(12, 6))
pivot_table.plot(kind='bar', stacked=True)
plt.title('Популярность типов платежей по возрасту')
plt.xlabel('Возраст')
plt.ylabel('Количество')
plt.legend(title='Тип платежа')
plt.tight_layout()
plt.savefig('/root/lab6 Viktor/fig_age_payment_type.png')