import psycopg2
from connect import connect


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
        """,
        """
        CREATE TABLE IF NOT EXISTS companies (
            company_cik VARCHAR(255) NOT NULL PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            company_favicon_link VARCHAR(255),
            company_ticker VARCHAR(255)
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS companies_10k (
            data_id uuid DEFAULT uuid_generate_v4() UNIQUE PRIMARY KEY,
            "10k_submitted_date" TIMESTAMP WITH TIME ZONE NOT NULL,
            matric_1 VARCHAR(255),
            matric_2 VARCHAR(255),
            matric_3 VARCHAR(255),
            matric_4 VARCHAR(255),
            matric_5 VARCHAR(255),
            matric_6 VARCHAR(255),
            company_cik VARCHAR(255) NOT NULL,
            FOREIGN KEY (company_cik) REFERENCES companies(company_cik)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS companies_10q (
            data_id uuid DEFAULT uuid_generate_v4() UNIQUE PRIMARY KEY,
            "10q_submitted_date" TIMESTAMP WITH TIME ZONE NOT NULL,
            matric_1 VARCHAR(255),
            matric_2 VARCHAR(255),
            matric_3 VARCHAR(255),
            matric_4 VARCHAR(255),
            matric_5 VARCHAR(255),
            matric_6 VARCHAR(255),
            company_cik VARCHAR(255) NOT NULL,
            FOREIGN KEY (company_cik) REFERENCES companies(company_cik)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS companies_8k (
            data_id uuid DEFAULT uuid_generate_v4() UNIQUE PRIMARY KEY,
            "8k_submitted_date" TIMESTAMP WITH TIME ZONE NOT NULL,
            event VARCHAR,
            company_cik VARCHAR(255) NOT NULL,
            FOREIGN KEY (company_cik) REFERENCES companies(company_cik)
        )
        """)
    conn = connect()
    try:
        # creating the cursor
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
