import csv
from datetime import datetime
from CustomLogger import logger

from db_handler import Database
from sms_sender import send_sms


class Db_executer(Database):

    def __init__(self, db_name):
        super().__init__(db_name)

    def create_analysis_table(self):
        sql_create_table = f"""
            CREATE TABLE IF NOT EXISTS analysisss(
            probe_number integer PRIMARY KEY,
            analysis_id integer,
            patient_id integer,
            collection_time timestamp without time zone,
            result text
            ) ;
                     """
        try:
            #super().__init__(self.db_name) #obiekt klasy Database
            super().execute_sql(sql_create_table)
        except Exception as e:
            logger.error("Can not create table analysis: " + str(e))

    def insert_new_patient(self, id, name, surname, pesel):
        sql_insert = """
            INSERT INTO patients
            (id, name, surname, pesel)
            VALUES (?,?,?,?)
            """
        patient_data = [id,name, surname, pesel]
        try:
            #super().__init__(self.db_name)
            super().execute_sql(sql_insert, patient_data)
        except Exception as e:
            logger.error("Can not insert patient data: " + str(e))
            exit()

    def insert_analysis(self, probe_number, analysis_id, patient_id, collection_time, result):
        sql = """
        INSERT INTO analysis
        (probe_number, analysis_id, patient_id, collection_time, result)
        VALUES (?,?,?,?,?)
        """
        data = [probe_number, analysis_id, patient_id, collection_time, result]
        try:
            #super().__init__(self.db_name)
            super().execute_sql(sql, data)
        except Exception as e:
            logger.error("Can not insert new analysis: " + str(e))
            exit()
    def diagnostica_analysis(self):
        try:
            with open(r"C:\Users\cp24\Desktop\Akademia Kodu\Project\Diagnostica.csv", encoding='UTF8') as csv_file:
                all_row = csv.reader(csv_file, delimiter=',')
                for row in all_row:
                    #print(row)
                    if row[1] == 'blood':
                        row[1] = '1'
                    if row[3] != 'collection_time':
                        row[3] = str(datetime.strptime(row[3], "%d.%m.%Y %H:%M"))
                    if row[0] != "external_patient_id": # opuszczamy 1 wiersz
                        self.insert_analysis(probe_number=row[2], analysis_id=row[1], patient_id=row[0], collection_time=row[3], result=row[4])
        except Exception as e:
            logger.error("Diagnostica analysis failed", exc_info=True)

    def hospital_analysis(self, csv_path):
        try:
            with open(csv_path, encoding="UTF8") as csv_hospital:
                all_rows = csv.reader(csv_hospital, delimiter= ',')
                for one_row in all_rows:
                    if one_row[0] != 'external_patient_id':
                        one_row[2] = str(datetime.strptime(one_row[2], "%d.%m.%Y %H:%M"))
                        if one_row[4] == 'blood':
                            one_row[4] = '1'
                        if one_row[3] == 'T':
                            one_row[3] = 'True'
                        else:
                            one_row[3] = "False"
                        self.insert_analysis(
                            probe_number=one_row[1],
                            analysis_id=one_row[4],
                            patient_id=one_row[0],
                            collection_time=one_row[2],
                            result=one_row[3]
                        )
        except Exception as e:
            logger.error("Hospital analysis failed", exc_info=True)

    def antarctica_analysis(self, csv_file):
        try:
            all_db_patients = self.select_all_tasks("patients")
            with open(csv_file, encoding="utf-8-sig") as an_file:
                all_rows = csv.reader(an_file, delimiter=';')
                for one_row in all_rows:
                    #print(one_row)
                    for one_patient in all_db_patients:
                        #print(type(one_row[2]), one_row[2], type(one_patient[3]), one_patient[3])
                        if one_row[0] != 'id':
                            if one_row[2] == str(one_patient[3]): #porównuje pesele aby dostać id
                                one_row[4] = str(datetime.strptime(one_row[4], "%d.%m.%Y %H:%M"))
                                if one_row[5] == 'T':
                                    one_row[5] = 'True'
                                else:
                                    one_row[5] = 'False'
                                self.insert_analysis(
                                    probe_number=one_row[1],
                                    analysis_id=one_row[3],
                                    patient_id=one_patient[0], #odnosimy się do bazy danych do tablicy patients i wyciągamy id
                                    collection_time=one_row[4],
                                    result=one_row[5]
                                )
                                if one_row[5] == "False":
                                    week_days = ["Poniedzialek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
                                    obj_datetime = datetime.strptime(one_row[6], "%d.%m.%Y %H:%M")
                                    week_number = obj_datetime.weekday()
                                    msg = f'Dzień dobry, ' \
                                          f'Zapraszamy na wizytę kontrolną w {week_days[week_number]} dokładna data ' \
                                          f'{one_row[6]} o godzinie {obj_datetime.time()}'

                                    send_sms(msg, one_row[7])

        except Exception as e:
            logger.error("Antarctica analysis failed ", exc_info=True)