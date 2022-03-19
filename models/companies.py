import psycopg2
from db.connect import connect


def insert_company(company_cik, company_name, company_favicon_link="https://imgix.datadoghq.com/img/favicons/favicon-32x32.png", company_ticker="app"):
    """ insert a new company into the companies table """
    sql = """INSERT INTO companies(company_cik, company_name, company_favicon_link, company_ticker)
             VALUES(%s, %s, %s, %s);"""
    conn = connect()
    try:
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (company_cik, company_name,
                    company_favicon_link, company_ticker,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return True


def search_companies(company_name):
    """ query data from the vendors table """
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM companies WHERE company_name ILIKE %s", (company_name,))
        row = cur.fetchall()

        cur.close()
        print(row)
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
