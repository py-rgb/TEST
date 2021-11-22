from nltk.util import pr
import pymysql
conn=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='textoir',
        passwd='12345678',
        db='textoir',
        charset='utf8'
    )
cur=conn.cursor()
select_sql = 'Select Abbreviation from Skill where Type = "Robust"'
cur.execute(select_sql)
skills=cur.fetchall()
Types = ['Cognition','Robust']
select_sql = 'Select * from Trained_Model'
cur.execute(select_sql)
Models=cur.fetchall()
models = []
for Model in Models:
    model_name =Model[1]+'_'+Model[2]+"_"+str(Model[0])
    models.append(model_name)
skill_datas =[]
model_data = []
series_data_list = []
print(models)
print(skills)
for model in models:
    series_data = {"name":model,"type":"line"}
    sorce_list = []
    for skill in skills:
        same_type = []
        for Type in Types:
            select_sql='Select * from Skill_Test_Model where Abbreviation = "%s" and Type = "%s" and Model="%s"'%(skill[0],Type,model)
            cur.execute(select_sql)
            mes=cur.fetchall()
            fields = cur.description
            data ={}
            column_list =[]
            for i in fields:
                column_list.append(i[0])
            print(column_list)
            for i,column in  enumerate(column_list):
                data[column] = mes[0][i]
            same_type.append(data)
        Ablation_em = same_type[0]['EM']
        Ablation_f1 = same_type[0]['F1']
        Augmentation_em = same_type[0]['EM']
        Augmentation_f1 = same_type[1]['EM']
        sorce = ((Ablation_em-Augmentation_em)**2+(Ablation_f1-Augmentation_f1)**2)**0.5
        sorce = round(sorce,3)
        sorce_list.append(sorce)
    series_data['data'] = sorce_list
    series_data_list.append(series_data)
skill_list = [skill[0] for skill in skills]
result={'xAxis':skill_list,'legend':models,"series":series_data_list}
print(result)

    

    
