from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getC():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct *
                    from categories c"""

        cursor.execute(query)

        for row in cursor:
            results.append((row["category_id"], row["category_name"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getN(c):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p 
                    where p.category_id = %s"""

        cursor.execute(query, (c,))

        for row in cursor:
            results.append(Product(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getA(c, min, max):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select t1.p as p1, t2.p as p2, t1.nvendite as v1, t2.nvendite as v2, (t1.somma + t2.somma) as peso
                    from(
                    select oi.product_id as p,  Csum(oi.quantity) as nVendite, sum(oi.quantity) as somma
                    from products p, orders o, order_items oi 
                    where p.product_id = oi.product_id and o.order_id = oi.order_id and p.category_id = %s and o.order_date between %s and %s
                    group by oi.product_id) as t1,
                    (select oi.product_id as p,  sum(oi.quantity) as nVendite, sum(oi.quantity) as somma
                    from products p, orders o, order_items oi 
                    where p.product_id = oi.product_id and o.order_id = oi.order_id and p.category_id = %s and o.order_date between %s and %s
                    group by oi.product_id) as t2
                    where t1.p <> t2.p
                    """
        cursor.execute(query, (c, min, max, c, min, max))

        for row in cursor:
            results.append((row["p1"], row["p2"], row["v1"], row["v2"], row["peso"]))
        cursor.close()
        conn.close()
        return results