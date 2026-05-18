from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                from airports a
                order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result
    
    @staticmethod
    def getAllNodes(n,idMap):
        #passo la mappa perchè mi serve solo una parte degli airport e non tutti
        #evito di pasticciare troppo 
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.ID, t.IATA_CODE, count(*) as N
                    FROM (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                    from airports a, flights f
                    where a.ID = f.ORIGIN_AIRPORT_ID 
                    or a.ID = f.DESTINATION_AIRPORT_ID 
                    GROUP BY a.ID, a.IATA_CODE, f.AIRLINE_ID ) t
                    GROUP BY t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""

        cursor.execute(query,(n,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result
    
    def getAllEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID,count(*) as peso
                from flights f
                group by f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID
                order by f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(idMap[row["ORIGIN_AIRPORT_ID"]],idMap[row["DESTINATION_AIRPORT_ID"]],row["peso"]))

        cursor.close()
        conn.close()
        return result
    

    def getAllEdgesV2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #coalesce mi restituisce la prima variabile non nulla invece fare solo la somma tra numeo e null mi restituisce null
        query = """select t1.ORIGIN_AIRPORT_ID,t1.DESTINATION_AIRPORT_ID,coalesce(t1.peso,0)+coalesce(t2.peso,0) as peso
                from(SELECT f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID,count(*) as peso
                from flights f
                group by f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID
                order by f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID) t1
                left join(SELECT f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID,count(*) as peso
                from flights f
                group by f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID
                order by f.ORIGIN_AIRPORT_ID,f.DESTINATION_AIRPORT_ID) t2
                on t1.ORIGIN_AIRPORT_ID=t2.DESTINATION_AIRPORT_ID and t1.DESTINATION_AIRPORT_ID=t2.ORIGIN_AIRPORT_ID
                where t1.ORIGIN_AIRPORT_ID<t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null"""

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(idMap[row["ORIGIN_AIRPORT_ID"]],idMap[row["DESTINATION_AIRPORT_ID"]],row["peso"]))

        cursor.close()
        conn.close()
        return result